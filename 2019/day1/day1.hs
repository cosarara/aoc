main = do
    -- I can't say I really understand <-
    -- src <- readFile "day1_input.txt"
    src <- getContents
    print $ sum $ map (\x -> ((read x :: Integer) `div` 3) - 2) (lines src)
