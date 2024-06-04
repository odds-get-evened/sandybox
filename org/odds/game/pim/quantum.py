from ursina import Entity, Ursina, EditorCamera, DirectionalLight, Vec2, Mesh, Vec3, color, AmbientLight
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

        # pivot = Entity()

        dir_light = DirectionalLight(shadows=True)
        dir_light.look_at(Vec3(1, -1, 1))
        ambi_light = AmbientLight()

        EditorCamera()

    def add_plot(self, plot: list[tuple]):
        e = Entity(position=Vec3(0, 0, 0), model=Mesh(mode='line', thickness=2, vertices=plot), color=color.green, shader=lit_with_shadows_shader)
        self.__nodes__.append(e)
