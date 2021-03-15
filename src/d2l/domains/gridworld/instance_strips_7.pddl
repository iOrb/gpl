
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;; Instance file automatically generated by the Tarski FSTRIPS writer
;;; 
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(define (problem gridworld-7x7)
    (:domain gridworld-strips)

    (:objects
        c1 c2 c3 c4 c5 c6 c7 - coordinate
    )

    (:init
        (= (xpos ) c1)
        (= (ypos ) c1)
        (= (maxpos ) c7)
        (= (goal_xpos ) c7)
        (= (goal_ypos ) c7)
        (succ c4 c5)
        (succ c6 c7)
        (succ c1 c2)
        (succ c3 c4)
        (succ c2 c3)
        (succ c5 c6)
    )

    (:goal
        (and (= (xpos ) (goal_xpos )) (= (ypos ) (goal_ypos )))
    )

    
    
    
)

