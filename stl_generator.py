import numpy as np
from stl import mesh

def generate_stl_file(filename, width, height, thickness):
    # Create vertices
    vertices = np.array([
        [0, 0, 0],
        [width, 0, 0],
        [width, height, 0],
        [0, height, 0],
        [0, 0, thickness],
        [width, 0, thickness],
        [width, height, thickness],
        [0, height, thickness]
    ])

    # Create faces
    faces = np.array([
        [0, 3, 1],
        [1, 3, 2],
        [0, 4, 7],
        [0, 7, 3],
        [4, 5, 6],
        [4, 6, 7],
        [5, 1, 2],
        [5, 2, 6],
        [2, 3, 7],
        [2, 7, 6],
        [0, 5, 1],
        [0, 4, 5]
    ])

    # Create the mesh
    mesh_data = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
    for i, face in enumerate(faces):
        for j, vertex in enumerate(face):
            mesh_data.vectors[i][j] = vertices[vertex]

    # Save the mesh to an STL file
    mesh_data.save(filename)

# User input
filename = input("Enter the filename for the STL file: ")
filename += ".stl" 
width = float(input("Enter the width: "))
height = float(input("Enter the height: "))
thickness = float(input("Enter the thickness: "))

# Generate the STL file
generate_stl_file(filename, width, height, thickness)
print("STL file generated successfully!")
