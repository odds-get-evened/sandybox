from pathlib import Path

import noise
import numpy as np
from PIL import Image
from PIL.ImageDraw import ImageDraw
from ursina import Entity, Terrain, Vec3, Ursina, Texture, DirectionalLight, Vec2, EditorCamera


class TerrainNoise:
    X_SHAPE_SIZE = 1024
    Y_SHAPE_SIZE = 1024

    def __init__(self):
        shape = (self.X_SHAPE_SIZE, self.Y_SHAPE_SIZE)
        scale = 0.5
        octaves = 6
        persistence = 0.5
        lacunarity = 2.0
        seed = np.random.randint(0, 100)

        world = np.zeros(shape)

        xs = np.linspace(0, 1, shape[0])
        ys = np.linspace(0, 1, shape[1])
        world_x, world_y = np.meshgrid(xs, ys)

        # apply perlin noise, instead of np.vectorize, consider using itertools.starmap()
        world = np.vectorize(noise.pnoise2)(
            world_x / scale,
            world_y / scale,
            octaves=octaves,
            persistence=persistence,
            lacunarity=lacunarity,
            repeatx=self.X_SHAPE_SIZE,
            repeaty=self.Y_SHAPE_SIZE,
            base=seed
        )

        perlnoise_img = Path('PerlinNoise2.png')
        if not perlnoise_img.exists():
            img = np.floor((world + 0.5) * 255).astype(np.uint8)  # <-- normalize world first
            Image.fromarray(img, mode='L').save('PerlinNoise2.png', "PNG")


class WorldMesh(Entity):
    def __init__(self, texture='PerlinNoise2', position=(0, -30, 0), generate_noise=False, shader=None):
        if generate_noise:
            TerrainNoise()

        super().__init__(
            model=Terrain('PerlinNoise2', skip=8),
            scale=(470, 20, 470),
            texture_scale=(30, 30),
            position=position,
            texture=texture,
            collider='mesh',
            shader=shader
        )

        grid = [[None for _ in range(80)] for _ in range(80)]
        x_slices = 80
        y_slices = 80

        self.model.generated_vertices = [v + Vec3(0.5, 0.5) for v in self.model.generated_vertices]


class TheGame(Entity):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = Ursina(
            title='game prac',
            borderless=False,
            editor_ui_enabled=False,
            development_mode=False,
            size=(640, 480)
        )

        self.do_study()

    def do_study(self):
        e1 = Entity(model='cube', texture=Texture(Path("assets", "Dirty_Grass_DIFF.jpg")))
        e2 = Entity(model='cube', texture=e1.texture, position=Vec3(e1.x + 2, e1.y, e1.z))

        im = Image.new('RGBA', (400, 400), (255, 255, 255, 0))
        draw = ImageDraw(im)
        draw.polygon([
            (0, 0), (0, 400),
            (400, 400), (400, 0)
        ], fill='green', outline='purple')
        draw.line([(0, 0), (400, 400)], fill=(0, 0, 0), width=50)

        e3 = Entity(model='cube', texture=Texture(im), position=Vec3(e2.x + 2, e2.y, e2.z))

        pivot = Entity()
        light = DirectionalLight(
            parent=pivot,
            y=2,
            z=3,
            shadows=True,
            rotation=(45, -45, 45),
            shadow_map_resolution=Vec2(5024, 5024)
        )

        EditorCamera()
        # Sky(texture='sky_sunset')

        WorldMesh(generate_noise=True)

        self.app.run()

    def update(self):
        pass

    def input(self, key):
        pass


def main():
    TheGame()


if __name__ == "__main__":
    main()
