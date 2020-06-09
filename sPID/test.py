from sPID import *
import time
import matplotlib.pyplot as plt

controller = PID(0.2, 0, 0, 0, 5)

prec = 15

init = controller.getFromVal()
print("Time: 0, Pos: {}".format(init))

count = 1
rFeedbackP = []
ctimeP = []

while count <= prec:
    feedback = controller.update()

    ctime = float(round(count*0.2, 1))
    rFeedback = float(round(feedback, 5))

    print("Time: {}, Pos: {}".format(ctime, rFeedback))

    rFeedbackP.append(rFeedback)
    ctimeP.append(ctime)

    # time.sleep(0.2)
    count += 1

plt.plot(ctimeP, rFeedbackP)
plt.show()
