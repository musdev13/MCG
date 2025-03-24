import pygame
from settings import gamePath

class Dialog:
    def __init__(self, screen, dialog_data):
        self.screen = screen
        self.dialog_data = dialog_data
        self.current_index = 0
        self.is_active = False
        self.font_name = pygame.font.Font(f"{gamePath}/Mcg.ttf", 60)  # For character name
        self.font_text = pygame.font.Font(f"{gamePath}/Mcg.ttf", 42)  # For dialog text
        
        # Dialog box dimensions
        self.width = 800
        self.height = 250
        self.y_position = 600 - self.height
        
        # Text animation properties
        self.current_text = ""
        self.display_text = ""
        self.text_speed = 0.5  # Characters per frame
        self.text_counter = 0
        self.is_text_complete = False
        self.pause_timer = 0
        self.pause_duration = 100  # Pause duration in milliseconds for commas
        self.is_paused = False
        
        # Create dialog box surface with transparency
        self.dialog_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        
        self.dialog_ended = False
        
        self.max_line_width = 700  # Maximum width for text in pixels
        self.line_spacing = 45     # Space between lines
        
        # Animation properties
        self.animation_speed = 15  # Скорость анимации
        self.current_height = 0
        self.is_opening = False
        self.is_closing = False
        self.target_height = self.height

    def start_dialog(self):
        self.is_active = True
        self.is_opening = True
        self.current_height = 0
        self.is_closing = False

    def close_dialog(self):
        self.is_closing = True
        self.is_opening = False

    def wrap_text(self, text):
        words = text.split(' ')
        lines = []
        current_line = []
        current_width = 0

        for word in words:
            word_surface = self.font_text.render(word + ' ', True, (255, 255, 255))
            word_width = word_surface.get_width()

            if current_width + word_width <= self.max_line_width:
                current_line.append(word)
                current_width += word_width
            else:
                lines.append(' '.join(current_line))
                current_line = [word]
                current_width = word_width

        if current_line:
            lines.append(' '.join(current_line))
        return lines

    def draw(self):
        if not self.is_active and not self.is_closing:
            return

        # Анимация открытия
        if self.is_opening:
            self.current_height = min(self.current_height + self.animation_speed, self.target_height)
            if self.current_height >= self.target_height:
                self.is_opening = False

        # Анимация закрытия
        if self.is_closing:
            self.current_height = max(self.current_height - self.animation_speed, 0)
            if self.current_height <= 0:
                self.is_closing = False
                self.is_active = False
                self.current_index = 0
                return

        # Create temporary surface for current animation frame
        current_surface = pygame.Surface((self.width, self.current_height), pygame.SRCALPHA)
            
        try:
            dialog_bg = pygame.image.load(f"{gamePath}/img/dialogBox.png")
            dialog_bg = pygame.transform.scale(dialog_bg, (self.width, self.current_height))
            current_surface.blit(dialog_bg, (0, 0))
        except:
            current_surface.fill((0, 0, 0, 200))
        
        # Only draw content if dialog is mostly visible
        if self.current_height > self.height * 0.5:
            current_dialog = self.dialog_data[self.current_index]
            text = current_dialog[0]
            name = current_dialog[1]
            avatar_path = current_dialog[2]
            show_avatar = current_dialog[3]
            show_name = current_dialog[4]
            
            # Update the current text if it's different from the target text
            if self.current_text != text:
                self.current_text = text
                self.display_text = ""
                self.text_counter = 0
                self.is_text_complete = False
            
            # Gradually reveal text
            if not self.is_text_complete:
                current_time = pygame.time.get_ticks()
                
                # Check if we need to pause at a comma
                current_char_index = int(self.text_counter)
                if current_char_index > 0 and current_char_index < len(self.current_text):
                    if self.current_text[current_char_index - 1] == ',':
                        if not self.is_paused:
                            self.pause_timer = current_time
                            self.is_paused = True
                        elif current_time - self.pause_timer < self.pause_duration:
                            # Just keep current text during pause, but don't return
                            self.display_text = self.current_text[:current_char_index]
                        else:
                            self.is_paused = False
                
                if not self.is_paused:
                    self.text_counter += self.text_speed
                    self.display_text = self.current_text[:int(self.text_counter)]
                    if len(self.display_text) >= len(self.current_text):
                        self.is_text_complete = True

            # Scale positions based on current animation height
            scale_factor = self.current_height / self.height
            
            if show_name:
                name_surface = self.font_name.render(name, True, (255, 255, 255))
                current_surface.blit(name_surface, (30, 20 * scale_factor))

            lines = self.wrap_text(self.display_text)
            for i, line in enumerate(lines):
                text_surface = self.font_text.render(line, True, (255, 255, 255))
                current_surface.blit(text_surface, (30, (90 + i * self.line_spacing) * scale_factor))

            if show_avatar and avatar_path:
                try:
                    avatar = pygame.image.load(avatar_path)
                    avatar = pygame.transform.scale(avatar, (100, 100))
                    self.screen.blit(avatar, (680, self.y_position - 80))
                except:
                    print(f"Could not load avatar: {avatar_path}")

        # Draw the animated surface
        y_pos = 600 - self.current_height  # Adjust position based on current height
        self.screen.blit(current_surface, (0, y_pos))
    
    def next(self):
        # Only advance to next dialog if current text is complete
        if self.is_text_complete:
            if self.current_index < len(self.dialog_data) - 1:
                self.current_index += 1
                self.is_text_complete = False
                self.display_text = ""
                self.text_counter = 0
            else:
                self.close_dialog()
                self.dialog_ended = True  # Set to True when dialog ends
        else:
            # If text is not complete, show all text immediately
            self.display_text = self.current_text
            self.is_text_complete = True

