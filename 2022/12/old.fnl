(local lume (require "lume"))

(local view (require "fennel.view"))

(lambda pprint [...]
  (each [i x (ipairs [...])]
    (print (view x))))

(fn tup [[x y]] (+ (* x 1000) y)) ; hashable representation of pairs

(var grid [])
(var start nil)
(var goal nil)
(local graph [])

(lambda load-input [?filename]
  (local s (love.filesystem.read (or ?filename "input")))
  (set grid (icollect [line _ (s:gmatch "[^\n]+")]
              (icollect [char _ (line:gmatch ".")] char)))
  grid)

(lambda make-graph []
  (pprint grid)
  (each [y line (ipairs grid)]
    (each [x char (ipairs line)]
      (when (= char "S") (set start (tup [x y])))
      (when (= char "E") (set goal (tup [x y])))
      (local outs (icollect [_ [xx yy] (ipairs [[(- x 1) y] [(+ x 1) y]
                                                [x (- y 1)] [x (+ y 1)]])]
                      (if (and (>= xx 1) (>= yy 1)
                               (<= xx (length line)) (<= yy (length grid)))
                          (do
                            (local nei (. (. grid yy) xx))
                            (local out (tup [xx yy]))
                            (if (= nei "E") (if (= char "z") out)
                                (or (= char "S") (<= (nei:byte) (+ (char:byte) 1)))
                                out)))))
      (tset graph (tup [x y]) outs)))
  ;(pprint graph)
  graph)

(fn love.load []
  (love.window.setMode 1500 900)
  )

(load-input)
(make-graph)

(fn in-arr [arr x]
  (var found false)
  (each [_ y (ipairs arr) &until (if (= x y) (do (set found true) true))] nil)
  found)

(local bestpaths {})
(var path [(tup [1 1])])
(var bestpath [])

(fn dist-to-goal [x]
  (+
    (/ (math.abs (- x goal)) 1000)
    (% (math.abs (- x goal)) 1000)))

(fn sort-possibilities [possib]
  (table.sort possib (fn [a b]
                       (< (dist-to-goal a)
                          (dist-to-goal b)))))

(var iters 0)
(var visited {})
(fn walk2 [?coro]
  (local unvisited [[start]])
  (var best-path nil)
  (set visited {})

  (while (and (not best-path) (length unvisited))
    (set iters (+ iters 1))
    (local current-path (table.remove unvisited 1))
    (when (and ?coro (= 0 (% iters 50))) (coroutine.yield current-path))
    (local current (. current-path (length current-path)))
    (when (not (. visited current))
      (tset visited current (length current-path))
      (local possibilities (. graph current))
      (sort-possibilities possibilities)

      (each [_ node (ipairs possibilities)]
        (when (= goal node)
          (set best-path current-path))
        (when (not (. visited node))
          (local new (icollect [_ x (ipairs current-path)] x))
          (table.insert new node)
          (table.insert unvisited new)))))
  (set bestpath best-path)
  (when ?coro
    (print "now we just loop forever")
    (while true (coroutine.yield [])))
  best-path)

(print (length (walk2)))
(print "hohoho")

(fn walk [walked ?coro]
  (local len (length walked))
  (local last (. walked (length walked)))
  (local previous-dist-here (. bestpaths last))
  (when (or (not previous-dist-here) (< len previous-dist-here))
        (tset bestpaths last len)
        (local possibilities (. graph last))
        (sort-possibilities possibilities)
        (var found-goal false)
        (var break false)
        (each [_ node (ipairs possibilities) &until break]
          (when (not (in-arr walked node)) ; avoid loops
            (when (and ?coro (= 0 (% len 50))) (coroutine.yield walked))
            (local tmp (icollect [_ x (ipairs walked)] x))
            (table.insert tmp node)
            (if
              (= goal node)
              (do
                (print "found the goal" (not bestpath) bestpath)
                (set found-goal true)
                (when (or (not bestpath) (> (length bestpath) (length tmp)))
                  (print "set stupid bestpath")
                  (set bestpath tmp))
                (print "breaking")
                (set break true))
              (do
                (local path (walk tmp ?coro))
                )))))
  (when ?coro
    (print "now we just loop forever")
    (while true (coroutine.yield walked)))
  bestpath
)

(fn height [char]
  (/ (/ (- (char:byte) (string.byte "a"))
        (- (string.byte "z") (string.byte "a"))) 2))

(local worker (coroutine.create (fn []
                                  (walk2 [start] true)
                                  (print "work done")
                                  ;(pprint bestpath)
                                  (print (length bestpath))
                                  (print "kaboom")
                                  []
                                  )))

(var dtotal 0)
(var stopped false)
(var work-finished false)
(fn love.update [dt]
  (set dtotal (+ dtotal dt))
  (when (> dtotal 0.16)
    (set dtotal (- dtotal 0.16))
    (when (not (or work-finished stopped))
      (let [(alive p) (coroutine.resume worker)]
      nil)
        ;(if alive
        ;  (do
        ;    (set path p))
        ;  (do
        ;    (print "done!")
        ;    (set work-finished true))))
      )
    (when work-finished (print "yay nothing to do")))
  )

(fn love.draw []
  ;(love.graphics.print
  ;  "Hello from Fennel!\nPress q to quit" 10 10)
  ;(love.graphics.rectangle "fill" 50 50 20 20)
  (love.graphics.setColor 1 1 1)
  ;(love.graphics.print (view grid) 10 200)

  (each [y line (ipairs grid)]
    (each [x char (ipairs line)]
      (if (< (char:byte) (string.byte "f"))
        (love.graphics.setColor 0 (+ 0.5 (height char)) 0)
        (love.graphics.setColor (+ 0.5 (height char)) 0 (+ 0.5 (height char))))
      (love.graphics.rectangle "fill" (- (* 20 x) 4) (* 20 y) 15 15)
      (let [dist (. visited (tup [x y]))]
        (when dist
          (love.graphics.setColor 1 1 (/ dist 500))
          (love.graphics.rectangle "line" (- (* 20 x) 4) (* 20 y) 15 15)))
      (love.graphics.setColor 1 1 1)
      (love.graphics.print char (* 20 x) (* 20 y))
      (love.graphics.setColor 1 0 0)
      ;(each [_ pair (ipairs (or bestpath []))]
      ;  (when (= pair (tup [x y]))
      ;    (love.graphics.rectangle "line" (- (* 20 x) 4) (* 20 y) 15 15)))
      (love.graphics.setColor 1 0 0)
      (when path
        (each [_ pair (ipairs (or path []))]
          (when (= pair (tup [x y]))
            (love.graphics.rectangle "line" (- (* 20 x) 4) (* 20 y) 15 15))))))

  )

(local reload (require "reload.fnl"))
(fn love.keypressed [key]
  (when (= "f5" key)
    (let [name "game.fnl"]
      (reload name)))
  (when (= "space" key)
    (set stopped (not stopped)))
  (when (= "q" key)
    (love.event.quit)))

(print "game.fnl loaded!")
;{:load-input load-input
; :make-graph make-graph
; :start start
; :goal goal
; :graph graph
; :walk walk
; :bestpath bestpath
; :bestpaths bestpaths}
