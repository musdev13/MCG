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
        self.script_groups = {}  # Dictionary to store script groups
        self.current_script_group = None
        self.backgrounds = []  # List to store background layers
        self.player_layer = 0  # Default player layer
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
            ("Dialog Trigger", "dialog"),
            ("Script Trigger", "script")  # Add new tool type
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
        self.skin_var = tk.StringVar(value="marko")  # Default value
        
        # Get available skins from player folder
        player_skins = self.get_available_skins()
        
        skin_combo = ttk.Combobox(
            self.tools_frame,
            textvariable=self.skin_var,
            values=player_skins,
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
        
        # Add compile button after save/load buttons
        ttk.Button(
            self.tools_frame,
            text="Compile to .py",
            command=self.compile_to_py
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

        # Add startup script frame
        script_frame = ttk.LabelFrame(self.tools_frame, text="Startup Script")
        script_frame.pack(fill=tk.X, pady=5, padx=2)

        # Script text area
        self.script_text = tk.Text(script_frame, height=6, width=30)
        self.script_text.pack(fill=tk.X, pady=2)

        # Add script commands help button
        ttk.Button(
            script_frame,
            text="Show Commands Help",
            command=self.show_script_help
        ).pack(fill=tk.X, pady=2)

        # After dialog group frame, add script group frame
        script_group_frame = ttk.LabelFrame(self.tools_frame, text="Script Groups")
        script_group_frame.pack(fill=tk.X, pady=5, padx=2)

        # Create new script group
        ttk.Button(
            script_group_frame,
            text="New Script Group",
            command=self.create_script_group
        ).pack(fill=tk.X, pady=2)

        # Script group selector
        self.script_group_var = tk.StringVar()
        self.script_group_combo = ttk.Combobox(
            script_group_frame,
            textvariable=self.script_group_var,
            state="readonly"
        )
        self.script_group_combo.pack(fill=tk.X, pady=2)
        self.script_group_combo.bind('<<ComboboxSelected>>', self.on_script_group_selected)

        # Edit script group button
        ttk.Button(
            script_group_frame,
            text="Edit Script Group",
            command=self.edit_script_group
        ).pack(fill=tk.X, pady=2)

        # Add background layers frame
        layers_frame = ttk.LabelFrame(self.tools_frame, text="Background Layers")
        layers_frame.pack(fill=tk.X, pady=5, padx=2)
        
        # Add layer buttons
        ttk.Button(
            layers_frame,
            text="Add Layer",
            command=self.add_background_layer
        ).pack(fill=tk.X, pady=2)

        # Layer list
        self.layers_listbox = tk.Listbox(layers_frame, height=5)
        self.layers_listbox.pack(fill=tk.X, pady=2)
        
        # Layer controls
        layer_controls = ttk.Frame(layers_frame)
        layer_controls.pack(fill=tk.X)
        
        ttk.Button(
            layer_controls,
            text="Move Up",
            command=lambda: self.move_layer(-1)
        ).pack(side=tk.LEFT, padx=2)
        
        ttk.Button(
            layer_controls,
            text="Move Down",
            command=lambda: self.move_layer(1)
        ).pack(side=tk.LEFT, padx=2)
        
        ttk.Button(
            layer_controls,
            text="Delete",
            command=self.delete_layer
        ).pack(side=tk.LEFT, padx=2)
        
        # Player layer selector
        ttk.Label(layers_frame, text="Player Layer:").pack(pady=2)
        self.player_layer_var = tk.StringVar(value="0")
        self.player_layer_spin = ttk.Spinbox(
            layers_frame,
            from_=0,
            to=0,
            textvariable=self.player_layer_var,
            command=self.update_player_layer
        )
        self.player_layer_spin.pack(fill=tk.X, pady=2)
        
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
            image = original_image.resize((800, 600))
            
            self.bg_image = ImageTk.PhotoImage(image)
            self.canvas.delete("all")
            
            # If this is the first background, add it as first layer
            filename = os.path.basename(self.bg_path)
            if not self.backgrounds:
                self.backgrounds = [{
                    "path": filename,
                    "image": self.bg_image
                }]
                self.layers_listbox.delete(0, tk.END)  # Clear listbox
                self.layers_listbox.insert(tk.END, "Layer 0")
                self.player_layer_spin.config(to=0)
                
            # Draw all backgrounds in order
            self.redraw_canvas()

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
                
            elif self.current_tool == "script":
                if not self.current_script_group:
                    tk.messagebox.showerror("Error", "Please select a script group first!")
                    return
                
                # Add cell to script group
                if cell_index not in self.script_groups[self.current_script_group]["cells"]:
                    self.script_groups[self.current_script_group]["cells"].append(cell_index)
                    
                # Add cell to main cells dictionary
                self.cells[cell_index] = {
                    "type": "script",
                    "x": x,
                    "y": y,
                    "script_group": self.current_script_group
                }
                
                # Draw the cell
                self.draw_cell(x, y, "purple", cell_index)
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
            try:
                map_data = {
                    "backgrounds": [bg["path"] for bg in self.backgrounds],
                    "player_layer": self.player_layer,
                    "player_skin": self.skin_var.get(),
                    "player_spawn": self.player_spawn,
                    "cells": self.cells,
                    "dialog_groups": self.dialog_groups,
                    "startup_script": self.script_text.get("1.0", tk.END).strip(),
                    "script_groups": self.script_groups
                }
                
                # Create map directory if it doesn't exist
                map_name = os.path.splitext(os.path.basename(file_path))[0]
                map_dir = f"../img/{map_name}"
                os.makedirs(map_dir, exist_ok=True)
                
                # Handle background image copy
                try:
                    # First try to copy directly
                    shutil.copy2(self.bg_path, f"{map_dir}/bg.png")
                except PermissionError:
                    # If direct copy fails, try to create a new copy
                    with Image.open(self.bg_path) as img:
                        img.save(f"{map_dir}/bg.png")
                
                # Save map data
                with open(file_path, "w") as f:
                    json.dump(map_data, f, indent=4)
                    
                tk.messagebox.showinfo("Success", "Map saved successfully!")
                
            except Exception as e:
                tk.messagebox.showerror("Error", f"Failed to save map: {str(e)}")
                
    def load_map(self):
        try:
            file_path = filedialog.askopenfilename(
                filetypes=[("JSON files", "*.json")]
            )
            if not file_path:
                return
                
            with open(file_path, "r") as f:
                map_data = json.load(f)
            
            map_name = os.path.splitext(os.path.basename(file_path))[0]
            self.map_name_var.set(map_name)
            
            # Clear existing backgrounds
            self.backgrounds = []
            self.layers_listbox.delete(0, tk.END)
            
            # Handle old format with single background
            if "background" in map_data:
                bg_path = f"../img/{map_name}/{map_data['background']}"
                if os.path.exists(bg_path):
                    image = Image.open(bg_path)
                    image = image.resize((800, 600))
                    photo = ImageTk.PhotoImage(image)
                    self.backgrounds.append({
                        "path": map_data["background"],
                        "image": photo
                    })
                    self.layers_listbox.insert(tk.END, "Layer 0")
                    self.player_layer = 0
                    self.player_layer_var.set("0")
                    self.bg_path = bg_path
                    self.bg_image = photo
            
            # Handle new format with multiple backgrounds
            elif "backgrounds" in map_data:
                for i, bg_path in enumerate(map_data["backgrounds"]):
                    full_path = f"../img/{map_name}/{bg_path}"
                    if os.path.exists(full_path):
                        image = Image.open(full_path)
                        image = image.resize((800, 600))
                        photo = ImageTk.PhotoImage(image)
                        self.backgrounds.append({
                            "path": bg_path,
                            "image": photo
                        })
                        self.layers_listbox.insert(tk.END, f"Layer {i}")
                
                self.player_layer = map_data.get("player_layer", 0)
                self.player_layer_var.set(str(self.player_layer))
                if self.backgrounds:
                    self.bg_path = f"../img/{map_name}/{self.backgrounds[0]['path']}"
                    self.bg_image = self.backgrounds[0]['image']

            self.player_layer_spin.config(to=len(self.backgrounds)-1)
            
            # Load other map data
            self.skin_var.set(map_data["player_skin"])
            self.player_spawn = map_data["player_spawn"]
            self.cells = map_data["cells"]
            self.dialog_groups = map_data.get("dialog_groups", {})
            self.script_groups = map_data.get("script_groups", {})
            
            if "startup_script" in map_data:
                self.script_text.delete("1.0", tk.END)
                self.script_text.insert("1.0", map_data["startup_script"])
            
            self.redraw_canvas()
            self.update_dialog_group_list()
            self.update_script_group_list()
                    
        except Exception as e:
            tk.messagebox.showerror("Error", f"Failed to load map: {str(e)}")
            
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
                "dialog": "blue",
                "script": "purple"  # Add script type with purple color
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

        # Add rename and delete buttons at the top
        control_frame = ttk.Frame(dialog)
        control_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(
            control_frame,
            text="Rename Group",
            command=lambda: self.rename_dialog_group(dialog)
        ).pack(side=tk.LEFT, padx=2)
        
        ttk.Button(
            control_frame,
            text="Delete Group",
            command=lambda: self.delete_dialog_group(dialog)
        ).pack(side=tk.LEFT, padx=2)

        # Dialog list frame
        dialog_list_frame = ttk.LabelFrame(dialog, text="Dialogs")
        dialog_list_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        def refresh_dialog_list():
            # Clear existing widgets
            for widget in dialog_list_frame.winfo_children():
                widget.destroy()
                
            # Redraw dialog list
            dialogs = self.dialog_groups[self.current_dialog_group]["dialogs"]
            for i, d in enumerate(dialogs):
                frame = ttk.Frame(dialog_list_frame)
                frame.pack(fill=tk.X, pady=2)
                ttk.Label(frame, text=f"Dialog {i+1}:").pack(side=tk.LEFT)
                ttk.Label(frame, text=d["text"][:30] + "...").pack(side=tk.LEFT)
                
                button_frame = ttk.Frame(frame)
                button_frame.pack(side=tk.RIGHT)
                
                ttk.Button(
                    button_frame,
                    text="Edit",
                    command=lambda idx=i: self.edit_dialog(idx, refresh_dialog_list)
                ).pack(side=tk.LEFT, padx=2)
                
                ttk.Button(
                    button_frame,
                    text="Delete",
                    command=lambda idx=i: self.delete_dialog(idx, refresh_dialog_list)
                ).pack(side=tk.LEFT, padx=2)

        refresh_dialog_list()

        # Add new dialog button
        ttk.Button(
            dialog,
            text="Add New Dialog",
            command=lambda: self.edit_dialog(len(self.dialog_groups[self.current_dialog_group]["dialogs"]), refresh_dialog_list)
        ).pack(fill=tk.X, pady=5)

    def rename_dialog_group(self, parent_dialog):
        dialog = tk.Toplevel(parent_dialog)
        dialog.title("Rename Dialog Group")
        dialog.grab_set()

        ttk.Label(dialog, text="New Name:").pack(pady=5)
        name_var = tk.StringVar(value=self.current_dialog_group)
        ttk.Entry(dialog, textvariable=name_var).pack(pady=5)

        def save():
            new_name = name_var.get()
            if new_name and new_name != self.current_dialog_group:
                # Copy group data to new name
                self.dialog_groups[new_name] = self.dialog_groups[self.current_dialog_group]
                # Delete old group
                del self.dialog_groups[self.current_dialog_group]
                # Update current group
                self.current_dialog_group = new_name
                # Update UI
                self.update_dialog_group_list()
                self.dialog_group_var.set(new_name)
                # Close both dialogs
                dialog.destroy()
                parent_dialog.destroy()
                # Reopen edit dialog with new name
                self.edit_dialog_group()

        ttk.Button(dialog, text="Save", command=save).pack(pady=5)

    def delete_dialog_group(self, parent_dialog):
        if tk.messagebox.askyesno("Confirm Delete", f"Delete dialog group '{self.current_dialog_group}'?"):
            # Remove all cells associated with this group
            cells_to_remove = []
            for index, cell in self.cells.items():
                if cell.get("type") == "dialog" and cell.get("dialog_group") == self.current_dialog_group:
                    cells_to_remove.append(index)
            
            for index in cells_to_remove:
                del self.cells[index]
                self.canvas.delete(f"cell_{index}")
            
            # Delete the group
            del self.dialog_groups[self.current_dialog_group]
            self.current_dialog_group = None
            self.dialog_group_var.set("")
            self.update_dialog_group_list()
            parent_dialog.destroy()

    def delete_dialog(self, index, refresh_callback):
        if tk.messagebox.askyesno("Confirm Delete", "Delete this dialog?"):
            del self.dialog_groups[self.current_dialog_group]["dialogs"][index]
            refresh_callback()

    def edit_dialog(self, index, refresh_callback=None):
        dialog = tk.Toplevel(self.root)
        dialog.title("Edit Dialog")
        dialog.grab_set()

        group = self.dialog_groups[self.current_dialog_group]
        if index < len(group["dialogs"]):
            current = group["dialogs"][index]
        else:
            current = {"text": "", "character": "", "expression": None, "wait": True}

        # Dialog text
        ttk.Label(dialog, text="Text:").pack(pady=5)
        text_var = tk.StringVar(value=current["text"])
        ttk.Entry(dialog, textvariable=text_var, width=50).pack(pady=5)

        # Character name
        ttk.Label(dialog, text="Character:").pack(pady=5)
        char_var = tk.StringVar(value=current["character"])
        ttk.Entry(dialog, textvariable=char_var).pack(pady=5)

        # Wait for input option
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
                "wait": wait_var.get()
            }
            if index < len(group["dialogs"]):
                group["dialogs"][index] = dialog_data
            else:
                group["dialogs"].append(dialog_data)
            dialog.destroy()
            if refresh_callback:
                refresh_callback()

        ttk.Button(dialog, text="Save", command=save).pack(pady=5)

    def update_dialog_group_list(self):
        groups = list(self.dialog_groups.keys())
        self.dialog_group_combo['values'] = groups

    def on_dialog_group_selected(self, event):
        self.current_dialog_group = self.dialog_group_var.get()

    def compile_to_py(self):
        map_name = self.map_name_var.get()
        if not map_name:
            tk.messagebox.showerror("Error", "Please enter a map name first!")
            return
            
        template = f'''# filepath: {{gamePath}}/maps/{map_name}.py
import pygame
import time
from settings import gamePath, Level
from debugGrid import debugGrid as dG
from Player import Player
from dialog import Dialog

class {map_name}:
    def __init__(self, screen, gamePath=gamePath):
        self.screen = screen
        self.running = True
        self.grid_size = 48
        self.grid = []
        self.cutscene_active = False
        self.is_fading = False
        self.fade_screen = None

        # Create grid
        for y in range(12):
            row = []
            for x in range(16):
                row.append((x * self.grid_size, y * self.grid_size))
            self.grid.append(row)

        self.backgrounds = []
        # Load background layers
        {self.generate_background_loading()}

        # Initialize player one cell above spawn point
        start_position = {self.player_spawn}
        spawn_y = start_position // 16 - 1  # Subtract 1 to move up one cell
        spawn_x = start_position % 16
        self.player = Player(
            self.grid[spawn_y][spawn_x][0],
            self.grid[spawn_y][spawn_x][1],
            0,
            "{self.skin_var.get()}"
        )
        self.player_layer = {self.player_layer}

        # Add collision blocks
        self.collisionBlocks = {self.get_collision_blocks()}

        # Initialize dialogs
{self.generate_dialog_initialization()}

        # Run startup script
{self.parse_script()}

{self.parse_script_method()}

    def draw(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_z:
                        player_grid_index = self.get_player_grid_index()
{self.generate_dialog_triggers()}
{self.generate_script_triggers()}
{self.generate_dialog_next_checks()}

            # Draw backgrounds up to player layer
            for i in range(self.player_layer + 1):
                self.screen.blit(self.backgrounds[i], (0, 0))
            
            dG.draw(False, self.screen)
            
            self.player.is_moving = not (self.is_any_dialog_active() or self.cutscene_active)
            
            if not self.cutscene_active and not self.is_any_dialog_active():
                self.player.move(self)
            
            self.player.draw(self.screen)

            # Draw remaining backgrounds
            for i in range(self.player_layer + 1, len(self.backgrounds)):
                self.screen.blit(self.backgrounds[i], (0, 0))

{self.generate_dialog_drawing()}

            pygame.display.flip()
            #pygame.time.Clock().tick(60)

    def get_player_grid_index(self):
        player_feet_x = self.player.x + self.player.sprite_width // 2
        player_feet_y = self.player.y + self.player.sprite_height
        
        grid_x = player_feet_x // self.grid_size
        grid_y = player_feet_y // self.grid_size
        
        index = grid_y * 16 + grid_x
        return index if 0 <= grid_x < 16 and 0 <= grid_y < 12 else None

    def is_any_dialog_active(self):
        return any([
            {self.generate_dialog_checks()}
        ])
'''
        try:
            with open(f"../maps/{map_name}.py", "w", encoding='utf-8') as f:
                f.write(template)
            tk.messagebox.showinfo("Success", f"Map compiled to {map_name}.py")
        except Exception as e:
            tk.messagebox.showerror("Error", f"Failed to compile map: {str(e)}")

    def get_collision_blocks(self):
        collision_cells = [str(index) for index, cell in self.cells.items() 
                          if cell["type"] == "collision"]
        return f"[{', '.join(collision_cells)}]"

    def generate_dialog_initialization(self):
        init_code = []
        for group_name, group_data in self.dialog_groups.items():
            dialog_data = []
            for dialog in group_data["dialogs"]:
                dialog_data.append([
                    dialog["text"],
                    dialog["character"] if dialog["character"] else "None",
                    "None",  # expression
                    "False",  # show_avatar
                    "True" if dialog["character"] else "False"  # show_name
                ])
            init_code.append(f'        self.{group_name} = Dialog(screen, {dialog_data}, self.player)')
        return "\n".join(init_code)

    def generate_dialog_drawing(self):
        draw_code = []
        for group_name in self.dialog_groups.keys():
            draw_code.append(f'            if self.{group_name}.is_active:\n                self.{group_name}.draw()')
        return "\n".join(draw_code)

    def generate_dialog_triggers(self):
        triggers = []
        for group_name, group_data in self.dialog_groups.items():
            if group_data["cells"]:
                cells_str = str(group_data["cells"])
                triggers.append(f'                        if player_grid_index in {cells_str} and not self.{group_name}.is_active:\n                            self.{group_name}.start_dialog()')
        return "\n".join(triggers)

    def generate_dialog_next_checks(self):
        next_checks = []
        for group_name in self.dialog_groups.keys():
            next_checks.append(f'''                        elif self.{group_name}.is_active:
                            if self.{group_name}.dialog_ended:
                                self.{group_name}.current_index = 0
                                self.{group_name}.dialog_ended = False
                                self.{group_name}.is_active = False
                                self.{group_name}.current_text = ""
                                self.{group_name}.display_text = ""
                                self.{group_name}.text_counter = 0
                                self.{group_name}.is_text_complete = False
                            else:
                                self.{group_name}.next()''')
        return "\n".join(next_checks)

    def generate_dialog_checks(self):
        """Generate code to check if any dialog is active"""
        checks = []
        for group_name in self.dialog_groups.keys():
            checks.append(f'hasattr(self, "{group_name}") and self.{group_name}.is_active')
        return " or\n            ".join(checks) if checks else "False"

    def show_script_help(self):
        help_text = """Available Commands:
        
fadeIn(duration) - Fade in from black screen
fadeOut(duration) - Fade out to black screen
wait(seconds) - Wait specified seconds
dialog(groupName) - Start dialog from group
playerCantMove() - Disable player movement
playerCanMove() - Enable player movement
changeSprite(path) - Change player sprite (e.g. "player/d/idle_l")
resetSprite() - Reset player sprite to default animation set

Example:
playerCantMove();
fadeIn(3);
wait(2);
dialog("intro");
changeSprite("player/d/idle_l");
wait(1);
resetSprite();
playerCanMove();"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Script Commands Help")
        dialog.grab_set()
        
        text = tk.Text(dialog, height=12, width=50)
        text.pack(padx=5, pady=5)
        text.insert("1.0", help_text)
        text.config(state="disabled")

    def parse_script(self):
        """Parse script into executable Python code"""
        script = self.script_text.get("1.0", tk.END).strip()
        if not script:
            return ""
            
        # Split by newlines and semicolons
        lines = []
        for line in script.split("\n"):
            # Split line by semicolons and strip whitespace
            commands = [cmd.strip() for cmd in line.split(";") if cmd.strip()]
            lines.extend(commands)
        
        parsed_lines = []
        parsed_lines.append("        # Initialize fade surfaces")
        parsed_lines.append("        self.black_surface = pygame.Surface((800, 600))")
        parsed_lines.append("        self.black_surface.fill((0, 0, 0))")
        
        # Создаем шаблон для отрисовки слоев
        layer_drawing = """        # Draw backgrounds up to player layer
        for i in range(self.player_layer + 1):
            self.screen.blit(self.backgrounds[i], (0, 0))
        self.player.draw(self.screen)
        for i in range(self.player_layer + 1, len(self.backgrounds)):
            self.screen.blit(self.backgrounds[i], (0, 0))"""
    
        for line in lines:
            # Remove trailing semicolon if present
            line = line.rstrip(";")
            if line:
                if line.startswith("dialog("):
                    group = line[7:-1].strip('"\'')
                    parsed_lines.append(f"""        self.{group}.start_dialog()
        while self.{group}.is_active:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_z:
                        self.{group}.next()
{layer_drawing}
            if self.{group}.is_active:
                self.{group}.draw()
            pygame.display.flip()""")
                elif line.startswith("wait("):
                    seconds = line[5:-1]
                    parsed_lines.append(f"""        start_time = time.time()
        while time.time() - start_time < {seconds}:
{layer_drawing}
            pygame.display.flip()
            for event in pygame.event.get(): pass""")
                elif line.startswith("fadeIn("):
                    duration = line[7:-1]
                    parsed_lines.append(f"""        start_time = time.time()
        fade_duration = {duration}
        while True:
            current_time = time.time() - start_time
            if current_time >= fade_duration:
                break
            fade_alpha = max(0, 255 * (1 - current_time / fade_duration))
            fade_surface = self.black_surface.copy()
            fade_surface.set_alpha(int(fade_alpha))
{layer_drawing}
            self.screen.blit(fade_surface, (0, 0))
            pygame.display.flip()
            for event in pygame.event.get(): pass""")
                elif line.startswith("fadeOut("):
                    duration = line[8:-1]
                    parsed_lines.append(f"""        start_time = time.time()
        fade_duration = {duration}
        while True:
            current_time = time.time() - start_time
            if current_time >= fade_duration:
                break
            fade_alpha = min(255, 255 * (current_time / fade_duration))
            fade_surface = self.black_surface.copy()
            fade_surface.set_alpha(int(fade_alpha))
{layer_drawing}
            self.screen.blit(fade_surface, (0, 0))
            pygame.display.flip()
            for event in pygame.event.get(): pass""")
                elif line.startswith("wait("):
                    seconds = line[5:-1]
                    parsed_lines.append(f"""        start_time = time.time()
        while time.time() - start_time < {seconds}:
{layer_drawing}
            pygame.display.flip()
            for event in pygame.event.get(): pass""")
                elif line.startswith("dialog("):
                    group = line[7:-1].strip('"\'')
                    parsed_lines.append(f"""        self.{group}.start_dialog()
        while self.{group}.is_active:
            self.screen.blit(self.bg_image, (0, 0))
            self.player.draw(self.screen)
            {self.generate_dialog_drawing()}
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_z:
                        self.{group}.next()""")
                elif line == "playerCantMove()":
                    parsed_lines.append(f"        self.cutscene_active = True")
                elif line == "playerCanMove()":
                    parsed_lines.append(f"        self.cutscene_active = False")
                elif line.startswith("changeSprite("):
                    sprite_path = line[12:-1].strip()  # Remove changeSprite( and )
                    if sprite_path.startswith('"') or sprite_path.startswith("'"):
                        sprite_path = sprite_path[1:-1]  # Remove quotes
                    sprite_path = sprite_path[2:-1]
                    # sprite_path = sprite_path[:-1]
                    parsed_lines.append(f"""        # Change player sprite
        print(f"Changing sprite to: {sprite_path}")
        self.player.change_sprite("{sprite_path}")
        self.screen.blit(self.bg_image, (0, 0))
        self.player.draw(self.screen)
        pygame.display.flip()""")
                elif line == "resetSprite()":
                    parsed_lines.append(f"""        # Reset player sprites
        skin_type = self.player.skin_type
        sprite_path = f"{{gamePath}}/img/player/{{self.player.skin_type}}/idle_"
        
        # Reset all sprites to default
        self.player.sprites = {{
            'up': pygame.transform.scale(pygame.image.load(f"{{sprite_path}}u.png"), (96, 96)),
            'up1': pygame.transform.scale(pygame.image.load(f"{{sprite_path}}u1.png"), (96, 96)),
            'up2': pygame.transform.scale(pygame.image.load(f"{{sprite_path}}u2.png"), (96, 96)),
            'down': pygame.transform.scale(pygame.image.load(f"{{sprite_path}}d.png"), (96, 96)),
            'down1': pygame.transform.scale(pygame.image.load(f"{{sprite_path}}d1.png"), (96, 96)),
            'down2': pygame.transform.scale(pygame.image.load(f"{{sprite_path}}d2.png"), (96, 96)),
            'left': pygame.transform.scale(pygame.image.load(f"{{sprite_path}}l.png"), (96, 96)),
            'left1': pygame.transform.scale(pygame.image.load(f"{{sprite_path}}l1.png"), (96, 96)),
            'left2': pygame.transform.scale(pygame.image.load(f"{{sprite_path}}l2.png"), (96, 96)),
            'right': pygame.transform.scale(pygame.image.load(f"{{sprite_path}}r.png"), (96, 96)),
            'right1': pygame.transform.scale(pygame.image.load(f"{{sprite_path}}r1.png"), (96, 96)),
            'right2': pygame.transform.scale(pygame.image.load(f"{{sprite_path}}r2.png"), (96, 96))
        }}
        self.player.current_sprite = self.player.sprites[self.player.direction]
        self.screen.blit(self.bg_image, (0, 0))
        self.player.draw(self.screen)
        pygame.display.flip()""")
    
        return "\n".join(parsed_lines)

    def edit_script_trigger(self, cell_index, x, y):
        dialog = tk.Toplevel(self.root)
        dialog.title("Edit Script Trigger")
        dialog.grab_set()

        # Get existing script if any
        current_script = ""
        if cell_index in self.cells and self.cells[cell_index]["type"] == "script":
            current_script = self.cells[cell_index].get("script", "")

        ttk.Label(dialog, text="Enter script commands:").pack(pady=5)
        script_text = tk.Text(dialog, height=10, width=40)
        script_text.pack(padx=5, pady=5)
        script_text.insert("1.0", current_script)

        # Add help button
        ttk.Button(
            dialog,
            text="Show Commands Help",
            command=self.show_script_help
        ).pack(fill=tk.X, pady=2, padx=5)

        def save():
            script = script_text.get("1.0", tk.END).strip()
            if script:
                self.cells[cell_index] = {
                    "type": "script",
                    "x": x,
                    "y": y,
                    "script": script
                }
                self.draw_cell(x, y, "purple", cell_index)  # Purple for script triggers
            else:
                if cell_index in self.cells:
                    del self.cells[cell_index]
                self.canvas.delete(f"cell_{cell_index}")
            dialog.destroy()

        ttk.Button(dialog, text="Save", command=save).pack(pady=5)

    def generate_script_triggers(self):
        triggers = []
        for group_name, group_data in self.script_groups.items():
            if group_data["cells"]:
                cells_str = str(group_data["cells"])
                triggers.append(f'''                        if player_grid_index in {cells_str}:
                            self.execute_script("""{group_data["script"]}""")''')
        return "\n".join(triggers)

    def parse_script_method(self):
        return '''    def execute_script(self, script):
        # Split by newlines and semicolons
        commands = []
        for line in script.split("\\n"):
            # Split line by semicolons and strip whitespace
            commands.extend([cmd.strip() for cmd in line.split(";") if cmd.strip()])
            
        for line in commands:
            line = line.strip()
            if line:
                if line.startswith("fadeIn("):
                    duration = float(line[7:-1])
                    start_time = time.time()
                    while True:
                        current_time = time.time() - start_time
                        if current_time >= duration:
                            break
                        fade_alpha = max(0, 255 * (1 - current_time / duration))
                        fade_surface = self.black_surface.copy()
                        fade_surface.set_alpha(int(fade_alpha))
                        self.screen.blit(self.bg_image, (0, 0))
                        self.player.draw(self.screen)
                        self.screen.blit(fade_surface, (0, 0))
                        pygame.display.flip()
                        for event in pygame.event.get(): pass
                elif line.startswith("fadeOut("):
                    duration = float(line[8:-1])
                    start_time = time.time()
                    while True:
                        current_time = time.time() - start_time
                        if current_time >= duration:
                            break
                        fade_alpha = min(255, 255 * (current_time / duration))
                        fade_surface = self.black_surface.copy()
                        fade_surface.set_alpha(int(fade_alpha))
                        self.screen.blit(self.bg_image, (0, 0))
                        self.player.draw(self.screen)
                        self.screen.blit(fade_surface, (0, 0))
                        pygame.display.flip()
                        for event in pygame.event.get(): pass
                elif line.startswith("wait("):
                    seconds = float(line[5:-1])
                    start_time = time.time()
                    while time.time() - start_time < seconds:
                        self.screen.blit(self.bg_image, (0, 0))
                        self.player.draw(self.screen)
                        pygame.display.flip()
                        for event in pygame.event.get(): pass
                elif line.startswith("dialog("):
                    group = line[7:-1].strip('"\\'"')
                    dialog = getattr(self, group)
                    dialog.start_dialog()
                    while dialog.is_active:
                        for event in pygame.event.get():
                            if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_z:
                                    dialog.next()
                        self.screen.blit(self.bg_image, (0, 0))
                        self.player.draw(self.screen)
                        if dialog.is_active:
                            dialog.draw()
                        pygame.display.flip()
                elif line == "playerCantMove()":
                    self.cutscene_active = True
                elif line == "playerCanMove()":
                    self.cutscene_active = False
                elif line.startswith("changeSprite("):
                    sprite_path = line[12:-1].strip()  # Remove changeSprite( and )
                    if sprite_path.startswith('"') or sprite_path.startswith("'"):
                        sprite_path = sprite_path[1:-1]  # Remove quotes
                    print(f"Changing sprite to path: {sprite_path}")
                    self.player.change_sprite(sprite_path)
                    # Redraw to show the change immediately
                    self.screen.blit(self.bg_image, (0, 0))
                    self.player.draw(self.screen)
                    pygame.display.flip()
                elif line == "resetSprite()":
                    skin_type = self.player.skin_type
                    sprite_path = f"{gamePath}/img/player/{'d/' if skin_type == 'd' else ''}idle_"
                    
                    # Reset all sprites to default
                    self.player.sprites = {
                        'up': pygame.transform.scale(pygame.image.load(f"{sprite_path}u.png"), (96, 96)),
                        'up1': pygame.transform.scale(pygame.image.load(f"{sprite_path}u1.png"), (96, 96)),
                        'up2': pygame.transform.scale(pygame.image.load(f"{sprite_path}u2.png"), (96, 96)),
                        'down': pygame.transform.scale(pygame.image.load(f"{sprite_path}d.png"), (96, 96)),
                        'down1': pygame.transform.scale(pygame.image.load(f"{sprite_path}d1.png"), (96, 96)),
                        'down2': pygame.transform.scale(pygame.image.load(f"{sprite_path}d2.png"), (96, 96)),
                        'left': pygame.transform.scale(pygame.image.load(f"{sprite_path}l.png"), (96, 96)),
                        'left1': pygame.transform.scale(pygame.image.load(f"{sprite_path}l1.png"), (96, 96)),
                        'left2': pygame.transform.scale(pygame.image.load(f"{sprite_path}l2.png"), (96, 96)),
                        'right': pygame.transform.scale(pygame.image.load(f"{sprite_path}r.png"), (96, 96)),
                        'right1': pygame.transform.scale(pygame.image.load(f"{sprite_path}r1.png"), (96, 96)),
                        'right2': pygame.transform.scale(pygame.image.load(f"{sprite_path}r2.png"), (96, 96))
                    }
                    self.player.current_sprite = self.player.sprites[self.player.direction]
                    # Redraw to show the change immediately
                    self.screen.blit(self.bg_image, (0, 0))
                    self.player.draw(self.screen)
                    pygame.display.flip()'''

    def create_script_group(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Create Script Group")
        dialog.grab_set()

        ttk.Label(dialog, text="Group Name:").pack(pady=5)
        name_var = tk.StringVar()
        ttk.Entry(dialog, textvariable=name_var).pack(pady=5)

        def save():
            name = name_var.get()
            if name:
                self.script_groups[name] = {
                    "script": "",
                    "cells": []
                }
                self.update_script_group_list()
                dialog.destroy()

        ttk.Button(dialog, text="Save", command=save).pack(pady=5)

    def edit_script_group(self):
        if not self.current_script_group:
            tk.messagebox.showerror("Error", "Please select a script group first!")
            return

        dialog = tk.Toplevel(self.root)
        dialog.title(f"Edit Script Group: {self.current_script_group}")
        dialog.grab_set()

        # Add rename and delete buttons
        control_frame = ttk.Frame(dialog)
        control_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(
            control_frame,
            text="Rename Group",
            command=lambda: self.rename_script_group(dialog)
        ).pack(side=tk.LEFT, padx=2)
        
        ttk.Button(
            control_frame,
            text="Delete Group",
            command=lambda: self.delete_script_group(dialog)
        ).pack(side=tk.LEFT, padx=2)

        # Script editor
        ttk.Label(dialog, text="Script:").pack(pady=5)
        script_text = tk.Text(dialog, height=10, width=50)
        script_text.pack(padx=5, pady=5)
        script_text.insert("1.0", self.script_groups[self.current_script_group]["script"])

        # Add help button
        ttk.Button(
            dialog,
            text="Show Commands Help",
            command=self.show_script_help
        ).pack(fill=tk.X, pady=2, padx=5)

        def save():
            self.script_groups[self.current_script_group]["script"] = script_text.get("1.0", tk.END).strip()
            dialog.destroy()

        ttk.Button(dialog, text="Save", command=save).pack(pady=5)

    def rename_script_group(self, parent_dialog):
        dialog = tk.Toplevel(parent_dialog)
        dialog.title("Rename Script Group")
        dialog.grab_set()

        ttk.Label(dialog, text="New Name:").pack(pady=5)
        name_var = tk.StringVar(value=self.current_script_group)
        ttk.Entry(dialog, textvariable=name_var).pack(pady=5)

        def save():
            new_name = name_var.get()
            if new_name and new_name != self.current_script_group:
                self.script_groups[new_name] = self.script_groups[self.current_script_group]
                del self.script_groups[self.current_script_group]
                self.current_script_group = new_name
                self.update_script_group_list()
                self.script_group_var.set(new_name)
                dialog.destroy()
                parent_dialog.destroy()
                self.edit_script_group()

        ttk.Button(dialog, text="Save", command=save).pack(pady=5)

    def delete_script_group(self, parent_dialog):
        if tk.messagebox.askyesno("Confirm Delete", f"Delete script group '{self.current_script_group}'?"):
            # Remove all cells associated with this group
            cells_to_remove = []
            for index, cell in self.cells.items():
                if cell.get("type") == "script" and cell.get("script_group") == self.current_script_group:
                    cells_to_remove.append(index)
            
            for index in cells_to_remove:
                del self.cells[index]
                self.canvas.delete(f"cell_{index}")
            
            del self.script_groups[self.current_script_group]
            self.current_script_group = None
            self.script_group_var.set("")
            self.update_script_group_list()
            parent_dialog.destroy()

    def update_script_group_list(self):
        groups = list(self.script_groups.keys())
        self.script_group_combo['values'] = groups

    def on_script_group_selected(self, event):
        self.current_script_group = self.script_group_var.get()

    def add_background_layer(self):
        # Check if map name is set
        if not self.map_name_var.get():
            tk.messagebox.showerror("Error", "Please enter a map name first!")
            return

        # Get path to map's image folder
        map_dir = os.path.join("../img", self.map_name_var.get())
        
        # Check if directory exists
        if not os.path.exists(map_dir):
            tk.messagebox.showerror("Error", f"No image folder found for map '{self.map_name_var.get()}'")
            return

        # Get list of available images
        available_images = [f for f in os.listdir(map_dir) 
                           if f.endswith(('.png', '.jpg', '.jpeg'))]
        
        if not available_images:
            tk.messagebox.showerror("Error", "No images found in map folder!")
            return

        # Create image selection dialog
        dialog = tk.Toplevel(self.root)
        dialog.title("Select Layer Image")
        dialog.grab_set()

        ttk.Label(dialog, text="Select image from map folder:").pack(pady=5)

        def select_image(image_name):
            # Load and resize image
            image_path = os.path.join(map_dir, image_name)
            image = Image.open(image_path)
            image = image.resize((800, 600))
            photo = ImageTk.PhotoImage(image)
            
            # Store layer info
            layer_num = len(self.backgrounds)
            self.backgrounds.append({
                "path": image_name,
                "image": photo
            })
            
            # Update UI
            self.layers_listbox.insert(tk.END, f"Layer {layer_num}")
            self.player_layer_spin.config(to=layer_num)
            self.redraw_canvas()
            dialog.destroy()

        # Create button for each available image
        for img in available_images:
            ttk.Button(
                dialog,
                text=img,
                command=lambda i=img: select_image(i)
            ).pack(fill=tk.X, pady=2, padx=5)

    def move_layer(self, direction):
        selection = self.layers_listbox.curselection()
        if not selection:
            return
            
        index = selection[0]
        new_index = index + direction
        
        if 0 <= new_index < len(self.backgrounds):
            # Swap layers
            self.backgrounds[index], self.backgrounds[new_index] = \
                self.backgrounds[new_index], self.backgrounds[index]
                
            # Update listbox
            text = self.layers_listbox.get(index)
            self.layers_listbox.delete(index)
            self.layers_listbox.insert(new_index, text)
            self.layers_listbox.selection_set(new_index)
            
            self.redraw_canvas()

    def delete_layer(self):
        selection = self.layers_listbox.curselection()
        if not selection:
            return
            
        index = selection[0]
        del self.backgrounds[index]
        self.layers_listbox.delete(index)
        self.player_layer_spin.config(to=len(self.backgrounds)-1)
        
        if int(self.player_layer_var.get()) >= len(self.backgrounds):
            self.player_layer_var.set(str(len(self.backgrounds)-1))
        
        self.redraw_canvas()

    def update_player_layer(self):
        self.player_layer = int(self.player_layer_var.get())
        self.redraw_canvas()

    def redraw_canvas(self):
        self.canvas.delete("all")
        
        # Draw all backgrounds in order
        for bg in self.backgrounds:
            self.canvas.create_image(
                (800 - 768) // 2,
                (600 - 576) // 2,
                anchor=tk.NW,
                image=bg["image"]
            )
        
        self.draw_grid()
        self.redraw_cells()

    def generate_background_loading(self):
        lines = []
        for bg in self.backgrounds:
            lines.append(f'self.backgrounds.append(pygame.image.load(f"{{gamePath}}/img/{self.map_name_var.get()}/{bg["path"]}"))')
        return "\n        ".join(lines)

    def generate_background_drawing(self):
        return """
        # Draw backgrounds up to player layer
        for i in range(self.player_layer + 1):
            self.screen.blit(self.backgrounds[i], (0, 0))
            
        # Draw player
        self.player.draw(self.screen)
        
        # Draw remaining backgrounds
        for i in range(self.player_layer + 1, len(self.backgrounds)):
            self.screen.blit(self.backgrounds[i], (0, 0))
    """

    def get_available_skins(self):
        """Get list of available player skins from the player directory"""
        player_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "img", "player")
        
        # Get all directories in player folder
        skins = [d for d in os.listdir(player_dir) 
                if os.path.isdir(os.path.join(player_dir, d))]
        
        # Ensure at least one skin exists
        if not skins:
            tk.messagebox.showwarning(
                "Warning", 
                "No skin folders found in player directory!\nPlease create at least one skin folder."
            )
            return ["marko"]  # Return default skin
            
        return skins

if __name__ == "__main__":
    root = tk.Tk()
    app = MapMaker(root)
    root.mainloop()