import Debug.Trace
import Data.Array
import Data.Maybe

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
    in
        --trace ("in " ++ (show d) ++ " " ++ (show (input state))) $
        state { pc=tpc+2
              , mem=tmem // [(d, fromJust $ input state)]
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

do_op 99 state = state {pc=(-1)}

do_op x state = error "bad instruction"

execute state out =
    --trace (show mem) $
    --trace ("pc: " ++ (show (pc state))) $
    let op = ((mem state) ! (pc state)) `mod` 100
        state' =
            --trace ("op: " ++ (show op)) $
            do_op op state
        out' = case output state'
                of Just x -> x:out
                   Nothing -> out
        in
        if (pc state') > 0
            then execute (state' {output=Nothing}) out'
            --else trace (show $ mem state') $ out'
            else out'

toArr list =
    listArray (0, length list - 1) list

parseSrc src = toArr (map (\x -> (read x :: Int)) (splitc src))

initState src input = State {mem=parseSrc src, pc=0, input=input, output=Nothing}

-- Arrays need Int (not Integer)
main = do
    -- test program
    -- print $ execute (initState "3,9,8,9,10,9,4,9,99,-1,8" (Just 0)) []
    -- print $ execute (initState "3,9,8,9,10,9,4,9,99,-1,8" (Just 1)) []
    -- print $ execute (initState "3,9,8,9,10,9,4,9,99,-1,8" (Just 8)) []

    src <- getContents
    let tmem = parseSrc src
    let tmem' = tmem -- // [(1, 12), (2, 2)]
    --let state = State {mem=tmem', pc=0, input=Just 1, output=Nothing}
    let state = initState src (Just 1)
    print $ execute state []
    --let stateb = State {mem=tmem', pc=0, input=Just 5, output=Nothing}
    let stateb = initState src (Just 5)
    print $ execute stateb []
    --print (mem state)
