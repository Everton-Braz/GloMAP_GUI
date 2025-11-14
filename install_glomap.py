"""
GloMAP Installation Helper for Windows

GloMAP provides 10-100x faster sparse reconstruction than COLMAP.
This script helps you download and set up GloMAP.
"""
import os
import sys
import subprocess
import urllib.request
import zipfile
from pathlib import Path


def print_header(text):
    """Print a formatted header."""
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60)


def check_git():
    """Check if git is installed."""
    try:
        subprocess.run(["git", "--version"], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def install_glomap_from_source():
    """Install GloMAP from source (requires build tools)."""
    print_header("Building GloMAP from Source")
    
    print("\nThis requires:")
    print("  - Visual Studio 2019 or later with C++ tools")
    print("  - CMake")
    print("  - CUDA Toolkit (optional, for GPU support)")
    
    response = input("\nDo you have these installed? (y/n): ")
    if response.lower() != 'y':
        print("\nPlease install the required tools first:")
        print("  Visual Studio: https://visualstudio.microsoft.com/")
        print("  CMake: https://cmake.org/download/")
        return False
    
    if not check_git():
        print("\n❌ Git is required but not found.")
        print("   Install from: https://git-scm.com/download/win")
        return False
    
    # Clone GloMAP
    glomap_dir = Path("glomap_build")
    if not glomap_dir.exists():
        print("\nCloning GloMAP repository...")
        try:
            subprocess.run([
                "git", "clone", "--recursive",
                "https://github.com/colmap/glomap.git",
                str(glomap_dir)
            ], check=True)
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to clone repository: {e}")
            return False
    
    print("\nGloMAP cloned to:", glomap_dir.absolute())
    print("\nTo build GloMAP:")
    print(f"  1. cd {glomap_dir}")
    print("  2. mkdir build && cd build")
    print("  3. cmake ..")
    print("  4. cmake --build . --config Release")
    print("\nAfter building, copy the glomap.exe to your COLMAP directory")
    
    return True


def use_colmap_mapper_fallback():
    """Configure to use COLMAP's mapper instead of GloMAP."""
    print_header("Using COLMAP Mapper (Fallback)")
    
    print("\nGloMAP is not available, but you can still use COLMAP's mapper.")
    print("Note: COLMAP's mapper is slower but still produces good results.")
    print("\nThe application will automatically fall back to COLMAP mapper")
    print("when GloMAP is not found.")
    
    return True


def main():
    """Main installation helper."""
    print_header("GloMAP Installation Helper")
    
    print("\nGloMAP Options:")
    print("  1. Use COLMAP mapper (slower, no installation needed)")
    print("  2. Build GloMAP from source (advanced, requires build tools)")
    print("  3. Download pre-built binaries (if available)")
    print("  4. Exit")
    
    choice = input("\nSelect option (1-4): ")
    
    if choice == "1":
        use_colmap_mapper_fallback()
        print("\n✅ You can use the application with COLMAP mapper")
        print("   Run: python main.py")
        
    elif choice == "2":
        install_glomap_from_source()
        
    elif choice == "3":
        print("\nPre-built binaries for Windows are not officially available.")
        print("You can:")
        print("  1. Check the releases page: https://github.com/colmap/glomap/releases")
        print("  2. Build from source (option 2)")
        print("  3. Use COLMAP mapper instead (option 1)")
        
    else:
        print("\nExiting...")
        return
    
    print_header("Installation Helper Complete")


if __name__ == "__main__":
    main()
