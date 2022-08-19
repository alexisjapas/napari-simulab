from time import sleep
from qtpy.QtWidgets import QWidget, QVBoxLayout
from magicgui import magicgui
import numpy as np
from random import randint, shuffle
from napari.qt.threading import thread_worker

from Predator import Predator
from Prey import Prey


class Darwin(QWidget):
    def __init__(self, viewer) -> None:
        super().__init__()
        self.viewer = viewer
        # Define the layout
        layout = QVBoxLayout()
        layout.addWidget(self.simulate.native)
        self.setLayout(layout)

    @magicgui(call_button="Start simulation")
    def simulate(self, map_height=10, map_width=10, n_predators=10, n_preys=10, n_epochs=10):
        def _update_map():
            for pred in self.predators:
                self.map[pred.y, pred.x] = 255
            for prey in self.preys:
                self.map[prey.y, prey.x] = 128

            if 'map' in self.viewer.layers:
                self.viewer.layers['map'].data = self.map
            else:
                self.viewer.add_image(self.map, name='map')

        @thread_worker
        def _simulate():
            # Initialising individuals
            self.predators = [Predator('genes', randint(0, map_height-1), randint(0, map_width-1)) for _ in range(n_predators)]
            self.preys = [Prey('genes', randint(0, map_height-1), randint(0, map_width-1)) for _ in range(n_preys)]

            # Initialising the map
            self.map = np.zeros((map_height, map_width), dtype=np.uint8)
            _update_map()

            # Looping
            for _ in range(n_epochs):
                individuals = self.preys + self.predators
                shuffle(individuals)
                for individual in individuals:
                    individual.act(self.map)
                _update_map()
                sleep(1)

        # Simulation
        simulator = _simulate()
        simulator.start()


if __name__ == '__main__':
    import napari
    
    # Creates a viewer
    viewer = napari.Viewer()

    # Adds widget to the viewer
    charles = Darwin(viewer)
    viewer.window.add_dock_widget(charles, name="Natural selection simulator")

    # Run napari
    napari.run()
