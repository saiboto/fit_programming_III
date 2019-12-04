import typing

import pybullet
import pybullet_data


class Config:
    def __init__(self,
                 gravity,
                 ground,
                 show_gui: bool,
                 text_on_screen_position: typing.List[float]):
        self.gravity = gravity
        self.ground = ground
        self.show_gui = show_gui
        self.text_on_screen_position = text_on_screen_position


class Simulation:
    def __init__(self, config: Config):
        self._config = config

        if config.show_gui:
            self._pybullet_server_id = pybullet.connect(pybullet.GUI)
        else:
            self._pybullet_server_id = pybullet.connect(pybullet.DIRECT)

        # necessary for using objects of the pybullet_data package
        pybullet.setAdditionalSearchPath(pybullet_data.getDataPath())

        pybullet.setGravity(config.gravity[0],
                            config.gravity[1],
                            config.gravity[2])

        self._ground_id = pybullet.loadURDF(config.ground)

        if config.show_gui:
            self._screen_text_id = pybullet.addUserDebugText(
                text='',
                textPosition=config.text_on_screen_position
            )
        else:
            self._screen_text_id = None

    ERROR_PRINT_TO_SCREEN = (
        'Attempted to print something to the screen of the physics engine"s '
        'GUI while that GUI was turned off.')

    def print_to_screen(self, text: str):
        if not self._config.show_gui:
            raise RuntimeError(Simulation.ERROR_PRINT_TO_SCREEN)
        else:
            self._screen_text_id = pybullet.addUserDebugText(
                text,
                self._config.text_on_screen_position,
                replaceItemUniqueId=self._screen_text_id)

    def run(self, duration: int):
        pybullet.stepSimulation(duration)
