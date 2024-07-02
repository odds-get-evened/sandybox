import math


def linear(t):
    return t


def in_sine(t):
    return -math.cos(t * math.pi / 2) + 1


def out_sine(t):
    return math.sin(t * math.pi / 2)


def in_out_sine(t):
    return -(math.cos(math.pi * t) - 1) / 2


def in_quad(t):
    return t * t


def out_quad(t):
    return -t * (t - 2)


def in_out_quad(t):
    t *= 2
    if t < 1:
        return t * t / 2
    else:
        t -= 1
        return -(t * (t - 2) - 1) / 2


def in_cubic(t):
    return t * t * t


def out_cubic(t):
    t -= 1
    return t * t * t + 1


def in_out_cubic(t):
    t *= 2
    if t < 1:
        return t * t * t / 2
    else:
        t -= 2
        return (t * t * t + 2) / 2


def in_quart(t):
    return t * t * t * t


def out_quart(t):
    t -= 1
    return -(t * t * t * t - 1)


def in_out_quart(t):
    t *= 2
    if t < 1:
        return t * t * t * t / 2
    else:
        t -= 2
        return -(t * t * t * t - 2) / 2


def in_quint(t):
    return t * t * t * t * t


def out_quint(t):
    t -= 1
    return t * t * t * t * t + 1


def in_out_quint(t):
    t *= 2
    if t < 1:
        return t * t * t * t * t / 2
    else:
        t -= 2
        return (t * t * t * t * t + 2) / 2


def in_expo(t):
    return math.pow(2, 10 * (t - 1))


def out_expo(t):
    return -math.pow(2, -10 * t) + 1


def in_out_expo(t):
    t *= 2
    if t < 1:
        return math.pow(2, 10 * (t - 1)) / 2
    else:
        t -= 1
        return -math.pow(2, -10 * t) - 1


def in_circ(t):
    return 1 - math.sqrt(1 - t * t)


def out_circ(t):
    t -= 1
    return math.sqrt(1 - t * t)


def in_out_circ(t):
    t *= 2
    if t < 1:
        return -(math.sqrt(1 - t * t) - 1) / 2
    else:
        t -= 2
        return (math.sqrt(1 - t * t) + 1) / 2
