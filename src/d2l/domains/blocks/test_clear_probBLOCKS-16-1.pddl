(define (problem BLOCKS-16-1)
(:domain BLOCKS)
(:objects K C D B I N P J M L G E A O H F )
(:INIT (CLEAR F) (CLEAR H) (CLEAR O) (ONTABLE A) (ONTABLE E) (ONTABLE G)
 (ON F L) (ON L M) (ON M J) (ON J P) (ON P N) (ON N I) (ON I B) (ON B D)
 (ON D C) (ON C K) (ON K A) (ON H E) (ON O G) (HANDEMPTY))
(:goal (AND (CLEAR A)))

)