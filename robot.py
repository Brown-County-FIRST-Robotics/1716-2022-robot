import wpilib
import ctre
import rev
from wpilib import interfaces
import wpiutil
import helper_functions
# from networktables import NetworkTables
# from statistics import mean



class MyRobot(wpilib.TimedRobot):
    def robotInit(self):
        self.back_left = ctre.WPI_TalonFX(0)        
        self.front_left = ctre.WPI_TalonFX(1)
        self.front_right = ctre.WPI_TalonFX(2)                
        self.back_right = ctre.WPI_TalonFX(3)
        self.shooter_top = ctre.WPI_TalonFX(6)
        self.shooter_bottom = ctre.WPI_TalonFX(7)
        self.shooter_angle_1 = ctre.WPI_TalonSRX(10)
        self.shooter_angle_2 = ctre.WPI_TalonSRX(11)        
        self.intake = ctre.WPI_TalonFX(12)
        self.winch = rev.CANSparkMax(1, rev.CANSparkMax.MotorType.kBrushless)


        self.front_left.setNeutralMode(ctre.NeutralMode.Brake)
        self.front_right.setNeutralMode(ctre.NeutralMode.Brake)
        self.back_left.setNeutralMode(ctre.NeutralMode.Brake)
        self.back_right.setNeutralMode(ctre.NeutralMode.Brake)
        self.front_right.setInverted(True)
        self.back_right.setInverted(True)
        self.shooter_top.setInverted(True)
        self.winch.setInverted(True)

        #solenoids:
        self.shooter_solenoid = wpilib.DoubleSolenoid(wpilib.PneumaticsModuleType.CTREPCM, forwardChannel = 0, reverseChannel = 1)
        self.shooter_solenoid_timer = wpilib.Timer()
        
        self.climber_solenoid = wpilib.DoubleSolenoid(wpilib.PneumaticsModuleType.CTREPCM, forwardChannel = 4, reverseChannel = 5)
        self.climber_solenoid_previous_position = wpilib.DoubleSolenoid.Value.kReverse
        self.climber_solenoid_timer = wpilib.Timer()

        self.intake_solenoid = wpilib.DoubleSolenoid(wpilib.PneumaticsModuleType.CTREPCM, forwardChannel = 2, reverseChannel = 3)
        self.intake_solenoid_previous_position = wpilib.DoubleSolenoid.Value.kForward
        self.intake_solenoid_timer = wpilib.Timer()

        #motor controller groups
        self.shooter_angle = wpilib.MotorControllerGroup(self.shooter_angle_1, self.shooter_angle_2)
        self.shooter = wpilib.MotorControllerGroup(self.shooter_top, self.shooter_bottom)

        #controller variables
        self.controller = wpilib.XboxController(0)
        self.controllerHID = interfaces.GenericHID(0)
        
        #other variables
        self.drive_speed = 10
        self.shooter_angle_speed = 1
        self.hub_shooting = False
        self.timer = wpilib.Timer()

        # self.limit_switch = wpilib.DigitalInput(0)
        self.potentiometer = wpilib.AnalogInput(0) #0 degrees: 3512, 90 degrees: 3850

        #auto-shoot variables(used in auto-aiming function shoot())
        # self.shooter_dictionary = {
        #     "shooting": False,
        #     "step" : 0,
        #     "lock_on_mode" : False,
        #     "timer" : 0,
        #     "firing" : False, #used for spinning up shooter motors and firing the ball
        #     "potentiometer" : self.potentiometer,
        #     "shooter_solenoid" : self.shooter_solenoid,
        #     "shooter_position" : 45, #contains shooter angle based on rolling average
        #     "angle" : 45,
        #     "centered" : [False, False],
        # }
        # self.shooter_timer = wpilib.Timer()
        # self.shooter_rolling_average = [45]

        #motor dictionary: (now in robotInit for function support)
        target_position = 0
        motor_position = 0
        previous_position = 0

        self.motor_dictionary = {
            "front_right": {
                "motor": self.front_right,
                "target_position": target_position,
                "position": motor_position,
                "previous_position" : previous_position,
            },
            "front_left": {
                "motor": self.front_left,
                "target_position": target_position,
                "position": motor_position,
                "previous_position" : previous_position,

            },
            "back_right": {
                "motor": self.back_right,
                "target_position": target_position,
                "position": motor_position,
                "previous_position" : previous_position,
            },
            "back_left": {
                "motor": self.back_left,
                "target_position": target_position,
                "position": motor_position,
                "previous_position" : previous_position,
            },
            "intake": {
                "motor": self.intake,
                "target_position": target_position,
                "position": motor_position,
                "previous_position" : previous_position,
            },
            "shooter_angle": {
                "motor": self.shooter_angle,
                "target_position": target_position,
                "position": motor_position,
                "previous_position" : previous_position,
            },
            "shooter": {
                "motor": self.shooter,
                "target_position": target_position,
                "position": motor_position,
                "previous_position" : previous_position,
            },
        }
        self.testTimer = wpilib.Timer
        self.testList = []


    def teleopInit(self):
        ...


    def disabledInit(self):
        ...

    def teleopPeriodic(self):
        if abs(self.controller.getLeftY()) > .3 or abs(self.controller.getLeftX()) > .3 or abs(self.controller.getRightX()) > .3:
            # if not self.shooter_dictionary["shooting"] or (self.shooter_dictionary["shooting"] and self.shooter_dictionary["step"] == 0):
            self.front_right.setVoltage((-self.controller.getLeftY() - self.controller.getLeftX() - self.controller.getRightX()) * self.drive_speed)
            self.front_left.setVoltage((-self.controller.getLeftY() + self.controller.getLeftX() + self.controller.getRightX()) * self.drive_speed)
            self.back_left.setVoltage((-self.controller.getLeftY() - self.controller.getLeftX() + self.controller.getRightX()) * self.drive_speed)
            self.back_right.setVoltage((-self.controller.getLeftY() + self.controller.getLeftX() - self.controller.getRightX()) * self.drive_speed)
        else:
            self.front_right.set(0)
            self.front_left.set(0)
            self.back_right.set(0)
            self.back_left.set(0)

        # if not self.shooter_dictionary["shooting"] or (self.shooter_dictionary["shooting"] and self.shooter_dictionary["step"] == 0):
        if not self.hub_shooting:
            if self.controller.getRightBumper():
                self.shooter_angle.set(-self.shooter_angle_speed)
            elif self.controller.getLeftBumper():
                self.shooter_angle.set(self.shooter_angle_speed)
            else:
                self.shooter_angle.set(0)

        # if not self.shooter_dictionary["shooting"]:
        if self.controller.getRightTriggerAxis() > self.controller.getLeftTriggerAxis():
            self.shooter.set(self.controller.getRightTriggerAxis())
            self.intake.set(self.controller.getRightTriggerAxis())

        if self.controller.getRightTriggerAxis() < self.controller.getLeftTriggerAxis():
            self.intake.set(self.controller.getLeftTriggerAxis() * -0.8)
            self.shooter.set(self.controller.getLeftTriggerAxis() * -0.8)

        if self.controller.getRightTriggerAxis() == self.controller.getLeftTriggerAxis():
            self.intake.set(0)
            self.shooter_bottom.set(0)
            self.shooter_top.set(0)

        
        #solenoids:
        if self.controller.getAButtonPressed():
            self.shooter_solenoid_timer.start()
            self.shooter_solenoid.set(wpilib.DoubleSolenoid.Value.kForward)
        if self.shooter_solenoid_timer.hasElapsed(.1):
            self.shooter_solenoid.set(wpilib.DoubleSolenoid.Value.kOff)
        if self.shooter_solenoid_timer.hasElapsed(.5):
            self.shooter_solenoid.set(wpilib.DoubleSolenoid.Value.kReverse)
        if self.shooter_solenoid_timer.hasElapsed(.6):
            self.shooter_solenoid_timer.stop()
            self.shooter_solenoid_timer.reset()
            self.shooter_solenoid.set(wpilib.DoubleSolenoid.Value.kOff)      

        if self.controller.getBButtonPressed():
            self.climber_solenoid_timer.start()
            if self.climber_solenoid_previous_position == wpilib.DoubleSolenoid.Value.kForward:
                self.climber_solenoid.set(wpilib.DoubleSolenoid.Value.kReverse)
                self.climber_solenoid_previous_position == wpilib.DoubleSolenoid.Value.kReverse
            if self.climber_solenoid_previous_position == wpilib.DoubleSolenoid.Value.kReverse:
                self.climber_solenoid.set(wpilib.DoubleSolenoid.Value.kForward)
                self.climber_solenoid_previous_position == wpilib.DoubleSolenoid.Value.kForward
        if self.climber_solenoid_timer.hasElapsed(.25):
            self.climber_solenoid_timer.stop()
            self.climber_solenoid_timer.reset()
            self.climber_solenoid_previous_position = self.climber_solenoid.get()
            self.climber_solenoid.set(wpilib.DoubleSolenoid.Value.kOff)

        if self.controller.getStartButtonPressed():
            self.intake_solenoid_timer.start()
            if self.intake_solenoid_previous_position == wpilib.DoubleSolenoid.Value.kForward:
                self.intake_solenoid.set(wpilib.DoubleSolenoid.Value.kReverse)
                self.intake_solenoid_previous_position == wpilib.DoubleSolenoid.Value.kReverse
            if self.intake_solenoid_previous_position == wpilib.DoubleSolenoid.Value.kReverse:
                self.intake_solenoid.set(wpilib.DoubleSolenoid.Value.kForward)
                self.intake_solenoid_previous_position == wpilib.DoubleSolenoid.Value.kForward
        if self.intake_solenoid_timer.hasElapsed(.25):
            self.intake_solenoid_timer.stop()
            self.intake_solenoid_timer.reset()
            self.intake_solenoid_previous_position = self.intake_solenoid.get()
            self.intake_solenoid.set(wpilib.DoubleSolenoid.Value.kOff)

        # auto-aiming:
        # self.shooter_rolling_average.append((self.potentiometer.getValue() - 3512) * (90/338))
        # self.shooter_rolling_average = self.shooter_rolling_average[1:20]

        # self.shooter_dictionary["shooter_position"] = mean(self.shooter_rolling_average)

        # if self.shooter_dictionary["shooting"] and self.shooter_dictionary["step"] == 0:
        #     self.controllerHID.setRumble(interfaces.GenericHID.RumbleType.kRightRumble, 1)
        #     # self.controllerHID.setRumble(interfaces.GenericHID.RumbleType.kLeftRumble, 1)
        # else:
        #     self.controllerHID.setRumble(interfaces.GenericHID.RumbleType.kRightRumble, 0)
        #     # self.controllerHID.setRumble(interfaces.GenericHID.RumbleType.kLeftRumble, 0)

        # if self.controller.getYButtonPressed():
        #     self.motor_dictionary["shooter_angle"]["previous_position"] = (self.potentiometer.getValue() - 3512) * (90/338)
        #     self.shooter_dictionary["timer"] = 0
        #     self.shooter_timer.stop()
        #     self.shooter_timer.reset()
        #     self.shooter_dictionary["step"] = 0
        #     self.shooter_dictionary["shooting"] = True
        #     self.shooter_dictionary["centered"] = [False, False]
        #     self.shooter_dictionary = helper_functions.shoot(self.shooter_dictionary, self.motor_dictionary)
        
        # elif self.controller.getBackButtonPressed():
        #     self.shooter_dictionary["shooting"] = False
        #     self.shooter_dictionary["step"] = 0
        #     self.shooter_dictionary["centered"] = [False, False]
                 
        # elif self.shooter_dictionary["shooting"]:
        #     if self.shooter_dictionary["firing"]:
        #         self.shooter_timer.start()
        #         self.shooter_dictionary["timer"] = self.shooter_timer.get()
        #     else:
        #         self.shooter_timer.stop()
        #         self.shooter_timer.reset()
        #         self.shooter_dictionary["timer"] = 0
        #     self.shooter_dictionary = helper_functions.shoot(self.shooter_dictionary, self.motor_dictionary)

        # print(self.shooter_dictionary["shooting"])
        # print(self.shooter_dictionary["step"])
        # print(NetworkTables.getTable("limelight").getNumber("tx", 0))
        # print(NetworkTables.getTable("limelight").getNumber("ty", 0))
        # print(self.controller.getRightTriggerAxis())

        #arm limit switch
        # if self.limit_switch.get():
        #     self.shooter_angle.set(0)

        if self.controllerHID.getPOV() == 0:
            self.winch.set(1)
        elif self.controllerHID.getPOV() == 180:
            self.winch.set(-1)
        else:
            self.winch.set(0)

        #hub aiming
        # print(((self.potentiometer.getValue() - 3512) * (90/338)))
        print(self.potentiometer.getValue())

        #0:3955 90: 3962

        if self.controller.getXButtonPressed():
            self.hub_shooting = True
        if self.hub_shooting:
            if ((self.potentiometer.getValue() - 3512) * (90/338)) < 70:
                self.shooter_angle.set(.5)
            if ((self.potentiometer.getValue() - 3512) * (90/338)) > 80:
                self.shooter_angle.set(-.5)
            else:
                self.shooter_angle.set(0)
                self.shooter.set(.7)
                self.timer.start()
                self.hub_shooting = False
        if self.timer.hasElapsed(1):
            self.shooter_solenoid.set(wpilib.DoubleSolenoid.Value.kForward)
        if self.timer.hasElapsed(1.25):
            self.shooter_solenoid.set(wpilib.DoubleSolenoid.Value.kOff)
        if self.timer.hasElapsed(1.75):
            self.shooter.set(0)
            self.shooter_solenoid.set(wpilib.DoubleSolenoid.Value.kReverse)
        if self.timer.hasElapsed(2):
            self.shooter_solenoid.set(wpilib.DoubleSolenoid.Value.kOff)
            self.timer.stop()
            self.timer.reset()

        if self.controller.getBackButtonPressed:
            self.hub_shooting = False

        # if self.controller.getXButton():
        #     self.motor_dictionary["shooter_angle"]["motor"].set(.1)
        # else:
        #     self.motor_dictionary["shooter_angle"]["motor"].set(0)

    def autonomousInit(self):
        self.timer.start()

        # #Initial motor values
        self.shooter.set(.3)
        # self.front_right.set(-.3)
        # self.front_left.set(-.3)
        # self.back_right.set(-.3)
        # self.back_left.set(-.3)

        # #intake ejection
        self.intake_solenoid_timer.start()
        self.climber_solenoid_timer.start()

    def autonomousPeriodic(self):
        ...
        #solenoid defaults
        if self.intake_solenoid_timer.get() > 10 and self.intake_solenoid_timer.get() < 10.1:
            self.intake_solenoid.set(wpilib.DoubleSolenoid.Value.kForward)
        if self.climber_solenoid_timer.get() > 10 and self.climber_solenoid_timer.get() < 10.1:
            self.climber_solenoid.set(wpilib.DoubleSolenoid.Value.kReverse)
        if self.intake_solenoid_timer.get() > 10.25 and self.intake_solenoid_timer.get() < 10.35:
            self.intake_solenoid.set(wpilib.DoubleSolenoid.Value.kOff)
            self.intake_solenoid_timer.stop()
            self.intake_solenoid_timer.reset()
        if self.climber_solenoid_timer.get() > 10.25 and self.climber_solenoid_timer.get() < 10.35:
            self.climber_solenoid.set(wpilib.DoubleSolenoid.Value.kOff)
            self.climber_solenoid_timer.stop()
            self.climber_solenoid_timer.reset()

        if self.timer.hasElapsed(2):
            self.shooter_solenoid.set(wpilib.DoubleSolenoid.Value.kForward)
        if self.timer.hasElapsed(2.25):
            self.shooter_solenoid.set(wpilib.DoubleSolenoid.Value.kOff)
            self.shooter.set(0)
        if self.timer.hasElapsed(2.75):
            self.shooter_solenoid.set(wpilib.DoubleSolenoid.Value.kReverse)
            self.front_right.set(-.3)
            self.front_left.set(-.3)
            self.back_right.set(-.3)
            self.back_left.set(-.3)
        if self.timer.hasElapsed(3):
            self.shooter_solenoid.set(wpilib.DoubleSolenoid.Value.kOff)
        if self.timer.hasElapsed(5):
            self.front_right.set(0)
            self.front_left.set(0)
            self.back_right.set(0)
            self.back_left.set(0)
        
        self.timer.stop()
        self.timer.reset()


if __name__ == "__main__": 
    wpilib.run(MyRobot)
