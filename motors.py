import logging
import wpilib
import wpilib.drive
import ctre
from wpilib import interfaces

class MyRobot(wpilib.TimedRobot):
    def testInit(self):
        self.front_right = ctre.WPI_TalonFX(0)
        self.front_left = ctre.WPI_TalonFX(1) 
        self.back_left = ctre.WPI_TalonFX(2)
        self.back_right = ctre.WPI_TalonFX(3)
        self.intake = ctre.WPI_TalonFX(4)
        self.shooter_bottom = ctre.WPI_TalonFX(5)
        self.shooter_top = ctre.WPI_TalonFX(6)
        self.shooter_angle = ctre.WPI_TalonFX(7)
        self.queuer = ctre.WPI_TalonFX(8)
        self.climber_FR = ctre.WPI_TalonFX(9)
        self.climber_FL = ctre.WPI_TalonFX(10)
        self.climber_BL = ctre.WPI_TalonFX(11)
        self.climber_BR = ctre.WPI_TalonFX(12)
        self.climber_angle = ctre.WPI_TalonFX(13)

        
        self.front_left.setInverted(True)
        self.back_left.setInverted(True)
        self.shooter_top.setInverted(True)

        self.shooter = wpilib.SpeedControllerGroup(self.shooter_top, self.shooter_bottom)
        self.left = wpilib.SpeedControllerGroup(self.front_left, self.front_right)
        self.right = wpilib.SpeedControllerGroup(self.front_right, self.back_right)
        self.drive = wpilib.drive.DifferentialDrive(self.left, self.right)

        self.left_hand = interfaces._interfaces.GenericHID.Hand.kLeftHand
        self.right_hand = interfaces._interfaces.GenericHID.Hand.kRightHand
        self.controller = wpilib.XboxController(0)
        self.controllerHID = interfaces.GenericHID(0)
        self.rumbleType = interfaces.GenericHID.RumbleType.kLeftRumble

        self.queuer_on = 0

    def testPeriodic(self):
        if self.controller.getBackButtonPressed(): #queuer toggle
            if self.queuer_on == 0:
                self.queuer_on = 1
            else:
                self.queuer_on = 0
        self.queuer.set(self.queuer_on * .2)
        self.intake.set(self.controller.getBumper(self.left_hand) * .2)
        self.shooter.set(self.controller.getTriggerAxis(self.right_hand))
        self.controllerHID.setRumble(self.rumbleType, self.controller.getTriggerAxis(self.right_hand))
        if self.controllerHID.getPOV() == 0: #shooter angle with D-pad
            self.shooter_angle.set(.2)
        elif self.controllerHID.getPOV() == 180:
            self.shooter_angle.set(-.2)
        else:
            self.shooter_angle.set(0)
        
        

        
if __name__ == "__main__":
    wpilib.run(MyRobot)