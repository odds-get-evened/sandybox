import math
import random
import sys
import time


def ease_in_out(x):
    """Easing method t oslow down near bounds (-1, 1)"""
    return 1 - (math.cos(x * math.pi) / 2 + 0.5)


def main():
    low = -1.0
    high = 1.0

    position = -1.0
    direction = 1  # 1 for forward, and -1 backward
    speed = 0.01  # base increment step

    position = random.uniform(low, high)
    direction = random.choice([-1, 1])

    while True:
        position += direction * speed
        print(position)
        time.sleep(1)


if __name__ == "__main__":
    try:  # because Python doesn't know how to exit gracefully
        main()
    except KeyboardInterrupt:
        print('program ending')
        sys.exit(130)
