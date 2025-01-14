import numpy as np
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
from stl import mesh

# Function to reset the position of the 3D model to the origin (0, 0, 0)
def reset_position(event):
    model.set_verts(original_vertices)
    slider_x.set_val(0)
    slider_y.set_val(0)
    slider_z.set_val(0)
    fig.canvas.draw_idle()

# Function to load and display the STL file
def load_stl_file(filename):
    your_mesh = mesh.Mesh.from_file(filename)
    print(your_mesh)

    # Extract vertex coordinates from the mesh
    vertices = your_mesh.vectors.reshape(-1, 3)
    original_vertices = np.copy(vertices)  # Store the original vertices

    # Create the 3D plot
    fig = plt.figure()
    ax = plt.axes(projection='3d')

    # Plot the STL file
    model = mplot3d.art3d.Poly3DCollection(your_mesh.vectors)
    ax.add_collection3d(model)

    # Set the initial position and limits of the plot
    ax.set_xlim3d(-1, 1)
    ax.set_ylim3d(-1, 1)
    ax.set_zlim3d(-1, 1)

    # Create sliders for adjusting the position
    slider_x = Slider(plt.axes([0.25, 0.1, 0.65, 0.03]), 'X', -1.0, 1.0, valinit=0)
    slider_y = Slider(plt.axes([0.25, 0.05, 0.65, 0.03]), 'Y', -1.0, 1.0, valinit=0)
    slider_z = Slider(plt.axes([0.25, 0.0, 0.65, 0.03]), 'Z', -1.0, 1.0, valinit=0)

    # Update the position of the model when sliders are changed
    def update(val):
        x = slider_x.val
        y = slider_y.val
        z = slider_z.val
        model.set_verts(original_vertices + np.array([x, y, z]))
        fig.canvas.draw_idle()

    slider_x.on_changed(update)
    slider_y.on_changed(update)
    slider_z.on_changed(update)

    # Create a reset button
    reset_button_ax = plt.axes([0.8, 0.9, 0.1, 0.05])
    reset_button = Button(reset_button_ax, 'Reset', color='lightgray', hovercolor='0.975')
    reset_button.on_clicked(reset_position)

    # Display the 3D plot
    plt.show()

# Load and display the STL file generated by generate_stl_file()
filename = "model1.stl"
load_stl_file(filename)