import ctre
import wpilib
from ctre._ctre import TalonFXControlMode
from wpilib import interfaces
from wpilib.interfaces._interfaces import GenericHID
from networktables import NetworkTables

class MyRobot(wpilib.TimedRobot):

    

    def autonomousInit(self):
        """Robot initialization function"""
        # self.motor = ctre.WPI_TalonSRX(0)  # initialize the motor as a Talon on channel 0
        self.joystickleft = wpilib.Joystick(0)
        self.controller = wpilib.XboxController(0)
        self.sensor_type = ctre.FeedbackDevice(1)
        self.demand_type = ctre.DemandType(1)
        self.motor_control_mode = ctre.TalonFXControlMode(1)
        self.motor1 = ctre.TalonFX(0)
        self.motor1.configSelectedFeedbackSensor(self.sensor_type)

    def autonomousPeriodic(self):
        """Runs the motor from a joystick."""
        self.previous1 = self.motor1.getSelectedSensorPosition(0)
        print (self.previous1)
        self.motor1.setSelectedSensorPosition(500 + self.previous1)
        self.motor1.set(self.motor_control_mode, self.motor1.getSelectedSensorPosition(), self.demand_type, 0.5)
        


if __name__ == "__main__":
    wpilib.run(MyRobot)