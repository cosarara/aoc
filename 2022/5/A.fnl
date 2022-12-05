#!/bin/lu9 /bin/fennel

(local view (require "fennel.view"))

(fn pprint [x] (print (view x)))

(local file (io.open "example"))
(local lines (icollect [line _ (file:lines)] line))

(local stacks {})

(each [i line (pairs lines)]
	(print line)
	(let [len (length line)
		width (math.ceil (/ len 4))] ; "[?] "
		(print len width)
		(for [i 1 width]
			(let [s (+ 1 (* (- i 1) 4))
				crate (line:sub s (+ s 3))]
				(if (crate:find "[" 1 true)
					(print "crate" crate "line" line "i" i))))))
