import ctre
import wpilib


class MyRobot(wpilib.TimedRobot):

    def testInit(self):
        self.motor0 = ctre.WPI_TalonFX(0)
        self.motor1 = ctre.WPI_TalonFX(1)
        self.motor2 = ctre.WPI_TalonFX(2)
        self.motor3 = ctre.WPI_TalonFX(3)
        self.joystick = wpilib.Joystick(0)
        self.joystick2 = wpilib.Joystick(1)

        self.motor0.setInverted(True)
        self.motor3.setInverted(True)
    
    def testPeriodic(self):
        self.multiplier = .25
        #*self.multiplier
        self.motor0.set((self.joystick.getY() - self.joystick.getX() - self.joystick2.getX()) * self.multiplier)
        self.motor1.set((self.joystick.getY() + self.joystick.getX() + self.joystick2.getX()) * self.multiplier)
        self.motor2.set((self.joystick.getY() - self.joystick.getX() + self.joystick2.getX()) * self.multiplier)
        self.motor3.set((self.joystick.getY() + self.joystick.getX() - self.joystick2.getX()) * self.multiplier)
        

if __name__ == "__main__":
    wpilib.run(MyRobot)
    