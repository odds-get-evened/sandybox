from pathlib import Path

from ursina import Entity, Ursina, EditorCamera, DirectionalLight, Mesh, Vec3, color, AmbientLight, load_texture, \
    Texture, Terrain, Sky, scene
from ursina.shaders import lit_with_shadows_shader


class QuantumRealm(Entity):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.__nodes__ = []

        self.app = Ursina(
            title="Quantum Realm",
            borderless=False,
            editor_ui_enabled=False,
            development_mode=False,
            size=(640, 480)
        )

        self.pivot = Entity()

        self.directional_light = DirectionalLight(parent=self.pivot, y=2, z=3, shadows=True, rotation=Vec3(45, -45, 45))
        self.ambient_light = AmbientLight(parent=self.pivot, color=color.rgba(100, 100, 100, 0.1))

        EditorCamera()

    def add_plot(self, plot: list[tuple], the_color=color.green):
        e = Entity(position=Vec3(0, 0, 0), model=Mesh(mode='line', thickness=2, vertices=plot), color=the_color,
                   shader=lit_with_shadows_shader)
        self.__nodes__.append(e)
