import Debug.Trace
import Data.Array
import Data.Maybe
import Data.List
import Data.Ord

-- ok this fucking sucks tbh
split :: String -> Char -> [String]
split str sep = foldr (\c list ->
        if c == sep
        then []:list
        else (c:(head list)):(tail list)) [[]] str
splitc str = split str ','

-- wow this was hard to google
-- thanks http://learnyouahaskell.com/making-our-own-types-and-typeclasses

data State = State { mem :: Array Int Int
                   , pc :: Int
                   , input :: Maybe Int
                   , output :: Maybe Int
                   , running :: Bool
                   } deriving (Show)

arg :: State -> Int -> Int
arg state n =
    let tpc = (pc state)
        tmem = (mem state)
        ins = (tmem ! tpc) `quot` (10 * 10 ^ n)
        a = tmem ! (tpc + n)
        mode = ins `mod` 10
    in
        --trace ("arg n " ++ (show n) ++ " mode " ++ (show mode) ++
        --       " a " ++ (show a) ++ " tpc+n " ++ (show $ tpc + n)) $
        case mode
            of 0 -> tmem ! a
               1 -> a
               --2 -> todo
               x -> error "what kind of access is that"

outarg state n =
    let tpc = (pc state)
        tmem = (mem state)
        ins = (tmem ! tpc) `quot` (10 * 10 ^ n)
        a = tmem ! (tpc + n)
        mode = ins `mod` 10
    in
        --trace ("oarg n " ++ (show n) ++ " mode " ++ (show mode) ++
        --       " a " ++ (show a) ++ " tpc " ++ (show tpc)) $
        case mode
            of 0 -> a
               --1 -> a
               --2 -> todo a + rel
               x -> error "what kind of access is that"

do_op 1 state =
    let tmem = mem state
        tpc = pc state
        a = arg state 1
        b = arg state 2
        d = outarg state 3
    in
        --trace ("sum " ++ (show a) ++ " " ++ (show b) ++ " " ++ (show d)) $
        state {pc=tpc+4, mem=tmem // [(d, a+b)]}
        --(tpc+4, tmem // [(d, (tmem ! a)+(tmem ! b))])

do_op 2 state =
    let tmem = mem state
        tpc = pc state
        a = arg state 1
        b = arg state 2
        d = outarg state 3
    in
        --trace ("mul " ++ (show a) ++ " " ++ (show b) ++ " " ++ (show d)) $
        state {pc=tpc+4, mem=tmem // [(d, a*b)]}

do_op 3 state =
    let tmem = mem state
        tpc = pc state
        d = outarg state 1
        x = case input state
            of Just x -> x
               Nothing -> error "input somehow empty"
    in
        --trace ("in " ++ (show d) ++ " " ++ (show x)) $
        state { pc=tpc+2
              , mem=tmem // [(d, x)]
              , input=Nothing}

do_op 4 state =
    let tmem = mem state
        tpc = pc state
        d = arg state 1
    in
        --trace ("out " ++ (show d)) $
        state { pc=tpc+2
              , output=Just d}

do_op 5 state = -- jump if true
    let tmem = mem state
        tpc = pc state
        a = arg state 1
        d = arg state 2
    in
        if a /= 0
        then state { pc=d }
        else state { pc=tpc + 3 }

do_op 6 state = -- jump if false
    let tmem = mem state
        tpc = pc state
        a = arg state 1
        d = arg state 2
    in
        if a == 0
        then state { pc=d }
        else state { pc=tpc + 3 }

do_op 7 state = -- less than
    let tmem = mem state
        tpc = pc state
        a = arg state 1
        b = arg state 2
        d = outarg state 3
    in
        state { pc=tpc + 4
                ,mem=tmem // [(d, if a < b then 1 else 0)] }

do_op 8 state = -- eq
    let tmem = mem state
        tpc = pc state
        a = arg state 1
        b = arg state 2
        d = outarg state 3
        v = if a == b then 1 else 0
    in
        --trace ("eq " ++ (show [a, b, v, d])) $
        state { pc=tpc + 4
                ,mem=tmem // [(d, v)] }

do_op 99 state = state {running=False}

do_op x state = error "bad instruction"

getop state = ((mem state) ! (pc state)) `mod` 100

execute state out =
    --trace (show mem) $
    --trace ("pc: " ++ (show (pc state))) $
    let op = getop state
        state' =
            --trace ("op: " ++ (show op)) $
            do_op op state
        out' = case output state'
                of Just x -> x:out
                   Nothing -> out
        in
        if running state'
            then execute (state' {output=Nothing}) out'
            --else trace (show $ mem state') $ out'
            else out'

-- a version of execute that blocks on output
tillOutput state0 =
    let state = state0 {output=Nothing}
        bleh = trace ("pc: " ++ (show (pc state))) $
               trace ("input: " ++ (show (input state))) $ 0
        op = getop state
        state' = do_op op state
        in
        case output state'
           of Just x -> state'
              Nothing ->
                if running state'
                    then tillOutput state'
                    else state'

-- a version of execute that blocks after reading input
tillInput state =
    let op = getop state
        state' = do_op op state
        in
        case input state'
           of Just x ->
                if running state'
                    then tillInput state'
                    else state'
              Nothing -> state'

inOut state inp = tillOutput (state {input=inp})

toArr list =
    listArray (0, length list - 1) list

parseSrc src = toArr (map (\x -> (read x :: Int)) (splitc src))

initState src input = State {mem=parseSrc src, pc=0, input=input, output=Nothing, running=True}

loopStep stateA stateB stateC stateD stateE inp =
    let stateAo = inOut stateA inp
        stateBo = inOut stateB (output stateAo)
        stateCo = inOut stateC (output stateBo)
        stateDo = inOut stateD (output stateCo)
        stateEo = inOut stateE (output stateDo)
    in
        (stateAo, stateBo, stateCo, stateDo, stateEo)

loop a b c d e =
    let (aa,bb,cc,dd,ee) = loopStep a b c d e (output e)
    in
        if running aa
        then loop aa bb cc dd ee
        else output e

amp src phases =
    let init x = tillInput $ initState src (Just x)
        [a, b, c, d, e] = map init phases
        v = loop a b c d (e {output=Just 0})
    in
        case v of
        Just x -> x
        Nothing -> error "ended up with nothing"

-- Arrays need Int (not Integer)
main = do
    src <- getContents
    print "part A"
    let phases = maximumBy (comparing (amp src)) (permutations [0, 1, 2, 3, 4])
    print $ phases
    print $ amp src phases
    print "part B"
    let phasesB = maximumBy (comparing (amp src)) (permutations [5, 6, 7, 8, 9])
    print $ phasesB
    print $ amp src phasesB
