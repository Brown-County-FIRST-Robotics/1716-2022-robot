# shooter angling
import wpilib
import ctre
import rev
from networktables import NetworkTables
import math


class MyRobot(wpilib.TimedRobot):
    def testInit(self):
        self.shooter_angle_1 = ctre.WPI_TalonFX(4)
        self.shooter_angle_2 = ctre.WPI_TalonFX(5)
        self.back_right = ctre.WPI_TalonFX(0)
        self.front_left = ctre.WPI_TalonFX(1)
        self.back_left = ctre.WPI_TalonFX(2)
        self.front_right = ctre.WPI_TalonFX(3)
        self.shooter_solenoid = wpilib.DoubleSolenoid(wpilib.PneumaticsModuleType.CTREPCM, 0, 1)

        self.motor1.setInverted(True)

        self.shooterAngleMotors = wpilib.MotorControllerGroup(self.motor1, self.motor2)
        self.controller = wpilib.XboxController

        self.timer = wpilib.Timer()
        self.timer.start()
        self.motor1.configSelectedFeedbackSensor(ctre.FeedbackDevice.IntegratedSensor)
        self.shooter_dictionary = {
            "shoooting": False,
            "step" : 0,
            "lock_on_mode" : False,
            "timer" : 0,
            "firing" : False #used for spinning up shooter motors and firing the ball
        }
        self.shooter_timer = wpilib.Timer()
        self.motor_dictionary = {}

    def shoot(shooter_dictionary, motor_dictionary, speed = 1) -> dict:
        if NetworkTables.getTable("limelight").getNumber("tv", 0) == 0 and shooter_dictionary["step"] == 0:
            motor_dictionary["back_right"]["motor"].set(speed)
            motor_dictionary["front_left"]["motor"].set(speed)
            motor_dictionary["back_left"]["motor"].set(speed)
            motor_dictionary["front_right"]["motor"].set(speed)
        
        elif  NetworkTables.getTable("limelight").getNumber("tv", 0) == 1 and shooter_dictionary["step"] == 0:
            motor_dictionary["shooterAngleMotors"]["motor"].set(0) #likely will need to have name of motor fixed
            motor_dictionary["back_right"]["motor"].set(0)
            motor_dictionary["front_left"]["motor"].set(0)
            motor_dictionary["back_left"]["motor"].set(0)
            motor_dictionary["front_right"]["motor"].set(0)
            shooter_dictionary["step"] = 1


        if NetworkTables.getTable("limelight").getNumber("tx", 0) < 0 and shooter_dictionary["step"] == 1:  # horizontal offset
            motor_dictionary["back_right"]["motor"].set(speed * 0.5)
            motor_dictionary["front_left"]["motor"].set(-speed * 0.5)
            motor_dictionary["back_left"]["motor"].set(-speed * 0.5)
            motor_dictionary["front_right"]["motor"].set(speed * 0.5)
        elif NetworkTables.getTable("limelight").getNumber("tx", 0) > 0 and shooter_dictionary["step"] == 1:
            motor_dictionary["back_right"]["motor"].set(-speed * 0.5)
            motor_dictionary["front_left"]["motor"].set(speed * 0.5)
            motor_dictionary["back_left"]["motor"].set(speed * 0.5)
            motor_dictionary["front_right"]["motor"].set(-speed * 0.5)
        elif NetworkTables.getTable("limelight").getNumber("tx", 0) == 0 and shooter_dictionary["step"] == 1:
            motor_dictionary["back_right"]["motor"].set(0)
            motor_dictionary["front_left"]["motor"].set(0)
            motor_dictionary["back_left"]["motor"].set(0)
            motor_dictionary["front_right"]["motor"].set(0)

        if NetworkTables.getTable("limelight").getNumber("ty", 0) < 0 and shooter_dictionary["step"] == 1:  # vertical offset
            motor_dictionary["shooterAngleMotors"]["motor"].set(speed * .5)
        elif NetworkTables.getTable("limelight").getNumber("ty", 0) > 0 and shooter_dictionary["step"] == 1:
            motor_dictionary["shooterAngleMotors"]["motor"].set(speed * .5)
        elif NetworkTables.getTable("limelight").getNumber("ty", 0) == 0 and shooter_dictionary["step"] == 1:
            motor_dictionary["shooterAngleMotors"]["motor"].set(0)
    
        if motor_dictionary["front_right"]["motor"].getMotorOutputPercent() == 0 and motor_dictionary["shooter_angle_1"]["motor"].getMotorOutputPercent() == 0:
            shooter_dictionary["step"] = 2

        if shooter_dictionary["step"] == 2:
            angle = (motor_dictionary["shooter_angle_1"]["motor"].getSelectedSensorPosition() * (45 / 256)) * (math.pi/180) #shooter angle in radians
            shooterHeight = (math.sin(angle) * 1) + 0  # * arm length + chassis height
            basketY = (10400 / 3937) - shooterHeight  # top basket total height in meters - shooter height to make the shot from (0, 0)
            basketX = basketY / math.tan(angle)
            basketY += 0.30  # height raised to aim for basket (in meters), not for reflective strip and to allow ball to clear rim
            #angle calculation for final angle (1 is the velocity(may need to be convert to m/s)):
            angle_plus = 180 / (math.atan(((1**2)+ math.sqrt((1**4) - (9.80665* ((9.80665 * (basketX**2)) + (2 * (basketY * (1**2))))))) / (basketX * 9.80665)) * math.pi)
            angle_minus = 180 / (math.atan(((1**2)- math.sqrt((1**4) - (9.80665 * ((9.80665 * (basketX**2)) + (2 * (basketY * (1**2))))))) / (basketX * 9.80665)) * math.pi)

            if angle_plus > angle_minus:  # sets the shooter angle to whichever is larger, plus or minus, this will help avoid negative values
                angle = angle_plus
            elif  angle_plus < angle_minus:
                angle = angle_minus
            #at this point angle is in degrees rather than radians(probably)

            motor_dictionary["shooter_angle_1"]["previous_position"] = motor_dictionary["shooter_angle_1"]["motor"].getSelectedSensorPosition

            shooter_dictionary["step"] = 3
        
        if motor_dictionary["shooter_angle_1"]["previous_position"] < (angle * (256 / 45)) and shooter_dictionary["step"] == 3:
            if motor_dictionary["shooter_angle_1"]["motor"].getSelectedSensorPosition() < (angle * (256 / 45)):
                motor_dictionary["shooterAngleMotors"]["motor"].set(speed * .3)
        elif motor_dictionary["shooter_angle_1"]["previous_position"] > (angle * (256 / 45)) and shooter_dictionary["step"] == 3:
            if motor_dictionary["shooter_angle_1"]["motor"].getSelectedSensorPosition() > (angle * (256 / 45)):
                motor_dictionary["shooterAngleMotors"]["motor"].set(-speed * .3)
        elif shooter_dictionary["step"] == 3:
            motor_dictionary["shooterAngleMotors"]["motors"].set(0)
            shooter_dictionary["step"] = 4

        if shooter_dictionary["step"] == 4:
            if shooter_dictionary["timer"] > 0 and shooter_dictionary["timer"] <= 3:
                motor_dictionary["shooter1"]["motor"].set(1)
                motor_dictionary["shooter2"]["motor"].set(1)
            if shooter_dictionary["timer"] >= 3 and shooter_dictionary["timer"] <= 3.1:
                wpilib.DoubleSolenoid(wpilib.PneumaticsModuleType.CTREPCM, 0, 1).set(wpilib.DoubleSolenoid.Value.kForward) #experimental
            if shooter_dictionary["timer"] >= 3.25 and shooter_dictionary["timer"] <= 3.35:
                wpilib.DoubleSolenoid(wpilib.PneumaticsModuleType.CTREPCM, 0, 1).set(wpilib.DoubleSolenoid.Value.kOff)
                motor_dictionary["shooter1"]["motor"].set(0)
                motor_dictionary["shooter2"]["motor"].set(0)
                shooter_dictionary["shooting"] = False
                shooter_dictionary["firing"] = False
                return shooter_dictionary

        shooter_dictionary["shooting"] = True
        return shooter_dictionary
   
    def testPeriodic(self):
        if self.controller.getRightBumperPressed:
            self.motor_dictionary["shooter_angle_1"]["previous_position"] = self.shooter_angle_1.getSelectedSensorPosition
            self.shooter_dictionary["timer"] = 0
            self.shooter_timer.stop()
            self.shooter_timer.reset()
            self.shooter_dictionary = self.shoot(self.shooter_dictionary, self.motor_dictionary)
        elif self.shooter_dictionary["shooting"]:
            if self.shooter_dictionary["firing"]:
                self.shooter_timer.start()
                self.shooter_dictionary["timer"] = self.shooter_timer.get()
            self.shooter_dictionary = self.shoot(self.shooter_dictionary, self.motor_dictionary)

        elif self.controller.getBackButtonPressed:
            self.shooter_dictionary["shooting"] = False
        
        if self.shooter_dictionary["step"] == 0:
            ... #d-pad shooter angle control code here
        
if __name__ == "__main__":
    wpilib.run(MyRobot)
