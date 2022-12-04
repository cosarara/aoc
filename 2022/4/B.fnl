#!/bin/lu9 /bin/fennel

(local view (require "fennel.view"))

(fn pprint [x] (print (view x)))

(lambda maps2i [arr]
	(icollect [_ a (ipairs arr)] (tonumber a)))

(lambda icol [iterator]
	(icollect [a _ iterator] a))

(lambda split [s sep]
	(icol (s:gmatch (.. "[^" sep "]+"))))

(local file (io.input))
(lambda check-overlap [[range-a range-b]]
	(let [[start-a end-a] (maps2i (split range-a "-"))
		  [start-b end-b] (maps2i (split range-b "-"))]
		(or (<= start-a start-b end-a) (<= start-a end-b end-a)
			(<= start-b start-a end-b))))

(print
	(accumulate [sum 0 line _ (file:lines)]
		(if (check-overlap (split line ","))
			(+ sum 1)
			sum)))

(print "all ok")