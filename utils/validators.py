"""Input validation utilities."""
import os
from pathlib import Path


class ValidationError(Exception):
    """Custom exception for validation errors."""
    pass


def validate_image_folder(path):
    """
    Validate image folder before processing.
    
    Args:
        path: Path to image folder
        
    Returns:
        Tuple of (is_valid, message, image_count)
        
    Raises:
        ValidationError: If validation fails critically
    """
    path = Path(path)
    
    # Check if folder exists
    if not path.exists():
        return False, "Folder does not exist", 0
    
    if not path.is_dir():
        return False, "Path is not a directory", 0
    
    # Check for supported image formats
    valid_exts = {'.jpg', '.jpeg', '.png', '.bmp', '.tif', '.tiff', '.JPG', '.JPEG', '.PNG'}
    images = [f for f in path.iterdir() 
              if f.is_file() and f.suffix in valid_exts]
    
    image_count = len(images)
    
    if image_count < 3:
        return False, f"Need at least 3 images for reconstruction (found {image_count})", image_count
    
    # Check if images are readable
    try:
        test_image = images[0]
        with open(test_image, 'rb') as f:
            f.read(100)  # Read first 100 bytes to test
    except Exception as e:
        return False, f"Cannot read images: {str(e)}", image_count
    
    return True, f"Found {image_count} valid images", image_count


def validate_project_path(path):
    """
    Validate project path.
    
    Args:
        path: Project path to validate
        
    Returns:
        Tuple of (is_valid, message)
    """
    path = Path(path)
    
    # Check if parent directory exists
    if not path.parent.exists():
        return False, "Parent directory does not exist"
    
    # Check if we can create/write to the directory
    try:
        path.mkdir(parents=True, exist_ok=True)
        test_file = path / '.test_write'
        test_file.touch()
        test_file.unlink()
        return True, "Project path is valid"
    except PermissionError:
        return False, "No write permission for project path"
    except Exception as e:
        return False, f"Cannot access project path: {str(e)}"


def validate_executable_path(path, exe_name):
    """
    Validate executable path.
    
    Args:
        path: Path to executable
        exe_name: Name of executable
        
    Returns:
        Tuple of (is_valid, message)
    """
    path = Path(path)
    
    if not path.exists():
        return False, f"{exe_name} not found at {path}"
    
    if not path.is_file() and not path.is_dir():
        return False, f"{exe_name} path is invalid"
    
    return True, f"{exe_name} found"


def validate_database_path(path):
    """
    Validate COLMAP database path.
    
    Args:
        path: Path to database file
        
    Returns:
        Tuple of (is_valid, message)
    """
    path = Path(path)
    
    # Database doesn't need to exist yet, but parent must
    if not path.parent.exists():
        return False, "Database directory does not exist"
    
    if path.exists() and not path.is_file():
        return False, "Database path exists but is not a file"
    
    return True, "Database path is valid"


def sanitize_path(path):
    """
    Sanitize and normalize path.
    
    Args:
        path: Path to sanitize
        
    Returns:
        Normalized Path object
    """
    return Path(path).resolve()
