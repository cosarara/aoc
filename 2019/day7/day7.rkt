#lang racket
(require racket/generator)
(define (parse input) (list->vector (map string->number (string-split input ","))))

(define (run program [input '()])
  ;; internal variables
  (define pc 0)
  (define inst 0)
  (define rb 0)
  (define mem (vector-copy program))
  ;; helper functions
  (define (at addr)
    (vector-ref mem addr))
  (define (read)
    (define v (at pc))
    (set! pc (+ 1 pc))
    v)
  (define (in-param)
    (define v (read))
    ; 0 = position mode (default)
    ; 1 = immediate
    ; 2 = relative
    (cond [(= (modulo inst 10) 0)
           (set! v (at v))]
          [(= (modulo inst 10) 2)
           (set! v (at (+ rb v)))])
    (set! inst (quotient inst 10))
    v)
  (define (out-param)
    (define v (read))
    (when (= (modulo inst 10) 2)
      (set! v (at (+ rb v))))
    (set! inst (quotient inst 10))
    v)
  (define (write addr value)
    (vector-set! mem addr value))

  ;; main loop
  (let loop ()
    (set! inst (read))
    ;(printf "INSTRUCTION: ~a\n" inst)
    (define opcode (modulo inst 100))
    (set! inst (quotient inst 100))
    (case opcode
      [(1) ; add
       (define a (in-param))
       (define b (in-param))
       (define c (out-param))
       (write c (+ a b))]
      [(2) ; mul
       (define a (in-param))
       (define b (in-param))
       (define c (out-param))
       (write c (* a b))]
      [(3) ; input->mem
       (define a (out-param))
       (write a (let ([v (car input)]) ; pop from input
                  (set! input (cdr input))
                  v))]
      [(4) #t] ; output handled later
      [(5) ; jump-if-true
       (define a (in-param))
       (define b (in-param))
       (unless (= a 0)
         (set! pc b))]
      [(6) ; jump-if-false
       (define a (in-param))
       (define b (in-param))
       (when (= a 0)
         (set! pc b))]
      [(7) ; lt
       (define a (in-param))
       (define b (in-param))
       (define c (out-param))
       (write c (if (< a b) 1 0))]
      [(8) ; eq
       (define a (in-param))
       (define b (in-param))
       (define c (out-param))
       (write c (if (= a b) 1 0))]
      [(99) #t] ; end handled later
      [else
       (print "bug")
       (exit (list opcode pc mem))])
    (case opcode
      [(99) ; end handled here
       (list (vector-ref mem 0) #f)
       ;mem
       ]
      [(4) ; output handled here
       (define a (in-param))
       (list a
             (lambda (x)
               (set! input x)
               (loop)))]
      [else
       (loop)])))

(define (srun in) (car (run in)))

(define (day2)
  (define input "1,0,0,3,1,1,2,3,1,3,4,3,1,5,0,3,2,6,1,19,2,19,9,23,1,23,5,27,2,6,27,31,1,31,5,35,1,35,5,39,2,39,6,43,2,43,10,47,1,47,6,51,1,51,6,55,2,55,6,59,1,10,59,63,1,5,63,67,2,10,67,71,1,6,71,75,1,5,75,79,1,10,79,83,2,83,10,87,1,87,9,91,1,91,10,95,2,6,95,99,1,5,99,103,1,103,13,107,1,107,10,111,2,9,111,115,1,115,6,119,2,13,119,123,1,123,6,127,1,5,127,131,2,6,131,135,2,6,135,139,1,139,5,143,1,143,10,147,1,147,2,151,1,151,13,0,99,2,0,14,0")
  (define day2-mem (parse input))
  (vector-set! day2-mem 1 12)
  (vector-set! day2-mem 2 2)
  ;(println (run day2-mem))
  (printf "day2 ~a\n" (equal? (srun day2-mem) 4576384))

  ; day 2 b
  (define (with-nv noun verb)
    (vector-set! day2-mem 1 noun)
    (vector-set! day2-mem 2 verb)
    (srun day2-mem))
  (define day2-b (for*/list
                     ([noun 99]
                      [verb 99]
                      #:when (equal? (with-nv noun verb) 19690720))
                   (list noun verb)))
  (printf "day2b ~a\n" (equal? day2-b '((53 98)))))
(day2)

(define (day5)
  ; part A
  (define input "3,225,1,225,6,6,1100,1,238,225,104,0,1102,57,23,224,101,-1311,224,224,4,224,1002,223,8,223,101,6,224,224,1,223,224,223,1102,57,67,225,102,67,150,224,1001,224,-2613,224,4,224,1002,223,8,223,101,5,224,224,1,224,223,223,2,179,213,224,1001,224,-469,224,4,224,102,8,223,223,101,7,224,224,1,223,224,223,1001,188,27,224,101,-119,224,224,4,224,1002,223,8,223,1001,224,7,224,1,223,224,223,1,184,218,224,1001,224,-155,224,4,224,1002,223,8,223,1001,224,7,224,1,224,223,223,1101,21,80,224,1001,224,-101,224,4,224,102,8,223,223,1001,224,1,224,1,224,223,223,1101,67,39,225,1101,89,68,225,101,69,35,224,1001,224,-126,224,4,224,1002,223,8,223,1001,224,1,224,1,224,223,223,1102,7,52,225,1102,18,90,225,1101,65,92,225,1002,153,78,224,101,-6942,224,224,4,224,102,8,223,223,101,6,224,224,1,223,224,223,1101,67,83,225,1102,31,65,225,4,223,99,0,0,0,677,0,0,0,0,0,0,0,0,0,0,0,1105,0,99999,1105,227,247,1105,1,99999,1005,227,99999,1005,0,256,1105,1,99999,1106,227,99999,1106,0,265,1105,1,99999,1006,0,99999,1006,227,274,1105,1,99999,1105,1,280,1105,1,99999,1,225,225,225,1101,294,0,0,105,1,0,1105,1,99999,1106,0,300,1105,1,99999,1,225,225,225,1101,314,0,0,106,0,0,1105,1,99999,1007,226,226,224,102,2,223,223,1005,224,329,1001,223,1,223,108,677,226,224,1002,223,2,223,1005,224,344,1001,223,1,223,1007,677,677,224,1002,223,2,223,1005,224,359,1001,223,1,223,1107,677,226,224,102,2,223,223,1006,224,374,1001,223,1,223,8,226,677,224,1002,223,2,223,1006,224,389,101,1,223,223,8,677,677,224,102,2,223,223,1006,224,404,1001,223,1,223,1008,226,226,224,102,2,223,223,1006,224,419,1001,223,1,223,107,677,226,224,102,2,223,223,1006,224,434,101,1,223,223,7,226,226,224,1002,223,2,223,1005,224,449,1001,223,1,223,1107,226,226,224,1002,223,2,223,1006,224,464,1001,223,1,223,1107,226,677,224,1002,223,2,223,1005,224,479,1001,223,1,223,8,677,226,224,1002,223,2,223,1006,224,494,1001,223,1,223,1108,226,677,224,1002,223,2,223,1006,224,509,101,1,223,223,1008,677,677,224,1002,223,2,223,1006,224,524,1001,223,1,223,1008,677,226,224,102,2,223,223,1006,224,539,1001,223,1,223,1108,677,677,224,102,2,223,223,1005,224,554,101,1,223,223,108,677,677,224,102,2,223,223,1006,224,569,101,1,223,223,1108,677,226,224,102,2,223,223,1005,224,584,1001,223,1,223,108,226,226,224,1002,223,2,223,1005,224,599,1001,223,1,223,1007,226,677,224,102,2,223,223,1005,224,614,1001,223,1,223,7,226,677,224,102,2,223,223,1006,224,629,1001,223,1,223,107,226,226,224,102,2,223,223,1005,224,644,101,1,223,223,7,677,226,224,102,2,223,223,1005,224,659,101,1,223,223,107,677,677,224,1002,223,2,223,1005,224,674,1001,223,1,223,4,223,99,226")
  (define day5-mem (parse input))
  (define (run-to-end input)
    (let loop ([out (list 0 (lambda (_) (run day5-mem (list input))))]
               [prev 0])
      (match-define (list diagnostic n) out)
      ;(println diagnostic)
      (if n
          (loop (n '()) diagnostic)
          prev)))
  (printf "day5 ~a\n" (equal? (run-to-end 1) 14155342))
  ;part B
  (printf "day5b ~a\n" (equal? (run-to-end 5) 8684145)))
(day5)

(define (day7)
  ; This took me forever to write and I am not even happy with the result tbh
  (define input "3,8,1001,8,10,8,105,1,0,0,21,38,63,76,93,118,199,280,361,442,99999,3,9,101,3,9,9,102,3,9,9,101,4,9,9,4,9,99,3,9,1002,9,2,9,101,5,9,9,1002,9,5,9,101,5,9,9,1002,9,4,9,4,9,99,3,9,101,2,9,9,102,3,9,9,4,9,99,3,9,101,2,9,9,102,5,9,9,1001,9,5,9,4,9,99,3,9,102,4,9,9,1001,9,3,9,1002,9,5,9,101,2,9,9,1002,9,2,9,4,9,99,3,9,1002,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,2,9,9,4,9,99,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,1,9,4,9,99,3,9,101,1,9,9,4,9,3,9,101,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1002,9,2,9,4,9,99,3,9,1001,9,1,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,1001,9,2,9,4,9,99,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,101,2,9,9,4,9,3,9,1002,9,2,9,4,9,99")
  (define mem (parse input))
  (define (run-amp phase v)
    (run mem (list phase v)))
  (define (vm->gen first-vm)
    (generator (first-val)
               (let loop ([vm first-vm] [val first-val])
                 (match-define (list next next-vm) (vm (list val)))
                 ;(printf "hey hey ~a ~a\n" val next)
                 (if next-vm
                     (loop next-vm (yield next))
                     #f))))
  (define (calculate phases)
    ; initialize vms
    (define prev 0)
    (define vms
      (map (lambda (phase)
             (match-define (list val vm) (run-amp phase prev))
             (set! prev val)
             (vm->gen vm)) phases))

    
    (let loop ()
      (case (generator-state (car vms))
        [(fresh suspended)
         (map (lambda (vm)
                (define next (vm prev))
                ;(println (list next prev))
                (set! prev (or next prev)))
              vms)
         (loop)]))
    prev)
  (define (find-best in)
    (argmax calculate (permutations in)))
  (define best-a (find-best '(0 1 2 3 4)))
  ;(println (list best-a (calculate best-a)))
  (define best-b (find-best '(5 6 7 8 9)))
  ;(println (list best-b (calculate best-b)))
  (printf "day7a ~a\n" (equal? best-a '(0 3 1 2 4)))
  (printf "day7b ~a\n" (equal? best-b '(7 8 5 9 6)))
  )
(day7)