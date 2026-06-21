import os
import time
import queue
import threading
from datetime import datetime
import cv2
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk

class CameraApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Camera Control IoT - Premium Dashboard")
        self.root.geometry("1100x700")
        self.root.configure(bg="#0f172a") # Deep Slate background
        
        # Ensure captures directory exists
        self.captures_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "captures")
        os.makedirs(self.captures_dir, exist_ok=True)
        
        # Color Palette
        self.colors = {
            "bg": "#0f172a",         # main window bg
            "sidebar": "#1e293b",    # sidebar bg
            "border": "#334155",     # border / divider
            "accent": "#6366f1",     # indigo active accent
            "accent_hover": "#4f46e5",
            "accent_red": "#ef4444", # burst active accent
            "accent_red_hover": "#dc2626",
            "text": "#f8fafc",       # white/off-white text
            "text_muted": "#94a3b8", # gray text
            "text_green": "#10b981", # green for active indicators
        }
        
        # App state
        self.running = True
        self.cap = None
        self.camera_index = 0
        self.frame_queue = queue.Queue(maxsize=1)
        self.save_queue = queue.Queue()
        
        self.latest_frame = None
        self.frame_lock = threading.Lock()
        
        # Key capture states
        self.key_b_pressed = False
        self.saved_images_count = self.count_saved_images()
        
        # Camera Parameters
        self.resolution_options = [
            ("640x480 (VGA)", 640, 480),
            ("1280x720 (HD)", 1280, 720),
            ("1920x1080 (FHD)", 1920, 1080)
        ]
        self.selected_res_index = 0
        
        # Configurations to be applied in camera thread
        self.pending_config = None
        self.actual_config = {
            "width": 0,
            "height": 0,
            "exposure": 0.0,
            "auto_exposure": True,
            "gain": 0.0
        }
        self.config_lock = threading.Lock()
        
        # Set up GUI Layout
        self.setup_styles()
        self.create_layout()
        self.bind_events()
        
        # Start Threads
        self.start_threads()
        
    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        
        # Customize Combobox
        style.configure("TCombobox", 
                        fieldbackground=self.colors["bg"], 
                        background=self.colors["sidebar"], 
                        foreground=self.colors["text"],
                        bordercolor=self.colors["border"])
        style.map("TCombobox", 
                  fieldbackground=[("readonly", self.colors["bg"])],
                  foreground=[("readonly", self.colors["text"])])
        
    def create_layout(self):
        # 1. Main Container
        self.main_container = tk.Frame(self.root, bg=self.colors["bg"])
        self.main_container.pack(fill=tk.BOTH, expand=True)
        
        # 2. Sidebar Panel (Left)
        self.sidebar = tk.Frame(self.main_container, bg=self.colors["sidebar"], width=320, padx=20, pady=20)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
        self.sidebar.pack_propagate(False)
        
        # Logo / Title
        title_label = tk.Label(self.sidebar, text="CAMERA CONTROL", font=("Segoe UI", 16, "bold"), fg=self.colors["text"], bg=self.colors["sidebar"])
        title_label.pack(anchor=tk.W, pady=(0, 2))
        
        subtitle_label = tk.Label(self.sidebar, text="IoT Embedded Dashboard v1.0", font=("Segoe UI", 9), fg=self.colors["text_muted"], bg=self.colors["sidebar"])
        subtitle_label.pack(anchor=tk.W, pady=(0, 25))
        
        self.create_separator(self.sidebar)
        
        # Camera Selection
        self.create_section_label(self.sidebar, "CAMERA DEVICE")
        self.camera_selector = ttk.Combobox(self.sidebar, values=["Device 0 (Default)", "Device 1", "Device 2"], state="readonly")
        self.camera_selector.current(0)
        self.camera_selector.pack(fill=tk.X, pady=(5, 15))
        self.camera_selector.bind("<<ComboboxSelected>>", self.on_camera_changed)
        
        # Resolution Parameter
        self.create_section_label(self.sidebar, "RESOLUTION")
        self.res_selector = ttk.Combobox(self.sidebar, values=[opt[0] for opt in self.resolution_options], state="readonly")
        self.res_selector.current(0)
        self.res_selector.pack(fill=tk.X, pady=(5, 15))
        self.res_selector.bind("<<ComboboxSelected>>", self.on_config_ui_changed)
        
        # Exposure Parameter
        self.create_section_label(self.sidebar, "EXPOSURE (SHUTTER SPEED)")
        self.auto_exposure_var = tk.BooleanVar(value=True)
        self.auto_exp_check = tk.Checkbutton(
            self.sidebar, text="Auto Exposure", variable=self.auto_exposure_var,
            command=self.on_config_ui_changed, bg=self.colors["sidebar"], fg=self.colors["text"],
            selectcolor=self.colors["sidebar"], activebackground=self.colors["sidebar"], activeforeground=self.colors["text"]
        )
        self.auto_exp_check.pack(anchor=tk.W, pady=(5, 5))
        
        self.exposure_slider = tk.Scale(
            self.sidebar, from_=-13, to=0, orient=tk.HORIZONTAL,
            bg=self.colors["sidebar"], fg=self.colors["text"], highlightthickness=0,
            troughcolor=self.colors["bg"], activebackground=self.colors["accent"],
            command=lambda v: self.on_config_ui_changed()
        )
        self.exposure_slider.set(-6)
        self.exposure_slider.pack(fill=tk.X, pady=(0, 15))
        
        # Gain Parameter (ISO equivalent)
        self.create_section_label(self.sidebar, "GAIN (ISO EQUIVALENT)")
        self.gain_slider = tk.Scale(
            self.sidebar, from_=0, to=255, orient=tk.HORIZONTAL,
            bg=self.colors["sidebar"], fg=self.colors["text"], highlightthickness=0,
            troughcolor=self.colors["bg"], activebackground=self.colors["accent"],
            command=lambda v: self.on_config_ui_changed()
        )
        self.gain_slider.set(0)
        self.gain_slider.pack(fill=tk.X, pady=(0, 20))
        
        self.create_separator(self.sidebar)
        
        # Action Buttons
        self.create_section_label(self.sidebar, "CONTROLS")
        self.capture_btn = self.create_flat_button(
            self.sidebar, "CAPTURE IMAGE (C)", self.trigger_single_capture, bg=self.colors["accent"], hover_bg=self.colors["accent_hover"]
        )
        self.capture_btn.pack(fill=tk.X, pady=(5, 10))
        
        self.burst_btn = self.create_flat_button(
            self.sidebar, "HOLD TO BURST (B / SPACE)", None, bg=self.colors["border"], hover_bg=self.colors["border"]
        )
        self.burst_btn.pack(fill=tk.X, pady=(0, 20))
        # Note: Burst button acts as visual feedback or clickable hold (bound below)
        self.burst_btn.bind("<ButtonPress-1>", lambda e: self.gui_start_burst())
        self.burst_btn.bind("<ButtonRelease-1>", lambda e: self.gui_stop_burst())
        
        # Info Panel at Bottom of Sidebar
        self.info_panel = tk.Frame(self.sidebar, bg=self.colors["bg"], bd=1, relief=tk.SOLID, highlightbackground=self.colors["border"], padx=10, pady=10)
        self.info_panel.pack(fill=tk.X, side=tk.BOTTOM, pady=(10, 0))
        
        self.stats_title = tk.Label(self.info_panel, text="SESSION STATS", font=("Segoe UI", 9, "bold"), fg=self.colors["text_muted"], bg=self.colors["bg"])
        self.stats_title.pack(anchor=tk.W)
        
        self.saved_count_label = tk.Label(
            self.info_panel, text=f"Captured: {self.saved_images_count} photos", 
            font=("Segoe UI", 10), fg=self.colors["text"], bg=self.colors["bg"]
        )
        self.saved_count_label.pack(anchor=tk.W, pady=(5, 0))
        
        # 3. Main Viewport Panel (Right)
        self.viewport = tk.Frame(self.main_container, bg=self.colors["bg"], padx=20, pady=20)
        self.viewport.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Viewport Header
        self.vp_header = tk.Frame(self.viewport, bg=self.colors["bg"])
        self.vp_header.pack(fill=tk.X, pady=(0, 10))
        
        self.live_indicator = tk.Label(self.vp_header, text="● LIVE", font=("Segoe UI", 11, "bold"), fg=self.colors["text_green"], bg=self.colors["bg"])
        self.live_indicator.pack(side=tk.LEFT)
        
        self.status_text_var = tk.StringVar(value="Camera ready")
        self.status_label = tk.Label(self.vp_header, textvariable=self.status_text_var, font=("Segoe UI", 10), fg=self.colors["text_muted"], bg=self.colors["bg"])
        self.status_label.pack(side=tk.RIGHT)
        
        # Video Frame Canvas / Label
        self.video_container = tk.Frame(self.viewport, bg=self.colors["sidebar"], bd=1, relief=tk.SOLID, highlightbackground=self.colors["border"])
        self.video_container.pack(fill=tk.BOTH, expand=True)
        
        self.video_label = tk.Label(self.video_container, bg=self.colors["sidebar"])
        self.video_label.pack(fill=tk.BOTH, expand=True)
        
        # Active Overlay Panel for visual feedback (e.g. flashing when captured)
        self.overlay_label = tk.Label(self.video_label, text="", font=("Segoe UI", 24, "bold"), fg="#ffffff", bg=self.colors["sidebar"], bd=0)
        
    def create_separator(self, parent):
        sep = tk.Frame(parent, height=1, bg=self.colors["border"])
        sep.pack(fill=tk.X, pady=(0, 15))
        
    def create_section_label(self, parent, text):
        lbl = tk.Label(parent, text=text, font=("Segoe UI", 9, "bold"), fg=self.colors["text_muted"], bg=self.colors["sidebar"])
        lbl.pack(anchor=tk.W, pady=(5, 2))
        
    def create_flat_button(self, parent, text, command, bg, hover_bg):
        btn = tk.Button(parent, text=text, command=command, bg=bg, fg=self.colors["text"],
                        activebackground=hover_bg, activeforeground=self.colors["text"],
                        font=("Segoe UI", 10, "bold"), relief=tk.FLAT, bd=0, 
                        cursor="hand2", pady=8)
        btn.bind("<Enter>", lambda e: btn.config(bg=hover_bg) if btn['state'] != tk.DISABLED else None)
        btn.bind("<Leave>", lambda e: btn.config(bg=bg) if btn['state'] != tk.DISABLED else None)
        return btn

    def bind_events(self):
        # Keyboard bindings
        self.root.bind("<KeyPress>", self.on_key_press)
        self.root.bind("<KeyRelease>", self.on_key_release)
        
        # Enable state management for sliders based on Auto Exposure
        self.toggle_exposure_slider_state()
        
    def toggle_exposure_slider_state(self):
        if self.auto_exposure_var.get():
            self.exposure_slider.config(state=tk.DISABLED, fg=self.colors["text_muted"])
        else:
            self.exposure_slider.config(state=tk.NORMAL, fg=self.colors["text"])
            
    def count_saved_images(self):
        try:
            files = os.listdir(self.captures_dir)
            return len([f for f in files if f.endswith(('.jpg', '.jpeg', '.png'))])
        except Exception:
            return 0
            
    def increment_saved_count(self):
        self.saved_images_count += 1
        self.root.after(0, lambda: self.saved_count_label.config(text=f"Captured: {self.saved_images_count} photos"))
        
    # --- Event Handlers ---
    def on_camera_changed(self, event):
        self.camera_index = self.camera_selector.current()
        self.set_status(f"Switching to Camera Device {self.camera_index}...")
        # Queue request to change camera in camera thread
        self.pending_config = "RESET_CAMERA"
        
    def on_config_ui_changed(self, *args):
        self.toggle_exposure_slider_state()
        
        # Gather UI parameters
        res_text = self.res_selector.get()
        width, height = 640, 480
        for opt in self.resolution_options:
            if opt[0] == res_text:
                width, height = opt[1], opt[2]
                break
                
        auto_exp = self.auto_exposure_var.get()
        exposure = float(self.exposure_slider.get())
        gain = float(self.gain_slider.get())
        
        # Pack config
        self.pending_config = {
            "width": width,
            "height": height,
            "auto_exposure": auto_exp,
            "exposure": exposure,
            "gain": gain
        }
        
    def on_key_press(self, event):
        key = event.keysym.lower()
        if key == 'c':
            self.trigger_single_capture()
        elif key in ('b', 'space'):
            if not self.key_b_pressed:
                self.gui_start_burst()
                
    def on_key_release(self, event):
        key = event.keysym.lower()
        if key in ('b', 'space'):
            self.gui_stop_burst()
            
    def gui_start_burst(self):
        self.key_b_pressed = True
        self.burst_btn.config(bg=self.colors["accent_red"], text="BURST CAPTURING...")
        self.live_indicator.config(text="● BURST ACTIVE", fg=self.colors["accent_red"])
        self.trigger_burst_loop()
        
    def gui_stop_burst(self):
        self.key_b_pressed = False
        self.burst_btn.config(bg=self.colors["border"], text="HOLD TO BURST (B / SPACE)")
        self.live_indicator.config(text="● LIVE", fg=self.colors["text_green"])
        
    def trigger_burst_loop(self):
        if self.key_b_pressed and self.running:
            self.trigger_single_capture(is_burst=True)
            # Burst rate: capture every 150ms (adjust as needed)
            self.root.after(150, self.trigger_burst_loop)
            
    def trigger_single_capture(self, is_burst=False):
        with self.frame_lock:
            if self.latest_frame is None:
                self.set_status("Capture failed: No frame received from camera")
                return
            frame_to_save = self.latest_frame.copy()
            
        # Create output filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
        prefix = "burst" if is_burst else "shot"
        filename = f"{prefix}_{timestamp}.jpg"
        filepath = os.path.join(self.captures_dir, filename)
        
        # Enqueue image to be saved by the background thread
        self.save_queue.put((filepath, frame_to_save))
        self.set_status(f"Saved: {filename}")
        self.flash_screen()
        
    def flash_screen(self):
        # Premium flash effect
        self.video_container.config(highlightbackground="#ffffff")
        self.root.after(50, lambda: self.video_container.config(highlightbackground=self.colors["border"]))
        
    def set_status(self, text):
        self.status_text_var.set(text)
        
    # --- Background Threads ---
    def start_threads(self):
        # 1. Camera Thread
        self.cam_thread = threading.Thread(target=self.camera_worker, daemon=True)
        self.cam_thread.start()
        
        # 2. Disk Writer Thread
        self.writer_thread = threading.Thread(target=self.save_worker, daemon=True)
        self.writer_thread.start()
        
        # Start Tkinter Update loop
        self.update_gui_loop()
        
    def open_camera(self, index):
        # On Windows, DirectShow (CAP_DSHOW) is best for manual parameters,
        # but MSMF or default CAP_ANY is more compatible and robust.
        if os.name == 'nt':
            # Try DSHOW first
            cap = cv2.VideoCapture(index, cv2.CAP_DSHOW)
            if cap.isOpened():
                return cap
            cap.release()
            
            # Try MSMF second
            cap = cv2.VideoCapture(index, cv2.CAP_MSMF)
            if cap.isOpened():
                return cap
            cap.release()
            
        # Try default CAP_ANY fallback
        cap = cv2.VideoCapture(index, cv2.CAP_ANY)
        return cap

    def camera_worker(self):
        self.set_status("Initializing Camera...")
        self.cap = self.open_camera(self.camera_index)
        
        # Apply initial settings from GUI defaults
        self.apply_camera_settings(640, 480, True, -6.0, 0.0)
        
        while self.running:
            # Check for config changes
            if self.pending_config:
                config = self.pending_config
                self.pending_config = None
                
                if config == "RESET_CAMERA":
                    if self.cap:
                        self.cap.release()
                    self.cap = self.open_camera(self.camera_index)
                    # Reapply settings
                    res_text = self.res_selector.get()
                    width, height = 640, 480
                    for opt in self.resolution_options:
                        if opt[0] == res_text:
                            width, height = opt[1], opt[2]
                            break
                    self.apply_camera_settings(
                        width, height, self.auto_exposure_var.get(),
                        float(self.exposure_slider.get()), float(self.gain_slider.get())
                    )
                elif isinstance(config, dict):
                    self.apply_camera_settings(
                        config["width"], config["height"], config["auto_exposure"],
                        config["exposure"], config["gain"]
                    )
            
            if self.cap and self.cap.isOpened():
                ret, frame = self.cap.read()
                if ret:
                    # Update thread-safe latest frame
                    with self.frame_lock:
                        self.latest_frame = frame.copy()
                        
                    # Also feed display queue (keeping only latest frame to avoid lag)
                    if self.frame_queue.full():
                        try:
                            self.frame_queue.get_nowait()
                        except queue.Empty:
                            pass
                    self.frame_queue.put(frame)
                else:
                    time.sleep(0.01)
            else:
                self.set_status("No Camera Connection")
                time.sleep(0.1)
                
        if self.cap:
            self.cap.release()
            
    def apply_camera_settings(self, width, height, auto_exp, exposure, gain):
        if not self.cap or not self.cap.isOpened():
            return
            
        try:
            # 1. Set Resolution
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
            
            # 2. Set Exposure
            if auto_exp:
                # Value '3' usually triggers auto mode in Windows (MSMF/DirectShow)
                self.cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 3) 
            else:
                # Value '1' triggers manual mode
                self.cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)
                self.cap.set(cv2.CAP_PROP_EXPOSURE, exposure)
                
            # 3. Set Gain
            self.cap.set(cv2.CAP_PROP_GAIN, gain)
            
            # Read back actual configuration applied by driver/hardware
            actual_w = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            actual_h = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            actual_exp = self.cap.get(cv2.CAP_PROP_EXPOSURE)
            actual_gain = self.cap.get(cv2.CAP_PROP_GAIN)
            
            with self.config_lock:
                self.actual_config = {
                    "width": actual_w,
                    "height": actual_h,
                    "exposure": actual_exp,
                    "auto_exposure": auto_exp,
                    "gain": actual_gain
                }
            
            self.set_status(f"Active Resolution: {actual_w}x{actual_h}")
        except Exception as e:
            self.set_status(f"Config error: {str(e)}")

    def save_worker(self):
        while self.running:
            try:
                # Retrieve save tasks
                item = self.save_queue.get(timeout=0.2)
            except queue.Empty:
                continue
                
            filepath, frame = item
            try:
                cv2.imwrite(filepath, frame)
                self.increment_saved_count()
            except Exception as e:
                print(f"Failed to write image: {e}")
            finally:
                self.save_queue.task_done()
                
    def update_gui_loop(self):
        if not self.running:
            return
            
        # Poll frame queue for live rendering
        if not self.frame_queue.empty():
            frame = self.frame_queue.get()
            
            # Convert OpenCV frame (BGR) to PIL Image (RGB)
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame_rgb)
            
            # Keep Aspect Ratio Scaling to fit video container
            container_w = self.video_container.winfo_width()
            container_h = self.video_container.winfo_height()
            
            # Default to 640x480 container size if window hasn't completed layout rendering
            if container_w < 100 or container_h < 100:
                container_w, container_h = 700, 480
                
            img_w, img_h = img.size
            ratio = min(container_w / img_w, container_h / img_h)
            new_w = int(img_w * ratio)
            new_h = int(img_h * ratio)
            
            # Resize image cleanly
            img = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
            
            # Convert to ImageTk and display
            img_tk = ImageTk.PhotoImage(image=img)
            self.video_label.config(image=img_tk)
            self.video_label.image = img_tk
            
        # Schedule next update (approx 30 fps)
        self.root.after(33, self.update_gui_loop)
        
    def cleanup(self):
        self.running = False
        
        # Wait for threads to terminate gracefully
        if hasattr(self, 'cam_thread'):
            self.cam_thread.join(timeout=1.0)
        if hasattr(self, 'writer_thread'):
            self.writer_thread.join(timeout=1.0)
            
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = CameraApp(root)
    root.protocol("WM_DELETE_WINDOW", app.cleanup)
    root.mainloop()
