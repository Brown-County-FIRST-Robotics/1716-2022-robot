#shooter angling
from ast import While
from cmath import sqrt
from pickle import NONE
import wpilib
import ctre
import rev
import sys
from networktables import NetworkTables
import math

class MyRobot(wpilib.TimedRobot):
    def testInit(self):
        self.motor1 = ctre.WPI_TalonFX(4)
        self.motor2 = ctre.WPI_TalonFX(5)
        self.back_right = ctre.WPI_TalonFX(0)
        self.front_left = ctre.WPI_TalonFX(1) 
        self.back_left = ctre.WPI_TalonFX(2)
        self.front_right = ctre.WPI_TalonFX(3)

        self.motor1.setInverted(True)
        self.motor1.configSelectedFeedbackSensor(1)
        self.motor2.configSelectedFeedbackSensor(1)

        self.shooterAngleMotors = wpilib.MotorControllerGroup(self.motor1, self.motor2)
        self.controller = wpilib.XboxController

        self.timer = wpilib.Timer()
        self.timer.start()
        self.sensor = self.motor1.getSensorCollection()
        self.sensor.setIntegratedSensorPosition(0)
    
    def shoot(self) -> None:
        while self.sensor.getIntegratedSensorPosition() < (45 * (256/45)) and NetworkTables.getTable("limelight").getNumber('tv', 0) == 0: #coversion factor from sensor ticks to degrees is 45/256
            self.shooterAngleMotors.set(.5)
        while self.sensor.getIntegratedSensorPosition() > (45 * (256/45)) and NetworkTables.getTable("limelight").getNumber('tv', 0) == 0:
            self.shooterAngleMotors.set(-.5)
        self.shooterAngleMotors.set(0)
        while NetworkTables.getTable("limelight").getNumber('tv', 0) == 0:
            self.back_right.set(.5)
            self.front_left.set(.5)
            self.back_left.set(.5)
            self.front_right.set(.5)
            if self.controller.getBackButtonPressed():
                break
        self.back_right.set(0)
        self.front_left.set(0)
        self.back_left.set(0)
        self.front_right.set(0)

        while NetworkTables.getTable("limelight").getNumber('tx', 0) < 0: #horizontal offset
            self.back_right.set(.3)
            self.front_left.set(.3)
            self.back_left.set(.3)
            self.front_right.set(.3)
        while NetworkTables.getTable("limelight").getNumber('tx', 0) > 0:
            self.back_right.set(-.3)
            self.front_left.set(-.3)
            self.back_left.set(-.3)
            self.front_right.set(-.3)
        self.back_right.set(-.3)
        self.front_left.set(-.3)
        self.back_left.set(-.3)
        self.front_right.set(-.3)            
        while NetworkTables.getTable("limelight").getNumber('ty', 0) < 0: #vertical offset
            self.shooterAngleMotors.set(.3)
        while NetworkTables.getTable("limelight").getNumber('ty', 0) < 0:
            self.shooterAngleMotors.set(-.3)
        self.shooterAngleMotors.set(0)

        self.distance = NetworkTables.getTable("limelight").getNumber('ta', 0) * 1#<insert conversion factor to meters here>
        self.angle = self.sensor.getIntegratedSensorPosition() * (45/256)
        self.shooterHeight = ((180 / (math.sin(self.angle) * math.pi)) * 1) + 0 # * arm length + chassis height (with a conversion from radians to degrees) 
        self.basketY = (10400/3937) - self.shooterHeight #top basket total height in meters - shooter height to make the shot from (0, 0)
        self.basketX = math.sqrt((self.distance ** 2) - (self.basketY ** 2)) #pythagorean theorem
        self.basketY += .30 #height raised to aim for basket (in meters), not for reflective strip and to allow ball to clear rim
        self.angle_plus = 180 / (math.atan(((1 ** 2) + math.sqrt((1 ** 4) - (9.80665 * ((9.80665 * (self.basketX ** 2)) + (2 * (self.basketY * (1 ** 2))))))) / (self.basketX * 9.80665)) * math.pi)
        self.angle_minus = 180 / (math.atan(((1 ** 2) - math.sqrt((1 ** 4) - (9.80665 * ((9.80665 * (self.basketX ** 2)) + (2 * (self.basketY * (1 ** 2))))))) / (self.basketX * 9.80665)) * math.pi)
       
        if self.angle_plus > self.angle_minus: #sets the shooter angle to whichever is larger, plus or minus
            self.angle = self.angle_plus
        if self.angle_minus > self.angle_plus:
            self.angle = self.angle_minus
        while self.sensor.getIntegratedSensorPosition() < (self.angle * (256/45)):
            self.shooterAngleMotors.set(.3)
        while self.sensor.getIntegratedSensorPosition() > (self.angle * (256/45)):
            self.shooterAngleMotors.set(-.3)
        self.shooterAngleMotors.set(0)


if __name__ == "__main__":
    wpilib.run(MyRobot)