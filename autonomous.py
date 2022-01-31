import ctre
import wpilib
from wpilib import interfaces
from networktables import NetworkTables


class MyRobot(wpilib.TimedRobot):
    def autonomousInit(self):
        """Robot initialization function"""
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

        self.timer = wpilib.Timer()
        self.timer.start()
        self.routine1 = [
            True,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
        ]

        target_position = 0
        motor_position = 0
        motor_speed = 0

        motor_dictionary = {
            "front_right": {
                "motor": self.front_right,
                "target_position": target_position,
                "position": motor_position,
                "speed": motor_speed,
            },
            "front_left": {
                "motor": self.front_left,
                "target_position": target_position,
                "position": motor_position,
                "speed": motor_speed,
            },
            "back_right": {
                "motor": self.back_right,
                "target_position": target_position,
                "position": motor_position,
                "speed": motor_speed,
            },
            "back_left": {
                "motor": self.back_left,
                "target_position": target_position,
                "position": motor_position,
                "speed": motor_speed,
            },
            "intake": {
                "motor": self.intake,
                "target_position": target_position,
                "position": motor_position,
                "speed": motor_speed,
            },
            "shooter_bottom": {
                "motor": self.shooter_bottom,
                "target_position": target_position,
                "position": motor_position,
                "speed": motor_speed,
            },
            "shooter_top": {
                "motor": self.shooter_top,
                "target_position": target_position,
                "position": motor_position,
                "speed": motor_speed,
            },
            "shooter_angle": {
                "motor": self.shooter_angle,
                "target_position": target_position,
                "position": motor_position,
                "speed": motor_speed,
            },
            "queuer": {
                "motor": self.queuer,
                "target_position": target_position,
                "position": motor_position,
                "speed": motor_speed,
            },
            "climber_FR": {
                "motor": self.climber_FR,
                "target_position": target_position,
                "position": motor_position,
                "speed": motor_speed,
            },
            "climber_FL": {
                "motor": self.climber_FL,
                "target_position": target_position,
                "position": motor_position,
                "speed": motor_speed,
            },
            "climber_BR": {
                "motor": self.climber_BR,
                "target_position": target_position,
                "position": motor_position,
                "speed": motor_speed,
            },
            "climber_BL": {
                "motor": self.climber_BL,
                "target_position": target_position,
                "position": motor_position,
                "speed": motor_speed,
            },
            "climber_angle": {
                "motor": self.climber_angle,
                "target_position": target_position,
                "position": motor_position,
                "speed": motor_speed,
            },
        }

    def disabledInit(self) -> None:
        self.i = 0

    def autonomousPeriodic(self):
        self.i += 1
        collection = self.motor.getSensorCollection()
        collection.setIntegratedSensorPosition(self.i)

        if self.timer.hasPeriodPassed(1):
            self.logger.info("TalonFX: %f", collection.getIntegratedSensorPosition())


if __name__ == "__main__":
    wpilib.run(MyRobot)
