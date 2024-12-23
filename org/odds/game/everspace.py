import random
import time

from ursina import *


class Starfield:
    def __init__(self, num_stars=1000, boundary=300):
        self.num_stars = num_stars
        self.boundary = boundary
        #self.stars = []
        #self.generate_stars()
        self.star_mesh = self.generate_star_mesh()

    def generate_star_mesh(self):
        vertices = []
        colors = []

        for _ in range(self.num_stars):
            x = random.uniform(-self.boundary, self.boundary)
            y = random.uniform(-self.boundary, self.boundary)
            z = random.uniform(-self.boundary, self.boundary)
            vertices.append(Vec3(x, y, z))

            # random color
            color_choice = random.choice([
                color.white, color.white10, color.white33,
                color.yellow, color.red, color.brown
            ])
            colors.append(color_choice)

        # creates a mesh with the generated vertices
        _mesh = Mesh(vertices=vertices, mode='point', colors=colors)
        Entity(model=_mesh)

        return _mesh

    def generate_stars(self):
        for _ in range(self.num_stars):
            star = Entity(
                model='sphere',
                scale=random.uniform(0.1, 0.3),
                color=random.choice([color.white, color.cyan, color.yellow, color.red, color.brown]),
                position=Vec3(
                    random.uniform(-self.boundary, self.boundary),
                    random.uniform(-self.boundary, self.boundary),
                    random.uniform(-self.boundary, self.boundary)
                )
            )
            # self.stars.append(star)


class SpaceGame:
    def __init__(self):
        self.last_time = time.time()

        self.engine = Ursina()

        self.starfield = Starfield(num_stars=1000000, boundary=1000)

        self.spaceship = Entity(
            model='cube',
            texture='white_cube',
            color=color.gray,
            scale=(2, 1, 4),
            position=(0, 0, 0),
            collider='box'
        )

        # camera setup
        self.cam_pivot = Entity(parent=self.spaceship, position=Vec3(0, 2, 0))
        camera.parent = self.cam_pivot
        self.first_person_mode = False
        self.third_person_offset = Vec3(0, 2, -10)
        self.set_camera_view()

        # instructions and state
        self.mission_text = Text(text="press 'V' to switch views", position=(-0.5, 0.45), scale=1.2)
        self.collected_resources = 0

        # input handling
        self.engine.input = self.handle_inputs

        # run the update method
        self.engine.update = self.update_game

    def handle_inputs(self, key):
        if key == 'v up':
            self.first_person_mode = not self.first_person_mode
            self.set_camera_view()

    def set_camera_view(self):
        if self.first_person_mode:
            camera.position = Vec3(0, 0, 0)
            camera.rotation = Vec3(0, 0, 0)
        else:
            camera.position = self.third_person_offset

    def update_game(self):
        print("update_game")
        self.spaceship_movement()

    def spaceship_movement(self):
        speed = 5
        rotation_speed = 60
        print(held_keys)

        # movement
        if held_keys['w']:
            self.spaceship.position += self.spaceship.forward * speed * self.dt()
        if held_keys['s']:
            self.spaceship.position -= self.spaceship.forward * speed * self.dt()
        if held_keys['a']:
            self.spaceship.position -= self.spaceship.right * speed * self.dt()
        if held_keys['d']:
            self.spaceship.position += self.spaceship.right * speed * self.dt()

        # rotation
        if held_keys['q']:
            self.spaceship.rotation_y -= rotation_speed * self.dt()
        if held_keys['e']:
            self.spaceship.rotation_y += rotation_speed * self.dt()

    def dt(self):
        cur_time = time.time()
        delta = cur_time - self.last_time
        self.last_time = cur_time

        return delta

    def run(self):
        self.engine.run()


def main():
    space_game = SpaceGame()
    space_game.run()


if __name__ == "__main__":
    main()
