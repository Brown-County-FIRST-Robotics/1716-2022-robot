
from flask import Flask, json
from networktables import NetworkTables
import json

#first define what table we pull the values from, by default SmartDashboard is the only one on the robot, but you can make additional ones
smartdash = NetworkTables.getTable("/SmartDashboard")
motor0voltage = 0
motor1voltage = 0
motor2voltage = 0
motor3voltage = 0
motor0velocity = 0
motor1velocity = 0
motor2velocity = 0
motor3velocity = 0

api = Flask(__name__)

@api.route('/robot', methods=['GET'])
def get_data():
    voltage0 =  smartdash.getValue("motor0voltage", 0)
    voltage1 =  smartdash.getValue("motor1voltage", 0)
    voltage2 =  smartdash.getValue("motor2voltage", 0)
    voltage3 =  smartdash.getValue("motor3voltage", 0)
    velocity0 = smartdash.getValue("motor0velocity", 0)
    velocity1 = smartdash.getValue("motor1velocity", 0)
    velocity2 = smartdash.getValue("motor2velocity", 0)
    velocity3 = smartdash.getValue("motor3velocity", 0)

    robot_data = {
        "motor0" : {
            "voltage": voltage0,
            "speed": velocity0
        },
        "motor1" : {
            "voltage": voltage1,
            "speed": velocity1
        },
        "motor2" : {
            "voltage": voltage2,
            "speed": velocity2
        },
        "motor3" : {
            "voltage": voltage3,
            "speed": velocity3
        },
    }
    return json.dumps(robot_data)

if __name__ == '__main__':
    api.run() 
