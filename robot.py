import wpilib
import ctre
from wpilib import DoubleSolenoid, PneumaticsModuleType, interfaces


class MyRobot(wpilib.TimedRobot):
    def teleopInit(self):
        self.back_right = ctre.WPI_TalonFX(2)
        self.front_left = ctre.WPI_TalonFX(3)
        self.back_left = ctre.WPI_TalonFX(4)
        self.front_right = ctre.WPI_TalonFX(5)
        self.intake = ctre.WPI_TalonFX(12)
        self.shooter_top = ctre.WPI_TalonFX(6)
        self.shooter_bottom = ctre.WPI_TalonFX(7)
        self.shooter_angle_1 = ctre.WPI_TalonSRX(11)
        self.shooter_angle_2 = ctre.WPI_TalonSRX(10)
        self.front_right.setInverted(True)
        self.back_right.setInverted(True)
        self.shooter_bottom.setInverted(True)

        # self.module_type = wpilib.PneumaticsModuleType(0)
        # self.shooterout = wpilib.DoubleSolenoid(self.module_type, forwardChannel=0, reverseChannel=1)




        #motor controller groups
        self.shooter_angle = wpilib.MotorControllerGroup(self.shooter_angle_1, self.shooter_angle_2)

        #controller variables
        self.controller = wpilib.XboxController(0)
        self.controllerHID = interfaces.GenericHID(0)

        #other variables
        self.drive_speed = .5

    def autonomousInit(self):
        self.timer = wpilib.Timer()
        self.timer.start()
        self.routine1 = []

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

    def disabledInit(self):
        ...

    def teleopPeriodic(self):
        self.front_right.set((self.controller.getLeftY() - self.controller.getLeftX() - self.controller.getRightX()) * self.drive_speed)
        self.front_left.set((self.controller.getLeftY() + self.controller.getLeftX() + self.controller.getRightX()) * self.drive_speed)
        self.back_left.set((self.controller.getLeftY() - self.controller.getLeftX() + self.controller.getRightX()) * self.drive_speed)
        self.back_right.set((self.controller.getLeftY() + self.controller.getLeftX() - self.controller.getRightX()) * self.drive_speed)

        if self.controllerHID.getPOV() == -1 or self.controllerHID.getPOV() == 90 or self.controllerHID.getPOV() == 270:
            self.shooter_angle.set(0)
        elif self.controllerHID.getPOV() == 0:
            self.shooter_angle.set(-1)
        elif self.controllerHID.getPOV() == 180:
            self.shooter_angle.set(1)

        if self.controller.getRightTriggerAxis() > self.controller.getLeftTriggerAxis():
            self.intake.set(self.controller.getRightTriggerAxis())
            self.shooter_bottom.set(self.controller.getRightTriggerAxis())
            self.shooter_top.set(self.controller.getRightTriggerAxis())

        if self.controller.getRightTriggerAxis() < self.controller.getLeftTriggerAxis():
            self.intake.set(self.controller.getLeftTriggerAxis() * -0.8)
            self.shooter_bottom.set(self.controller.getLeftTriggerAxis() * -0.8)
            self.shooter_top.set(self.controller.getLeftTriggerAxis() * -0.8)

        if self.controller.getRightTriggerAxis() == self.controller.getLeftTriggerAxis():
            self.intake.set(0)
            self.shooter_bottom.set(0)
            self.shooter_top.set(0)

        if self.controller.getRightTriggerAxis() != 0:
            self.controllerHID.setRumble(interfaces.GenericHID.RumbleType.kRightRumble, 1)
            self.controllerHID.setRumble(interfaces.GenericHID.RumbleType.kLeftRumble, 1)
        else:
            self.controllerHID.setRumble(interfaces.GenericHID.RumbleType.kRightRumble, 0)
            self.controllerHID.setRumble(interfaces.GenericHID.RumbleType.kLeftRumble, 0)
        # if self.controller.getAButtonPressed():
        #     self.shooterout.set(wpilib.DoubleSolenoid.Value.kForward)
        # if self.controller.getBButtonPressed():
        #     self.shooterout.set(wpilib.DoubleSolenoid.Value.kReverse)
    def autonomousPeriodic(self):
        ...

if __name__ == "__main__":
    wpilib.run(MyRobot)