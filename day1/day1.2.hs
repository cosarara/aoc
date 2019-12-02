fuel x = if y > 0
        then y + fuel y
        else 0
    where y = (x `div` 3) - 2

main = do
    -- I can't say I really understand <-
    -- src <- readFile "day1_input.txt"
    src <- getContents
    print $ sum $ map (\x -> fuel $ read x :: Integer) (lines src)
