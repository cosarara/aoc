#!/bin/lu9 /bin/fennel

(local view (require "fennel.view"))

(fn pprint [x] (print (view x)))

(lambda icol [iterator]
	(icollect [a _ iterator] a))

(lambda split [s sep]
	(icol (s:gmatch (.. "[^" sep "]+"))))

(lambda maps2i [arr]
	(icollect [_ a (ipairs arr)] (tonumber a)))

(lambda check-contains [[range-a range-b]]
	(let [[start-a end-a] (maps2i (split range-a "-"))
		  [start-b end-b] (maps2i (split range-b "-"))]
		(or (and (<= start-a start-b) (>= end-a end-b))
			(and (<= start-b start-a) (>= end-b end-a)))))

(local file (io.input))

(print
	(accumulate [sum 0 line _ (file:lines)]
		(if (check-contains (split line ","))
			(+ sum 1)
			sum)))

(print "all ok")