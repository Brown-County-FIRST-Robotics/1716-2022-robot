# 1716 FIRST Robotics 2022

**Repository for FIRST Robotics team 1716, season of 2022**
## Navigation:
[Information on motors we used](#motors-used)

[Information on controller input](#controller-functions)

[NetworkTables variables used](#networktables-variables)

## Motors used:
|Motor name|Manufacturer|Controller|ID|Is Inverted?|
|-|-|-|-|-|
|self.back_left|CTRE|WPI_TalonFX|0|yes|
|self.front_left|CTRE|WPI_TalonFX|1|yes|
|self.front_right|CTRE|WPI_TalonFX|2|no|
|self.back_right|CTRE|WPI_TalonFX|3|no|
|self.shooter_top|CTRE|WPI_TalonFX|6|yes|
|self.shooter_bottom|CTRE|WPI_TalonFX|7|no|
|self.shooter_angle_1|CTRE|WPI_TalonSRX|10|no|
|self.shooter_angle_2|CTRE|WPI_TalonSRX|11|no|
|self.intake|CTRE|WPI_TalonFX|12|no|

## Motor Controller Groups:
|Group Name|Motor 1|Motor 2|
|-|-|-|
|self.shooter_angle|self.shooter_angle_1|self.shooter_angle_2|
|self.shooter|self.shooter_top|self.shooter_bottom|

## Controller Input:

Extensive list of all input methods on our robot.

|Controller Name|Input Method|Axis|Value|Outputed Action|
|-|-|-|-|-|
|Xbox Controller|Left Joystick|X|-1 - 1|Strafe Left & Right|
|Xbox Controller|Left Joystick|Y|-1 - 1|Move Forwards and Backwards|
|Xbox Controller|Right Joystick|X| -1 - 1|Rotate|
|Xbox Controller|Right Bumper|N/A|True/False|Raise Shooter Arm|
|Xbox Controller|Left Bumper|N/A|True/False|Lower Shooter Arm|
|Xbox Controller|Left Trigger|N/A|0 - 1|Spin Intake In Reverse(Output)|
|Xbox Controller|Right Trigger|N/A|0 - 1|Spin Intake Forwards(Intake)|

## NetworkTables Variables:

List of `NetworkTables` variables used in our code.

|Variable Name|Sub Table _If Applicable_|Key Example|
|-|-|-|
|Parent Table|N/A|smartdash/|
|NetworkSync Function|motor_dict|smartdash/motor_dict/_variable-name_|
