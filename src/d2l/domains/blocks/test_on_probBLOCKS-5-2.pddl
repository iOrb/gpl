(define (problem BLOCKS-5-2)
(:domain BLOCKS)
(:objects A C E B D )
(:INIT (CLEAR D) (ONTABLE B) (ON D E) (ON E C) (ON C A) (ON A B) (HANDEMPTY))
(:goal (AND (ON A B)))
)