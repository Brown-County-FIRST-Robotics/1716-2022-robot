import logging
import wpilib
import ctre
from wpilib import interfaces
import rev

#drive, angle, shooter, intake


class MyRobot(wpilib.TimedRobot):
    def testInit(self):
        self.back_right = ctre.WPI_TalonFX(0)
        self.front_left = ctre.WPI_TalonFX(1) 
        self.back_left = ctre.WPI_TalonFX(2)
        self.front_right = ctre.WPI_TalonFX(3)
        self.intake = ctre.WPI_TalonFX(4)
        self.shooter_bottom = ctre.WPI_TalonFX(5)
        self.shooter_top = ctre.WPI_TalonFX(6)
        self.shooter_angle = ctre.WPI_TalonFX(7)
        self.shooter_solenoid = wpilib.Solenoid(wpilib.PneumaticsModuleType(0), 0)
        self.enable_intake_solenoid = wpilib.Solenoid(wpilib.PneumaticsModuleType(0), 1)
        
        self.front_right.setInverted(True)
        self.back_right.setInverted(True)
        self.shooter_top.setInverted(True)

        #controller groups
        self.shooter = wpilib.MotorControllerGroup(self.shooter_top, self.shooter_bottom)

        #controller variables
        self.controller = wpilib.XboxController(0)
        self.controllerHID = interfaces.GenericHID(0)

        self.drive_speed = .2
        
    def testPeriodic(self):
        self.front_right.set((self.controller.getLeftY() - self.controller.getLeftX() - self.controller.getRightX()) * self.drive_speed)
        self.front_left.set((self.controller.getLeftY() + self.controller.getLeftX() + self.controller.getRightX()) * self.drive_speed)
        self.back_left.set((self.controller.getLeftY() - self.controller.getLeftX() + self.controller.getRightX()) * self.drive_speed)
        self.back_right.set((self.controller.getLeftY() + self.controller.getLeftX() - self.controller.getRightX()) * self.drive_speed)

        if self.controller.getRightBumper():
            self.intake.set(.5)
        #     self.shooter.set(-.2)
        # elif self.controller.getRightTriggerAxis() < .05:
        #     self.shooter.set(0)
        else:
            self.intake.set(0)

        self.shooter.set(self.controller.getRightTriggerAxis())
        self.controllerHID.setRumble(interfaces.GenericHID.RumbleType.kRightRumble, self.controller.getRightTriggerAxis())

        if self.controllerHID.getPOV() == 0: #shooter angle with D-pad
            self.shooter_angle.set(.2)
        elif self.controllerHID.getPOV() == 180:
            self.shooter_angle.set(-.2)
        else:
            self.shooter_angle.set(0)

        if self.controller.getAButtonPressed() and self.shooter_solenoid.get() == False:
            self.shooter_solenoid.set(True)
        elif self.controller.getAButtonPressed() and self.shooter_solenoid.get() == True:
            self.shooter_solenoid.set(False)
        if self.controller.getBButtonPressed() and self.enable_intake_solenoid.get() == False:
            self.enable_intake_solenoid.set(True)
        elif self.controller.getBButtonPressed() and self.enable_intake_solenoid.get() == True:
            self.enable_intake_solenoid.set(False)

        
if __name__ == "__main__":
    wpilib.run(MyRobot)