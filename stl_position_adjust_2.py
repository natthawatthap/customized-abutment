import numpy as np
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
from stl import mesh

# Function to reset the positions of the models to the origin (0, 0, 0)
def reset_positions(event):
    for model, original_verts in zip(models, original_vertices):
        model.set_verts(original_verts)
    slider_x1.set_val(0)
    slider_y1.set_val(0)
    slider_z1.set_val(0)
    slider_x2.set_val(0)
    slider_y2.set_val(0)
    slider_z2.set_val(0)
    fig.canvas.draw_idle()

# Function to load and display the STL files
def load_stl_files(filenames):
    fig = plt.figure(figsize=(10, 8))
    ax = plt.axes(projection='3d')

    models = []
    original_vertices = []
    for filename in filenames:
        your_mesh = mesh.Mesh.from_file(filename)
        print(your_mesh)

        # Extract vertex coordinates from the mesh
        vertices = your_mesh.vectors.reshape(-1, 3)
        original_verts = np.copy(vertices)  # Store the original vertices

        # Plot the STL file
        model = mplot3d.art3d.Poly3DCollection(your_mesh.vectors)
        ax.add_collection3d(model)

        models.append(model)
        original_vertices.append(original_verts)

    # Set the initial position and limits of the plot
    ax.set_xlim3d(-1, 1)
    ax.set_ylim3d(-1, 1)
    ax.set_zlim3d(-1, 1)

    # Create sliders for adjusting the positions of model1
    slider_x1 = Slider(plt.axes([0.25, 0.1, 0.65, 0.03]), 'X1', -1.0, 1.0, valinit=0)
    slider_y1 = Slider(plt.axes([0.25, 0.06, 0.65, 0.03]), 'Y1', -1.0, 1.0, valinit=0)
    slider_z1 = Slider(plt.axes([0.25, 0.02, 0.65, 0.03]), 'Z1', -1.0, 1.0, valinit=0)

    # Create sliders for adjusting the positions of model2
    slider_x2 = Slider(plt.axes([0.25, 0.28, 0.65, 0.03]), 'X2', -1.0, 1.0, valinit=0)
    slider_y2 = Slider(plt.axes([0.25, 0.24, 0.65, 0.03]), 'Y2', -1.0, 1.0, valinit=0)
    slider_z2 = Slider(plt.axes([0.25, 0.2, 0.65, 0.03]), 'Z2', -1.0, 1.0, valinit=0)


    # Update the positions of the models when sliders are changed
    def update(val):
        x1 = slider_x1.val
        y1 = slider_y1.val
        z1 = slider_z1.val
        x2 = slider_x2.val
        y2 = slider_y2.val
        z2 = slider_z2.val

        models[0].set_verts(original_vertices[0] + np.array([x1, y1, z1]))
        models[1].set_verts(original_vertices[1] + np.array([x2, y2, z2]))
        fig.canvas.draw_idle()

    slider_x1.on_changed(update)
    slider_y1.on_changed(update)
    slider_z1.on_changed(update)
    slider_x2.on_changed(update)
    slider_y2.on_changed(update)
    slider_z2.on_changed(update)

    # Create a reset button
    reset_button_ax = plt.axes([0.8, 0.9, 0.1, 0.05])
    reset_button = Button(reset_button_ax, 'Reset', color='lightgray', hovercolor='0.975')
    reset_button.on_clicked(reset_positions)

    # Display the 3D plot
    plt.show()

# Load and display the STL files
filenames = ["model1.stl", "model2.stl"]
load_stl_files(filenames)
