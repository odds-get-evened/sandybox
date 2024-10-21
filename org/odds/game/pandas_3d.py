import math

from direct.actor.Actor import Actor
from direct.showbase.ShowBase import ShowBase
from direct.task.Task import Task
from panda3d.core import WindowProperties, CollisionTraverser, CollisionHandlerPusher, CollisionNode, CollisionSphere, \
    Vec3


class SomeGame(ShowBase):
    def __init__(self):
        self.pusher = None
        self.mouse_sensitivity = 0.2

        ShowBase.__init__(self)

        # hide the mouse cursor and lock it to center of the window
        props = WindowProperties()
        props.setCursorHidden(True)
        props.setMouseMode(WindowProperties.M_relative)  # mouse locking mode
        self.win.requestProperties(props)

        # load environment
        self.enviro = self.loader.loadModel("models/environment")
        self.enviro.reparentTo(self.render)
        self.enviro.setScale(0.25, 0.25, 0.25)
        self.enviro.setPos(-8, 42, 0)

        # load player (panda)
        self.player = Actor("models/panda-model", {'walk': 'models/panda-walk4'})
        self.player.reparentTo(self.render)
        self.player.setScale(0.005, 0.005, 0.005)
        self.player.setPos(0, 10, 0)

        # disable default mouse control
        self.disableMouse()

        # initialize camera properties
        self.cam_distance = 30
        self.cam_pitch = 10
        self.cam_yaw = 0

        # flag for movement direction
        self.is_moving_fwd = False
        self.is_moving_bwd = False

        # collision detection and controls
        self.setup_collisions()
        self.setup_controls()

        # task to update player, camera, and handle mouse input
        self.taskMgr.add(self.update, 'update')

    def setup_collisions(self):
        self.cTrav = CollisionTraverser()
        self.pusher = CollisionHandlerPusher()

        c_node = CollisionNode('player')
        c_node.addSolid(CollisionSphere(0, 0, 1, 1))
        c_nodepath = self.player.attachNewNode(c_node)
        c_nodepath.show()  # shows tehe collision path

        self.pusher.addCollider(c_nodepath, self.player)
        self.cTrav.addCollider(c_nodepath, self.pusher)

    def setup_controls(self):
        self.accept('w', self.start_fwd)
        self.accept('s', self.start_bwd)

        self.accept('w-up', self.stop_mv)
        self.accept('s-up', self.stop_mv)

    def start_fwd(self):
        self.is_moving_fwd = True
        self.player.loop('walk')

    def start_bwd(self):
        self.is_moving_bwd = True
        self.player.loop('walk')

    def stop_mv(self):
        self.is_moving_fwd = False
        self.is_moving_bwd = False
        self.player.stop()

    def cam_fwd_vector(self):
        cam_rad = math.radians(self.cam_yaw)

        return Vec3(math.sin(cam_rad), math.cos(cam_rad), 0)

    def update(self, task):
        # handle mouse input for camera rotation
        if self.mouseWatcherNode.hasMouse():
            # mouse deltas (relative to previous position
            md = self.win.getPointer(0)
            mouse_x = md.getX() - self.win.getProperties().getXSize() / 2
            mouse_y = md.getY() - self.win.getProperties().getYSize() / 2

            # recenter the mouse to middle of screen
            self.win.movePointer(0, self.win.getProperties().getXSize() // 2, self.win.getProperties().getYSize() // 2)

            # adjust yaw and pitch based on mouse movement
            self.cam_yaw -= mouse_x * self.mouse_sensitivity
            self.cam_pitch -= mouse_x * self.mouse_sensitivity

        # update camera position
        self.update_cam_pos()

        # camera follows player
        self.camera.lookAt(self.player.getPos() + Vec3(0, 0, 5))

        # handle player movement
        if self.is_moving_fwd:
            self.mv_player(1)
        elif self.is_moving_bwd:
            self.mv_player(-1)

        return Task.cont

    def mv_player(self, direction):
        fwd_vec = self.cam_fwd_vector() * direction
        self.player.setPos(self.player.getPos() + fwd_vec * 0.2)

        # rotate the player to face the camera's direction
        heading = self.cam_yaw
        self.player.setH(heading)

    def update_cam_pos(self):
        heading_rad = math.radians(self.cam_yaw)
        pitch_rad = math.radians(self.cam_pitch)

        # calculate the camera's position relative to player
        cam_x = math.sin(heading_rad) * self.cam_distance * math.cos(pitch_rad)
        cam_y = math.cos(heading_rad) * self.cam_distance * math.cos(pitch_rad)
        cam_z = math.sin(pitch_rad) * self.cam_distance

        # set the camera position
        self.camera.setPos(self.player.getPos() + Vec3(cam_x, cam_y, cam_z))


def main():
    game = SomeGame()
    game.run()


if __name__ == "__main__":
    main()
