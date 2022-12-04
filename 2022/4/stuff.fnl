(lambda sub-array [arr start ?e]
	(let [end (or ?e (length arr))]
		(fcollect [i start end] (. arr i))))

(lambda groups [arr len]
	(var i -1)
	(lambda []
		(set i (+ i 1))
		(let [start (+ (* i len) 1)
			  end (+ start (- len 1))
			  group (sub-array arr start end)]
			(if (> (length group) 0)
				(values i group) nil))))

(local view (require "fennel.view"))

(fn pprint [x] (print (view x)))

(lambda icol [iterator]
	(icollect [a _ iterator] a))
(lambda icol2 [iterator]
	(icollect [_ a iterator] a))

(lambda maps2i [arr]
	(icollect [_ a (ipairs arr)] (tonumber a)))
