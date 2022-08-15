from qtpy.QtWidgets import QWidget, QVBoxLayout
from magicgui import magicgui


class Darwin(QWidget):
    def __init__(self, viewer) -> None:
        super().__init__()
        self.viewer = viewer
        # Define the layout
        layout = QVBoxLayout()
        layout.addWidget(self.simulate.native)

    @magicgui(call_button="Start simulation")
    def simulate(self):
        pass


if __name__ == '__main__':
    import napari
    
    # Creates a viewer
    viewer = napari.Viewer()

    # Adds widget to the viewer
    charles = Darwin(viewer)
    viewer.window.add_dock_widget(charles, name="Natural selection simulator")

    # Run napari
    napari.run()
