#lang racket
(define (move n src dest temp)
  (if (> n 0)
      (begin
        (move (- n 1) src temp dest)
        (printf "move ~a from ~a to ~a~n" n src dest)
        (move (- n 1) temp dest src))
      "done"))

(move 3 "src" "dest" "temp")
