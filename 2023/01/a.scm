(use-modules (ice-9 rdelim)
             (ice-9 regex)
             (srfi srfi-1))

(define (get-num line)
  (let* ((matches (list-matches "[0-9]" line))
         (first-last (list (first matches) (last matches)))
         (s (string-concatenate (map match:substring first-last))))
    (string->number s)))

(define (loop-lines f)
  (let ((line (read-line)))
    (if (eof-object? line)
      '()
      (cons (f line) (loop-lines f)))))

(define (sum l) (fold + 0 l))

(define (part-1 filename)
  (with-input-from-file
    filename
    (lambda () (display (sum (loop-lines get-num))))))

(part-1 "example.txt")
(newline)
(part-1 "input.txt")
(newline)
