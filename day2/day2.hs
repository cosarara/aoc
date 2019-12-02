import Data.Array
import Debug.Trace

-- ok this fucking sucks tbh
split :: String -> Char -> [String]
split str sep = foldr (\c list ->
        if c == sep
        then []:list
        else (c:(head list)):(tail list)) [[]] str
splitc str = split str ','

do_op 1 pc mem =
    let a = mem ! (pc + 1)
        b = mem ! (pc + 2)
        d = mem ! (pc + 3)
    in
        --trace ("sum " ++ (show a) ++ " " ++ (show b) ++ " " ++ (show d)) $
        (pc+4, mem // [(d, (mem ! a)+(mem ! b))])

do_op 2 pc mem =
    let a = mem ! (pc + 1)
        b = mem ! (pc + 2)
        d = mem ! (pc + 3)
    in (pc+4, mem // [(d, (mem ! a) * (mem ! b))])

do_op 99 pc mem = (-1, mem)

-- TODO: how to handle errors
do_op x pc mem = (-2, mem)

execute pc mem =
    --trace (show mem) $
    let op = mem ! pc
        (pc', mem') = do_op op pc mem
        in --trace ("pc: " ++ show pc) $
        if pc' > 0
            then execute pc' mem'
            else mem' ! 0

toArr list =
    listArray (0, length list - 1) list

-- Arrays need Int (not Integer)
main = do
    src <- getContents
    let mem = toArr (map (\x -> (read x :: Int)) (splitc src))
    let mem' = mem // [(1, 12), (2, 2)]
    print $ execute 0 mem'
