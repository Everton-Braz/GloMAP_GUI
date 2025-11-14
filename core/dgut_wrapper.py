"""Wrapper for 3DGUT (3D Gaussian Unscented Transform) operations."""
import subprocess
import os
from pathlib import Path


class DGUTWrapper:
    """Wrapper for 3DGUT Gaussian Splatting with fisheye support."""
    
    def __init__(self, dgut_path=None):
        """
        Initialize 3DGUT wrapper.
        
        Args:
            dgut_path: Path to 3DGUT installation (train.py location)
        """
        self.dgut_path = dgut_path
        self.train_script = None
        self.render_script = None
        self.export_script = None
        
        # Try to locate 3DGUT installation
        self._locate_dgut()
    
    def _locate_dgut(self):
        """Attempt to locate 3D GRUT installation."""
        if self.dgut_path:
            dgut_path = Path(self.dgut_path)
            self.train_script = dgut_path / "train.py"
            self.render_script = dgut_path / "render.py"
            self.export_script = dgut_path / "export_ply.py"
        else:
            # Check common locations (both 3dgrut and 3DGUT for compatibility)
            possible_paths = [
                Path.home() / "3dgrut",
                Path.home() / "3DGUT",
                Path.home() / "Documents" / "3dgrut",
                Path.home() / "Documents" / "3DGUT",
                Path("C:/3dgrut"),
                Path("C:/3DGUT"),
                Path("3dgrut"),
                Path("3DGUT")
            ]
            
            for path in possible_paths:
                train_py = path / "train.py"
                if train_py.exists():
                    self.dgut_path = str(path)
                    self.train_script = train_py
                    self.render_script = path / "render.py"
                    self.export_script = path / "export_ply.py"
                    break
    
    def check_installation(self):
        """
        Check if 3DGUT is installed and accessible.
        
        Returns:
            Tuple of (success, message)
        """
        if self.train_script and self.train_script.exists():
            return True, "3DGUT installed"
        return False, "3DGUT not found. Install: https://github.com/nv-tlabs/3dgrut"
    
    def train(self, source_path, model_path, camera_model='perspective',
              use_mcmc=True, iterations=30000, down_sample_factor=2, 
              with_gui=False, export_ply=True, callback=None):
        """
        Train 3D GRUT Gaussian Splatting model.
        
        Args:
            source_path: Path to project folder (contains images/ and sparse/)
            model_path: Output path for trained model
            camera_model: 'perspective' or 'fisheye' (mapped to colmap/mcmc config)
            use_mcmc: Enable MCMC optimization (uses 'mcmc' config)
            iterations: Training iterations (not used directly, controlled by config)
            down_sample_factor: Resolution reduction (1=full, 2=half, 4=quarter)
            with_gui: Open interactive viewer during training
            export_ply: Export PLY point cloud after training
            callback: Progress callback function
            
        Returns:
            Tuple of (success, message)
        """
        if not self.train_script or not self.train_script.exists():
            return False, "3D GRUT not installed"
        
        # Choose config based on settings
        config_name = "mcmc" if use_mcmc else "colmap"
        
        # Build command following 3D GRUT conventions
        cmd = [
            "python",
            str(self.train_script),
            "--config_name", config_name,
            "--data.path", str(source_path),
            "--output_dir", str(model_path),
            "--down_sample_factor", str(down_sample_factor),
            "--export_ply_enabled", "true" if export_ply else "false"
        ]
        
        # Add GUI option (note: requires manual "Train" checkbox activation)
        if with_gui:
            cmd.extend(["--with_gui", "true"])
        
        if callback:
            callback(f"Training 3D GRUT...")
            callback(f"  Config: {config_name}")
            callback(f"  Data: {source_path}")
            callback(f"  Output: {model_path}")
            callback(f"  Downsample: {down_sample_factor}x")
            if with_gui:
                callback("  GUI: Enabled (remember to click 'Train' checkbox!)")
            callback("")
            callback(f"Command: {' '.join(cmd)}")
            callback("")
        
        # Run training
        return self._run_command(cmd, callback)
    
    def render(self, model_path, camera_model='perspective', iteration=30000,
               skip_train=True, render_path=None, output_path=None, callback=None):
        """
        Render views from trained 3DGUT model.
        
        Args:
            model_path: Path to trained model
            camera_model: 'perspective' or 'fisheye'
            iteration: Which checkpoint to render
            skip_train: Skip training images
            render_path: Custom camera path for rendering
            output_path: Output folder for rendered images
            callback: Progress callback function
            
        Returns:
            Tuple of (success, message)
        """
        if not self.render_script or not self.render_script.exists():
            return False, "3DGUT render script not found"
        
        cmd = [
            "python",
            str(self.render_script),
            "--model_path", str(model_path),
            "--camera_model", camera_model,
            "--iteration", str(iteration)
        ]
        
        if skip_train:
            cmd.append("--skip_train")
        
        if render_path:
            cmd.extend(["--render_path", str(render_path)])
        
        if output_path:
            cmd.extend(["--output_path", str(output_path)])
        
        if callback:
            callback(f"Rendering 3DGUT model...")
        
        return self._run_command(cmd, callback)
    
    def export_pointcloud(self, model_path, output_path, num_points=1000000, callback=None):
        """
        Export 3DGUT model to PLY point cloud.
        
        Args:
            model_path: Path to trained model
            output_path: Output PLY file path
            num_points: Number of points to export
            callback: Progress callback function
            
        Returns:
            Tuple of (success, message)
        """
        if not self.export_script or not self.export_script.exists():
            return False, "3DGUT export script not found"
        
        cmd = [
            "python",
            str(self.export_script),
            "--model_path", str(model_path),
            "--output", str(output_path),
            "--num_points", str(num_points)
        ]
        
        if callback:
            callback(f"Exporting point cloud ({num_points:,} points)...")
        
        return self._run_command(cmd, callback)
    
    def _run_command(self, cmd, callback=None):
        """
        Run a 3DGUT command.
        
        Args:
            cmd: Command list to execute
            callback: Progress callback function
            
        Returns:
            Tuple of (success, message)
        """
        try:
            # Set up environment
            env = os.environ.copy()
            
            # Run command with streaming output
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                env=env,
                bufsize=1
            )
            
            # Stream output
            output_lines = []
            for line in process.stdout:
                line = line.rstrip()
                output_lines.append(line)
                if callback:
                    callback(line)
            
            # Wait for completion
            process.wait()
            
            if process.returncode == 0:
                return True, "3DGUT operation completed successfully"
            else:
                error_msg = '\n'.join(output_lines[-20:])  # Last 20 lines
                return False, f"3DGUT failed: {error_msg}"
                
        except FileNotFoundError:
            return False, "Python not found in PATH"
        except Exception as e:
            return False, f"Error running 3DGUT: {str(e)}"
