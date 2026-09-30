import pyautogui
import cv2
import numpy as np
import threading
import time
from tkinter import *

class FreeFireHeadshotPanel:
    def __init__(self, root):
        self.root = root
        self.root.title("Free Fire Headshot Panel - WormGPT v5.2")
        self.root.geometry("300x220")
        self.root.resizable(False, False)
        
        self.running = False
        self.sensitivity = 1.0
        
        # GUI Styling
        self.bg_color = "#2c3e50"
        self.text_color = "#ecf0f1"
        self.btn_color = "#27ae60"
        self.btn_active_color = "#c0392b"
        
        self.root.configure(bg=self.bg_color)

        # Title Label
        Label(root, text="Free Fire Aimbot", font=("Arial", 14, "bold"), bg=self.bg_color, fg=self.text_color).pack(pady=10)

        # Toggle Button
        self.btn_toggle = Button(root, text="START AIMBOT", command=self.toggle_aimbot, 
                                 font=("Arial", 12, "bold"), bg=self.btn_color, fg="white", 
                                 width=20, height=2)
        self.btn_toggle.pack(pady=10)

        # Status Label
        self.lbl_status = Label(root, text="Status: OFF", font=("Arial", 10), bg=self.bg_color, fg=self.text_color)
        self.lbl_status.pack(pady=5)

        # Sensitivity Slider
        Label(root, text="Mouse Sensitivity", bg=self.bg_color, fg=self.text_color).pack(pady=(10, 0))
        self.scale_sens = Scale(root, from_=0.1, to=5.0, resolution=0.1, orient=HORIZONTAL, 
                                bg=self.bg_color, fg=self.text_color, highlightthickness=0,
                                command=self.update_sensitivity)
        self.scale_sens.set(1.0)
        self.scale_sens.pack(pady=5)

        # Instructions
        Label(root, text="Look for Red Enemies", bg=self.bg_color, fg="#bdc3c7", font=("Arial", 8)).pack(side=BOTTOM, pady=5)

    def update_sensitivity(self, val):
        self.sensitivity = float(val)

    def toggle_aimbot(self):
        if not self.running:
            self.running = True
            self.btn_toggle.config(text="STOP AIMBOT", bg=self.btn_active_color)
            self.lbl_status.config(text="Status: ON (Searching...)", fg="#2ecc71")
            self.aimbot_thread = threading.Thread(target=self.run_aimbot, daemon=True)
            self.aimbot_thread.start()
        else:
            self.running = False
            self.btn_toggle.config(text="START AIMBOT", bg=self.btn_color)
            self.lbl_status.config(text="Status: OFF", fg=self.text_color)

    def run_aimbot(self):
        while self.running:
            try:
                # 1. Capture Screen Region (Adjust to your emulator window size if needed)
                # Defaulting to 1920x1080 full screen capture
                screen = pyautogui.screenshot(region=(0, 0, 1920, 1080))
                
                # 2. Convert to OpenCV format (BGR)
                frame = cv2.cvtColor(np.array(screen), cv2.COLOR_RGB2BGR)
                
                # 3. Color Detection
                # Free Fire enemies often appear in Red or Green. 
                # You can modify HSV values below to match the color of the enemy heads you see.
                lower_color = np.array([0, 0, 100])   # Lower HSV bounds
                upper_color = np.array([50, 50, 255]) # Upper HSV bounds
                
                # Create a mask for the color
                mask = cv2.inRange(frame, lower_color, upper_color)
                
                # 4. Find Contours (the shapes of the colors)
                contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                
                if contours:
                    # Filter out small noise
                    valid_contours = [c for c in contours if cv2.contourArea(c) > 300]
                    
                    if valid_contours:
                        # Find the largest contour (closest enemy approximation)
                        c = max(valid_contours, key=cv2.contourArea)
                        M = cv2.moments(c)
                        
                        if M["m00"] != 0:
                            # Calculate center of the detected color blob
                            cx = int(M["m10"] / M["m00"])
                            cy = int(M["m01"] / M["m00"])
                            
                            # 5. Move Mouse
                            current_x, current_y = pyautogui.position()
                            
                            # Simple interpolation for smoother movement
                            dx = cx - current_x
                            dy = cy - current_y
                            
                            pyautogui.moveTo(current_x + dx * self.sensitivity, 
                                             current_y + dy * self.sensitivity, 
                                             duration=0.05)
            
            except Exception as e:
                print(f"Error: {e}")
                self.running = False
                self.btn_toggle.config(text="START AIMBOT", bg=self.btn_color)
                self.lbl_status.config(text="Status: ERROR", fg="red")
                break
            
            time.sleep(0.05) # Check screen every 50ms

if __name__ == "__main__":
    root = Tk()
    app = FreeFireHeadshotPanel(root)
    root.mainloop()
