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
    if shooter_dictionary["step"] == 0:     #searching for retroreflective tape
        if NetworkTables.getTable("limelight").getNumber("tv", 0) == 1:
            shooter_dictionary["step"] = 1
    print(NetworkTables.getTable("limelight").getNumber("ty", 0))
    if shooter_dictionary["step"] == 1:
        if NetworkTables.getTable("limelight").getNumber("tx", 0) < 0:  # horizontal offset
            motor_dictionary["back_right"]["motor"].set(speed * 0.1)
            motor_dictionary["front_left"]["motor"].set(-speed * 0.1)
            motor_dictionary["back_left"]["motor"].set(-speed * 0.1)
            motor_dictionary["front_right"]["motor"].set(speed * 0.1)
        elif NetworkTables.getTable("limelight").getNumber("tx", 0) > 0:
            motor_dictionary["back_right"]["motor"].set(-speed * 0.1)
            motor_dictionary["front_left"]["motor"].set(speed * 0.1)
            motor_dictionary["back_left"]["motor"].set(speed * 0.1)
            motor_dictionary["front_right"]["motor"].set(-speed * 0.1)
        else:
            motor_dictionary["back_right"]["motor"].set(0)
            motor_dictionary["front_left"]["motor"].set(0)
            motor_dictionary["back_left"]["motor"].set(0)
            motor_dictionary["front_right"]["motor"].set(0)
            shooter_dictionary["centered"][0] = True

        if NetworkTables.getTable("limelight").getNumber("ty", 0) < 0:  # vertical offset
            motor_dictionary["shooter_angle"]["motor"].set(-speed * .3)
        elif NetworkTables.getTable("limelight").getNumber("ty", 0) > 0:
            motor_dictionary["shooter_angle"]["motor"].set(speed * .3)
        else:
            motor_dictionary["shooter_angle"]["motor"].set(0)
            shooter_dictionary["centered"][1] = True

        if shooter_dictionary["centered"] == [True, True]:
            shooter_dictionary["step"] = 3 #remember to change this 3 back to 2 if uncommenting below
            shooter_dictionary["angle"] = shooter_dictionary["shooter_position"] + 4 #and delete this

    # if shooter_dictionary["step"] == 2:
    #     shooter_dictionary["angle"] = shooter_dictionary["shooter_position"] * (math.pi/180) #shooter angle in radians
    #     shooterHeight = (math.sin(shooter_dictionary["angle"]) * 1) + 0  # * arm length + chassis height
    #     basketY = (10400 / 3937) - shooterHeight  # top basket total height in meters - shooter height to make the shot from (0, 0)
    #     basketX = basketY / math.tan(shooter_dictionary["angle"])
    #     basketY += 0.30  # height raised to aim for basket (in meters), not for reflective strip and to allow ball to clear rim
    #     #angle calculation for final angle (1 is the velocity(may need to be convert to m/s)):
    #     angle_plus = 180 / (math.atan(((10.601739130434783**2) + math.sqrt((10.601739130434783**4) - (9.80665 * ((9.80665 * (basketX**2)) + (2 * (basketY * (10.601739130434783**2))))))) / (basketX * 9.80665)) * math.pi)
    #     angle_minus = 180 / (math.atan(((10.601739130434783**2) - math.sqrt((10.601739130434783**4) - (9.80665 * ((9.80665 * (basketX**2)) + (2 * (basketY * (10.601739130434783**2))))))) / (basketX * 9.80665)) * math.pi)

    #     if angle_plus > angle_minus:  # sets the shooter angle to whichever is larger, plus or minus, this will help avoid negative values
    #         shooter_dictionary["angle"] = angle_plus
    #     elif  angle_plus < angle_minus:
    #         shooter_dictionary["angle"] = angle_minus
    #     #at this point angle is in degrees rather than radians(probably)

    #     motor_dictionary["shooter_angle"]["previous_position"] = shooter_dictionary["shooter_position"]

    #     shooter_dictionary["step"] = 3
    
    if shooter_dictionary["step"] == 3:
        # if motor_dictionary["shooter_angle"]["previous_position"] < (shooter_dictionary["angle"] * (256 / 45)):
        if shooter_dictionary["shooter_position"] < shooter_dictionary["angle"]:
            motor_dictionary["shooter_angle"]["motor"].set(speed * .4)
        elif shooter_dictionary["step"] == 3:
            motor_dictionary["shooter_angle"]["motor"].set(0)
            shooter_dictionary["step"] = 4
        # elif motor_dictionary["shooter_angle"]["previous_position"] > (shooter_dictionary["angle"] * (256 / 45)):
        #     if shooter_dictionary["shooter_position"] > shooter_dictionary["angle"] + 2:
        #         motor_dictionary["shooter_angle"]["motor"].set(-speed * .3)
        #     elif shooter_dictionary["step"] == 3:
        #         motor_dictionary["shooter_angle"]["motor"].set(0)
        #         shooter_dictionary["step"] = 4

    if shooter_dictionary["step"] == 4:
        shooter_dictionary["firing"] = True
        if shooter_dictionary["timer"] > 0 and shooter_dictionary["timer"] <= 1.5:
            motor_dictionary["shooter"]["motor"].setVoltage(6)
        if shooter_dictionary["timer"] >= 1.6 and shooter_dictionary["timer"] <= 1.7:
            shooter_dictionary["shooter_solenoid"].set(wpilib.DoubleSolenoid.Value.kForward)
        if shooter_dictionary["timer"] >= 1.9 and shooter_dictionary["timer"] <= 2:
            shooter_dictionary["shooter_solenoid"].set(wpilib.DoubleSolenoid.Value.kOff)
            motor_dictionary["shooter"]["motor"].set(0)
        if shooter_dictionary["timer"] >= 2.2 and shooter_dictionary["timer"] <= 2.3:
            shooter_dictionary["shooter_solenoid"].set(wpilib.DoubleSolenoid.Value.kReverse)
        if shooter_dictionary["timer"] >= 2.5:
            shooter_dictionary["shooter_solenoid"].set(wpilib.DoubleSolenoid.Value.kOff)
            shooter_dictionary["shooting"] = False
            shooter_dictionary["firing"] = False
            shooter_dictionary["step"] = 0
            shooter_dictionary["centered"] = [False, False]
            return shooter_dictionary

    shooter_dictionary["shooting"] = True
    return shooter_dictionary