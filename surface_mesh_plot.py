import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from stl import mesh
from matplotlib.widgets import Slider
from matplotlib import cm

# Load the STL file
your_mesh = mesh.Mesh.from_file('models/model2.stl')

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

# Create subplots for each plane
fig = plt.figure(figsize=(16, 8))

# XY plane
ax_xy = fig.add_subplot(231, projection='3d')
ax_xy.add_collection3d(Poly3DCollection(your_mesh.vectors, facecolors=cmap(normalized_heights)))
ax_xy.set_xlabel('X')
ax_xy.set_ylabel('Y')
ax_xy.set_zlabel('Z')
ax_xy.set_title('XY Plane')

# YZ plane
ax_yz = fig.add_subplot(232, projection='3d')
ax_yz.add_collection3d(Poly3DCollection(your_mesh.vectors, facecolors=cmap(normalized_heights)))
ax_yz.set_xlabel('Y')
ax_yz.set_ylabel('Z')
ax_yz.set_zlabel('X')
ax_yz.set_title('YZ Plane')

# XZ plane
ax_xz = fig.add_subplot(233, projection='3d')
ax_xz.add_collection3d(Poly3DCollection(your_mesh.vectors, facecolors=cmap(normalized_heights)))
ax_xz.set_xlabel('X')
ax_xz.set_ylabel('Z')
ax_xz.set_zlabel('Y')
ax_xz.set_title('XZ Plane')

# Upper plane
ax_upper = fig.add_subplot(234, projection='3d')
ax_upper.add_collection3d(Poly3DCollection(your_mesh.vectors, facecolors=cmap(normalized_heights)))
ax_upper.set_xlabel('X')
ax_upper.set_ylabel('Y')
ax_upper.set_zlabel('Z')
ax_upper.set_title('Upper Plane')
ax_upper.view_init(elev=90, azim=-90)  # Adjust view angle

# Lower plane
ax_lower = fig.add_subplot(235, projection='3d')
ax_lower.add_collection3d(Poly3DCollection(your_mesh.vectors, facecolors=cmap(normalized_heights)))
ax_lower.set_xlabel('X')
ax_lower.set_ylabel('Y')
ax_lower.set_zlabel('Z')
ax_lower.set_title('Lower Plane')
ax_lower.view_init(elev=-90, azim=-90)  # Adjust view angle

# Create sliders for graph scale control
scale_slider = Slider(fig.add_axes([0.2, 0.1, 0.6, 0.03]), 'Scale', 0.1, 20.0, valinit=1.0)

# Function to update graph scale
def update_scale(val):
    scale = scale_slider.val
    for ax in [ax_xy, ax_yz, ax_xz, ax_upper, ax_lower]:
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
