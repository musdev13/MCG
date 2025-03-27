import tkinter as tk
from tkinter import filedialog, ttk
from PIL import Image, ImageTk
import json
import os
import shutil

class MapMaker:
    def __init__(self, root):
        self.root = root
        self.root.title("MCG Map Maker")
        
        # Variables
        self.cell_size = 48
        self.grid_width = 16
        self.grid_height = 12
        self.selected_cell = None
        self.bg_image = None
        self.bg_path = None
        self.cells = {}  # Dictionary to store cell properties
        self.current_tool = "normal"  # Default tool
        self.player_skin = "marko"  # Default skin
        self.player_spawn = None
        self.map_name = None  # Add this line to store map name
        
        self.setup_ui()
        
    def setup_ui(self):
        # Main layout
        self.tools_frame = ttk.Frame(self.root)
        self.tools_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        
        self.canvas_frame = ttk.Frame(self.root)
        self.canvas_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Canvas for map
        self.canvas = tk.Canvas(
            self.canvas_frame,
            width=self.cell_size * self.grid_width,
            height=self.cell_size * self.grid_height
        )
        self.canvas.pack()
        
        # Tools
        ttk.Label(self.tools_frame, text="Tools").pack(pady=5)
        
        # Background button
        ttk.Button(
            self.tools_frame,
            text="Select Background from Folder",
            command=self.load_background
        ).pack(fill=tk.X, pady=2)
        
        # Tool selection
        self.tool_var = tk.StringVar(value="normal")
        tools = [
            ("Normal Cell", "normal"),
            ("Collision", "collision"),
            ("Player Spawn", "spawn"),
            ("Dialog Trigger", "dialog")
        ]
        
        for text, value in tools:
            ttk.Radiobutton(
                self.tools_frame,
                text=text,
                value=value,
                variable=self.tool_var,
                command=self.update_tool
            ).pack(fill=tk.X, pady=2)
            
        # Player skin selection
        ttk.Label(self.tools_frame, text="\nPlayer Skin").pack(pady=5)
        self.skin_var = tk.StringVar(value="marko")
        skins = ["marko", "d"]
        ttk.Combobox(
            self.tools_frame,
            textvariable=self.skin_var,
            values=skins,
            state="readonly"
        ).pack(fill=tk.X, pady=2)
        
        # Save/Load buttons
        ttk.Button(
            self.tools_frame,
            text="Save Map",
            command=self.save_map
        ).pack(fill=tk.X, pady=2)
        
        ttk.Button(
            self.tools_frame,
            text="Load Map",
            command=self.load_map
        ).pack(fill=tk.X, pady=2)
        
        # Bind canvas events
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.canvas.bind("<Motion>", self.on_canvas_move)
        
        # Draw initial grid
        self.draw_grid()

        # Add map name input
        ttk.Label(self.tools_frame, text="Map Name").pack(pady=5)
        self.map_name_var = tk.StringVar()
        ttk.Entry(
            self.tools_frame,
            textvariable=self.map_name_var
        ).pack(fill=tk.X, pady=2)
        
    def draw_grid(self):
        self.canvas.delete("grid")
        
        # Draw vertical lines
        for i in range(self.grid_width + 1):
            x = i * self.cell_size
            self.canvas.create_line(
                x, 0, x, self.cell_size * self.grid_height,
                tags="grid",
                fill="gray",
                width=1
            )
        
        # Draw horizontal lines
        for i in range(self.grid_height + 1):
            y = i * self.cell_size
            self.canvas.create_line(
                0, y, self.cell_size * self.grid_width, y,
                tags="grid",
                fill="gray",
                width=1
            )
            
    def load_background(self):
        # Get map name from input
        self.map_name = self.map_name_var.get()
        if not self.map_name:
            tk.messagebox.showerror("Error", "Please enter a map name first!")
            return

        # Check if map folder exists
        map_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "img", self.map_name)
        if not os.path.exists(map_dir):
            response = tk.messagebox.askyesno(
                "Folder not found", 
                f"Folder for map '{self.map_name}' doesn't exist. Create it?"
            )
            if response:
                os.makedirs(map_dir)
            else:
                return

        # List available images in the map folder
        available_images = [f for f in os.listdir(map_dir) if f.endswith(('.png', '.jpg', '.jpeg'))]
        
        if not available_images:
            file_path = filedialog.askopenfilename(
                filetypes=[("Image files", "*.png *.jpg *.jpeg")]
            )
            if file_path:
                # Copy selected image to map folder
                shutil.copy2(file_path, os.path.join(map_dir, "bg.png"))
                self.bg_path = os.path.join(map_dir, "bg.png")
        else:
            # Create image selection dialog
            dialog = tk.Toplevel(self.root)
            dialog.title("Select Background")
            dialog.grab_set()  # Make dialog modal
            
            def select_image(image_name):
                self.bg_path = os.path.join(map_dir, image_name)
                dialog.destroy()
                self.update_background()

            for img in available_images:
                ttk.Button(
                    dialog,
                    text=img,
                    command=lambda i=img: select_image(i)
                ).pack(fill=tk.X, pady=2)

    def update_background(self):
        if self.bg_path and os.path.exists(self.bg_path):
            # Load and resize image
            original_image = Image.open(self.bg_path)
            # Ensure minimum size is 800x600
            target_width = max(800, self.cell_size * self.grid_width)
            target_height = max(600, self.cell_size * self.grid_height)
            image = original_image.resize((target_width, target_height))
            
            # Crop to exact grid size if larger
            if image.size[0] > self.cell_size * self.grid_width or image.size[1] > self.cell_size * self.grid_height:
                image = image.crop((0, 0, self.cell_size * self.grid_width, self.cell_size * self.grid_height))
            
            self.bg_image = ImageTk.PhotoImage(image)
            self.canvas.delete("all")
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.bg_image)
            self.draw_grid()
            self.redraw_cells()
            
    def update_tool(self):
        self.current_tool = self.tool_var.get()
        
    def on_canvas_click(self, event):
        x = event.x // self.cell_size
        y = event.y // self.cell_size
        if 0 <= x < self.grid_width and 0 <= y < self.grid_height:
            cell_index = y * self.grid_width + x
            
            if self.current_tool == "spawn":
                # Remove old spawn point if exists
                if self.player_spawn is not None:
                    old_index = self.player_spawn
                    self.canvas.delete(f"cell_{old_index}")
                self.player_spawn = cell_index
                self.canvas.create_rectangle(
                    x * self.cell_size, y * self.cell_size,
                    (x + 1) * self.cell_size, (y + 1) * self.cell_size,
                    fill="green", stipple="gray50",
                    tags=f"cell_{cell_index}"
                )
            else:
                self.cells[cell_index] = {
                    "type": self.current_tool,
                    "x": x,
                    "y": y
                }
                color = {
                    "normal": "",
                    "collision": "red",
                    "dialog": "blue"
                }[self.current_tool]
                
                if color:
                    self.canvas.create_rectangle(
                        x * self.cell_size, y * self.cell_size,
                        (x + 1) * self.cell_size, (y + 1) * self.cell_size,
                        fill=color, stipple="gray50",
                        tags=f"cell_{cell_index}"
                    )
                else:
                    self.canvas.delete(f"cell_{cell_index}")
                    
    def on_canvas_move(self, event):
        x = event.x // self.cell_size
        y = event.y // self.cell_size
        if 0 <= x < self.grid_width and 0 <= y < self.grid_height:
            cell_index = y * self.grid_width + x
            if cell_index != self.selected_cell:
                self.selected_cell = cell_index
                
    def save_map(self):
        if not self.bg_path:
            tk.messagebox.showerror("Error", "Please select a background image first!")
            return
            
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json")]
        )
        if file_path:
            map_data = {
                "background": os.path.basename(self.bg_path),
                "player_skin": self.skin_var.get(),
                "player_spawn": self.player_spawn,
                "cells": self.cells
            }
            
            # Create map directory if it doesn't exist
            map_name = os.path.splitext(os.path.basename(file_path))[0]
            map_dir = f"../img/{map_name}"
            os.makedirs(map_dir, exist_ok=True)
            
            # Copy background image
            shutil.copy2(self.bg_path, f"{map_dir}/bg.png")
            
            # Save map data
            with open(file_path, "w") as f:
                json.dump(map_data, f, indent=4)
                
    def load_map(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json")]
        )
        if file_path:
            with open(file_path, "r") as f:
                map_data = json.load(f)
                
            map_name = os.path.splitext(os.path.basename(file_path))[0]
            bg_path = f"../img/{map_name}/bg.png"
            
            if os.path.exists(bg_path):
                self.bg_path = bg_path
                image = Image.open(bg_path)
                image = image.resize((
                    self.cell_size * self.grid_width,
                    self.cell_size * self.grid_height
                ))
                self.bg_image = ImageTk.PhotoImage(image)
                self.canvas.create_image(0, 0, anchor=tk.NW, image=self.bg_image)
                
            self.skin_var.set(map_data["player_skin"])
            self.player_spawn = map_data["player_spawn"]
            self.cells = map_data["cells"]
            
            self.redraw_cells()
            
    def redraw_cells(self):
        self.canvas.delete("cell")
        for index, cell in self.cells.items():
            x = cell["x"]
            y = cell["y"]
            color = {
                "normal": "",
                "collision": "red",
                "dialog": "blue"
            }[cell["type"]]
            
            if color:
                self.canvas.create_rectangle(
                    x * self.cell_size, y * self.cell_size,
                    (x + 1) * self.cell_size, (y + 1) * self.cell_size,
                    fill=color, stipple="gray50",
                    tags=f"cell_{index}"
                )
                
        if self.player_spawn is not None:
            x = self.player_spawn % self.grid_width
            y = self.player_spawn // self.grid_width
            self.canvas.create_rectangle(
                x * self.cell_size, y * self.cell_size,
                (x + 1) * self.cell_size, (y + 1) * self.cell_size,
                fill="green", stipple="gray50",
                tags=f"cell_{self.player_spawn}"
            )

if __name__ == "__main__":
    root = tk.Tk()
    app = MapMaker(root)
    root.mainloop()