steering_i_output = 90
steering_new_result = 70
STEERING_I_MAX = 0
STEERING_I_MIN = -0
steering_i_output = max(min(steering_i_output + steering_new_result, STEERING_I_MAX), STEERING_I_MIN)
print(steering_i_output)