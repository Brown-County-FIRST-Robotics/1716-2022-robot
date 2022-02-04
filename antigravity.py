import logging
import wpilib
import wpilib.drive
import ctre
from wpilib import interfaces
import rev
import math

class MyRobot(wpilib.TimedRobot):
    def testInit(self):
        self.motor = rev.CANSparkMax(0)
        self.controller = wpilib.XboxController(0)
        self.encoder = rev.RelativeEncoder
        self.antigravity_multiplier = .15 #placeholder value, needs testing
        self.encoder.setPositionConversionFactor(360)

    def antigrav_force(self, position):
        position = math.cos(position)
        position = position * self.antigravity_multiplier
        return position

    def testPeriodic(self):
        if self.controller.getYButtonPressed:
            self.antigravity_multiplier = self.antigravity_multiplier + .01
            print(self.antigravity_multiplier)
        elif self.controller.getAButtonPressed:
            self.antigravity_multiplier = self.antigravity_multiplier - .01
            print(self.antigravity_multiplier)
        elif self.controller.getStartButtonPressed:
            self.antigravity_multiplier = self.antigravity_multiplier + .001
            print(self.antigravity_multiplier)
        elif self.controller.getBackButtonPressed:
            self.antigravity_multiplier = self.antigravity_multiplier - .001
            print(self.antigravity_multiplier)

if __name__ == "__main__":
        wpilib.run(MyRobot)