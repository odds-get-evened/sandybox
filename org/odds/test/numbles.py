from numpy import bitwise_and


def main():
    a1 = [2, 3, 1, 0, -1, -3]
    a2 = [1, 3, -1, 2, -2, -1]
    res = bitwise_and(a1, a2)
    print(res)


if __name__ == "__main__":
    main()
    