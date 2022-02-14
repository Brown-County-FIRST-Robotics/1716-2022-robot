# 1716 FIRST Robotics 2022

**Repository for FIRST Robotics team 1716, season of 2022**
## Navigation
[Information of Motors We Used](#motors-used)

[NetworkTables Variables Used](#networktables-variables)

###### Motors used:
|Motor name|Manufacturer|Controller|ID|
|-|-|-|-|
|self.front_right|CTRE|WPI_TalonFX|0|
|self.front_left|CTRE|WPI_TalonFX|1|
|self.back_left|CTRE|WPI_TalonFX|2|
|self.back_right|CTRE|WPI_TalonFX|3|
|self.intake|CTRE|WPI_TalonFX|4|
|self.shooter_angle_1|CTRE|WPI_TalonSRX|10|
|self.shooter_angle_2|CTRE|WPI_TalonSRX|11|


###### Controller Functions

Extensive list of all input methods on our robot.

|Controller Name|Input Method|Axis|Value|Outputed Action|
|-|-|-|-|-|
|Xbox Controller|Left Joystick|X|-1 - 1|Strafe Left & Right|
|Xbox Controller|Left Joystick|Y|-1 - 1|Move Forwards and Backwards|
|Xbox Controller|Right Joystick|X| -1 - 1|Rotate|
|Xbox Controller|D-Pad UP|N/A|0|Raise Shooter Arm|
|Xbox Controller|D-Pad DOWN|N/A|180|Lower Shooter Arm|
|Xbox Controller|Left Trigger|N/A|0 - 1|Spin Intake In Reverse(Output)|
|Xbox Controller|Right Trigger|N/A|0 - 1|Spin Intake Forwards(Intake)|

###### NetworkTables Variables

List of `NetworkTables` variables used in our code.

|Variable Name|Sub Table _If Applicable_|Key Example|
|-|-|-|
|Parent Table|N/A|smartdash/|
|NetworkSync Function|motor_dict|smartdash/motor_dict/_variable-name_|
