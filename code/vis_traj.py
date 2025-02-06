from ase.io import read, write
from ase.visualize import view
from ase.io import Trajectory

# From: https://wiki.fysik.dtu.dk/ase/ase/visualize/visualize.html

# Set import and add atoms
file = Trajectory(str(input('Trajectory Location:\n')))

view(file)
# list = 

# write('movie.gif', file[::10], interval=500, rotation='90x')

# for i, atoms in enumerate(file[::10]):
#     print(i)
#     renderer = write('movie' + str(i) + '.pov', atoms, format='pov',
#                     rotation='90x',
#                     povray_settings=dict(canvas_width=200))

#     renderer.render()