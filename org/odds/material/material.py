import os.path

from org.odds.material.network import NodeNetwork


class Material:
    def __init__(self):
        self.network = NodeNetwork(num_nodes=1000, trainer=False)
        self.network.start()


def main():
    mats = Material()


if __name__ == "__main__":
    main()
