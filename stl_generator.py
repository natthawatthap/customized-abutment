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
    width, height, thickness, radius = map(
        float, (width_entry.get(), height_entry.get(), thickness_entry.get(), radius_entry.get()))
    vertices, faces = create_geometry(shape, width, height, thickness, radius)

    mesh_data = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
    mesh_data.vectors = vertices[faces]
    mesh_data.save(filename)
    print("STL file generated successfully!")

# def generate_stl_file():
#     filename = filename_entry.get() + ".stl"
#     shape = shape_combobox.get()
#     width, height, thickness, radius = map(
#         float, (width_entry.get(), height_entry.get(), thickness_entry.get(), radius_entry.get()))
#     vertices, faces = create_geometry(shape, width, height, thickness, radius)

#     mesh_data = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
#     mesh_data.vectors = vertices[faces]

#     unit_comment = "  1.0000000000000000e+00  # STL file unit: mm"

#     with open(filename, 'wb') as f:
#         f.write(mesh_data.data.tobytes())
#         f.write(unit_comment.encode())

#     print("STL file generated successfully!")


def update_preview():
    shape = shape_combobox.get()
    width = float(width_entry.get() or '0')
    height = float(height_entry.get() or '0')
    thickness = float(thickness_entry.get() or '0')
    radius = float(radius_entry.get() or '0')
    vertices, faces = create_geometry(shape, width, height, thickness, radius)

    ax.cla()
    ax.add_collection3d(mplot3d.art3d.Poly3DCollection(vertices[faces]))
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    canvas.draw()


def create_geometry(shape, width, height, thickness, radius):
    if shape == "Cube":
        return create_cube(width, height, thickness)
    elif shape == "Pyramid":
        return create_pyramid(width, height, thickness)
    elif shape == "Cylindrical":
        return create_cylindrical(width, height, thickness, radius)
    elif shape == "Sphere":
        return create_sphere(radius)
    elif shape == "Cone":
        return create_cone(height, radius)
    else:
        # Default to cube if shape is not recognized
        return create_cube(width, height, thickness)


def create_cube(width, height, thickness):
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


def create_pyramid(width, height, thickness):
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

    return vertices, faces


def create_cylindrical(width, height, thickness, radius):
    # Calculate the number of points for the circular base
    num_points = 100

    # Generate the vertices for the cylindrical shape
    vertices = []
    for i in range(num_points):
        angle = 2 * np.pi * i / num_points
        x = radius * np.cos(angle)
        y = radius * np.sin(angle)
        vertices.append([x, y, 0])
        vertices.append([x, y, thickness])
    vertices.append([0, 0, 0])
    vertices.append([0, 0, thickness])

    # Generate the faces for the cylindrical shape
    faces = []
    for i in range(num_points):
        next_i = (i + 1) % num_points
        faces.append([i * 2, i * 2 + 1, next_i * 2 + 1])
        faces.append([i * 2, next_i * 2 + 1, next_i * 2])
        faces.append([i * 2, next_i * 2, i * 2 + 1])
        faces.append([i * 2 + 1, next_i * 2, next_i * 2 + 1])
    for i in range(num_points):
        faces.append([i * 2, i * 2 + 1, num_points * 2])
        faces.append([i * 2 + 1, (i + 1) * 2 %
                     (num_points * 2), num_points * 2 + 1])

    return np.array(vertices), np.array(faces)

def create_sphere(radius):
    # Calculate the number of points for the sphere
    num_points = 20

    # Generate the vertices for the sphere shape
    u = np.linspace(0, 2 * np.pi, num_points)
    v = np.linspace(0, np.pi, num_points)
    x = radius * np.outer(np.cos(u), np.sin(v))
    y = radius * np.outer(np.sin(u), np.sin(v))
    z = radius * np.outer(np.ones(np.size(u)), np.cos(v))

    # Reshape the vertex arrays into a list of vertices
    vertices = np.dstack((x, y, z)).reshape(-1, 3)

    # Generate the faces for the sphere shape
    faces = []
    for i in range(num_points - 1):
        for j in range(num_points - 1):
            faces.append([i * num_points + j, i * num_points + j + 1, (i + 1) * num_points + j + 1])
            faces.append([i * num_points + j, (i + 1) * num_points + j + 1, (i + 1) * num_points + j])

    return vertices, np.array(faces)

def create_cone(height, radius):
    # Calculate the number of points for the cone
    num_points = 100

    # Generate the vertices for the cone shape
    vertices = []
    for i in range(num_points):
        angle = 2 * np.pi * i / num_points
        x = radius * np.cos(angle)
        y = radius * np.sin(angle)
        vertices.append([x, y, 0])  # Base vertices
        vertices.append([0, 0, height])  # Apex vertex
    vertices.append([0, 0, 0])  # Base center vertex

    # Generate the faces for the cone shape
    faces = []
    base_center_idx = len(vertices) - 1
    for i in range(num_points):
        next_i = (i + 1) % num_points
        base_vertex_idx = i * 2
        apex_vertex_idx = i * 2 + 1
        next_base_vertex_idx = next_i * 2

        # Base triangles
        faces.append([base_vertex_idx, next_base_vertex_idx, base_center_idx])

        # Cone side triangles
        faces.append([apex_vertex_idx, base_vertex_idx, apex_vertex_idx + 1])

    return np.array(vertices), np.array(faces)

def create_label_entry_pair(window, label_text,default_value):
    label = tk.Label(window, text=label_text)
    label.pack()
    entry = tk.Entry(window)
    entry.insert(tk.END, default_value)  # Set the default value
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
shape_combobox = ttk.Combobox(
    input_pane, values=["Cube", "Pyramid", "Cylindrical", "Sphere", "Cone"])
shape_combobox.set("Cube") 
shape_combobox.pack()

width_entry = create_label_entry_pair(input_pane, "Width:", "0.3")
height_entry = create_label_entry_pair(input_pane, "Height:", "0.3")
thickness_entry = create_label_entry_pair(input_pane, "Thickness:", "0.3")
radius_entry = create_label_entry_pair(input_pane, "Radius:", "0.3")


preview_button = tk.Button(
    input_pane, text="Preview Model", command=update_preview)
preview_button.pack()

filename_entry = create_label_entry_pair(input_pane, "Filename:", "model")

generate_button = tk.Button(
    input_pane, text="Generate STL", command=generate_stl_file)
generate_button.pack()


fig = plt.figure()
ax = plt.axes(projection='3d')

canvas = FigureCanvasTkAgg(fig, master=preview_pane)
canvas.draw()
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

window.mainloop()
