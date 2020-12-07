#lang racket
(define day2 "1,0,0,3,1,1,2,3,1,3,4,3,1,5,0,3,2,6,1,19,2,19,9,23,1,23,5,27,2,6,27,31,1,31,5,35,1,35,5,39,2,39,6,43,2,43,10,47,1,47,6,51,1,51,6,55,2,55,6,59,1,10,59,63,1,5,63,67,2,10,67,71,1,6,71,75,1,5,75,79,1,10,79,83,2,83,10,87,1,87,9,91,1,91,10,95,2,6,95,99,1,5,99,103,1,103,13,107,1,107,10,111,2,9,111,115,1,115,6,119,2,13,119,123,1,123,6,127,1,5,127,131,2,6,131,135,2,6,135,139,1,139,5,143,1,143,10,147,1,147,2,151,1,151,13,0,99,2,0,14,0")
(define (parse input) (list->vector (map string->number (string-split input ","))))

(define (run program)
  ;; internal variables
  (define pc 0)
  (define mem (vector-copy program))
  ;; helper functions
  (define (at addr)
    (vector-ref mem addr))
  (define (read)
    (define v (at pc))
    (set! pc (+ 1 pc))
    v)
  (define (write addr value)
    (vector-set! mem addr value))

  ;; main loop
  (let loop ()
    (define inst (read))
    ;;(println inst)
    (define opcode (modulo inst 100))
    (case opcode
      [(1) ; add
       (define a (read))
       (define b (read))
       (define c (read))
       (write c (+ (at a) (at b)))]
      [(2) ; mul
       (define a (read))
       (define b (read))
       (define c (read))
       (write c (* (at a) (at b)))])
    (if (equal? 99 opcode)
        (vector-ref mem 0)
        (loop))))

; day 2
(define day2-mem (parse day2))
(vector-set! day2-mem 1 12)
(vector-set! day2-mem 2 2)
(printf "day2 ~a\n" (equal? (run day2-mem) 4576384))

; day 2 b
(define (with-nv noun verb)
  (vector-set! day2-mem 1 noun)
  (vector-set! day2-mem 2 verb)
  (run day2-mem))
(define day2-b (for*/list
                   ([noun 99]
                    [verb 99]
                    #:when (equal? (with-nv noun verb) 19690720))
                 (list noun verb)))
(printf "day2b ~a\n" (equal? day2-b '((53 98))))

