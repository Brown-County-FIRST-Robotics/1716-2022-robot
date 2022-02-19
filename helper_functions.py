from networktables import NetworkTables

# network sync function
NetworkTables.initialize()
smartdash = NetworkTables.getTable("smartdash")
motor_dict = smartdash.getSubTable("motor_dict")


def network_sync(motor_dictionary):
    for i in motor_dictionary:
        for j in motor_dictionary[i]:
            motor_dict.putNumber(f"{i}_{j}", motor_dictionary[i][j])


# motor positioner function
def motor_positioner(motor_dictionary, speed=1):
    for motor in motor_dictionary:
        if (
            motor_dictionary[motor]["previous_position"]
            < motor_dictionary[motor]["target_position"]
        ):
            if motor_dictionary[motor]["position"] < motor_dictionary[motor]["target_position"]:
                motor_dictionary[motor]["motor"].set(speed)
                return False
            else:
                motor_dictionary[motor]["motor"].set(0)
                return True

        if (
            motor_dictionary[motor]["previous_position"]
            > motor_dictionary[motor]["target_position"]
        ):
            if motor_dictionary[motor]["position"] > motor_dictionary[motor]["target_position"]:
                motor_dictionary[motor]["motor"].set(-speed)
                return False
            else:
                motor_dictionary[motor]["motor"].set(0)
                return True
