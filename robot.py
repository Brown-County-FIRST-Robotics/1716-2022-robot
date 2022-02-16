import wpilib
import ctre
from wpilib import interfaces


class MyRobot(wpilib.TimedRobot):
    
    def robotInit(self):
        self.back_right = ctre.WPI_TalonFX(0)
        self.front_left = ctre.WPI_TalonFX(1)
        self.back_left = ctre.WPI_TalonFX(2)
        self.front_right = ctre.WPI_TalonFX(3)
        self.intake = ctre.WPI_TalonFX(4)
        self.shooter_angle_1 = ctre.WPI_TalonSRX(11)
        self.shooter_angle_2 = ctre.WPI_TalonSRX(10)
        self.drive_speed = .5
    def testInit(self):
        
        #motor controller groups
        self.shooter_angle = wpilib.MotorControllerGroup(self.shooter_angle_1, self.shooter_angle_2)

        #controller variables
        self.controller = wpilib.XboxController(0)
        self.controllerHID = interfaces.GenericHID(0)

        #other variables
        

    def autonomousInit(self):
        self.timer = wpilib.Timer()
        self.timer.start()
        

        self.routine1 = []
        self.sensor = self.back_right.getSensorCollection()
        self.sensor.setIntegratedSensorPosition(0)
        self.target_position = 0
        motor_position = 0

        motor_dictionary = {
            "front_right": {
                "motor": self.front_right,
                "target_position": self.target_position,
                "position": motor_position,
            },
            "front_left": {
                "motor": self.front_left,
                "target_position": self.target_position,
                "position": motor_position,
            },
            "back_right": {
                "motor": self.back_right,
                "target_position": self.target_position,
                "position": motor_position,
            },
            "back_left": {
                "motor": self.back_left,
                "target_position": self.target_position,
                "position": motor_position,
            },
            "intake1": {
                "motor": self.intake,
                "target_position": self.target_position,
                "position": motor_position,
            },
            "shooter_angle_1": {
                "motor": self.shooter_angle_1,
                "target_position": self.target_position,
                "position": motor_position,
            },
            "shooter_angle_2": {
                "motor": self.shooter_angle_2,
                "target_position": self.target_position,
                "position": motor_position,
            },
        }
    
    def disabledInit(self):
        ...

    def testPeriodic(self):
        self.front_right.set((self.controller.getLeftY() - self.controller.getLeftX() - self.controller.getRightX()) * self.drive_speed)
        self.front_left.set((self.controller.getLeftY() + self.controller.getLeftX() + self.controller.getRightX()) * self.drive_speed)
        self.back_left.set((self.controller.getLeftY() - self.controller.getLeftX() + self.controller.getRightX()) * self.drive_speed)
        self.back_right.set((self.controller.getLeftY() + self.controller.getLeftX() - self.controller.getRightX()) * self.drive_speed)
        
        if self.controllerHID.getPOV() == -1 or self.controllerHID.getPOV() == 90 or self.controllerHID.getPOV() == 270:
            self.shooter_angle.set(0)
        elif self.controllerHID.getPOV() == 0:
            self.shooter_angle.set(-.5)
        elif self.controllerHID.getPOV() == 180:
            self.shooter_angle.set(.5)

        if self.controller.getRightTriggerAxis() > self.controller.getLeftTriggerAxis():
            self.intake.set(self.controller.getRightTriggerAxis() )

        if self.controller.getRightTriggerAxis() < self.controller.getLeftTriggerAxis():
            self.intake.set(self.controller.getLeftTriggerAxis() * -1 )

        if self.controller.getRightTriggerAxis() == self.controller.getLeftTriggerAxis():
            self.intake.set(0)

        if self.controller.getRightTriggerAxis() != 0:
            self.controllerHID.setRumble(interfaces.GenericHID.RumbleType.kRightRumble, 1)
            self.controllerHID.setRumble(interfaces.GenericHID.RumbleType.kLeftRumble, 1)
        else:
            self.controllerHID.setRumble(interfaces.GenericHID.RumbleType.kRightRumble, 0)
            self.controllerHID.setRumble(interfaces.GenericHID.RumbleType.kLeftRumble, 0)

    def autonomousPeriodic(self):
        if self.timer.hasPeriodPassed(5):
            while self.sensor.getIntegratedSensorPosition() < self.target_position :
                self.back_right.set(.5)
                print(self.sensor.getIntegratedSensorPosition())
        
        self.back_right.set(0)

        



if __name__ == "__main__":
    wpilib.run(MyRobot)