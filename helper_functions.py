from networktables import NetworkTables
import math
import wpilib
import ctre

#network sync function
NetworkTables.initialize()
smartdash = NetworkTables.getTable("smartdash")
motor_dict = smartdash.getSubTable("motor_dict")

def network_sync(motor_dictionary):
    for i in motor_dictionary:
        for j in motor_dictionary[i]:
            motor_dict.putNumber(f"{i}_{j}", motor_dictionary[i][j])


#motor positioner function
def motor_positioner(motor_dictionary):
    for motor in motor_dictionary:
        if motor ["postion"] < motor ["target_position"]:
                motor.set(1)
        else:
                motor.set(0)

#auto aim and shoot function
def shoot(shooter_dictionary, motor_dictionary, speed = 1) -> dict:
    if NetworkTables.getTable("limelight").getNumber("tv", 0) == 1 and shooter_dictionary["step"] == 0:
        shooter_dictionary["step"] = 1

    if NetworkTables.getTable("limelight").getNumber("tx", 0) < -2 and shooter_dictionary["step"] == 1:  # horizontal offset
        motor_dictionary["back_right"]["motor"].set(speed * 0.5)
        motor_dictionary["front_left"]["motor"].set(-speed * 0.5)
        motor_dictionary["back_left"]["motor"].set(-speed * 0.5)
        motor_dictionary["front_right"]["motor"].set(speed * 0.5)
    elif NetworkTables.getTable("limelight").getNumber("tx", 0) > 2 and shooter_dictionary["step"] == 1:
        motor_dictionary["back_right"]["motor"].set(-speed * 0.5)
        motor_dictionary["front_left"]["motor"].set(speed * 0.5)
        motor_dictionary["back_left"]["motor"].set(speed * 0.5)
        motor_dictionary["front_right"]["motor"].set(-speed * 0.5)
    elif shooter_dictionary["step"] == 1:
        motor_dictionary["back_right"]["motor"].set(0)
        motor_dictionary["front_left"]["motor"].set(0)
        motor_dictionary["back_left"]["motor"].set(0)
        motor_dictionary["front_right"]["motor"].set(0)

    if NetworkTables.getTable("limelight").getNumber("ty", 0) < -2 and shooter_dictionary["step"] == 1:  # vertical offset
        motor_dictionary["shooter_angle"]["motor"].set(speed * .5)
    elif NetworkTables.getTable("limelight").getNumber("ty", 0) > 2 and shooter_dictionary["step"] == 1:
        motor_dictionary["shooter_angle"]["motor"].set(-speed * .5)
    elif shooter_dictionary["step"] == 1:
        motor_dictionary["shooter_angle"]["motor"].set(0)

    if motor_dictionary["front_right"]["motor"].getMotorOutputPercent() == 0 and ctre.WPI_TalonSRX(11).getMotorOutputPercent() == 0:
        shooter_dictionary["step"] = 2

    if shooter_dictionary["step"] == 2:
        angle = shooter_dictionary["shooter_position"] * (math.pi/180) #shooter angle in radians
        shooterHeight = (math.sin(angle) * 1) + 0  # * arm length + chassis height
        basketY = (10400 / 3937) - shooterHeight  # top basket total height in meters - shooter height to make the shot from (0, 0)
        basketX = basketY / math.tan(angle)
        basketY += 0.30  # height raised to aim for basket (in meters), not for reflective strip and to allow ball to clear rim
        #angle calculation for final angle (1 is the velocity(may need to be convert to m/s)):
        angle_plus = 180 / (math.atan(((10.601739130434783**2) + math.sqrt((10.601739130434783**4) - (9.80665 * ((9.80665 * (basketX**2)) + (2 * (basketY * (10.601739130434783**2))))))) / (basketX * 9.80665)) * math.pi)
        angle_minus = 180 / (math.atan(((10.601739130434783**2) - math.sqrt((10.601739130434783**4) - (9.80665 * ((9.80665 * (basketX**2)) + (2 * (basketY * (10.601739130434783**2))))))) / (basketX * 9.80665)) * math.pi)

        if angle_plus > angle_minus:  # sets the shooter angle to whichever is larger, plus or minus, this will help avoid negative values
            angle = angle_plus
        elif  angle_plus < angle_minus:
            angle = angle_minus
        #at this point angle is in degrees rather than radians(probably)

        motor_dictionary["shooter_angle"]["previous_position"] = shooter_dictionary["shooter_position"]

        shooter_dictionary["step"] = 3
    
    if motor_dictionary["shooter_angle"]["previous_position"] < (angle * (256 / 45)) and shooter_dictionary["step"] == 3:
        if shooter_dictionary["shooter_position"] < angle:
            motor_dictionary["shooter_angle"]["motor"].set(speed * .3)
    elif motor_dictionary["shooter_angle"]["previous_position"] > (angle * (256 / 45)) and shooter_dictionary["step"] == 3:
       if shooter_dictionary["shooter_position"] > angle:
            motor_dictionary["shooter_angle"]["motor"].set(-speed * .3)
    elif shooter_dictionary["step"] == 3:
        motor_dictionary["shooter_angle"]["motors"].set(0)
        shooter_dictionary["step"] = 4

    if shooter_dictionary["step"] == 4:
        if shooter_dictionary["timer"] > 0 and shooter_dictionary["timer"] <= 3:
            motor_dictionary["shooter"]["motor"].set(1)
        if shooter_dictionary["timer"] >= 3 and shooter_dictionary["timer"] <= 3.1:
            shooter_dictionary["shooter_solenoid"].set(wpilib.DoubleSolenoid.Value.kForward)
        if shooter_dictionary["timer"] >= 3.25 and shooter_dictionary["timer"] <= 3.35:
            shooter_dictionary["shooter_solenoid"].set(wpilib.DoubleSolenoid.Value.kOff)
            motor_dictionary["shooter"]["motor"].set(0)
            shooter_dictionary["shooting"] = False
            shooter_dictionary["firing"] = False
            shooter_dictionary["step"] = 0
            return shooter_dictionary

    shooter_dictionary["shooting"] = True
    return shooter_dictionary

