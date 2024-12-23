import asyncio
import math
from pathlib import Path

from odds import rand


class NodeNetwork:
    def __init__(self, models_path: Path, num_nodes=31):
        self.models_path = models_path
        self.num_nodes = num_nodes

        if not self.models_path.exists():
            self.models_path.mkdir(parents=True, exist_ok=True)

        self.nodes = []

    def start(self):
        self.nodes = self.init_nodes()

        asyncio.run(self.train())

    async def train(self):
        train_y = await self.train_y()
        train_z = await self.train_z()

    async def train_y(self):
        pass

    async def train_z(self):
        pass

    def init_nodes(self):
        # build network structure
        return [
            [rand.random_secrets(-1, 1)] +
            [math.nan for _ in range(3)]
            for _ in range(self.len)
        ]
