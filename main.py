import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
from stl import mesh

# Load the first STL file
stl_file1 = 'models/model1.stl'
mesh_data1 = mesh.Mesh.from_file(stl_file1)

# Load the second STL file
stl_file2 = 'models/model2.stl'
mesh_data2 = mesh.Mesh.from_file(stl_file2)

# Merge the vectors and concatenate the points
combined_vectors = np.concatenate([mesh_data1.vectors, mesh_data2.vectors])
combined_points = np.concatenate([mesh_data1.points, mesh_data2.points])

# Create a new figure and axes
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Plot the combined surface
ax.add_collection3d(mplot3d.art3d.Poly3DCollection(combined_vectors))

# Set the aspect ratio of the plot
scale = combined_points.flatten()
ax.auto_scale_xyz(scale, scale, scale)

# Function to handle zoom event
def on_scroll(event):
    ax.set_xlim3d(ax.get_xlim3d())
    ax.set_ylim3d(ax.get_ylim3d())
    ax.set_zlim3d(ax.get_zlim3d())

# Connect the scroll event to the zoom function
fig.canvas.mpl_connect('scroll_event', on_scroll)

# Show the plot
plt.show()
