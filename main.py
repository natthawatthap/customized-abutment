import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
from stl import mesh
import tkinter as tk
from tkinter import filedialog

# Function to handle button click event
def load_stl_files():
    # Open file dialog to select the STL files
    stl_file_paths = filedialog.askopenfilenames(filetypes=[("STL Files", "*.stl")])

    # Create a new figure and axes
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    for stl_file_path in stl_file_paths:
        # Load the STL file
        mesh_data = mesh.Mesh.from_file(stl_file_path)

        # Plot the surface
        ax.add_collection3d(mplot3d.art3d.Poly3DCollection(mesh_data.vectors))

        # Set the aspect ratio of the plot
        scale = mesh_data.points.flatten()
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

# Create the main window
root = tk.Tk()

# Create a button to load STL files
load_button = tk.Button(root, text="Load STL Files", command=load_stl_files)
load_button.pack()

# Start the main event loop
root.mainloop()
