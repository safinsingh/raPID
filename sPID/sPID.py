class PID:
    def __init__(self, kP, kI, kD, fromVal, toVal):
        self.kP = kP
        self.kI = kI
        self.kD = kD
        self.fromVal = fromVal
        self.toVal = toVal

    def getFromVal(self):
        return self.fromVal

    def calcAdjKP(self, feedback):
        self.feedback = feedback
        err = self.toVal - self.feedback

        adjust = err * self.kP
        return adjust

    def update(self):
        adjust = self.calcAdjKP(self.fromVal)
        self.fromVal += adjust
        return self.fromVal
