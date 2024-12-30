import math
import random
import sys

import matplotlib.pyplot as plt
import numpy as np


def ease_in_out(x):
    """Easing method to slow down near bounds (a, b)"""
    return 1 - (math.cos(x * math.pi) / 2 + 0.5)



class Machine:
    UPPER: float = 1.0
    LOWER: float = -1.0

    def __init__(self, init_speed=0.01):
        self.speed = init_speed
        print(f"starting speed: {self.speed}")
        # position
        self.pos = random.uniform(self.LOWER, self.UPPER)
        print(f"starting position: {self.pos}")

    def run(self):
        pass


def main():
    mac = Machine()
    mac.run()


if __name__ == "__main__":
    try:  # because Python doesn't know how to exit gracefully
        main()
    except KeyboardInterrupt:
        print('program ending')
        sys.exit(130)
