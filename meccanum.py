import wpilib
import ctre
import logging

class MyRobot(wpilib.TimedRobot):

    def testInit(self):
        #Robot initialization function
        #declares motors (edit this later to use left/right, front/back)
        self.motor1 = ctre.WPI_TalonFX(0)
        self.motor2 = ctre.WPI_TalonFX(1)
        self.motor3 = ctre.WPI_TalonFX(2)
        self.motor4 = ctre.WPI_TalonFX(3)

        self.controller = wpilib.XboxController(0)  #declares joystick

    def testPeriodic(self):
        # Joystick input to motor output
        if abs(self.controller.Axis.kRightX()) > .2: #code for turning in place by rotating the joystick
            logging.debug("rotated")
            self.motor1.set(self.controller.Axis.kRightX() * .1)
            self.motor1.set(self.controller.Axis.kRightX() * .1)
            self.motor1.set(-self.controller.Axis.kRightX() * .1)
            self.motor1.set(-self.controller.Axis.kRightX() * .1)
        elif abs(self.controller.Axis.kLeftY()) > .2 and abs(self.controller.Axis.kLeftX()) < .6: #moving forward
            logging.debug("fowards/backwards")
            self.motor1.set(self.controller.Axis.kLeftY() * .1)
            self.motor2.set(self.controller.Axis.kLeftY() * .1)
            self.motor3.set(self.controller.Axis.kLeftY() * .1)
            self.motor4.set(self.controller.Axis.kLeftY() * .1)
        elif abs(self.controller.Axis.kLeftX()) > .2 and abs(self.controller.Axis.kLeftY()) < .6: #basic turning
            logging.debug("left/right")
            self.motor1.set(-self.controller.Axis.kLeftX() * .1)
            self.motor2.set(self.controller.Axis.kLeftX() * .1)
            self.motor3.set(self.controller.Axis.kLeftX() * .1)
            self.motor4.set(-self.controller.Axis.kLeftX() * .1)
        elif (self.controller.Axis.kLeftY() > .6) and (self.controller.Axis.kLeftX() > .6): #forward and right
            logging.debug("forward and right")
            self.motor1.set(0)
            self.motor2.set(.1)
            self.motor3.set(.1)
            self.motor4.set()
        elif (self.controller.Axis.kLeftY() > .6) and (-self.controller.Axis.kLeftX() < -.6): #forward and left
            logging.debug("forward and left")
            self.motor1.set(.1)
            self.motor2.set(0)
            self.motor3.set(0)
            self.motor4.set(.1)
        elif (-self.controller.Axis.kLeftY() < -.6) and (self.controller.Axis.kLeftX() > .6): #backward and right
            logging.debug("backward and right")
            self.motor1.set(-.1)
            self.motor2.set(0)
            self.motor3.set(0)
            self.motor4.set(-.1)
        elif (-self.controller.Axis.kLeftY() < -.6) and (-self.controller.Axis.kLeftX() < -.6): #backward and left
            logging.debug("backward and left")
            self.motor1.set(0)
            self.motor2.set(-.1)
            self.motor3.set(-.1)
            self.motor4.set(0)
        else:
            self.motor1.set(0)
            self.motor2.set(0)
            self.motor3.set(0)
            self.motor4.set(0)
            
if __name__ == "__main__":
    wpilib.run(MyRobot)