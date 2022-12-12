(local view (require "fennel.view"))

(lambda pprint [...]
    (print (table.unpack
             (icollect [i x (ipairs [...])]
               (view x)))))

(fn tup [[x y]] (+ (* x 1000) y)) ; hashable representation of pairs

(var grid [])
(var start nil)
(var goal nil)
(local graph [])

(lambda load-input [?filename]
  (local f (io.open (or ?filename "input")))
  (local s (f:read "a"))
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
    (print "looping forever")
    (while true (coroutine.yield [])))
  best-path)

;(print (length (walk2)))

(local worker (coroutine.create (fn []
                                  (walk2 [start] true)
                                  (print "work done")
                                  ;(pprint bestpath)
                                  (print (length bestpath))
                                  (print "kaboom")
                                  []
                                  )))

(for [i 1 200]
  (pprint (coroutine.resume worker)))
