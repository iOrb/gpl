(define (problem BLOCKS-5-CLEAR-X)
(:domain BLOCKS)
(:objects A B C D E)
(:init (ON E D) (ON D C) (ON C A) (ON A B) (ONTABLE B) (CLEAR E) (HANDEMPTY))
(:goal (AND (CLEAR A)))
)
