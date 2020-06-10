import time
import numpy as np
import matplotlib.pyplot as plt
plt.style.use('seaborn')


class PID:
    def __init__(self, kP, kI, kD, fromVal, toVal, prec, time, waitBool):
        """Init function run to declare variables within class scope

        Args:
            kP (float): Constant gain value for proportional controller
            kI (float): Constant gain value for integral controller
            kD (float): Constant gain value for derivative controller
            fromVal (float): The initial value you start from
            toVal (float): The desired setpoint
            prec (int): The number of iterations to run the control loop
            time (int): The amount of time to run the control loop for
            waitBool (bool): Enable/Disable wait time simulation when graphing controller values
        """

        self.kP = kP
        self.kI = kI
        self.kD = kD
        self.fromVal = fromVal
        self.toVal = toVal
        self.dt = 0.00001
        self.integral = 0.0
        self.prev_err = 0.0
        self.derivative = 0.0
        self.prec = prec
        self.time = time
        self.waitBool = waitBool

        self.READfromVal = self.fromVal
        self.READtoVal = self.toVal

    def getFromVal(self):
        """Get the value of fromVal

        Returns:
            float: READfromVal
        """
        return self.READfromVal

    def calcAdjKP(self):
        """Calculate the adjustment based on the proportional controller

        Returns:
            float: adjust
        """
        err = self.toVal - self.fromVal

        adjust = err * self.kP
        return adjust

    def calcAdjKI(self):
        """Calculate the adjustment based on the integral controller

        Returns:
            float: adjust
        """
        err = self.toVal - self.fromVal
        self.integral += err * self.dt

        adjust = self.integral * self.kI
        return adjust

    def calcAdjKD(self):
        """Calculate the adjustment based on the derivative controller

        Returns:
            float: adjust
        """
        err = self.toVal - self.fromVal
        self.prev_err = err

        self.derivative = (err - self.prev_err) / self.dt

        adjust = self.derivative * self.kD
        return adjust

    def update(self):
        """Update position based on the PID controller

        Returns:
            float: fromVal
        """
        adjust = self.calcAdjKP() + self.calcAdjKI() + self.calcAdjKD()
        self.fromVal += adjust
        return self.fromVal

    def graph(self):
        """Graph data from a PID controller object with Matplotlib
        """
        init = self.getFromVal()
        print("Time: 0, Pos: {}".format(init))

        count = 1
        rFeedbackP = []
        ctimeP = []
        updateFreq = self.time/self.prec

        while count <= self.prec:
            feedback = self.update()

            ctime = float(round(count * updateFreq, 1))
            rFeedback = float(round(feedback, 5))

            print("Time: {}, Pos: {}".format(ctime, rFeedback))

            rFeedbackP.append(rFeedback)
            ctimeP.append(ctime)

            if self.waitBool:
                time.sleep(updateFreq)

            count += 1

        plt.plot(ctimeP, rFeedbackP)
        plt.title("raPID Chart")
        plt.xlabel("Time (s)")
        plt.ylabel("Position (m)")
        plt.show()

    def gen_manim(self):
        """Animate movement of object according to PID loop with Manim
        """

        arr = []

        init = self.getFromVal()
        arr.append(init)

        count = 1

        while count <= self.prec:
            feedback = self.update()

            rFeedback = float(round(feedback, 5))
            arr.append(rFeedback)

            count += 1

        interval = round(1 / self.prec, 5)
        intervalC = 0

        npArr = np.array(arr)
        npArr = np.interp(npArr, (npArr.min(), npArr.max()), (0, +1))

        open("sim/sim.csv", 'w').close()

        for i in npArr:
            timestamp = interval * intervalC
            with open('sim.csv', 'a') as file:
                file.write(str('{0:.4f}'.format(round(timestamp, 4))) +
                           "," + str('{0:.4f}'.format(round(i, 4))) + "\n")
            intervalC += 1

        with open('sim/sim.py', 'r') as file:
            filedata = file.read()

        filedata = filedata.replace("ENDVALUEHERE", str(self.READtoVal))
        filedata = filedata.replace("STARTVALUEHERE", str(self.READfromVal))

        with open('sim/sim.py', 'w') as file:
            file.write(filedata)
