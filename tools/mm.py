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
        self.dialog_groups = {}  # Dictionary to store dialog groups
        self.current_dialog_group = None
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
            width=800,  # Minimum width
            height=600,  # Minimum height
            highlightthickness=0  # Remove canvas border
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

        # Dialog group management frame
        dialog_frame = ttk.LabelFrame(self.tools_frame, text="Dialog Groups")
        dialog_frame.pack(fill=tk.X, pady=5, padx=2)

        # Create new dialog group
        ttk.Button(
            dialog_frame,
            text="New Dialog Group",
            command=self.create_dialog_group
        ).pack(fill=tk.X, pady=2)

        # Dialog group selector
        self.dialog_group_var = tk.StringVar()
        self.dialog_group_combo = ttk.Combobox(
            dialog_frame,
            textvariable=self.dialog_group_var,
            state="readonly"
        )
        self.dialog_group_combo.pack(fill=tk.X, pady=2)
        self.dialog_group_combo.bind('<<ComboboxSelected>>', self.on_dialog_group_selected)

        # Edit dialog group button
        ttk.Button(
            dialog_frame,
            text="Edit Dialog Group",
            command=self.edit_dialog_group
        ).pack(fill=tk.X, pady=2)
        
    def draw_grid(self):
        self.canvas.delete("grid")
        
        # Calculate grid offset to center it on background
        offset_x = (800 - 768) // 2  # (canvas_width - grid_width*cell_size)/2
        offset_y = (600 - 576) // 2  # (canvas_height - grid_height*cell_size)/2
        
        # Draw vertical lines
        for i in range(self.grid_width + 1):
            x = offset_x + (i * self.cell_size)
            self.canvas.create_line(
                x, offset_y,
                x, offset_y + (self.grid_height * self.cell_size),
                tags="grid",
                fill="gray",
                width=1,
                dash=(2, 2)  # Make grid more visible with dashed lines
            )
        
        # Draw horizontal lines
        for i in range(self.grid_height + 1):
            y = offset_y + (i * self.cell_size)
            self.canvas.create_line(
                offset_x, y,
                offset_x + (self.grid_width * self.cell_size), y,
                tags="grid",
                fill="gray",
                width=1,
                dash=(2, 2)  # Make grid more visible with dashed lines
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
            # Load and resize image to 800x600
            original_image = Image.open(self.bg_path)
            image = original_image.resize((800, 600))  # Fixed size for background
            
            self.bg_image = ImageTk.PhotoImage(image)
            self.canvas.delete("all")
            # Draw background centered in canvas
            self.canvas.create_image(
                (800 - 768) // 2,  # Center horizontally (800-grid_width*48)/2
                (600 - 576) // 2,  # Center vertically (600-grid_height*48)/2
                anchor=tk.NW,
                image=self.bg_image
            )
            self.draw_grid()
            self.redraw_cells()
            
    def update_tool(self):
        self.current_tool = self.tool_var.get()
        
    def on_canvas_click(self, event):
        # Adjust click coordinates for grid offset
        offset_x = (800 - 768) // 2
        offset_y = (600 - 576) // 2
        x = (event.x - offset_x) // self.cell_size
        y = (event.y - offset_y) // self.cell_size
        if 0 <= x < self.grid_width and 0 <= y < self.grid_height:
            cell_index = y * self.grid_width + x
            
            if self.current_tool == "spawn":
                # Handle spawn point
                if self.player_spawn is not None:
                    old_index = self.player_spawn
                    self.canvas.delete(f"cell_{old_index}")
                self.player_spawn = cell_index
                self.draw_cell(x, y, "green", cell_index)
                
            elif self.current_tool == "dialog":
                # Handle dialog cell
                if not self.current_dialog_group:
                    tk.messagebox.showerror("Error", "Please select a dialog group first!")
                    return
                
                # Add cell to dialog group
                if cell_index not in self.dialog_groups[self.current_dialog_group]["cells"]:
                    self.dialog_groups[self.current_dialog_group]["cells"].append(cell_index)
                    
                # Add cell to main cells dictionary
                self.cells[cell_index] = {
                    "type": "dialog",
                    "x": x,
                    "y": y,
                    "dialog_group": self.current_dialog_group
                }
                
                # Draw the cell
                self.draw_cell(x, y, "blue", cell_index)
                
            else:
                # Handle other cell types
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
                    cell_index = y * self.grid_width + x
                    self.draw_cell(x, y, color, cell_index)
                else:
                    self.canvas.delete(f"cell_{cell_index}")

    def draw_cell(self, x, y, color, cell_index):
        """Helper method to draw a cell with given color"""
        offset_x = (800 - 768) // 2
        offset_y = (600 - 576) // 2
        self.canvas.create_rectangle(
            offset_x + (x * self.cell_size),
            offset_y + (y * self.cell_size),
            offset_x + ((x + 1) * self.cell_size),
            offset_y + ((y + 1) * self.cell_size),
            fill=color, stipple="gray50",
            tags=f"cell_{cell_index}"
        )
                    
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
                "cells": self.cells,
                "dialog_groups": self.dialog_groups  # Add dialog groups to save data
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
                # Load and process background image
                original_image = Image.open(bg_path)
                # Resize to 800x600 like in update_background
                image = original_image.resize((800, 600))
                
                self.bg_image = ImageTk.PhotoImage(image)
                self.canvas.delete("all")
                
                # Draw background centered like in update_background
                self.canvas.create_image(
                    (800 - 768) // 2,  # Center horizontally
                    (600 - 576) // 2,  # Center vertically
                    anchor=tk.NW,
                    image=self.bg_image
                )
                
                # Update map data
                self.map_name_var.set(map_name)
                self.skin_var.set(map_data["player_skin"])
                self.player_spawn = map_data["player_spawn"]
                self.cells = map_data["cells"]
                self.dialog_groups = map_data.get("dialog_groups", {})
                
                # Draw grid and cells with proper offsets
                self.draw_grid()
                self.redraw_cells()
                
                # Update dialog groups in UI
                self.update_dialog_group_list()
            
    def redraw_cells(self):
        self.canvas.delete("cell")
        offset_x = (800 - 768) // 2
        offset_y = (600 - 576) // 2
        
        for index, cell in self.cells.items():
            x = cell["x"]
            y = cell["y"]
            color = {
                "normal": "",
                "collision": "red",
                "dialog": "blue"
            }[cell["type"]]
            
            if color:
                self.draw_cell(x, y, color, index)
                
        if self.player_spawn is not None:
            x = self.player_spawn % self.grid_width
            y = self.player_spawn // self.grid_width
            self.draw_cell(x, y, "green", self.player_spawn)

    def create_dialog_group(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Create Dialog Group")
        dialog.grab_set()

        ttk.Label(dialog, text="Group Name:").pack(pady=5)
        name_var = tk.StringVar()
        ttk.Entry(dialog, textvariable=name_var).pack(pady=5)

        def save():
            name = name_var.get()
            if name:
                self.dialog_groups[name] = {
                    "dialogs": [],
                    "cells": []
                }
                self.update_dialog_group_list()
                dialog.destroy()

        ttk.Button(dialog, text="Save", command=save).pack(pady=5)

    def edit_dialog_group(self):
        if not self.current_dialog_group:
            tk.messagebox.showerror("Error", "Please select a dialog group first!")
            return

        dialog = tk.Toplevel(self.root)
        dialog.title(f"Edit Dialog Group: {self.current_dialog_group}")
        dialog.grab_set()

        # Dialog list frame
        dialog_list_frame = ttk.LabelFrame(dialog, text="Dialogs")
        dialog_list_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Dialog list
        dialogs = self.dialog_groups[self.current_dialog_group]["dialogs"]
        for i, d in enumerate(dialogs):
            frame = ttk.Frame(dialog_list_frame)
            frame.pack(fill=tk.X, pady=2)
            ttk.Label(frame, text=f"Dialog {i+1}:").pack(side=tk.LEFT)
            ttk.Label(frame, text=d["text"][:30] + "...").pack(side=tk.LEFT)
            ttk.Button(
                frame, 
                text="Edit",
                command=lambda idx=i: self.edit_dialog(idx)
            ).pack(side=tk.RIGHT)

        # Add new dialog button
        ttk.Button(
            dialog,
            text="Add New Dialog",
            command=lambda: self.edit_dialog(len(dialogs))
        ).pack(fill=tk.X, pady=5)

    def edit_dialog(self, index):
        dialog = tk.Toplevel(self.root)
        dialog.title("Edit Dialog")
        dialog.grab_set()

        group = self.dialog_groups[self.current_dialog_group]
        if index < len(group["dialogs"]):
            current = group["dialogs"][index]
        else:
            current = {"text": "", "character": "", "expression": None, "choices": False, "wait": True}

        # Dialog text
        ttk.Label(dialog, text="Text:").pack(pady=5)
        text_var = tk.StringVar(value=current["text"])
        ttk.Entry(dialog, textvariable=text_var, width=50).pack(pady=5)

        # Character name
        ttk.Label(dialog, text="Character:").pack(pady=5)
        char_var = tk.StringVar(value=current["character"])
        ttk.Entry(dialog, textvariable=char_var).pack(pady=5)

        # Options
        choices_var = tk.BooleanVar(value=current["choices"])
        ttk.Checkbutton(
            dialog,
            text="Has Choices",
            variable=choices_var
        ).pack(pady=5)

        wait_var = tk.BooleanVar(value=current["wait"])
        ttk.Checkbutton(
            dialog,
            text="Wait for Input",
            variable=wait_var
        ).pack(pady=5)

        def save():
            dialog_data = {
                "text": text_var.get(),
                "character": char_var.get(),
                "expression": None,
                "choices": choices_var.get(),
                "wait": wait_var.get()
            }
            if index < len(group["dialogs"]):
                group["dialogs"][index] = dialog_data
            else:
                group["dialogs"].append(dialog_data)
            dialog.destroy()

        ttk.Button(dialog, text="Save", command=save).pack(pady=5)

    def update_dialog_group_list(self):
        groups = list(self.dialog_groups.keys())
        self.dialog_group_combo['values'] = groups

    def on_dialog_group_selected(self, event):
        self.current_dialog_group = self.dialog_group_var.get()

if __name__ == "__main__":
    root = tk.Tk()
    app = MapMaker(root)
    root.mainloop()