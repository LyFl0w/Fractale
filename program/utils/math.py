#
#  Fracteur Copyright (c) 2023 LyFlow and Florely
#  This program comes with ABSOLUTELY NO WARRANTY; for details type `show w'.
#  This is free software, and you are welcome to redistribute it under certain conditions; type `show c' for details.
#
from numba import jit


@jit(nopython=True)
def power(number, n_power):
    if n_power == 0:
        return 1
    return number * power(number, n_power - 1)


@jit(nopython=True)
def power2(number, n_power):
    if n_power == 0:
        return 1
    temp = power2(number, int(n_power / 2))
    if n_power % 2 == 0:
        return temp * temp
    else:
        return number * temp * temp
