"""Main window GUI using CustomTkinter."""
import customtkinter as ctk
from tkinter import filedialog, messagebox
import os
import json
from pathlib import Path
import webbrowser

from core.colmap_wrapper import COLMAPWrapper
from core.glomap_wrapper import GloMAPWrapper
from core.dgut_wrapper import DGUTWrapper
from core.pipeline import PhotogrammetryPipeline
from gui.workers import PipelineWorker, DenseOnlyWorker, DGUTWorker
from utils.validators import validate_image_folder, validate_project_path
from utils.logger import get_logger


class MainWindow(ctk.CTk):
    """Main application window."""
    
    def __init__(self):
        """Initialize main window."""
        super().__init__()
        
        # Window configuration
        self.title("GloMAP Photogrammetry GUI")
        self.geometry("1000x700")
        
        # Set theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Initialize logger
        self.logger = get_logger()
        
        # Application state
        self.image_path = None
        self.project_path = None
        self.colmap_path = r"C:\Users\User\Documents\colmap-x64-windows-cuda"
        self.worker = None
        self.config = {
            'use_gpu': True,
            'matcher_type': 'sequential',
            'include_dense': False,
            'max_features': 8192,
            'overlap': 10,
            # Fisheye options
            'fisheye_enabled': False,
            'camera_model': 'OPENCV_FISHEYE',
            'camera_params': '',
            'single_camera': True,
            # 3DGUT options
            'dgut_enabled': False,
            'dgut_mcmc': True,
            'dgut_iterations': 30000,
            'dgut_export_ply': True
        }
        
        # Initialize wrappers
        self.setup_wrappers()
        
        # Create UI
        self.setup_ui()
        
        # Start update loop for worker messages
        self.check_worker_messages()
        
        # Log startup
        self.log_message("=" * 60)
        self.log_message("  GloMAP Photogrammetry GUI - Ready")
        self.log_message("=" * 60)
        self.check_installations()
    
    def setup_wrappers(self):
        """Initialize COLMAP, GloMAP, and 3DGUT wrappers."""
        try:
            self.colmap = COLMAPWrapper(self.colmap_path)
            self.glomap = GloMAPWrapper()
            self.dgut = DGUTWrapper()
            self.pipeline = PhotogrammetryPipeline(self.colmap, self.glomap, self.dgut)
        except Exception as e:
            self.logger.error(f"Failed to initialize wrappers: {e}")
            self.colmap = None
            self.glomap = None
            self.dgut = None
            self.pipeline = None
    
    def setup_ui(self):
        """Create the user interface."""
        # Main container
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Title
        title = ctk.CTkLabel(
            main_frame,
            text="🌍 GloMAP Photogrammetry Processing",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title.pack(pady=(10, 20))
        
        # Settings panel
        self.create_settings_panel(main_frame)
        
        # Fisheye camera panel
        self.create_fisheye_panel(main_frame)
        
        # 3DGUT panel
        self.create_dgut_panel(main_frame)
        
        # Control buttons
        self.create_control_panel(main_frame)
        
        # Progress bar
        self.progress = ctk.CTkProgressBar(main_frame)
        self.progress.pack(fill="x", padx=20, pady=10)
        self.progress.set(0)
        
        # Log display
        log_label = ctk.CTkLabel(
            main_frame,
            text="Processing Log:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        log_label.pack(anchor="w", padx=20, pady=(10, 5))
        
        self.log_text = ctk.CTkTextbox(main_frame, height=250, font=ctk.CTkFont(size=11))
        self.log_text.pack(fill="both", expand=True, padx=20, pady=(0, 10))
    
    def create_settings_panel(self, parent):
        """Create settings panel."""
        settings_frame = ctk.CTkFrame(parent)
        settings_frame.pack(fill="x", padx=20, pady=10)
        
        # Title
        ctk.CTkLabel(
            settings_frame,
            text="Project Settings",
            font=ctk.CTkFont(size=16, weight="bold")
        ).grid(row=0, column=0, columnspan=3, pady=(10, 15), sticky="w", padx=15)
        
        # Image folder selection
        ctk.CTkLabel(settings_frame, text="Images Folder:").grid(
            row=1, column=0, sticky="w", padx=15, pady=5
        )
        self.image_label = ctk.CTkLabel(
            settings_frame,
            text="No folder selected",
            text_color="gray"
        )
        self.image_label.grid(row=1, column=1, sticky="w", padx=10, pady=5)
        ctk.CTkButton(
            settings_frame,
            text="Browse",
            command=self.select_images,
            width=100
        ).grid(row=1, column=2, padx=15, pady=5)
        
        # Project folder selection
        ctk.CTkLabel(settings_frame, text="Project Folder:").grid(
            row=2, column=0, sticky="w", padx=15, pady=5
        )
        self.project_label = ctk.CTkLabel(
            settings_frame,
            text="No folder selected",
            text_color="gray"
        )
        self.project_label.grid(row=2, column=1, sticky="w", padx=10, pady=5)
        ctk.CTkButton(
            settings_frame,
            text="Browse",
            command=self.select_project,
            width=100
        ).grid(row=2, column=2, padx=15, pady=5)
        
        # Options frame
        options_frame = ctk.CTkFrame(settings_frame)
        options_frame.grid(row=3, column=0, columnspan=3, sticky="ew", padx=15, pady=10)
        
        # GPU option
        self.gpu_var = ctk.BooleanVar(value=True)
        ctk.CTkCheckBox(
            options_frame,
            text="Use GPU Acceleration",
            variable=self.gpu_var,
            command=self.update_config
        ).pack(side="left", padx=10, pady=10)
        
        # Matcher type
        ctk.CTkLabel(options_frame, text="Matcher:").pack(side="left", padx=(20, 5))
        self.matcher_var = ctk.StringVar(value="sequential")
        matcher_menu = ctk.CTkOptionMenu(
            options_frame,
            values=["sequential", "exhaustive"],
            variable=self.matcher_var,
            command=lambda x: self.update_config()
        )
        matcher_menu.pack(side="left", padx=5)
        
        # Dense reconstruction option
        self.dense_var = ctk.BooleanVar(value=False)
        self.dense_check = ctk.CTkCheckBox(
            options_frame,
            text="Include Dense Reconstruction",
            variable=self.dense_var,
            command=self.update_config
        )
        self.dense_check.pack(side="left", padx=20, pady=10)
        
        settings_frame.grid_columnconfigure(1, weight=1)
    
    def create_fisheye_panel(self, parent):
        """Create fisheye camera configuration panel."""
        fisheye_frame = ctk.CTkFrame(parent)
        fisheye_frame.pack(fill="x", padx=20, pady=10)
        
        # Title
        ctk.CTkLabel(
            fisheye_frame,
            text="🐟 Fisheye Camera Configuration",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(anchor="w", padx=15, pady=(10, 5))
        
        # Fisheye enable checkbox
        self.fisheye_var = ctk.BooleanVar(value=False)
        fisheye_check = ctk.CTkCheckBox(
            fisheye_frame,
            text="Enable Fisheye Camera Mode (180-220° FOV)",
            variable=self.fisheye_var,
            command=self.on_fisheye_toggle
        )
        fisheye_check.pack(anchor="w", padx=15, pady=5)
        
        # Camera model selection
        self.camera_model_frame = ctk.CTkFrame(fisheye_frame)
        self.camera_model_frame.pack(fill="x", padx=15, pady=5)
        
        ctk.CTkLabel(self.camera_model_frame, text="Camera Model:").pack(side="left", padx=5)
        self.camera_model_var = ctk.StringVar(value="OPENCV_FISHEYE")
        self.camera_model_menu = ctk.CTkOptionMenu(
            self.camera_model_frame,
            values=["OPENCV_FISHEYE", "SIMPLE_RADIAL_FISHEYE", "RADIAL_FISHEYE", "FOV"],
            variable=self.camera_model_var,
            command=lambda x: self.update_config(),
            state="disabled"
        )
        self.camera_model_menu.pack(side="left", padx=5)
        
        # Camera parameters input
        ctk.CTkLabel(self.camera_model_frame, text="Parameters (optional):").pack(side="left", padx=(20, 5))
        self.camera_params_entry = ctk.CTkEntry(
            self.camera_model_frame,
            placeholder_text="fx,fy,cx,cy,k1,k2,k3,k4",
            width=250,
            state="disabled"
        )
        self.camera_params_entry.pack(side="left", padx=5)
        
        # Single camera checkbox
        self.single_camera_var = ctk.BooleanVar(value=True)
        self.single_camera_check = ctk.CTkCheckBox(
            self.camera_model_frame,
            text="Single Camera",
            variable=self.single_camera_var,
            command=self.update_config,
            state="disabled"
        )
        self.single_camera_check.pack(side="left", padx=10)
    
    def create_dgut_panel(self, parent):
        """Create 3DGUT configuration panel."""
        dgut_frame = ctk.CTkFrame(parent)
        dgut_frame.pack(fill="x", padx=20, pady=10)
        
        # Title
        ctk.CTkLabel(
            dgut_frame,
            text="✨ 3DGUT (Gaussian Splatting) Configuration",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(anchor="w", padx=15, pady=(10, 5))
        
        # 3DGUT enable checkbox
        self.dgut_var = ctk.BooleanVar(value=False)
        dgut_check = ctk.CTkCheckBox(
            dgut_frame,
            text="Enable 3DGUT (Real-time Rendering & Superior Fisheye Quality)",
            variable=self.dgut_var,
            command=self.on_dgut_toggle
        )
        dgut_check.pack(anchor="w", padx=15, pady=5)
        
        # 3DGUT options
        self.dgut_options_frame = ctk.CTkFrame(dgut_frame)
        self.dgut_options_frame.pack(fill="x", padx=15, pady=5)
        
        # MCMC checkbox
        self.mcmc_var = ctk.BooleanVar(value=True)
        self.mcmc_check = ctk.CTkCheckBox(
            self.dgut_options_frame,
            text="MCMC Optimization",
            variable=self.mcmc_var,
            command=self.update_config,
            state="disabled"
        )
        self.mcmc_check.pack(side="left", padx=5)
        
        # Iterations
        ctk.CTkLabel(self.dgut_options_frame, text="Iterations:").pack(side="left", padx=(20, 5))
        self.iterations_var = ctk.StringVar(value="30000")
        self.iterations_entry = ctk.CTkEntry(
            self.dgut_options_frame,
            textvariable=self.iterations_var,
            width=80,
            state="disabled"
        )
        self.iterations_entry.pack(side="left", padx=5)
        
        # Export PLY
        self.export_ply_var = ctk.BooleanVar(value=True)
        self.export_ply_check = ctk.CTkCheckBox(
            self.dgut_options_frame,
            text="Export Point Cloud",
            variable=self.export_ply_var,
            command=self.update_config,
            state="disabled"
        )
        self.export_ply_check.pack(side="left", padx=(20, 5))
        
        # Note label
        note_label = ctk.CTkLabel(
            dgut_frame,
            text="Note: 3DGUT requires ~30-80 minutes on RTX 4090. Mutually exclusive with Dense MVS.",
            font=ctk.CTkFont(size=10),
            text_color="gray"
        )
        note_label.pack(anchor="w", padx=15, pady=(0, 10))
    
    def on_fisheye_toggle(self):
        """Handle fisheye mode toggle."""
        enabled = self.fisheye_var.get()
        state = "normal" if enabled else "disabled"
        self.camera_model_menu.configure(state=state)
        self.camera_params_entry.configure(state=state)
        self.single_camera_check.configure(state=state)
        self.config['fisheye_enabled'] = enabled
        self.update_config()
    
    def on_dgut_toggle(self):
        """Handle 3DGUT mode toggle."""
        enabled = self.dgut_var.get()
        state = "normal" if enabled else "disabled"
        
        # Enable/disable 3DGUT controls
        self.mcmc_check.configure(state=state)
        self.iterations_entry.configure(state=state)
        self.export_ply_check.configure(state=state)
        
        # Disable dense reconstruction when 3DGUT is enabled (mutually exclusive)
        if enabled:
            self.dense_var.set(False)
            self.dense_check.configure(state="disabled")
        else:
            self.dense_check.configure(state="normal")
        
        self.config['dgut_enabled'] = enabled
        self.update_config()
    
    def create_control_panel(self, parent):
        """Create control buttons panel."""
        control_frame = ctk.CTkFrame(parent)
        control_frame.pack(fill="x", padx=20, pady=10)
        
        # Run button
        self.run_btn = ctk.CTkButton(
            control_frame,
            text="▶ Run Complete Pipeline",
            command=self.run_pipeline,
            height=50,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color="#2fa572",
            hover_color="#25864d"
        )
        self.run_btn.pack(side="left", expand=True, fill="x", padx=5, pady=15)
        
        # Dense only button (for existing sparse models)
        self.dense_btn = ctk.CTkButton(
            control_frame,
            text="🔷 Dense Only",
            command=self.run_dense_only,
            height=50,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#1976d2",
            hover_color="#155a9c"
        )
        self.dense_btn.pack(side="left", padx=5, pady=15)
        
        # 3DGUT button
        self.dgut_btn = ctk.CTkButton(
            control_frame,
            text="✨ Run 3DGUT",
            command=self.run_3dgut,
            height=50,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#7b1fa2",
            hover_color="#6a1b9a"
        )
        self.dgut_btn.pack(side="left", padx=5, pady=15)
        
        # Stop button
        self.stop_btn = ctk.CTkButton(
            control_frame,
            text="⬛ Stop",
            command=self.stop_pipeline,
            height=50,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color="#d32f2f",
            hover_color="#b71c1c",
            state="disabled"
        )
        self.stop_btn.pack(side="left", padx=5, pady=15)
        
        # Open output button
        self.open_btn = ctk.CTkButton(
            control_frame,
            text="📁 Open Output",
            command=self.open_output,
            height=50,
            font=ctk.CTkFont(size=16, weight="bold"),
            state="disabled"
        )
        self.open_btn.pack(side="left", padx=5, pady=15)
    
    def select_images(self):
        """Select images folder."""
        folder = filedialog.askdirectory(title="Select Image Folder")
        if folder:
            self.image_path = folder
            
            # Validate folder
            valid, message, count = validate_image_folder(folder)
            
            if valid:
                self.image_label.configure(
                    text=f"{Path(folder).name} ({count} images)",
                    text_color="green"
                )
                self.log_message(f"✓ Selected: {folder}")
                self.log_message(f"  Found {count} images")
            else:
                self.image_label.configure(text=message, text_color="red")
                self.log_message(f"✗ {message}")
                messagebox.showwarning("Invalid Folder", message)
    
    def select_project(self):
        """Select project folder."""
        folder = filedialog.askdirectory(title="Select Project Output Folder")
        if folder:
            self.project_path = folder
            
            # Validate folder
            valid, message = validate_project_path(folder)
            
            if valid:
                self.project_label.configure(
                    text=Path(folder).name,
                    text_color="green"
                )
                self.log_message(f"✓ Project folder: {folder}")
            else:
                self.project_label.configure(text=message, text_color="red")
                self.log_message(f"✗ {message}")
                messagebox.showwarning("Invalid Folder", message)
    
    def update_config(self):
        """Update configuration from UI."""
        self.config['use_gpu'] = self.gpu_var.get()
        self.config['matcher_type'] = self.matcher_var.get()
        self.config['include_dense'] = self.dense_var.get()
        
        # Fisheye options
        self.config['fisheye_enabled'] = self.fisheye_var.get()
        self.config['camera_model'] = self.camera_model_var.get()
        self.config['camera_params'] = self.camera_params_entry.get()
        self.config['single_camera'] = self.single_camera_var.get()
        
        # 3DGUT options
        self.config['dgut_enabled'] = self.dgut_var.get()
        self.config['dgut_mcmc'] = self.mcmc_var.get()
        try:
            self.config['dgut_iterations'] = int(self.iterations_var.get() or 30000)
        except ValueError:
            self.config['dgut_iterations'] = 30000
        self.config['dgut_export_ply'] = self.export_ply_var.get()
    
    def check_installations(self):
        """Check if COLMAP and GloMAP are installed."""
        if not self.colmap or not self.glomap:
            self.log_message("⚠ Warning: Could not initialize wrappers")
            return
        
        # Check COLMAP
        colmap_ok, colmap_msg = self.colmap.check_installation()
        if colmap_ok:
            self.log_message(f"✓ COLMAP: {colmap_msg}")
        else:
            self.log_message(f"✗ COLMAP: {colmap_msg}")
            self.log_message("  ERROR: COLMAP is required!")
            messagebox.showerror(
                "COLMAP Not Found",
                "COLMAP is required but not found.\n\n"
                "Please install COLMAP or configure the path in the application."
            )
        
        # Check GloMAP
        glomap_ok, glomap_msg = self.glomap.check_installation()
        if glomap_ok:
            self.log_message(f"✓ GloMAP: {glomap_msg} (10-100x faster reconstruction!)")
        else:
            self.log_message(f"⚠ GloMAP: {glomap_msg}")
            self.log_message("  Note: Will use COLMAP mapper (slower but works)")
            self.log_message("  Run 'python install_glomap.py' for GloMAP options")
        
        # Check 3DGUT
        if self.dgut:
            dgut_ok, dgut_msg = self.dgut.check_installation()
            if dgut_ok:
                self.log_message(f"✓ 3DGUT: {dgut_msg} (Gaussian Splatting ready!)")
            else:
                self.log_message(f"⚠ 3DGUT: {dgut_msg}")
                self.log_message("  Install: git clone https://github.com/nv-tlabs/3dgrut && cd 3dgrut && ./install.sh")
                self.log_message("  Alternative: Use Dense Reconstruction for point clouds")
    
    def run_pipeline(self):
        """Run the complete photogrammetry pipeline."""
        # Validate inputs
        if not self.image_path:
            messagebox.showwarning("Missing Input", "Please select an images folder")
            return
        
        if not self.project_path:
            messagebox.showwarning("Missing Input", "Please select a project folder")
            return
        
        # Copy images to project if needed
        project_images = Path(self.project_path) / 'images'
        if not project_images.exists() or str(project_images) != str(self.image_path):
            import shutil
            if project_images.exists():
                response = messagebox.askyesno(
                    "Images Exist",
                    "Images folder already exists in project. Use existing images?"
                )
                if not response:
                    return
            else:
                self.log_message(f"Copying images to project folder...")
                try:
                    shutil.copytree(self.image_path, project_images)
                    self.log_message(f"✓ Images copied successfully")
                except Exception as e:
                    self.log_message(f"✗ Failed to copy images: {e}")
                    messagebox.showerror("Error", f"Failed to copy images: {e}")
                    return
        
        # Update config
        self.update_config()
        
        # Disable controls
        self.run_btn.configure(state="disabled")
        self.stop_btn.configure(state="normal")
        self.progress.set(0)
        
        # Clear log
        self.log_text.delete("1.0", "end")
        
        # Create and start worker
        self.worker = PipelineWorker(
            pipeline=self.pipeline,
            project_path=self.project_path,
            config=self.config,
            callback=self.log_message
        )
        self.worker.start()
        
        self.log_message("Starting pipeline...")
    
    def run_dense_only(self):
        """Run dense reconstruction on existing sparse model."""
        # Validate inputs
        if not self.project_path:
            messagebox.showwarning("Missing Input", "Please select a project folder with existing sparse reconstruction")
            return
        
        # Check if sparse reconstruction exists
        sparse_path = Path(self.project_path) / 'sparse' / '0'
        if not sparse_path.exists():
            messagebox.showerror(
                "Sparse Model Not Found",
                "No sparse reconstruction found in the project folder.\n\n"
                "Please run the complete pipeline first to generate the sparse model."
            )
            return
        
        # Confirm action
        response = messagebox.askyesno(
            "Run Dense Reconstruction",
            "This will run dense reconstruction on the existing sparse model.\n\n"
            "This may take a long time depending on the number of images.\n\n"
            "Continue?"
        )
        if not response:
            return
        
        # Disable controls
        self.run_btn.configure(state="disabled")
        self.dense_btn.configure(state="disabled")
        self.stop_btn.configure(state="normal")
        self.progress.set(0)
        
        # Clear log
        self.log_text.delete("1.0", "end")
        
        # Create and start worker
        self.worker = DenseOnlyWorker(
            pipeline=self.pipeline,
            project_path=self.project_path,
            callback=self.log_message
        )
        self.worker.start()
        
        self.log_message("Starting dense reconstruction...")
    
    def run_3dgut(self):
        """Run 3DGUT Gaussian Splatting on existing sparse model."""
        if not self.project_path:
            messagebox.showwarning("Missing Input", "Please select a project folder")
            return
        
        # Check if 3DGUT is installed
        if not self.dgut:
            messagebox.showerror("3DGUT Not Found", "3DGUT is not installed or configured.")
            return
        
        ok, msg = self.dgut.check_installation()
        if not ok:
            messagebox.showerror(
                "3DGUT Not Available",
                f"{msg}\n\n"
                "3DGUT (3D GRUT) is from NVIDIA Research.\n\n"
                "Installation:\n"
                "git clone https://github.com/nv-tlabs/3dgrut\n"
                "cd 3dgrut\n"
                "./install.sh  # Linux (CUDA 11.8/12.8)\n\n"
                "See GUIA_3DGRUT_INSTALACAO.md for detailed instructions.\n\n"
                "Alternative: Use 'Include Dense Reconstruction' for point clouds."
            )
            return
        
        # Check if sparse reconstruction exists (unless using depth-based init)
        sparse_path = Path(self.project_path) / 'sparse' / '0'
        images_path = Path(self.project_path) / 'images'
        
        if not images_path.exists() or not any(images_path.iterdir()):
            messagebox.showerror(
                "Images Not Found",
                "No images found in the project folder.\n\nPlease ensure images are in the 'images' subfolder."
            )
            return
        
        if not sparse_path.exists():
            response = messagebox.askyesno(
                "Sparse Model Not Found",
                "No sparse reconstruction found in the project folder.\n\n"
                "3DGUT requires either:\n"
                "1. Existing sparse model (run Complete Pipeline first)\n"
                "2. Depth-based initialization (UniK3D - not yet implemented)\n\n"
                "Do you want to run the complete pipeline first?"
            )
            if response:
                self.run_pipeline()
            return
        
        # Update config
        self.update_config()
        
        # Determine camera model
        camera_model = 'fisheye' if self.config['fisheye_enabled'] else 'perspective'
        
        # Confirm action
        response = messagebox.askyesno(
            "Run 3DGUT Training",
            f"Train 3D Gaussian Splatting model:\n\n"
            f"• Camera: {camera_model}\n"
            f"• Iterations: {self.config['dgut_iterations']:,}\n"
            f"• MCMC: {'Enabled' if self.config['dgut_mcmc'] else 'Disabled'}\n"
            f"• Export PLY: {'Yes' if self.config['dgut_export_ply'] else 'No'}\n\n"
            f"⏱ Estimated time: 30-80 minutes (RTX 4090)\n"
            f"💾 GPU memory required: ~16 GB\n\n"
            f"Continue?"
        )
        if not response:
            return
        
        # Disable controls
        self.run_btn.configure(state="disabled")
        self.dense_btn.configure(state="disabled")
        self.dgut_btn.configure(state="disabled")
        self.stop_btn.configure(state="normal")
        self.progress.set(0)
        
        # Clear log
        self.log_text.delete("1.0", "end")
        
        self.log_message("Starting 3DGUT training...")
        self.log_message(f"Camera model: {camera_model}")
        self.log_message(f"MCMC optimization: {'Enabled' if self.config['dgut_mcmc'] else 'Disabled'}")
        self.log_message(f"Training iterations: {self.config['dgut_iterations']:,}")
        self.log_message("")
        
        # Start 3DGUT worker thread for background processing
        self.worker = DGUTWorker(
            pipeline=self.pipeline,
            project_path=self.project_path,
            config=self.config.copy(),
            callback=self.log_message
        )
        self.worker.start()
        
        # Start checking for messages from worker
        self.check_worker_messages()
    
    def stop_pipeline(self):
        """Stop the running pipeline."""
        if self.worker and self.worker.is_running():
            self.log_message("⚠ Stopping pipeline (current step will finish)...")
            # Note: Actual stopping requires more complex implementation
            # For now, we just mark it as stopped
        
        self.run_btn.configure(state="normal")
        self.dense_btn.configure(state="normal")
        self.dgut_btn.configure(state="normal")
        self.stop_btn.configure(state="disabled")
    
    def check_worker_messages(self):
        """Check for messages from worker thread."""
        if self.worker:
            message = self.worker.get_message(timeout=0.01)
            
            if message:
                msg_type, msg_data = message
                
                if msg_type == 'progress':
                    # Progress update - already logged by callback
                    self.progress.set(0.5)  # Indeterminate progress
                
                elif msg_type == 'finished':
                    success, result_msg, paths = msg_data
                    
                    if success:
                        self.log_message("")
                        self.log_message("=" * 60)
                        self.log_message("  ✓ PIPELINE COMPLETED SUCCESSFULLY!")
                        self.log_message("=" * 60)
                        self.progress.set(1.0)
                        self.open_btn.configure(state="normal")
                        messagebox.showinfo("Success", "Pipeline completed successfully!")
                    else:
                        self.log_message("")
                        self.log_message(f"✗ Pipeline failed: {result_msg}")
                        self.progress.set(0)
                        messagebox.showerror("Error", f"Pipeline failed:\n{result_msg}")
                    
                    self.run_btn.configure(state="normal")
                    self.dense_btn.configure(state="normal")
                    self.dgut_btn.configure(state="normal")
                    self.stop_btn.configure(state="disabled")
                
                elif msg_type == 'error':
                    self.log_message(f"✗ Error: {msg_data}")
                    self.progress.set(0)
                    self.run_btn.configure(state="normal")
                    self.dense_btn.configure(state="normal")
                    self.dgut_btn.configure(state="normal")
                    self.stop_btn.configure(state="disabled")
                    messagebox.showerror("Error", f"An error occurred:\n{msg_data}")
        
        # Schedule next check
        self.after(100, self.check_worker_messages)
    
    def open_output(self):
        """Open the output folder."""
        if self.project_path:
            os.startfile(self.project_path)
    
    def log_message(self, message):
        """
        Add message to log display.
        
        Args:
            message: Message to log
        """
        self.log_text.insert("end", message + "\n")
        self.log_text.see("end")
        self.logger.info(message)
    
    def on_closing(self):
        """Handle window closing."""
        if self.worker and self.worker.is_running():
            response = messagebox.askyesno(
                "Pipeline Running",
                "Pipeline is still running. Are you sure you want to exit?"
            )
            if not response:
                return
        
        self.destroy()


def main():
    """Run the application."""
    app = MainWindow()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()


if __name__ == "__main__":
    main()
