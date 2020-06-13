from manim import *
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures


class Sim(SpecialThreeDScene):
    def construct(self):
        self.set_camera_orientation(**self.get_default_camera_position())

        data = pd.read_csv("sim.csv")
        xVals = data.iloc[:, 0:1].values
        yVals = data.iloc[:, 1].values

        poly = PolynomialFeatures(degree=8)
        x_poly = poly.fit_transform(xVals)
        poly.fit(x_poly, yVals)

        lin = LinearRegression()
        lin.fit(x_poly, yVals)

        customrate = bezier(lin.predict(poly.fit_transform(xVals)))

        obj = Sphere().move_to(np.array([ENDVALUEHERE, 0, 0]))

        self.play(obj.move_to, np.array(
            [STARTVALUEHERE, 0, 0]), rate_func=customrate)

        self.wait()
