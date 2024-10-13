from direct.actor.Actor import Actor
from direct.showbase.ShowBase import ShowBase
from panda3d.core import Vec3, CollisionTraverser, CollisionHandlerPusher, CollisionNode, CollisionSphere, \
    WindowProperties


class ThirdPersonGame(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        # hide mouse cursor
        props = WindowProperties()
        props.set_cursor_hidden(True)
        self.win.request_properties(props)

        self.pusher = None
        self.c_trav = None
        self.look_at_offset = None
        self.camera_offset = None

        # load environment
        self.enviro = self.loader.load_model("models/environment")
        self.enviro.reparent_to(self.render)
        self.enviro.set_scale(0.25, 0.25, 0.25)
        self.enviro.set_pos(-8, 42, 0)

        # load player
        self.character = Actor("models/panda-model", {"walk": "models/panda-walk4"})
        self.character.reparent_to(self.render)
        self.character.set_scale(0.005, (0.005, 0.005, 0.005))
        self.character.set_pos(0, 10, 0)

        # collision setup
        self.setup_collisions()

        # camera setup
        self.setup_camera()

        # key controls
        self.setup_controls()

        # task to update player and camera
        self.task_mgr.add(self.update, "update")

    def setup_camera(self):
        """ setup 3rd-person camera """
        self.camera_offset = Vec3(0, -3, 10)
        self.look_at_offset = Vec3(0, 0, 5)
        self.disable_mouse()  # disables default camera control
        self.camera.set_pos(self.character.get_pos() + self.camera_offset)
        self.camera.look_at(self.character.get_pos() + self.look_at_offset)

    def setup_collisions(self):
        """ setup player collisions """
        self.c_trav = CollisionTraverser()
        self.pusher = CollisionHandlerPusher()

        collision_node = CollisionNode('player')
        collision_node.add_solid(CollisionSphere(0, 0, 1, 1))
        collision_nodepath = self.character.attach_new_node(collision_node)
        collision_nodepath.show()  # shows the collision sphere around player

    def update(self, task):
        """ update the player and camera positions """
        # camera follows the player
        self.camera.set_pos(self.character.get_pos() + self.camera_offset)
        self.camera.look_at(self.character.get_pos() + self.look_at_offset)

        return task.cont

    def setup_controls(self):
        """ setup keyboard controls for the player """
        self.accept("arrow_up", self.move_forward)
        self.accept("arrow_down", self.move_backward)
        self.accept("arrow_left", self.turn_left)
        self.accept("arrow_right", self.turn_right)
        self.accept("arrow_up-up", self.stop)

    def move_forward(self):
        self.character.loop("walk")
        self.character.set_y(self.character, 1.0)

    def move_backward(self):
        self.character.set_y(self.character, -1.0)

    def turn_left(self):
        self.character.set_h(self.character.get_h() + 10)

    def turn_right(self):
        self.character.set_h(self.character.get_h() - 10)

    def stop(self):
        self.character.stop()


def main():
    game = ThirdPersonGame()
    game.run()


if __name__ == "__main__":
    main()
