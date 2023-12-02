(def game
  '{
  :color (choice "red" "green" "blue")
  :number (some (range "09"))
  :hand (sequence :number " " :color (opt ", "))
  :set (sequence (between 1 3 :hand) (set ";\n"))
  :content (some :set)
  :main :set
  })

(def line "3 blue, 4 red;")
(print
  (peg/match game line))
