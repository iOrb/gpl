(define (problem BLOCKS-5-CLEAR-X)
(:domain BLOCKS)
(:objects A B C D E F G)
(:init (ON G F) (ON F E) (ON E C) (ON C B) (CLEAR G) (ONTABLE B)
       (ON A D) (CLEAR A) (ONTABLE D)
       (HANDEMPTY))
(:goal (AND (ON A B)))
)
