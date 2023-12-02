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

(defn read-lines [filename]
  (coro
   (with [fl (file/open filename)]
    (loop [line :iterate (file/read fl :line)]
    (yield line)))))

(defn max-colors
  [[number color] [max-red max-blue max-green]]
   (case color
    :red [(max max-red number) max-blue max-green]
    :blue [max-red (max max-blue number) max-green]
    :green [max-red max-blue (max max-green number)]
    ))

(var sum 0)
(each line (read-lines "input.txt")
  (def game (parse-game line))
  (def game-id (in game 0))
  (def sets (array/slice game 1))
  (var maxs [0 0 0])
  (each set sets
    (each hand set
      (set maxs (max-colors hand maxs))))
  (var [r g b] maxs)
  (var power (* r g b))
  (print power)
  (+= sum power)
)
(print sum)
