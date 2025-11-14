# Building GloMAP on Windows - Complete Guide

## Current Status
- ✅ CMake installed
- ✅ Visual Studio 2019 Build Tools
- ✅ CUDA 11.8
- ❌ Missing dependencies: Eigen3, Ceres Solver, and others

## Option 1: Install vcpkg and Dependencies (RECOMMENDED)

vcpkg is Microsoft's C++ package manager - the easiest way to get all dependencies.

### Step 1: Install vcpkg
```powershell
cd C:\
git clone https://github.com/microsoft/vcpkg
cd vcpkg
.\bootstrap-vcpkg.bat
.\vcpkg integrate install
```

### Step 2: Install GloMAP Dependencies
```powershell
cd C:\vcpkg
.\vcpkg install eigen3:x64-windows
.\vcpkg install ceres:x64-windows
.\vcpkg install glog:x64-windows
.\vcpkg install gflags:x64-windows
.\vcpkg install freeimage:x64-windows
.\vcpkg install glew:x64-windows
.\vcpkg install sqlite3:x64-windows
```

**Note**: This will take 30-60 minutes but handles all dependencies automatically.

### Step 3: Build GloMAP with vcpkg
```powershell
cd C:\Users\User\Documents\APLICATIVOS\GloMAP_GUI\glomap\build

# Configure with vcpkg toolchain
& "C:\Program Files\CMake\bin\cmake.exe" .. `
  -G "Visual Studio 16 2019" -A x64 `
  -DCMAKE_TOOLCHAIN_FILE=C:/vcpkg/scripts/buildsystems/vcpkg.cmake `
  -DCMAKE_CUDA_ARCHITECTURES=native

# Build
& "C:\Program Files\CMake\bin\cmake.exe" --build . --config Release
```

### Step 4: Copy GloMAP to COLMAP directory
```powershell
copy Release\glomap.exe "C:\Users\User\Documents\colmap-x64-windows-cuda\bin\"
```

---

## Option 2: Use Conda (FASTER - 10 minutes)

If you have Anaconda or Miniconda:

```powershell
conda create -n glomap python=3.10
conda activate glomap
conda install -c conda-forge glomap
```

Then copy the glomap executable to your COLMAP bin directory.

---

## Option 3: Download Pre-built Binary (FASTEST - if available)

Check GitHub releases:
```powershell
Start-Process "https://github.com/colmap/glomap/releases"
```

Look for Windows binaries. If available, download and extract to:
`C:\Users\User\Documents\colmap-x64-windows-cuda\bin\`

---

## Option 4: Use Docker with GloMAP (Alternative)

Run GloMAP in a Docker container with pre-built environment.

---

## My Recommendation

**For you, I recommend Option 1 (vcpkg)** because:
- ✅ You already have Visual Studio and CUDA
- ✅ Most reliable on Windows
- ✅ One-time setup (30-60 min), then you're done
- ✅ Can build other COLMAP-related tools later

**Quick start now, optimize later:**
Your application works perfectly with COLMAP mapper right now. You can:
1. Use it today for smaller projects (< 50 images)
2. Install vcpkg and build GloMAP over the weekend
3. Upgrade to faster processing when ready

---

## Quick Commands to Start vcpkg Installation

Want me to set this up? Run these commands:

```powershell
# Navigate to C drive
cd C:\

# Clone vcpkg
git clone https://github.com/microsoft/vcpkg

# Bootstrap vcpkg
cd vcpkg
.\bootstrap-vcpkg.bat

# Integrate with Visual Studio
.\vcpkg integrate install

# Start installing dependencies (this takes a while)
.\vcpkg install eigen3:x64-windows ceres:x64-windows glog:x64-windows gflags:x64-windows
```

Then come back and we'll build GloMAP.

---

## Time Estimates

| Method | Time Required | Complexity |
|--------|--------------|------------|
| vcpkg | 30-60 min | Medium |
| Conda | 5-10 min | Easy |
| Pre-built binary | 2 min | Very Easy |
| Docker | 15 min | Medium |
| Manual dependencies | 2-4 hours | Hard |

---

## Current Application Status

**Your GUI application is FULLY WORKING right now!**

- ✅ Can process images
- ✅ Creates point clouds
- ✅ Uses COLMAP mapper (reliable, just slower)
- ✅ All features functional

**When you add GloMAP:**
- Same features
- 10-100x faster sparse reconstruction
- Better for large datasets

---

Would you like me to help you set up vcpkg and build GloMAP?
