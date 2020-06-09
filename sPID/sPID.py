class PID:
    def __init__(self, kP, kI, kD, toApproach):
        self.kP = kP
        self.kI = kI
        self.kD = kD
        self.toApproach = toApproach

    def calcKP(self, feedback):
        self.feedback = feedback
        err = self.toApproach - self.feedback

        adjust = err * kP
        return adjust
