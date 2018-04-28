# Print stm - By: aakoch - Tue Dec 12 2017

import stm

for var in dir(stm):
    val = getattr(stm, var)
    if type(val).__name__ == "str":
        print(str(var) + "=" + val)
    elif type(val).__name__ == "int" and val > stm.TIM2:
        print(str(var) + "=" + str(hex(val)))
    else:
        print(str(var) + "=" + str(val))
