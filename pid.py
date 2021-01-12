# PID

import pyb, machine

class SteeringPid():

    STEERING_OFFSET = const(105) # Change this if you need to fix an imbalance in your car (0 to 180).
    STEERING_P_GAIN = const(-23) # Make this smaller as you increase your speed and vice versa.
    STEERING_I_GAIN = const(2)
    STEERING_I_MIN = const(-1)
    STEERING_I_MAX = const(1)
    STEERING_D_GAIN = const(-9) # Make this larger as you increase your speed and vice versa.

    def __init__(self):
        self.old_time = pyb.millis()
        self.steering_old_result = None
        self.steering_i_output = 0
        self.p_gain = STEERING_P_GAIN
        self.i_gain = STEERING_I_GAIN
        self.d_gain = STEERING_D_GAIN

    def set_p_gain(gain):
        self.p_gain = gain

    def set_i_gain(gain):
        self.i_gain = gain

    def set_d_gain(gain):
        self.d_gain = gain

    def calculate(self, new_value):
        new_time = pyb.millis()
        delta_time = new_time - self.old_time
        self.old_time = new_time

        # Figure out steering and do steering PID
        steering_new_result = new_value
        # error = setpoint - measured_value
        steering_delta_result = (steering_new_result - self.steering_old_result) if (self.steering_old_result != None) else 0
        self.steering_old_result = steering_new_result

        steering_p_output = steering_new_result # Standard PID Stuff here... nothing particularly interesting :)
        # integral = integral + error * dt
        self.steering_i_output = max(min(self.steering_i_output + steering_new_result, STEERING_I_MAX), STEERING_I_MIN)
        # STEERING_I_MAX = 0
        # STEERING_I_MIN = -0
        # derivative = (error - previous_error) / dt
        steering_d_output = ((steering_delta_result * 1000) / delta_time) if delta_time else 0
        steering_pid_output = (self.p_gain * steering_p_output) + \
                              (self.i_gain * self.steering_i_output) + \
                              (self.d_gain * steering_d_output)
        # STEERING_P_GAIN = -23.0 # Make this smaller as you increase your speed and vice versa.
        # STEERING_I_GAIN = 0.0
        # STEERING_D_GAIN = -9 # Make this larger as you increase your speed and vice versa.

        # Steering goes from [-90,90] but we need to output [0,180] for the servos.
        steering_output = STEERING_OFFSET + max(min(round(steering_pid_output), 180 - STEERING_OFFSET), STEERING_OFFSET - 180)

        return steering_output

#steeringPID = SteeringPid()

#while(True):
    #new_value = pyb.rng() / 1e9
    #print(steeringPID.calculate(new_value))
