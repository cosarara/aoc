;; crashes on love 11.3 on intel, works on 11.4
(local view (require "fennel.view"))

(lambda pprint [...]
  (each [i x (ipairs [...])]
    (print (view x))))

(fn tup [[x y]] (+ (* x 1000) y)) ; hashable representation of pairs

(var grid [])
(var start nil)
(var goal nil)
(var as {})
(local graph [])

(lambda load-input [?filename]
  (local s (love.filesystem.read (or ?filename "input")))
  (set grid (icollect [line _ (s:gmatch "[^\n]+")]
              (icollect [char _ (line:gmatch ".")] char)))
  grid)

(lambda make-graph []
  (each [y line (ipairs grid)]
    (each [x char (ipairs line)]
      (when (= char "S") (set start (tup [x y])))
      (when (= char "E") (set goal (tup [x y])))
      (when (= char "a") (tset as (tup [x y]) true))
      (local outs (icollect [_ [xx yy] (ipairs [[(- x 1) y] [(+ x 1) y]
                                                [x (- y 1)] [x (+ y 1)]])]
                      (if (and (>= xx 1) (>= yy 1)
                               (<= xx (length line)) (<= yy (length grid)))
                          (do
                            (local nei (. (. grid yy) xx))
                            (local out (tup [xx yy]))
                            (if (= char "E")
                                (if (= nei "z") out)
                                (or (= char "S")
                                    ; reversed because we'll walk down
                                    (<= (char:byte) (+ (nei:byte) 1)))
                                out)))))
      (tset graph (tup [x y]) outs)))
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

(var iters 0)
(var visited {})
(fn walk [?coro]
  (local unvisited [[goal]])
  (var best-path nil)
  (set visited {})

  (while (and (not best-path) (length unvisited))
    (set iters (+ iters 1))
    (local current-path (table.remove unvisited 1))
    (when (and ?coro (= 0 (% iters 100))) (coroutine.yield current-path))
    (local current (. current-path (length current-path)))
    (when (not (. visited current))
      (tset visited current (length current-path))
      (local possibilities (. graph current))

      (each [_ node (ipairs possibilities)]
        (when (. as node)
          (set best-path current-path))
        (when (not (. visited node))
          (local new (icollect [_ x (ipairs current-path)] x))
          (table.insert new node)
          (table.insert unvisited new)))))
  (set bestpath best-path)
  best-path)

(fn height [char]
  (/ (/ (- (char:byte) (string.byte "a"))
        (- (string.byte "z") (string.byte "a"))) 2))

(local worker (coroutine.create (fn []
                                  (walk true)
                                  (print "work done")
                                  (print (length bestpath)))))

(var dtotal 0)
(var stopped false)
(var work-finished false)
(fn love.update [dt]
  (set dtotal (+ dtotal dt))
  (when (> dtotal 0.16)
    (set dtotal (- dtotal 0.16))
    (when (not (or work-finished stopped))
      (let [(alive p) (coroutine.resume worker)]
        (if alive
          (do
            (set path p))
          (do
            (print "done!")
            (set work-finished true)))))))

(fn scx [x]
  (- (* 20 x) 4))

(fn scy [y]
  (+ 10 (* 20 y)))

(fn square [x y ?mode]
  (love.graphics.rectangle (or ?mode "line") (scx x) (scy y) 15 15))

(fn love.draw []
  (love.graphics.setColor 1 1 1)

  (each [y line (ipairs grid)]
    (each [x char (ipairs line)]
      (if (< (char:byte) (string.byte "f"))
        (love.graphics.setColor 0 (+ 0.5 (height char)) 0)
        (love.graphics.setColor (+ 0.5 (height char)) 0 (+ 0.5 (height char))))
      (square x y "fill")
      (let [dist (. visited (tup [x y]))]
        (when dist
          (love.graphics.setColor 1 1 (/ dist 500))
          (square x y)))
      (love.graphics.setColor 1 1 1)
      (love.graphics.print char (* 20 x) (+ 10 (* 20 y)))
      (love.graphics.setColor 0 0 1)
      (each [i pair (ipairs (or bestpath []))]
        (when (= pair (tup [x y]))
          ;(love.graphics.setColor 0 0 1)
          (square x y)
          ;(love.graphics.setColor 1 1 1)
          ;(love.graphics.print (.. i "")
          ;                     (- (scx x) 3)
          ;                     (+ (scy y) (if (= 0 (% i 2)) -3 6)))
          ))
      (love.graphics.setColor 1 0 0)
      (when path
        (each [_ pair (ipairs (or path []))]
          (when (= pair (tup [x y]))
            (square x y))))))
  (when bestpath
    (love.graphics.setColor 1 1 1)
    (love.graphics.print (.. "best path length: " (length bestpath)) 10 10))
  (when stopped
    (love.graphics.setColor 1 1 1)
    (love.graphics.print "stopped; press [space] to start." 10 10)))

(local reload (require "reload.fnl"))
(fn love.keypressed [key]
  (when (= "f5" key)
    (let [name "game2.fnl"]
      (reload name)))
  (when (= "space" key)
    (set stopped (not stopped)))
  (when (= "q" key)
    (love.event.quit)))

(print "game2.fnl loaded!")
