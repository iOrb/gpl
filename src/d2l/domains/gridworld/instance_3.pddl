
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;; Instance file automatically generated by the Tarski FSTRIPS writer
;;; 
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(define (problem gridworld-3x3)
    (:domain gridworld)

    (:objects
        
    )

    (:init
        (= (xpos ) 1)
        (= (ypos ) 1)
        (= (maxpos ) 3)
        (= (goal_xpos ) 3)
        (= (goal_ypos ) 3)
    )

    (:goal
        (and (= (xpos ) (goal_xpos )) (= (ypos ) (goal_ypos )))
    )

    
    (:bounds
        (coordinate - int[1..3]))
    
)
