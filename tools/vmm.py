import tkinter as tk
from tkinter import filedialog, ttk
import json
import os
import shutil

class VideoMapMaker:
    def __init__(self, root):
        self.root = root
        self.root.title("MCG Video Map Maker")
        
        # Variables
        self.video_path = None
        self.next_level = None
        
        self.setup_ui()
        
    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="5")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Map name input
        ttk.Label(main_frame, text="Map Name:").pack(pady=5)
        self.map_name_var = tk.StringVar()
        ttk.Entry(
            main_frame,
            textvariable=self.map_name_var
        ).pack(fill=tk.X, pady=2)
        
        # Video selection
        ttk.Label(main_frame, text="\nVideo File:").pack(pady=5)
        self.video_label = ttk.Label(main_frame, text="No video selected")
        self.video_label.pack(pady=2)
        
        ttk.Button(
            main_frame,
            text="Select Video",
            command=self.select_video
        ).pack(fill=tk.X, pady=2)
        
        # Next level input
        ttk.Label(main_frame, text="\nNext Level:").pack(pady=5)
        self.next_level_var = tk.StringVar()
        ttk.Entry(
            main_frame,
            textvariable=self.next_level_var
        ).pack(fill=tk.X, pady=2)
        
        # Save/Load/Compile buttons
        ttk.Button(
            main_frame,
            text="Save Map",
            command=self.save_map
        ).pack(fill=tk.X, pady=2)
        
        ttk.Button(
            main_frame,
            text="Load Map",
            command=self.load_map
        ).pack(fill=tk.X, pady=2)
        
        ttk.Button(
            main_frame,
            text="Compile to .py",
            command=self.compile_to_py
        ).pack(fill=tk.X, pady=2)
        
    def select_video(self):
        map_name = self.map_name_var.get()
        if not map_name:
            tk.messagebox.showerror("Error", "Please enter a map name first!")
            return
            
        # Get path to map's video folder
        map_dir = os.path.join("../img", map_name)
        
        # Check if directory exists
        if not os.path.exists(map_dir):
            response = tk.messagebox.askyesno(
                "Directory not found", 
                f"Directory 'img/{map_name}' does not exist. Create it?"
            )
            if response:
                os.makedirs(map_dir)
            else:
                return

        # Create video selection dialog
        dialog = tk.Toplevel(self.root)
        dialog.title("Select Video")
        dialog.grab_set()
        
        # Get list of available videos
        available_videos = [f for f in os.listdir(map_dir) 
                           if f.endswith('.mp4')]
        
        if not available_videos:
            response = tk.messagebox.askyesno(
                "No Videos", 
                "No videos found in map folder. Would you like to import a video?"
            )
            dialog.destroy()
            if response:
                self.import_video(map_dir)
            return

        ttk.Label(dialog, text=f"Select video from img/{map_name}:").pack(pady=5)

        def select_video_file(video_name):
            self.video_path = video_name
            self.video_label.config(text=video_name)
            dialog.destroy()

        # Create button for each available video
        for video in available_videos:
            ttk.Button(
                dialog,
                text=video,
                command=lambda v=video: select_video_file(v)
            ).pack(fill=tk.X, pady=2, padx=5)
            
        # Add import new video button
        ttk.Button(
            dialog,
            text="Import New Video...",
            command=lambda: [dialog.destroy(), self.import_video(map_dir)]
        ).pack(fill=tk.X, pady=5, padx=5)

    def import_video(self, map_dir):
        # Get video file
        file_path = filedialog.askopenfilename(
            filetypes=[("Video files", "*.mp4")]
        )
        
        if file_path:
            # Copy video to map folder
            video_name = f"{self.map_name_var.get()}.mp4"
            target_path = os.path.join(map_dir, video_name)
            shutil.copy2(file_path, target_path)
            
            self.video_path = video_name
            self.video_label.config(text=video_name)
            
    def save_map(self):
        if not self.video_path:
            tk.messagebox.showerror("Error", "Please select a video first!")
            return
            
        map_name = self.map_name_var.get()
        if not map_name:
            tk.messagebox.showerror("Error", "Please enter a map name!")
            return
            
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json")]
        )
        
        if file_path:
            map_data = {
                "video": self.video_path,
                "next_level": self.next_level_var.get()
            }
            
            try:
                with open(file_path, "w") as f:
                    json.dump(map_data, f, indent=4)
                tk.messagebox.showinfo("Success", "Map saved successfully!")
            except Exception as e:
                tk.messagebox.showerror("Error", f"Failed to save map: {str(e)}")
                
    def load_map(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json")]
        )
        
        if file_path:
            try:
                with open(file_path, "r") as f:
                    map_data = json.load(f)
                    
                map_name = os.path.splitext(os.path.basename(file_path))[0]
                self.map_name_var.set(map_name)
                self.video_path = map_data["video"]
                self.video_label.config(text=self.video_path)
                self.next_level_var.set(map_data["next_level"])
                
            except Exception as e:
                tk.messagebox.showerror("Error", f"Failed to load map: {str(e)}")
                
    def compile_to_py(self):
        map_name = self.map_name_var.get()
        if not map_name or not self.video_path or not self.next_level_var.get():
            tk.messagebox.showerror("Error", "Please fill in all fields!")
            return
            
        template = f'''# filepath: {{gamePath}}/maps/{map_name}.py
import pygame
from settings import gamePath, Level
from pyvidplayer2 import Video

class {map_name}:
    def __init__(self, screen, gamePath=gamePath):
        self.screen = screen
        self.video = Video(f"{{gamePath}}/img/{map_name}/{self.video_path}")
    
    def draw(self):
        running = True
        while running:
            # Check if video has ended
            if self.video.get_pos() >= self.video.duration:
                running = False
                Level.levelName = "{self.next_level_var.get()}"
                return
            
            self.video.draw(self.screen, (0,0), force_draw=False)

            if Level.levelName == "{map_name}":
                pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    return'''
                    
        try:
            with open(f"../maps/{map_name}.py", "w") as f:
                f.write(template)
            tk.messagebox.showinfo("Success", f"Map compiled to {map_name}.py")
        except Exception as e:
            tk.messagebox.showerror("Error", f"Failed to compile map: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = VideoMapMaker(root)
    root.mainloop()