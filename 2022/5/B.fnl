#!/bin/lu9 /bin/fennel

(local view (require "fennel.view"))

(lambda pprint [...]
  (each [i x (ipairs [...])]
    (print (view x))))

(local file (io.open "input"))
(local lines (icollect [line _ (file:lines)] line))

(lambda find [arr item]
  (var x nil)
  (each [i line (pairs lines) &until (= line "")] (set x i))
  x)

(lambda sub-array [arr start ?e]
	(let [end (or ?e (length arr))]
		(fcollect [i start end] (. arr i))))

(lambda icol [iterator]
	(icollect [a _ iterator] a))

(lambda map [f arr]
  (icollect [_ a (ipairs arr)] (f a)))

(lambda split [s sep]
	(icol (s:gmatch (.. "[^" sep "]+"))))

(local split-location (find lines ""))
(local lines-initial (sub-array lines 1 (- split-location 1)))
(local moves  (sub-array lines (+ split-location 2)))

(lambda parse-initial []
  (local stacks {})
  (each [line-n line (ipairs lines-initial)]
    ;(print line)
    (let [y (+ 1 (- (length lines-initial) line-n))
          len (length line)
          width (math.ceil (/ len 4))] ; "[?] "
      ;(print len width)
      (for [x 1 width]
        (let [s (+ 1 (* (- x 1) 4))
          crate (line:sub s (+ s 3))]
          (when (crate:find "[" 1 true)
            (when (not (. stacks x)) (tset stacks x {}))
            (tset (. stacks x) y (crate:sub 2 2))
            ;(print "crate" crate "line" y "n" x)
            )))))
  stacks)
(local stacks (parse-initial))

(lambda do-moves! [stacks]
  (each [i move (ipairs moves)]
    (let [[n orig dest] (map tonumber (split move " "))
          ostack (. stacks orig)
          dstack (. stacks dest)
          isplit (- (length ostack) n)
          moved (sub-array ostack (+ 1 isplit))
          remainder (sub-array ostack 1 isplit)]
      ;(print "------")
      ;(pprint stacks)
      ;(print n orig dest move)
      ;(pprint "orig" ostack "dest" dstack)
      ;(pprint "moved" moved)
      ;(pprint remainder)
      (tset stacks orig remainder)
      (each [_ crate (pairs moved)]
         (table.insert dstack crate))))
  stacks)

(lambda last [arr]
  (. arr (length arr)))

(lambda tops [stacks]
    (map last stacks))

(lambda msg [arr]
  (accumulate [acc "" i s (ipairs arr)] (.. acc s)))

(print (msg (tops (do-moves! (parse-initial)))))
