# napari-simulab

This widget is a natural selection simulation tool.

## Simulation current structure

- Laboratory: retrieves user parameters for the simulation
	- map: single layer 2d matrix. Each pixel can represent:
		- background: 0
		- individual: 255
	- individual(s): each individual is autonomous. They have following attributes:
		- y: vertical position
		- x: horizontal position
		- max energy: maximum value reachable by the individual
		- energy: current value. Actions have energy cost, eating increase energy value. If fall to zero, die
