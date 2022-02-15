def motor_positioner(motor_dictionary):
        for motor in motor_dictionary:
            if motor ["postion"] < motor ["target_position"]:
                motor.set(1)
            else:
                motor.set(0)
