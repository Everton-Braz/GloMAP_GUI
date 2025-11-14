"""GloMAP command wrapper for fast global SfM."""
import os
import subprocess
from pathlib import Path


class GloMAPWrapper:
    """Wrapper class for GloMAP commands."""
    
    def __init__(self, glomap_path=None):
        """
        Initialize GloMAP wrapper.
        
        Args:
            glomap_path: Path to GloMAP executable. If None, assumes it's in PATH.
        """
        if glomap_path:
            self.glomap_exe = str(Path(glomap_path) / "glomap.exe")
        else:
            # Try conda installation first
            conda_glomap = Path("C:/Users/User/miniconda3/Library/bin/glomap.exe")
            if conda_glomap.exists():
                self.glomap_exe = str(conda_glomap)
            else:
                self.glomap_exe = "glomap"
    
    def mapper(self, database_path, image_path, output_path, callback=None):
        """
        Run GloMAP mapper for sparse reconstruction.
        
        This is 10-100x faster than COLMAP's incremental mapper while
        maintaining comparable quality.
        
        Args:
            database_path: Path to COLMAP database file with features
            image_path: Path to images folder
            output_path: Path to output sparse reconstruction
            callback: Function to call with output lines
            
        Returns:
            Tuple of (success, message)
        """
        # Ensure output directory exists
        os.makedirs(output_path, exist_ok=True)
        
        cmd = [
            self.glomap_exe,
            "mapper",
            "--database_path", str(database_path),
            "--image_path", str(image_path),
            "--output_path", str(output_path)
        ]
        
        return self._run_command(cmd, callback)
    
    def _run_command(self, cmd, callback=None):
        """
        Run a GloMAP command.
        
        Args:
            cmd: Command list to execute
            callback: Function to call with each output line
            
        Returns:
            Tuple of (success, message)
        """
        try:
            # Set up environment to include conda DLLs
            env = os.environ.copy()
            conda_bin = "C:/Users/User/miniconda3/Library/bin"
            if os.path.exists(conda_bin):
                env['PATH'] = conda_bin + os.pathsep + env.get('PATH', '')
            
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                encoding='utf-8',
                errors='replace',
                env=env
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
                return True, "GloMAP mapper completed successfully"
            else:
                return False, f"GloMAP mapper failed with return code {rc}"
                
        except FileNotFoundError:
            return False, f"GloMAP executable not found: {self.glomap_exe}"
        except Exception as e:
            return False, f"Error running GloMAP: {str(e)}"
    
    def check_installation(self):
        """
        Check if GloMAP is properly installed.
        
        Returns:
            Tuple of (is_installed, version_string)
        """
        try:
            result = subprocess.run(
                [self.glomap_exe, "-h"],
                capture_output=True,
                text=True,
                timeout=5
            )
            return True, "GloMAP installed"
        except FileNotFoundError:
            return False, "GloMAP not found"
        except Exception as e:
            return False, str(e)
