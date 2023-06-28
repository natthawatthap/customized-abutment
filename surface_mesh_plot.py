import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from stl import mesh
from matplotlib.widgets import Slider
import matplotlib.cm as cm

# Load the STL file
your_mesh = mesh.Mesh.from_file('model.stl')

# Extract vertex coordinates from the mesh
vertices = your_mesh.vectors.reshape(-1, 3)

# Extract the Z coordinates of the vertices
z_coords = vertices[:, 2]

# Calculate the normalized heights (between 0 and 1)
z_min = np.min(z_coords)
z_max = np.max(z_coords)
normalized_heights = (z_coords - z_min) / (z_max - z_min)

# Create colormap
cmap = cm.get_cmap('rainbow')

# Create subplots for each view
fig = plt.figure(figsize=(16, 12))

# Top view
ax_top = fig.add_subplot(231, projection='3d')
ax_top.add_collection3d(Poly3DCollection(your_mesh.vectors, facecolors=cmap(normalized_heights)))
ax_top.set_xlabel('X')
ax_top.set_ylabel('Y')
ax_top.set_zlabel('Z')
ax_top.set_title('Top View')
ax_top.view_init(elev=90, azim=-90)

# Bottom view
ax_bottom = fig.add_subplot(232, projection='3d')
ax_bottom.add_collection3d(Poly3DCollection(your_mesh.vectors, facecolors=cmap(normalized_heights)))
ax_bottom.set_xlabel('X')
ax_bottom.set_ylabel('Y')
ax_bottom.set_zlabel('Z')
ax_bottom.set_title('Bottom View')
ax_bottom.view_init(elev=-90, azim=-90)

# Left view
ax_left = fig.add_subplot(233, projection='3d')
ax_left.add_collection3d(Poly3DCollection(your_mesh.vectors, facecolors=cmap(normalized_heights)))
ax_left.set_xlabel('X')
ax_left.set_ylabel('Y')
ax_left.set_zlabel('Z')
ax_left.set_title('Left View')
ax_left.view_init(elev=0, azim=180)

# Right view
ax_right = fig.add_subplot(234, projection='3d')
ax_right.add_collection3d(Poly3DCollection(your_mesh.vectors, facecolors=cmap(normalized_heights)))
ax_right.set_xlabel('X')
ax_right.set_ylabel('Y')
ax_right.set_zlabel('Z')
ax_right.set_title('Right View')
ax_right.view_init(elev=0, azim=0)

# Front view
ax_front = fig.add_subplot(235, projection='3d')
ax_front.add_collection3d(Poly3DCollection(your_mesh.vectors, facecolors=cmap(normalized_heights)))
ax_front.set_xlabel('X')
ax_front.set_ylabel('Y')
ax_front.set_zlabel('Z')
ax_front.set_title('Front View')
ax_front.view_init(elev=0, azim=-90)

# Back view
ax_back = fig.add_subplot(236, projection='3d')
ax_back.add_collection3d(Poly3DCollection(your_mesh.vectors, facecolors=cmap(normalized_heights)))
ax_back.set_xlabel('X')
ax_back.set_ylabel('Y')
ax_back.set_zlabel('Z')
ax_back.set_title('Back View')
ax_back.view_init(elev=0, azim=90)

# Create sliders for graph scale control
scale_slider = Slider(fig.add_axes([0.2, 0.05, 0.6, 0.03]), 'Scale', 0.1, 20.0, valinit=1.0)

# Function to update graph scale
def update_scale(val):
    scale = scale_slider.val
    for ax in [ax_top, ax_bottom, ax_left, ax_right, ax_front, ax_back]:
        ax.cla()  # Clear the axes
        ax.set_xlim3d(-scale, scale)
        ax.set_ylim3d(-scale, scale)
        ax.set_zlim3d(-scale, scale)
        ax.add_collection3d(Poly3DCollection(your_mesh.vectors, facecolors=cmap(normalized_heights)))
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.set_box_aspect([1, 1, 1])  # Set equal aspect ratio
    fig.canvas.draw_idle()

scale_slider.on_changed(update_scale)

# Adjust subplot spacing
plt.subplots_adjust(wspace=0.3, hspace=0.3)

# Set initial graph scale
update_scale(1.0)

# Show the plot
plt.show()
