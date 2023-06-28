import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from stl import mesh

# Function to load and plot an STL file
def load_and_plot_stl(file_path, ax, color):
    # Load the STL file
    your_mesh = mesh.Mesh.from_file(file_path)
    
    # Plot the 3D model with the specified color
    ax.add_collection3d(Poly3DCollection(your_mesh.vectors, facecolors=color))
    ax.set_xlim3d(np.min(your_mesh.x), np.max(your_mesh.x))
    ax.set_ylim3d(np.min(your_mesh.y), np.max(your_mesh.y))
    ax.set_zlim3d(np.min(your_mesh.z), np.max(your_mesh.z))

# Load and plot the first STL file
file1_path = 'model1.stl'
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
load_and_plot_stl(file1_path, ax, 'red')

# Load and plot the second STL file
file2_path = 'model2.stl'
load_and_plot_stl(file2_path, ax, 'blue')

# Let the user enter the distance between the models
distance = float(input("Enter the distance between the models: "))

# Calculate the offset for the second model
offset = distance + np.max(mesh.Mesh.from_file(file1_path).z) - np.min(mesh.Mesh.from_file(file2_path).z)

# Load the mesh data of the first model
mesh1 = mesh.Mesh.from_file(file1_path)
vertices1 = mesh1.vectors.reshape(-1, 3)

# Load the mesh data of the second model
mesh2 = mesh.Mesh.from_file(file2_path)
vertices2 = mesh2.vectors.reshape(-1, 3)

# Create the combined mesh
combined_vertices = np.concatenate((vertices1, vertices2 + [0, 0, offset]))
combined_faces = np.arange(len(combined_vertices)).reshape(-1, 3)

# Plot the combined model
ax.add_collection3d(Poly3DCollection(combined_vertices[combined_faces], facecolors='green'))
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

# Show the plot
plt.show()
