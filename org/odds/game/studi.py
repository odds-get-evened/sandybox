from ursina import Ursina, Entity, DirectionalLight, Vec3, Vec2, held_keys, color, camera, mouse, \
    clamp


class ThirdPersonController(Entity):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.camera_pivot = Entity(parent=self, y=2)
        self.camera_distance = 5
        self.rotation_speed = Vec2(40, 60)
        self.movement_speed = 5
        self.mouse_sensitivity = Vec2(40, 40)

        self.cursor = Entity(parent=self.camera_pivot, model='cube', color=color.azure, scale=0.1, y=0)

        # set any kwargs
        for kw_key, kw_val in kwargs.items():
            setattr(self, kw_key, kw_val)

        camera.parent = self.camera_pivot
        camera.position = (0, 0, -self.camera_distance)
        camera.rotation_x = 0

    def update(self):
        # camera rotation
        self.camera_pivot.rotation_y += mouse.velocity[0] * self.mouse_sensitivity[0]
        self.camera_pivot.rotation_x -= mouse.velocity[1] * self.mouse_sensitivity[1]
        self.camera_pivot.rotation_x = clamp(self.camera_pivot.rotation_x, -60, 60)

        # character movement
        direction = Vec3(
            self.forward * (held_keys['w'] - held_keys['s']) + self.right * (held_keys['d'] - held_keys['a'])
        ).normalized()

        self.position += direction * 0.06 * self.movement_speed


class StudiGame(Entity):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.app = Ursina(
            title='studi',
            borderless=False,
            editor_ui_enabled=False,
            development_mode=False,
            size=(1024, 768)
        )

        self.pivot = Entity()

        self.directional_light = DirectionalLight(
            parent=self.pivot,
            y=2, z=3, shadows=True, rotation=Vec3(45, -45, 45),
            shadow_map_resolution=Vec2(1024, 1024)
        )

        self.ground = Entity(model='plane', scale=(100, 1, 100), texture='white_cube', texture_scale=(100, 100),
                             collider='box')

        self.player = ThirdPersonController(model='cube', color=color.orange, scale_y=2)

        # EditorCamera()

        self.app.run()


def main(*args):
    StudiGame()


if __name__ == "__main__":
    main()
