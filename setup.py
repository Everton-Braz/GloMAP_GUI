"""
Installation and Setup Script for GloMAP Photogrammetry GUI
"""
import subprocess
import sys
import os
from pathlib import Path


def check_python_version():
    """Check if Python version is 3.8 or higher."""
    print("Checking Python version...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"❌ Python 3.8+ required, found {version.major}.{version.minor}")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro}")
    return True


def install_requirements():
    """Install required Python packages."""
    print("\nInstalling Python requirements...")
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ])
        print("✅ Requirements installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install requirements: {e}")
        return False


def check_colmap():
    """Check if COLMAP is installed."""
    print("\nChecking COLMAP installation...")
    try:
        result = subprocess.run(
            ["colmap", "-h"],
            capture_output=True,
            text=True,
            timeout=5
        )
        print("✅ COLMAP is installed")
        return True
    except FileNotFoundError:
        print("⚠️  COLMAP not found in PATH")
        print("   Please install COLMAP from: https://github.com/colmap/colmap/releases")
        return False
    except Exception as e:
        print(f"⚠️  Error checking COLMAP: {e}")
        return False


def check_glomap():
    """Check if GloMAP is installed."""
    print("\nChecking GloMAP installation...")
    try:
        result = subprocess.run(
            ["glomap", "-h"],
            capture_output=True,
            text=True,
            timeout=5
        )
        print("✅ GloMAP is installed")
        return True
    except FileNotFoundError:
        print("⚠️  GloMAP not found in PATH")
        print("   Please install GloMAP from: https://github.com/colmap/glomap/releases")
        return False
    except Exception as e:
        print(f"⚠️  Error checking GloMAP: {e}")
        return False


def create_directories():
    """Create necessary directories."""
    print("\nCreating application directories...")
    dirs = ['logs', 'projects']
    for dir_name in dirs:
        Path(dir_name).mkdir(exist_ok=True)
    print("✅ Directories created")


def test_imports():
    """Test if all required packages can be imported."""
    print("\nTesting package imports...")
    packages = {
        'customtkinter': 'CustomTkinter',
    }
    
    all_ok = True
    for module, name in packages.items():
        try:
            __import__(module)
            print(f"✅ {name}")
        except ImportError:
            print(f"❌ {name} - not installed")
            all_ok = False
    
    return all_ok


def main():
    """Run the setup process."""
    print("=" * 60)
    print("  GloMAP Photogrammetry GUI - Setup")
    print("=" * 60)
    
    steps = [
        ("Python Version", check_python_version),
        ("Python Packages", install_requirements),
        ("Package Imports", test_imports),
        ("COLMAP", check_colmap),
        ("GloMAP", check_glomap),
        ("Directories", lambda: (create_directories(), True)[1])
    ]
    
    results = []
    for step_name, step_func in steps:
        try:
            result = step_func()
            results.append((step_name, result))
        except Exception as e:
            print(f"❌ Error in {step_name}: {e}")
            results.append((step_name, False))
    
    print("\n" + "=" * 60)
    print("  Setup Summary")
    print("=" * 60)
    
    for step_name, result in results:
        status = "✅" if result else "⚠️ "
        print(f"{status} {step_name}")
    
    all_ok = all(result for _, result in results if _ in ["Python Version", "Python Packages", "Package Imports"])
    
    print("\n" + "=" * 60)
    if all_ok:
        print("✅ Setup completed successfully!")
        print("\nYou can now run the application with:")
        print("  python main.py")
    else:
        print("⚠️  Setup completed with warnings")
        print("\nSome components are missing. Please install:")
        print("  - COLMAP: https://github.com/colmap/colmap/releases")
        print("  - GloMAP: https://github.com/colmap/glomap/releases")
        print("\nYou can still run the application, but it may not work properly.")
    print("=" * 60)


if __name__ == "__main__":
    main()
