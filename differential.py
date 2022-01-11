import wpilib
import wpilib.drive
import ctre

class MyRobot(wpilib.TimedRobot):
    def testInit(self):
        self.motor1 = ctre.WPI_TalonSRX(0)
        self.motor2 = ctre.WPI_TalonFX(1) 
        self.motor3 = ctre.WPI_TalonFX(2)
        self.motor4 = ctre.WPI_TalonFX(3)

        self.left = wpilib.SpeedControllerGroup(self.motor1, self.motor4)
        self.right = wpilib.SpeedControllerGroup(self.motor2, self.motor3)
        self.drive = wpilib.drive.DifferentialDrive(self.left, self.right)

        self.controller = wpilib.Joystick(0)

    def testPeriodic(self):
        if abs(self.controller.getY()) > .2:
            self.drive.curvatureDrive(-self.controller.getY() *.1, self.controller.getZ() * .1, True)
        else:
            self.drive.arcadeDrive(0, 0)

if __name__ == "__main__":
    wpilib.run(MyRobot)