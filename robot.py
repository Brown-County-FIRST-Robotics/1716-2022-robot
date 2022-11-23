import wpilib
import ctre
from wpilib import interfaces

class MyRobot(wpilib.TimedRobot):
    def robotInit(self):
        # compressor = wpilib.Compressor(wpilib.PneumaticsModuleType.CTREPCM)
        # compressor.disable()


        self.back_left = ctre.WPI_TalonFX(0)        
        self.front_left = ctre.WPI_TalonFX(1)
        self.front_right = ctre.WPI_TalonFX(2)                
        self.back_right = ctre.WPI_TalonFX(3)
        self.shooter_top = ctre.WPI_TalonFX(6)
        self.shooter_bottom = ctre.WPI_TalonFX(7)
        self.shooter_angle_1 = ctre.WPI_TalonSRX(10)
        self.shooter_angle_2 = ctre.WPI_TalonSRX(11)        
        self.intake = ctre.WPI_TalonFX(12)

    
        self.front_left.setNeutralMode(ctre.NeutralMode.Brake)
        self.front_right.setNeutralMode(ctre.NeutralMode.Brake)
        self.back_left.setNeutralMode(ctre.NeutralMode.Brake)
        self.back_right.setNeutralMode(ctre.NeutralMode.Brake)
        self.front_right.setInverted(True)
        self.back_right.setInverted(True)
        self.shooter_top.setInverted(True)
        self.shooter_angle_1.setInverted(True)
        self.shooter_angle_2.setInverted(True)

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
        
        #speed/safety variables
        self.drive_speed = .7
        self.shooter_angle_speed = 1
        self.shooter_speed = .35
        self.is_birb_activated = True

        #other variables
        self.hub_shooting = [False, False] #[isHubShooting, isMovingToCorrectAngle]
        self.hub_shooting_timer = wpilib.Timer()

        # self.limit_switch = wpilib.DigitalInput(0)
        self.potentiometer = wpilib.AnalogInput(0) #0 degrees: 3512, 90 degrees: 3850

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

    def teleopPeriodic(self):
        #driving
        if abs(self.controller.getLeftY()) > .3 or abs(self.controller.getLeftX()) > .3 or abs(self.controller.getRightX()) > .3:
            self.front_right.set((-self.controller.getLeftY() - self.controller.getLeftX() - self.controller.getRightX()) * self.drive_speed)
            self.front_left.set((-self.controller.getLeftY() + self.controller.getLeftX() + self.controller.getRightX()) * self.drive_speed)
            self.back_left.set((-self.controller.getLeftY() - self.controller.getLeftX() + self.controller.getRightX()) * self.drive_speed)
            self.back_right.set((-self.controller.getLeftY() + self.controller.getLeftX() - self.controller.getRightX()) * self.drive_speed)
        else:
            self.front_right.set(0)
            self.front_left.set(0)
            self.back_right.set(0)
            self.back_left.set(0)
        
        # if self.controller.getYButtonPressed():
        #     if self.drive_speed == 1:
        #         self.drive_speed = .4
        #         print("slow mode")
        #     else:
        #         self.drive_speed = 1
        #         print("FAST MODE")
        

        #shooter angle
        if not self.hub_shooting[0]:
            if self.controller.getRightBumper():
                self.shooter_angle.set(self.shooter_angle_speed)
            elif self.controller.getLeftBumper():
                self.shooter_angle.set(-self.shooter_angle_speed)
            else:
                self.shooter_angle.set(0)

        #shooter/intake
        if not self.hub_shooting[0]:
            if self.controller.getRightTriggerAxis() > self.controller.getLeftTriggerAxis():
                self.shooter.set(self.controller.getRightTriggerAxis() * self.shooter_speed)
                self.intake.set(self.controller.getRightTriggerAxis() * self.shooter_speed)

            if self.controller.getRightTriggerAxis() < self.controller.getLeftTriggerAxis():
                self.intake.set(self.controller.getLeftTriggerAxis() * -.5)
                self.shooter.set(self.controller.getLeftTriggerAxis() * -.5)

            if self.controller.getRightTriggerAxis() == self.controller.getLeftTriggerAxis():
                self.intake.set(0)
                self.shooter_bottom.set(0)
                self.shooter_top.set(0)

        #solenoids:
        if self.controller.getAButtonPressed():
            self.shooter_solenoid_timer.start()
            self.shooter_solenoid.set(wpilib.DoubleSolenoid.Value.kForward)
        if self.shooter_solenoid_timer.hasElapsed(.1) and self.shooter_solenoid_timer.get() < .2:
            self.shooter_solenoid.set(wpilib.DoubleSolenoid.Value.kOff)
        if self.shooter_solenoid_timer.hasElapsed(.5) and self.shooter_solenoid_timer.get() < .55:
            self.shooter_solenoid.set(wpilib.DoubleSolenoid.Value.kReverse)
        if self.shooter_solenoid_timer.hasElapsed(.6) and self.shooter_solenoid_timer.get() < .7:
            self.shooter_solenoid_timer.stop()
            self.shooter_solenoid_timer.reset()
            self.shooter_solenoid.set(wpilib.DoubleSolenoid.Value.kOff)

        if self.controller.getBButtonPressed() and self.is_birb_activated:
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

        #auto angling/hub shooting
        # print((self.potentiometer.getValue() - 2554) * (90/448))

        if self.controller.getXButtonPressed():
            self.hub_shooting = [True, True]

        if self.hub_shooting[0]:
            if self.hub_shooting[1]:
                if ((self.potentiometer.getValue() - 2554) * (90/448)) < 55:
                    self.shooter_angle.set(1)
                elif ((self.potentiometer.getValue() - 2554) * (90/448)) > 60:
                    self.shooter_angle.set(-1)
                else:
                    self.shooter_angle.set(0)
                    self.hub_shooting_timer.start()
                    self.hub_shooting[1] = False
                    self.shooter.set(.3)

            if self.hub_shooting_timer.hasElapsed(1) and self.hub_shooting_timer.get() < 1.1:
                self.shooter_solenoid.set(wpilib.DoubleSolenoid.Value.kForward)
            elif self.hub_shooting_timer.hasElapsed(1.25) and self.hub_shooting_timer.get() < 1.35:
                self.shooter_solenoid.set(wpilib.DoubleSolenoid.Value.kOff)
            elif self.hub_shooting_timer.hasElapsed(1.75) and self.hub_shooting_timer.get() < 1.85:
                self.shooter_solenoid.set(wpilib.DoubleSolenoid.Value.kReverse)
            elif self.hub_shooting_timer.hasElapsed(2) and self.hub_shooting_timer.get() < 2.1:
                self.shooter_solenoid.set(wpilib.DoubleSolenoid.Value.kOff)
            elif self.hub_shooting_timer.hasElapsed(2.75) and self.hub_shooting_timer.get() < 2.8:
                self.shooter_solenoid.set(wpilib.DoubleSolenoid.Value.kForward)
            elif self.hub_shooting_timer.hasElapsed(2.85) and self.hub_shooting_timer.get() < 2.95:
                self.shooter_solenoid.set(wpilib.DoubleSolenoid.Value.kOff)
            elif self.hub_shooting_timer.hasElapsed(2.25) and self.hub_shooting_timer.get() < 2.3:
                self.shooter_solenoid.set(wpilib.DoubleSolenoid.Value.kReverse)
            elif self.hub_shooting_timer.hasElapsed(2.35) and self.hub_shooting_timer.get() < 2.45:
                self.hub_shooting_timer.reset()
                self.hub_shooting_timer.stop()
                self.shooter_solenoid.set(wpilib.DoubleSolenoid.Value.kOff)
                self.shooter.set(0)
                self.shooter_angle.set(-1)
            if ((self.potentiometer.getValue() - 2554) * (90/448)) < -5 and not self.hub_shooting[1]:
                self.shooter_angle.set(0)
                self.hub_shooting[0] = False

        # print(self.hub_shooting_timer.get())

        if self.controller.getBackButtonPressed():
            self.shooter.set(0)
            self.shooter_angle.set(0)
            self.hub_shooting[0] = False
            self.hub_shooting_timer.stop()
            self.hub_shooting_timer.reset()
            self.shooter_solenoid.set(wpilib.DoubleSolenoid.Value.kOff)

    def autonomousInit(self):
        self.timer = wpilib.Timer()
        self.timer.start()
        self.autonomous_shooting = False
        # #Initial motor values
        self.front_right.set(-.3)
        self.front_left.set(-.3)
        self.back_right.set(-.3)
        self.back_left.set(-.3)

        # #intake ejection
        self.intake_solenoid_timer.start()
        self.climber_solenoid_timer.start()

    def autonomousPeriodic(self):
        print(self.timer.get())
        #solenoid defaults
        if self.intake_solenoid_timer.get() > 10 and self.intake_solenoid_timer.get() < 10.1:
            self.intake_solenoid.set(wpilib.DoubleSolenoid.Value.kForward)
        if self.climber_solenoid_timer.get() > 10 and self.climber_solenoid_timer.get() < 10.1:
            self.climber_solenoid.set(wpilib.DoubleSolenoid.Value.kForward)
        if self.intake_solenoid_timer.get() > 10.25 and self.intake_solenoid_timer.get() < 10.35:
            self.intake_solenoid.set(wpilib.DoubleSolenoid.Value.kOff)
            self.intake_solenoid_timer.stop()
            self.intake_solenoid_timer.reset()
        if self.climber_solenoid_timer.get() > 10.25 and self.climber_solenoid_timer.get() < 10.35:
            self.climber_solenoid.set(wpilib.DoubleSolenoid.Value.kOff)
            self.climber_solenoid_timer.stop()
            self.climber_solenoid_timer.reset()

        if self.timer.hasElapsed(2):
            self.front_right.set(0)
            self.front_left.set(0)
            self.back_right.set(0)
            self.back_left.set(0)
        #     self.autonomous_shooting = True
        #     self.timer.reset()
        # if self.autonomous_shooting:
        #     if ((self.potentiometer.getValue() - 2554) * (90/448)) < 60:
        #         self.shooter_angle.set(1)
        #     elif ((self.potentiometer.getValue() - 2554) * (90/448)) > 65:
        #         self.shooter_angle.set(-1)
        #     else:
        #         self.shooter_angle.set(0)
        #         self.shooter.setVoltage(5.7)
        #         self.timer.start()
        #     if self.timer.hasElapsed(1):
        #         self.shooter_solenoid.set(wpilib.DoubleSolenoid.Value.kForward)
        #     if self.timer.hasElapsed(1.25):
        #         self.shooter_solenoid.set(wpilib.DoubleSolenoid.Value.kOff)
        #     if self.timer.hasElapsed(1.75):
        #         self.shooter.set(0)
        #         self.shooter_solenoid.set(wpilib.DoubleSolenoid.Value.kReverse)
        #     if self.timer.hasElapsed(2):
        #         self.autonomous_shooting = False
        #         self.shooter_solenoid.set(wpilib.DoubleSolenoid.Value.kOff)
        #         self.front_right.set(-.2)
        #         self.front_left.set(-.2)
        #         self.back_right.set(-.2)
        #         self.back_left.set(-.2)
        #     if self.timer.hasElapsed(3):
        #         self.front_right.set(0)
        #         self.front_left.set(0)
        #         self.back_right.set(0)
        #         self.back_left.set(0)
        #         self.timer.stop()
        #         self.timer.reset()
        # if self.timer.hasElapsed(2.25):
        #     self.shooter_solenoid.set(wpilib.DoubleSolenoid.Value.kOff)
        #     self.shooter.set(0)
        # if self.timer.hasElapsed(2.75):
        #     self.shooter_solenoid.set(wpilib.DoubleSolenoid.Value.kReverse)
        #     self.front_right.set(-.3)
        #     self.front_left.set(-.3)
        #     self.back_right.set(-.3)
        #     self.back_left.set(-.3)
        # if self.timer.hasElapsed(3):
        #     self.shooter_solenoid.set(wpilib.DoubleSolenoid.Value.kOff)
        # if self.timer.hasElapsed(5):
        #     self.front_right.set(0)
        #     self.front_left.set(0)
        #     self.back_right.set(0)
        #     self.back_left.set(0)
        
        # self.timer.stop()
        # self.timer.reset()


if __name__ == "__main__": 
    wpilib.run(MyRobot)