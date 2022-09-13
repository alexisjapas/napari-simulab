from time import sleep
from qtpy.QtWidgets import QWidget, QVBoxLayout, QPushButton
from magicgui import magicgui
import numpy as np
from random import randint, shuffle
from napari.qt.threading import thread_worker

from Individual import Individual


class Darwin(QWidget):
    def __init__(self, viewer) -> None:
        super().__init__()
        self.viewer = viewer
        # Define the layout
        layout = QVBoxLayout()
        layout.addWidget(self.simulate.native)
        self.button_stop = QPushButton('Stop simulation')
        layout.addWidget(self.button_stop)
        self.setLayout(layout)


    @magicgui(call_button="Start simulation")
    def simulate(self, map_height=100, map_width=100, n_individuals=100, n_epochs=250, dt=0.04, max_energy=100, energy=100, cost_moving=5, cost_resting=1, cost_eating=-7):
        def _update_viewer(map):
            # Add map to viewer
            if 'map' in self.viewer.layers:
                self.viewer.layers['map'].data = self.map
            else:
                self.viewer.add_image(self.map, name='map')

        def _update_positions():
            # Reset the map
            self.map = np.zeros((map_height, map_width), dtype=np.uint8)
            # Setup each individual
            index = 0
            while index < self.n_individuals:
                indi = self.individuals[index]
                if indi.energy < 1:
                    self.individuals.pop(index)
                    self.n_individuals -= 1
                else:
                    self.map[indi.y, indi.x] = 255
                    index += 1  # Only increase the index when not poping item

        @thread_worker
        def _simulate():
            # Initialising individuals
            y_pos = [y * map_height // self.n_individuals for y in range(0, self.n_individuals)]
            shuffle(y_pos)
            x_pos = [x * map_width // self.n_individuals for x in range(0, self.n_individuals)]
            shuffle(x_pos)
            self.individuals = [Individual('genes', y_pos.pop(0), x_pos.pop(0), max_energy, energy, cost_moving, cost_resting, cost_eating, i) for i in range(self.n_individuals)]

            # Initialising the map
            _update_positions()
            yield self.map
            sleep(dt)

            # Looping
            for i in range(n_epochs):
                shuffle(self.individuals)
                for indi in self.individuals:
                    if indi.act(self.map):
                        _update_positions()
                _update_positions()
                yield self.map
                sleep(dt)

        # Simulation
        self.n_individuals = n_individuals
        worker = _simulate()
        worker.yielded.connect(_update_viewer)
        self.button_stop.clicked.connect(worker.quit)
        worker.finished.connect(self.button_stop.clicked.disconnect)
        worker.start()


if __name__ == '__main__':
    import napari

    # Creates a viewer
    viewer = napari.Viewer()

    # Adds widget to the viewer
    charles = Darwin(viewer)
    viewer.window.add_dock_widget(charles, name="Natural selection simulator")

    # Run napari
    napari.run()
