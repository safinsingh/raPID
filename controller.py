from raPID import *

controller = PID(0.2, 171, 0.001, 5, 0, 15, 3, False)

controller.graph()

controller2 = PID(0.2, 171, 0.001, 5, 0, 15, 3, False)

controller2.gen_manim()
