"""COLMAP command wrapper for photogrammetry processing."""
import os
import subprocess
from pathlib import Path


class COLMAPWrapper:
    """Wrapper class for COLMAP commands."""
    
    def __init__(self, colmap_path=None):
        """
        Initialize COLMAP wrapper.
        
        Args:
            colmap_path: Path to COLMAP executable. If None, assumes it's in PATH.
        """
        if colmap_path:
            # Try different possible locations
            bat_path = Path(colmap_path) / "COLMAP.bat"
            exe_path = Path(colmap_path) / "bin" / "colmap.exe"
            
            if bat_path.exists():
                self.colmap_exe = str(bat_path)
            elif exe_path.exists():
                self.colmap_exe = str(exe_path)
            else:
                # Fallback to exe in root
                self.colmap_exe = str(Path(colmap_path) / "colmap.exe")
        else:
            self.colmap_exe = "colmap"
    
    def feature_extraction(self, database_path, image_path, use_gpu=True, 
                          max_features=8192, camera_model=None, camera_params=None, 
                          single_camera=False, callback=None):
        """
        Extract features from images.
        
        Args:
            database_path: Path to COLMAP database file
            image_path: Path to images folder
            use_gpu: Enable GPU acceleration
            max_features: Maximum number of features per image
            camera_model: Camera model (e.g., 'OPENCV_FISHEYE', 'SIMPLE_RADIAL_FISHEYE', 'RADIAL_FISHEYE', 'FOV')
            camera_params: Camera parameters as string (e.g., "fx,fy,cx,cy,k1,k2,k3,k4")
            single_camera: Force single camera for all images
            callback: Function to call with output lines
            
        Returns:
            Tuple of (success, message)
        """
        cmd = [
            self.colmap_exe,
            "feature_extractor",
            "--database_path", str(database_path),
            "--image_path", str(image_path),
            "--SiftExtraction.use_gpu", "1" if use_gpu else "0",
            "--SiftExtraction.max_num_features", str(max_features),
            "--SiftExtraction.first_octave", "-1"
        ]
        
        # Add fisheye camera support
        if camera_model:
            cmd.extend(["--ImageReader.camera_model", camera_model])
        
        if camera_params:
            cmd.extend(["--ImageReader.camera_params", camera_params])
        
        if single_camera:
            cmd.extend(["--ImageReader.single_camera", "1"])
        
        # Increase max image size for fisheye images
        if camera_model and 'FISHEYE' in camera_model.upper():
            cmd.extend(["--SiftExtraction.max_image_size", "4000"])
        
        return self._run_command(cmd, callback)
    
    def sequential_matcher(self, database_path, overlap=10, callback=None):
        """
        Match features sequentially.
        
        Args:
            database_path: Path to COLMAP database file
            overlap: Number of overlapping images to match
            callback: Function to call with output lines
            
        Returns:
            Tuple of (success, message)
        """
        cmd = [
            self.colmap_exe,
            "sequential_matcher",
            "--database_path", str(database_path),
            "--SequentialMatching.overlap", str(overlap)
        ]
        
        return self._run_command(cmd, callback)
    
    def exhaustive_matcher(self, database_path, callback=None):
        """
        Match features exhaustively.
        
        Args:
            database_path: Path to COLMAP database file
            callback: Function to call with output lines
            
        Returns:
            Tuple of (success, message)
        """
        cmd = [
            self.colmap_exe,
            "exhaustive_matcher",
            "--database_path", str(database_path)
        ]
        
        return self._run_command(cmd, callback)
    
    def mapper(self, database_path, image_path, output_path, callback=None):
        """
        Run COLMAP's incremental mapper for sparse reconstruction.
        
        Note: This is slower than GloMAP but doesn't require separate installation.
        
        Args:
            database_path: Path to COLMAP database file
            image_path: Path to images folder
            output_path: Path to output sparse reconstruction
            callback: Function to call with output lines
            
        Returns:
            Tuple of (success, message)
        """
        # Ensure output directory exists
        os.makedirs(output_path, exist_ok=True)
        
        cmd = [
            self.colmap_exe,
            "mapper",
            "--database_path", str(database_path),
            "--image_path", str(image_path),
            "--output_path", str(output_path)
        ]
        
        return self._run_command(cmd, callback)
    
    def image_undistorter(self, image_path, input_path, output_path, callback=None):
        """
        Undistort images for dense reconstruction.
        
        Args:
            image_path: Path to original images
            input_path: Path to sparse reconstruction
            output_path: Path to output dense workspace
            callback: Function to call with output lines
            
        Returns:
            Tuple of (success, message)
        """
        cmd = [
            self.colmap_exe,
            "image_undistorter",
            "--image_path", str(image_path),
            "--input_path", str(input_path),
            "--output_path", str(output_path),
            "--max_image_size", "2000"
        ]
        
        return self._run_command(cmd, callback)
    
    def patch_match_stereo(self, workspace_path, callback=None):
        """
        Compute stereo depth maps.
        
        Args:
            workspace_path: Path to dense workspace
            callback: Function to call with output lines
            
        Returns:
            Tuple of (success, message)
        """
        cmd = [
            self.colmap_exe,
            "patch_match_stereo",
            "--workspace_path", str(workspace_path),
            "--PatchMatchStereo.window_radius", "5"
        ]
        
        return self._run_command(cmd, callback)
    
    def stereo_fusion(self, workspace_path, output_path, callback=None):
        """
        Fuse depth maps into point cloud.
        
        Args:
            workspace_path: Path to dense workspace
            output_path: Path to output PLY file
            callback: Function to call with output lines
            
        Returns:
            Tuple of (success, message)
        """
        cmd = [
            self.colmap_exe,
            "stereo_fusion",
            "--workspace_path", str(workspace_path),
            "--output_path", str(output_path),
            "--StereoFusion.min_num_pixels", "3"
        ]
        
        return self._run_command(cmd, callback)
    
    def model_converter(self, input_path, output_path, output_type="PLY", callback=None):
        """
        Convert sparse model to different format.
        
        Args:
            input_path: Path to sparse model
            output_path: Path to output file
            output_type: Output format (PLY, TXT, BIN)
            callback: Function to call with output lines
            
        Returns:
            Tuple of (success, message)
        """
        cmd = [
            self.colmap_exe,
            "model_converter",
            "--input_path", str(input_path),
            "--output_path", str(output_path),
            "--output_type", output_type
        ]
        
        return self._run_command(cmd, callback)
    
    def _run_command(self, cmd, callback=None):
        """
        Run a COLMAP command.
        
        Args:
            cmd: Command list to execute
            callback: Function to call with each output line
            
        Returns:
            Tuple of (success, message)
        """
        try:
            # Quote all paths to handle spaces and special characters
            quoted_cmd = []
            for arg in cmd:
                if isinstance(arg, (str, Path)):
                    arg_str = str(arg)
                    # Quote if contains spaces or special characters
                    if ' ' in arg_str or any(c in arg_str for c in ['(', ')', '&']):
                        quoted_cmd.append(f'"{arg_str}"')
                    else:
                        quoted_cmd.append(arg_str)
                else:
                    quoted_cmd.append(str(arg))
            
            # On Windows, use shell=True to properly handle quoted paths
            is_windows = os.name == 'nt'
            if is_windows:
                cmd_str = ' '.join(quoted_cmd)
                process = subprocess.Popen(
                    cmd_str,
                    shell=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    universal_newlines=True,
                    encoding='utf-8',
                    errors='replace'
                )
            else:
                process = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    universal_newlines=True,
                    encoding='utf-8',
                    errors='replace'
                )
            
            output_lines = []
            while True:
                line = process.stdout.readline()
                if line == '' and process.poll() is not None:
                    break
                if line:
                    line = line.strip()
                    output_lines.append(line)
                    if callback:
                        callback(line)
            
            rc = process.poll()
            success = (rc == 0)
            
            if success:
                return True, "Command completed successfully"
            else:
                return False, f"Command failed with return code {rc}"
                
        except FileNotFoundError:
            return False, f"COLMAP executable not found: {self.colmap_exe}"
        except Exception as e:
            return False, f"Error running command: {str(e)}"
    
    def check_installation(self):
        """
        Check if COLMAP is properly installed.
        
        Returns:
            Tuple of (is_installed, version_string)
        """
        try:
            result = subprocess.run(
                [self.colmap_exe, "-h"],
                capture_output=True,
                text=True,
                timeout=5
            )
            return True, "COLMAP installed"
        except FileNotFoundError:
            return False, "COLMAP not found"
        except Exception as e:
            return False, str(e)
