(use-modules (ice-9 rdelim)
             (ice-9 regex)
             (srfi srfi-1))
(import (rnrs hashtables (6)))

(define (new-string-hash l)
  (let ((my-hash (make-hashtable string-hash equal?)))
    (map (lambda (mapping)
           (hashtable-set! my-hash (first mapping) (second mapping)))
         l)
    my-hash))

(define num-hash
  (new-string-hash
    '(("one" "1")
      ("two" "2")
      ("three" "3")
      ("four" "4")
      ("five" "5")
      ("six" "6")
      ("seven" "7")
      ("eight" "8")
      ("nine" "9"))))

(define (convert-numeric s)
  (hashtable-ref num-hash s s))

(define (get-num line)
  (let* ((matches (list-matches
                    "[0-9]|one|two|three|four|five|six|seven|eight|nine" line))
         (first-last (list (first matches) (last matches)))
         (numeric (map (lambda (s) (convert-numeric (match:substring s)))
                       first-last))
         (s (string-concatenate numeric)))
    (string->number s)))

(define (loop-lines f)
  (let ((line (read-line)))
    (if (eof-object? line)
      '()
      (cons (f line) (loop-lines f)))))

(define (sum l) (fold + 0 l))

(define (part-2 filename)
  (with-input-from-file
    filename
    (lambda () (display (sum (loop-lines get-num))))))

(part-2 "example.txt")
(newline)
(part-2 "input.txt")
(newline)
