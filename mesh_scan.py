from stl import mesh
import numpy as np

# Load the STL file

stl_file = 'model.stl'
mesh_data = mesh.Mesh.from_file(stl_file)

# Get the vertices and faces
vertices = mesh_data.vectors.reshape((-1, 3))
faces = np.arange(len(vertices)).reshape((-1, 3))

# Save vertices and faces to a text file
output_file = 'output.txt'
np.savetxt(output_file, vertices, fmt='%f', delimiter=' ', header='Vertices', comments='')
with open(output_file, 'a') as file:
    np.savetxt(file, faces, fmt='%d', delimiter=' ', header='Faces', comments='')
