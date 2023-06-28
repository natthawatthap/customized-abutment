import tkinter as tk
from tkinter import filedialog
from stl import mesh
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class STLViewerGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("STL Viewer")

        # Create a frame for the control bar
        control_frame = tk.Frame(self.window)
        control_frame.pack(side=tk.TOP, fill=tk.X)

        self.load_button = tk.Button(control_frame, text="Load STL", command=self.load_stl_files)
        self.load_button.grid(row=0, column=0)

        self.model_index_entry = tk.Entry(control_frame)
        self.model_index_entry.grid(row=0, column=1)
        self.x_offset_entry = tk.Entry(control_frame)
        self.x_offset_entry.grid(row=1, column=1)
        self.y_offset_entry = tk.Entry(control_frame)
        self.y_offset_entry.grid(row=2, column=1)
        self.z_offset_entry = tk.Entry(control_frame)
        self.z_offset_entry.grid(row=3, column=1)


        self.adjust_button = tk.Button(control_frame, text="Adjust Position", command=self.adjust_position)
        self.adjust_button.grid(row=4, column=0, columnspan=2)
        self.reset_button = tk.Button(control_frame, text="Reset Position", command=self.reset_position)
        self.reset_button.grid(row=5, column=0, columnspan=2)

        # Create a frame for the figure
        figure_frame = tk.Frame(self.window)
        figure_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111, projection='3d')

        self.canvas = FigureCanvasTkAgg(self.fig, master=figure_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.stl_files = []

        self.window.mainloop()
    
    def load_stl_files(self):
        self.stl_files = []
        
        for i in range(2):
            filename = filedialog.askopenfilename(filetypes=[("STL files", "*.stl")])
            
            if filename:
                self.stl_files.append(mesh.Mesh.from_file(filename))
        
        self.display_models()
    
    def display_models(self):
        self.ax.cla()
        
        for stl_file in self.stl_files:
            self.ax.add_collection3d(mplot3d.art3d.Poly3DCollection(stl_file.vectors))
        
        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.ax.set_zlabel('Z')
        
        self.canvas.draw()
    
    def adjust_position(self):
        # Get the values from the entry widgets
        model_index = int(self.model_index_entry.get())
        x_offset = float(self.x_offset_entry.get())
        y_offset = float(self.y_offset_entry.get())
        z_offset = float(self.z_offset_entry.get())

        # Implement your logic to adjust the positions of the loaded STL models
        # This function will be called when the "Adjust Position" button is clicked
        
        # Example: Move the specified model along the x, y, and z axes
        if model_index < len(self.stl_files):
            stl_model = self.stl_files[model_index]
            stl_model.x = x_offset
            stl_model.y = y_offset
            stl_model.z = z_offset
            
            self.display_models()
            
    def reset_position(self):
        # Reset the positions of the loaded STL models to their original positions
        for stl_model in self.stl_files:
            stl_model.x = 0.0
            stl_model.y = 0.0
            stl_model.z = 0.0
        
        self.display_models()
# Create the STLViewerGUI object to start the application
stl_viewer = STLViewerGUI()
