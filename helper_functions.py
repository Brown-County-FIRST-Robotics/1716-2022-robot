from networktables import NetworkTables

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
        if motor ["position"] < motor ["target_position"]:
                motor["motor"].set(1)
                return True
        elif motor ["position"] > motor ["target_position"]:
                motor["motor"].set(-1)
                return True
        else:
                motor["motor"].set(0)
                return False