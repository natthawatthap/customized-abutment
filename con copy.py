import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from stl import mesh
from matplotlib.widgets import Slider, Button

# Function to load and plot an STL file
def load_and_plot_stl(file_path, ax, color, translation=None):
    # Load the STL file
    your_mesh = mesh.Mesh.from_file(file_path)
    
    # Apply translation if provided
    if translation is not None:
        your_mesh.vectors += translation
    
    # Plot the 3D model with the specified color
    ax.add_collection3d(Poly3DCollection(your_mesh.vectors, facecolors=color))
    ax.set_xlim3d(np.min(your_mesh.x), np.max(your_mesh.x))
    ax.set_ylim3d(np.min(your_mesh.y), np.max(your_mesh.y))
    ax.set_zlim3d(np.min(your_mesh.z), np.max(your_mesh.z))

# Function to generate model 3
def generate_model3():
    # Calculate the vertices for model 3
    model3_vertices = np.vstack((mesh1.vertices[mesh1.vertices[:, 2] <= 0], mesh2.vertices[mesh2.vertices[:, 2] >= 0]))
    
    # Create the mesh for model 3
    model3_mesh = mesh.Mesh(np.zeros(model3_vertices.shape[0], dtype=mesh.Mesh.dtype))
    model3_mesh.vertices = model3_vertices
    model3_mesh.save('model3.stl')
    
    # Load and plot model 3
    file3_path = 'model3.stl'
    load_and_plot_stl(file3_path, ax, 'green')

# Load and plot the first STL file (model A)
file1_path = 'model1.stl'
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
load_and_plot_stl(file1_path, ax, 'red')

# Load and plot the second STL file (model B)
file2_path = 'model2.stl'
load_and_plot_stl(file2_path, ax, 'blue')

# Set initial distance between model A and B
initial_distance = 10.0

# Calculate the offset for model B
offset = initial_distance + np.max(mesh.Mesh.from_file(file1_path).z) - np.min(mesh.Mesh.from_file(file2_path).z)

# Translation for model A (positioned at origin)
translation_A = np.array([0, 0, 0])

# Translation for model B (adjusted position)
translation_B = np.array([0, 0, offset])

# Load and plot model A
load_and_plot_stl(file1_path, ax, 'red', translation_A)

# Load and plot model B
load_and_plot_stl(file2_path, ax, 'blue', translation_B)

# Set up the slider for distance adjustment
ax_distance = plt.axes([0.2, 0.05, 0.6, 0.03])
slider_distance = Slider(ax_distance, 'Distance', -20.0, 20.0, valinit=initial_distance)

# Set up the button for generating model 3
ax_generate = plt.axes([0.8, 0.01, 0.1, 0.04])
button_generate = Button(ax_generate, 'Generate')

# Function to update the plot based on the slider value
def update_distance(val):
    distance = slider_distance.val
    
    # Calculate the offset for model B based on the distance value
    offset = distance + np.max(mesh.Mesh.from_file(file1_path).z) - np.min(mesh.Mesh.from_file(file2_path).z)
    
    # Clear the plot
    ax.cla()
    
    # Load and plot model A
    load_and_plot_stl(file1_path, ax, 'red', translation_A)
    
    # Load and plot model B with adjusted position
    translation_B_adjusted = np.array([0, 0, offset])
    load_and_plot_stl(file2_path, ax, 'blue', translation_B_adjusted)
    
    # Refresh the plot
    fig.canvas.draw_idle()

def generate_button_clicked(event):
    generate_model3()
    
slider_distance.on_changed(update_distance)
button_generate.on_clicked(generate_button_clicked)

# Show the plot
plt.show()
