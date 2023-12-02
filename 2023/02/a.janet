(def game-peg
  (peg/compile
    '{
    :color (choice (/ "red" :red) (/ "green" :green) (/ "blue" :blue))
    :number (number (some (range "09")))
    :hand (sequence (group (sequence :number " " :color)) (opt ", "))
    :set (sequence (between 1 3 :hand) (set ";\n") (opt " "))
    :content (sequence "Game " :number ": " (some (group :set)))
    :main :content
    }))

(defn parse-game [line] (peg/match game-peg line))

#(def line "Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green")
#(pp (parse-game line))

(defn read-lines [filename]
  (coro
   (with [fl (file/open filename)]
    (loop [line :iterate (file/read fl :line)]
    (yield line)))))

(defn possible-hand?
  "We only have 12 red cubes, 13 green cubes, and 14 blue cubes"
  [[number color]]
  (<= number
   (case color
    :red 12
    :green 13
    :blue 14)))

(var sum 0)
(each line (read-lines "input.txt")
  (def game (parse-game line))
  (def game-id (in game 0))
  (def sets (array/slice game 1))
  (if (all (fn [set] (all possible-hand? set)) sets)
    (do
      (pp game-id)
      #(pp sets)
      (+= sum game-id)
    ))
)
(print sum)
