import tkinter as tk
from tkinter import ttk
from stl import mesh
import numpy as np
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def generate_stl_file():
    filename = filename_entry.get() + ".stl"
    shape = shape_combobox.get()
    width, height, thickness = map(
        float, (width_entry.get(), height_entry.get(), thickness_entry.get()))
    vertices, faces = create_geometry(shape, width, height, thickness)

    mesh_data = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
    mesh_data.vectors = vertices[faces]
    mesh_data.save(filename)
    print("STL file generated successfully!")


def update_preview():
    shape = shape_combobox.get()
    width, height, thickness = map(
        float, (width_entry.get(), height_entry.get(), thickness_entry.get()))
    vertices, faces = create_geometry(shape, width, height, thickness)

    ax.cla()
    ax.add_collection3d(mplot3d.art3d.Poly3DCollection(vertices[faces]))
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    canvas.draw()


def create_geometry(shape, width, height, thickness):
    if shape == "Cube":
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
    elif shape == "Pyramid":
        vertices = np.array([
            [0, 0, 0],
            [width, 0, 0],
            [width, height, 0],
            [0, height, 0],
            [width/2, height/2, thickness]
        ])

        faces = np.array([
            [0, 1, 4],
            [1, 2, 4],
            [2, 3, 4],
            [3, 0, 4],
            [0, 3, 1],
            [1, 3, 2]
        ])
    else:
        # Default to cube if shape is not recognized
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

    return vertices, faces


def create_label_entry_pair(window, label_text):
    label = tk.Label(window, text=label_text)
    label.pack()
    entry = tk.Entry(window)
    entry.pack()
    return entry


window = tk.Tk()
window.title("STL Generator")

# Create a PanedWindow widget
pane = ttk.PanedWindow(window, orient=tk.HORIZONTAL)
pane.pack(fill=tk.BOTH, expand=True)

# Create the left pane for the preview
preview_pane = ttk.Frame(pane)
pane.add(preview_pane, weight=1)

# Create the right pane for the input controls
input_pane = ttk.Frame(pane)
pane.add(input_pane, weight=1)

shape_label = tk.Label(input_pane, text="Shape:")
shape_label.pack()
shape_combobox = ttk.Combobox(input_pane, values=["Cube", "Pyramid"])
shape_combobox.pack()


width_entry = create_label_entry_pair(input_pane, "Width:")
height_entry = create_label_entry_pair(input_pane, "Height:")
thickness_entry = create_label_entry_pair(input_pane, "Thickness:")




preview_button = tk.Button(
    input_pane, text="Preview Model", command=update_preview)
preview_button.pack()

filename_entry = create_label_entry_pair(input_pane, "Filename:")

generate_button = tk.Button(
    input_pane, text="Generate STL", command=generate_stl_file)
generate_button.pack()


fig = plt.figure()
ax = plt.axes(projection='3d')

canvas = FigureCanvasTkAgg(fig, master=preview_pane)
canvas.draw()
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

window.mainloop()
