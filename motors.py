import logging
import wpilib
import wpilib.drive
import ctre
from wpilib import interfaces
import rev

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
        self.solenoid0 = wpilib.Solenoid(wpilib.PneumaticsModuleType(0), 0)
        self.solenoid1 = wpilib.Solenoid(wpilib.PneumaticsModuleType(0), 1)
        
        self.front_left.setInverted(True)
        self.back_left.setInverted(True)
        self.shooter_top.setInverted(True)

        self.shooter = wpilib.SpeedControllerGroup(self.shooter_top, self.shooter_bottom)
        self.left = wpilib.SpeedControllerGroup(self.front_left, self.front_right)
        self.right = wpilib.SpeedControllerGroup(self.front_right, self.back_right)
        self.drive = wpilib.drive.DifferentialDrive(self.left, self.right)

        self.controller = wpilib.XboxController(0)
        self.controllerHID = interfaces.GenericHID(0)
        self.rumbleType = interfaces.GenericHID.RumbleType.kLeftRumble

        self.queuer_on = 0
        self.solenoid0.set(False)
        self.solenoid1.set(False)
        
    def testPeriodic(self):
        if self.controller.getBackButtonPressed(): #queuer toggle
            if self.queuer_on == 0:
                self.queuer_on = 1
            else:
                self.queuer_on = 0
        self.queuer.set(self.queuer_on * .2)
        self.intake.set(self.controller.getLeftBumper() * .2)
        self.shooter.set(self.controller.getRightTriggerAxis())
        self.controllerHID.setRumble(self.rumbleType, self.controller.getRightTriggerAxis())
        if self.controllerHID.getPOV() == 0: #shooter angle with D-pad
            self.shooter_angle.set(.2)
        elif self.controllerHID.getPOV() == 180:
            self.shooter_angle.set(-.2)
        else:
            self.shooter_angle.set(0)

        if self.controller.getAButtonPressed() and self.solenoid0.get() == False:
            self.solenoid0.set(True)
            self.solenoid1.set(True)
        elif self.controller.getAButtonPressed() and self.solenoid0.get() == True:
            self.solenoid0.set(False)
            self.solenoid1.set(False)

        
if __name__ == "__main__":
    wpilib.run(MyRobot)