import matplotlib.pyplot as plt
import time


class PID:
    def __init__(self, kP, kI, kD, fromVal, toVal, prec, time, waitBool):
        """Init function run to declare variables within class scope

        :param kP: Constant gain value for proportional controller
        :type kP: float
        :param kI: Constant gain value for integral controller
        :type kI: float
        :param kD: Constant gain value for derivative controller
        :type kD: float
        :param fromVal: The initial value you start from
        :type fromVal: float
        :param toVal: The desired setpoint
        :type toVal: float
        :param prec: The number of iterations to run the control loop
        :type prec: int
        :param time: The amount of time to run the control loop for
        :type time: int
        :param waitBool: Enable/Disable wait time simulation when graphing controller values
        :type waitBool: bool
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

    def getFromVal(self):
        """Get the value of FromVal

        :return: fromVal
        :rtype: string
        """
        return self.fromVal

    def calcAdjKP(self):
        """Calculate the adjustment based on the proportional controller

        :return: adjust
        :rtype: float
        """
        err = self.toVal - self.fromVal

        adjust = err * self.kP
        return adjust

    def calcAdjKI(self):
        """Calculate the adjustment based on the integral controller

        :return: adjust
        :rtype: float
        """
        err = self.toVal - self.fromVal
        self.integral += err * self.dt

        adjust = self.integral * self.kI
        return adjust

    def calcAdjKD(self):
        """Calculate the adjustment based on the derivative controller

        :return: adjust
        :rtype: float
        """
        err = self.toVal - self.fromVal
        self.prev_err = err

        self.derivative = (err - self.prev_err) / self.dt

        adjust = self.derivative * self.kD
        return adjust

    def update(self):
        """Update position based on the PID controller

        :return: fromVal
        :rtype: float
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
        plt.show()
