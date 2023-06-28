import tkinter as tk
from stl import mesh
import numpy as np
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Function to generate the STL file
def generate_stl_file():
    # Retrieve the input values
    filename = filename_entry.get()
    filename += ".stl"
    width = float(width_entry.get())
    height = float(height_entry.get())
    thickness = float(thickness_entry.get())

    # Create vertices and faces
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
    print("STL file generated successfully!")

# Function to update the model preview
def update_preview():
    # Retrieve the input values
    width = float(width_entry.get())
    height = float(height_entry.get())
    thickness = float(thickness_entry.get())

    # Clear the previous plot
    ax.cla()

    # Create vertices and faces
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

    # Plot the updated model
    ax.add_collection3d(mplot3d.art3d.Poly3DCollection(vertices[faces]))
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    # Update the canvas
    canvas.draw()

# Create the main window
window = tk.Tk()
window.title("STL Generator")

# Create input fields
filename_label = tk.Label(window, text="Filename:")
filename_label.pack()
filename_entry = tk.Entry(window)
filename_entry.pack()

width_label = tk.Label(window, text="Width:")
width_label.pack()
width_entry = tk.Entry(window)
width_entry.pack()

height_label = tk.Label(window, text="Height:")
height_label.pack()
height_entry = tk.Entry(window)
height_entry.pack()

thickness_label = tk.Label(window, text="Thickness:")
thickness_label.pack()
thickness_entry = tk.Entry(window)
thickness_entry.pack()

# Create buttons
generate_button = tk.Button(window, text="Generate STL", command=generate_stl_file)
generate_button.pack()

preview_button = tk.Button(window, text="Preview Model", command=update_preview)
preview_button.pack()

# Create the 3D plot
fig = plt.figure()
ax = plt.axes(projection='3d')

# Create the canvas to display the plot
canvas = FigureCanvasTkAgg(fig, master=window)
canvas.draw()
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

# Run the GUI event loop
window.mainloop()
