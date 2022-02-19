# shooter angling
from ast import While
from cmath import sqrt
from operator import ne
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

        self.shooterAngleMotors = wpilib.MotorControllerGroup(self.motor1, self.motor2)
        self.controller = wpilib.XboxController

        self.timer = wpilib.Timer()
        self.timer.start()
        self.motor1.configSelectedFeedbackSensor(ctre.FeedbackDevice.IntegratedSensor)
        self.shooter_dictionary = {
            "shoooting": False,
            "step" : 0,
            "previous_position" : 0,
            "lock_on_mode" : False
        }

    def shoot(self, shooter_dictionary, speed = 1) -> dict:
        if shooter_dictionary["previous_position"] < (45 * (256 / 45)) and NetworkTables.getTable("limelight").getNumber("tv", 0) == 0 and shooter_dictionary["step"] == 0:
            if self.motor1.getSelectedSensorPosition() < (45 * (256 / 45)) and NetworkTables.getTable("limelight").getNumber("tv", 0) == 0:  # coversion factor from sensor ticks to degrees is 45/256
                self.shooterAngleMotors.set(speed)
        elif shooter_dictionary["previous_position"] > (45 * (256 / 45)) and NetworkTables.getTable("limelight").getNumber("tv", 0) == 0 and shooter_dictionary["step"] == 0:
            if (self.motor1.getSelectedSensorPosition() > (45 * (256 / 45)) and NetworkTables.getTable("limelight").getNumber("tv", 0) == 0):
                self.shooterAngleMotors.set(-speed)
        elif shooter_dictionary["step"] == 0:
            self.shooterAngleMotors.set(0)
            self.shooter_dictionary["step"] = 1

        if NetworkTables.getTable("limelight").getNumber("tv", 0) == 0 and (shooter_dictionary["step"] == 0 or shooter_dictionary["step"] == 1):
            self.back_right.set(speed)
            self.front_left.set(speed)
            self.back_left.set(speed)
            self.front_right.set(speed)
        
        elif  NetworkTables.getTable("limelight").getNumber("tv", 0) == 1 and (shooter_dictionary["step"] == 0 or shooter_dictionary["step"] == 1):
            self.shooterAngleMotors.set(0)
            self.back_right.set(0)
            self.front_left.set(0)
            self.back_left.set(0)
            self.front_right.set(0)
            self.shooter_dictionary["step"] = 2


        if NetworkTables.getTable("limelight").getNumber("tx", 0) < 0 and self.shooter_dictionary["step"] == 2:  # horizontal offset
            self.back_right.set(speed * 0.5)
            self.front_left.set(-speed * 0.5)
            self.back_left.set(-speed * 0.5)
            self.front_right.set(speed * 0.5)
        elif NetworkTables.getTable("limelight").getNumber("tx", 0) > 0 and self.shooter_dictionary["step"] == 2:
            self.back_right.set(-speed * 0.5)
            self.front_left.set(speed * 0.5)
            self.back_left.set(speed * 0.5)
            self.front_right.set(-speed * 0.5)
        elif NetworkTables.getTable("limelight").getNumber("tx", 0) == 0 and self.shooter_dictionary["step"] == 2:
            self.back_right.set(0)
            self.front_left.set(0)
            self.back_left.set(0)
            self.front_right.set(0)

        if NetworkTables.getTable("limelight").getNumber("ty", 0) < 0 and self.shooter_dictionary["step"] == 2:  # vertical offset
            self.shooterAngleMotors.set(speed * .5)
        elif NetworkTables.getTable("limelight").getNumber("ty", 0) > 0 and self.shooter_dictionary["step"] == 2:
            self.shooterAngleMotors.set(speed * .5)
        elif NetworkTables.getTable("limelight").getNumber("ty", 0) == 0 and self.shooter_dictionary["step"] == 2:
            self.shooterAngleMotors.set(0)
    
        if self.front_right.getMotorOutputPercent() == 0 and self.motor1.getMotorOutputPercent() == 0:
            shooter_dictionary["step"] = 3

        if shooter_dictionary["step"] == 3:
            self.distance = (NetworkTables.getTable("limelight").getNumber("ta", 0) * 1)  # <insert conversion factor from percent to meters here>
            self.angle = self.motor1.getSelectedSensorPosition() * (45 / 256)
            self.shooterHeight = ((180 / (math.sin(self.angle) * math.pi)) * 1) + 0  # * arm length + chassis height (with a conversion from radians to degrees)
            self.basketY = (10400 / 3937) - self.shooterHeight  # top basket total height in meters - shooter height to make the shot from (0, 0)
            self.basketX = math.sqrt((self.distance ** 2) - (self.basketY ** 2))  # pythagorean theorem
            self.basketY += 0.30  # height raised to aim for basket (in meters), not for reflective strip and to allow ball to clear rim
            self.angle_plus = 180 / (math.atan(((1**2)+ math.sqrt((1**4)- (9.80665* ((9.80665 * (self.basketX**2)) + (2 * (self.basketY * (1**2))))))) / (self.basketX * 9.80665)) * math.pi)
            self.angle_minus = 180 / (math.atan(((1**2)- math.sqrt((1**4) - (9.80665 * ((9.80665 * (self.basketX**2)) + (2 * (self.basketY * (1**2))))))) / (self.basketX * 9.80665)) * math.pi)

            if self.angle_plus > self.angle_minus:  # sets the shooter angle to whichever is larger, plus or minus
                self.angle = self.angle_plus
            elif  self.angle_plus < self.angle_minus:
                self.angle = self.angle_minus
            
            shooter_dictionary["previous_position"] = self.motor1.getSelectedSensorPosition

            shooter_dictionary["step"] = 4
        
        if self.shooter_dictionary["previous_position"] < (self.angle * (256 / 45)) and shooter_dictionary["step"] == 4:
            if self.motor1.getSelectedSensorPosition() < (self.angle * (256 / 45)):
                self.shooterAngleMotors.set(speed * .3)
        elif self.shooter_dictionary["previous_position"] > (self.angle * (256 / 45)) and shooter_dictionary["step"] == 4:
            if self.motor1.getSelectedSensorPosition() > (self.angle * (256 / 45)):
                self.shooterAngleMotors.set(-speed * .3)
        elif shooter_dictionary["step"] == 4:
            self.shooterAngleMotors.set(0)
            shooter_dictionary["shooting"] = False
            return shooter_dictionary
        shooter_dictionary["shooting"] = True
        return shooter_dictionary
   
    def testPeriodic(self):
        if self.controller.getRightBumperPressed:
            self.shooter_dictionary["previous_position"] = self.motor1.getSelectedSensorPosition
            self.shooter_dictionary = self.shoot(self.shooter_dictionary)
        elif self.shooter_dictionary["shooting"]:
            self.shooter_dictionary = self.shoot(self.shooter_dictionary)

        elif self.controller.getBackButtonPressed:
            self.shooter_dictionary["shooting"] = False
        
        if self.shooter_dictionary["step"] == 1:
            ... #d-pad shooter angle control code here
        
if __name__ == "__main__":
    wpilib.run(MyRobot)
