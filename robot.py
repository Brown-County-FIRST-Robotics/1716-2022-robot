import wpilib
import ctre
from wpilib import interfaces
import helper_functions


class MyRobot(wpilib.TimedRobot):
    def robotInit(self):
        self.back_left = ctre.WPI_TalonFX(0) 
        self.front_left = ctre.WPI_TalonFX(1)
        self.front_right = ctre.WPI_TalonFX(2)               
        self.back_right = ctre.WPI_TalonFX(3)
        # self.intake = ctre.WPI_TalonFX(12)
        # self.shooter_top = ctre.WPI_TalonFX(6)
        # self.shooter_bottom = ctre.WPI_TalonFX(7)
        # self.shooter_angle_1 = ctre.WPI_TalonSRX(11)
        # self.shooter_angle_2 = ctre.WPI_TalonSRX(10)

        self.front_right.setInverted(True)
        self.back_right.setInverted(True)
        # self.shooter_bottom.setInverted(True)

        #solenoids
        self.mod_type = wpilib.PneumaticsModuleType.CTREPCM
        self.intake_solenoids = wpilib.DoubleSolenoid(self.mod_type, forwardChannel=1, reverseChannel=0)
        self.shooter_solenoid = wpilib.DoubleSolenoid(self.mod_type, forwardChannel=3, reverseChannel=4)

        #controller variables
        self.controller = wpilib.XboxController(0)
        self.controllerHID = interfaces.GenericHID(0)

        self.drive_speed = .5

    def disabledInit(self):
        self.compressor = wpilib.Compressor(wpilib.PneumaticsModuleType.CTREPCM)
        self.compressor.enableDigital()
    
    def testInit(self):
        ...
    
    def testPeriodic(self):
        self.front_right.set((self.controller.getLeftY() - self.controller.getLeftX() - self.controller.getRightX()) * self.drive_speed)
        self.front_left.set((self.controller.getLeftY() + self.controller.getLeftX() + self.controller.getRightX()) * self.drive_speed)
        self.back_left.set((self.controller.getLeftY() - self.controller.getLeftX() + self.controller.getRightX()) * self.drive_speed)
        self.back_right.set((self.controller.getLeftY() + self.controller.getLeftX() - self.controller.getRightX()) * self.drive_speed)

        # if self.controllerHID.getPOV() == -1 or self.controllerHID.getPOV() == 90 or self.controllerHID.getPOV() == 270:
        #     self.shooter_angle.set(0)
        # elif self.controllerHID.getPOV() == 0:
        #     self.shooter_angle.set(-.5)
        # elif self.controllerHID.getPOV() == 180:
        #     self.shooter_angle.set(.5)

        # if self.controller.getRightTriggerAxis() > self.controller.getLeftTriggerAxis():
        #     self.intake.set(self.controller.getRightTriggerAxis())
        #     self.shooter_bottom.set(self.controller.getRightTriggerAxis())
        #     self.shooter_top.set(self.controller.getRightTriggerAxis())

        # if self.controller.getRightTriggerAxis() < self.controller.getLeftTriggerAxis():
        #     self.intake.set(self.controller.getLeftTriggerAxis() * -0.8)
        #     self.shooter_bottom.set(self.controller.getLeftTriggerAxis() * -0.8)
        #     self.shooter_top.set(self.controller.getLeftTriggerAxis() * -0.8)

        # if self.controller.getRightTriggerAxis() == self.controller.getLeftTriggerAxis():
        #     self.intake.set(0)
        #     self.shooter_bottom.set(0)
        #     self.shooter_top.set(0)

        if self.controller.getRightTriggerAxis() != 0:
            self.controllerHID.setRumble(interfaces.GenericHID.RumbleType.kRightRumble, 1)
            self.controllerHID.setRumble(interfaces.GenericHID.RumbleType.kLeftRumble, 1)
        else:
            self.controllerHID.setRumble(interfaces.GenericHID.RumbleType.kRightRumble, 0)
            self.controllerHID.setRumble(interfaces.GenericHID.RumbleType.kLeftRumble, 0)

    def autonomousInit(self):
        self.timer = wpilib.Timer()
        self.timer.start()

        target_position = 0
        motor_position = 0

        motor_dictionary = {
            "front_right": {
                "motor": self.front_right,
                "target_position": target_position,
                "position": motor_position,
            },
            "front_left": {
                "motor": self.front_left,
                "target_position": target_position,
                "position": motor_position,
            },
            "back_right": {
                "motor": self.back_right,
                "target_position": target_position,
                "position": motor_position,
            },
            "back_left": {
                "motor": self.back_left,
                "target_position": target_position,
                "position": motor_position,
            },
            "intake": {
                "motor": self.intake,
                "target_position": target_position,
                "position": motor_position,
            },
            "shooter_angle": {
                "motor": self.shooter_angle,
                "target_position": target_position,
                "position": motor_position,
            },
        }

        #starting autonomous values
        self.front_right.set(.2)
        self.front_left.set(.2)
        self.back_right.set(.2)
        self.back_left.set(.2)

    def autonomousPeriodic(self):
        if self.timer.get() < 1:
            self.intake_solenoids.set(wpilib.DoubleSolenoid.Value.kForward)
        if self.timer.get() > 1.25 and self.timer.get() < 1.5:
            self.intake_solenoids.set(wpilib.DoubleSolenoid.Value.kOff)
        
        if self.timer.get() < 1:
            self.intake_solenoids.set(wpilib.DoubleSolenoid.Value.kForward)
        if self.timer.get() > 1.25 and self.timer.get() < 1.5:
            self.intake_solenoids.set(wpilib.DoubleSolenoid.Value.kOff)
            
        if self.timer.get() > 4 and self.timer.get() < 6:
            self.front_right.set(0)
            self.front_left.set(0)
            self.back_left.set(0)
            self.back_right.set(0)

        if self.timer.get() > 6 and self.timer.get() < 10:
            self.front_right.set(.2)
            self.front_left.set(.2)
            self.back_right.set(.2)
            self.back_left.set(.2)

        if self.timer.get() > 8 and self.timer.get() < 8.25:
            self.intake_solenoids.set(wpilib.DoubleSolenoid.Value.kReverse)

        if self.timer.get() > 8.25 and self.timer.get() < 8.5:
            self.intake_solenoids.set(wpilib.DoubleSolenoid.Value.kOff)

        if self.timer.get() > 10 and self.timer.get() < 10.25:
            self.front_right.set(0)
            self.front_left.set(0)
            self.back_right.set(0)
            self.back_left.set(0)            

if __name__ == "__main__":
    wpilib.run(MyRobot)
