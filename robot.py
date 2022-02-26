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

        self.mod_type = wpilib.PneumaticsModuleType.CTREPCM
        self.intake_solenoids = wpilib.DoubleSolenoid(self.mod_type, forwardChannel=1, reverseChannel=0)

        self.front_right.setInverted(True)
        self.back_right.setInverted(True)

    def disabledInit(self):
        self.compressor = wpilib.Compressor(self.mod_type)
        self.compressor.enableDigital()

    def autonomousInit(self):
        self.routine = [True, False, False, False]
        self.timer = wpilib.Timer()
        self.timer.start()
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
