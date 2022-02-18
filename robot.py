import wpilib
import ctre
from wpilib import interfaces
from . import helper_functions


class MyRobot(wpilib.TimedRobot):
    
    def robotInit(self):
        self.back_right = ctre.WPI_TalonFX(0)
        self.front_left = ctre.WPI_TalonFX(1)
        self.back_left = ctre.WPI_TalonFX(2)
        self.front_right = ctre.WPI_TalonFX(3)
        self.intake = ctre.WPI_TalonSRX(4)
        self.shooter_angle_1 = ctre.WPI_TalonSRX(11)
        self.shooter_angle_2 = ctre.WPI_TalonSRX(10)
        self.drive_speed = .5
        self.back_right.configSelectedFeedbackSensor(ctre.TalonFXFeedbackDevice.IntegratedSensor)
        self.front_left.configSelectedFeedbackSensor(ctre.TalonFXFeedbackDevice.IntegratedSensor)
        self.back_left.configSelectedFeedbackSensor(ctre.TalonFXFeedbackDevice.IntegratedSensor)
        self.front_right.configSelectedFeedbackSensor(ctre.TalonFXFeedbackDevice.IntegratedSensor)


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
        self.routine = [[True, True], [False, True], [False, True], [False, True]]

        self.routine1 = []
        self.sensor = self.back_right.getSensorCollection()
        self.sensor.setIntegratedSensorPosition(0)
        self.target_position = 0
        motor_position = 0

        self.motor_dictionary = {
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
        # if self.timer.hasPeriodPassed(5):
        #     while self.sensor.getIntegratedSensorPosition() < self.target_position :
        #         self.back_right.set(.5)
        #         print(self.sensor.getIntegratedSensorPosition())
        
        # self.back_right.set(0)

        

        for maneuver in self.routine:
            for motor in self.motor_dictionary:    #update motor positions for compatible motors
                motor["position"] = motor["motor"].getSelectedSensorPosition()

            if self.routine[0][0]:
                if self.routine[0][1]:
                    self.motor_dictionary["front_right"]["target_position"] = 360
                    self.routine[0][1] = False
                maneuver_enabled = helper_functions.motor_positioner(self.motor_dictionary)
                self.routine[0][0] = maneuver_enabled
                self.routine[1][0] = not maneuver_enabled

            if self.routine[1][0]:
                if self.routine[1][1]:
                    self.motor_dictionary["front_right"]["target_position"] = 0
                    self.routine[1][1] = False
                maneuver_enabled = helper_functions.motor_positioner(self.motor_dictionary)
                self.routine[1][0] = maneuver_enabled
                self.routine[2][0] = not maneuver_enabled

            if self.routine[2][0]:
                if self.routine[2][1]:
                    self.motor_dictionary["front_right"]["target_position"] = 123
                    self.routine[2][1] = False
                maneuver_enabled = helper_functions.motor_positioner(self.motor_dictionary)
                self.routine[2][0] = maneuver_enabled
                self.routine[3][0] = not maneuver_enabled
            
            if self.routine[4][0]:
                if self.routine[4][1]:
                    self.motor_dictionary["front_right"]["target_position"] = -43
                    self.routine[4][1] = False
                maneuver_enabled = helper_functions.motor_positioner(self.motor_dictionary)
                self.routine[4][0] = maneuver_enabled
                

if __name__ == "__main__":
    wpilib.run(MyRobot)