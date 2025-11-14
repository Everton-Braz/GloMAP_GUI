# GloMAP GUI - Photogrammetry Pipeline with Fisheye Support

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey)

**A modern graphical interface for COLMAP and GloMAP photogrammetry pipelines**

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [Documentation](#-documentation)

</div>

---

## ✨ Features

- 🖥️ **Modern GUI**: Clean interface built with CustomTkinter
- ⚡ **GloMAP Integration**: 10-100x faster sparse reconstruction than COLMAP
- 🐟 **Fisheye Support**: Native support for fisheye camera models (OPENCV_FISHEYE, SIMPLE_RADIAL_FISHEYE, etc.)
- 🎯 **3D GRUT Ready**: Interface prepared for Gaussian Splatting with 3D GRUT (optional)
- 🔄 **Dense-Only Mode**: Run dense reconstruction using existing sparse models
- 📊 **Real-time Progress**: Live output and progress tracking
- 🛠️ **PLY Tools**: Convert and fix PLY files for various viewers (SuperSplat, PlayCanvas, CloudCompare)
- ✅ **Path Handling**: Properly handles spaces and special characters in folder names

## 🚀 Quick Start

### Prerequisites

- **Windows 10/11** (64-bit)
- **Python 3.8+**
- **COLMAP** ([Download](https://github.com/colmap/colmap/releases))
- **CUDA** (optional, for GPU acceleration)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Everton-Braz/GloMAP_GUI.git
   cd GloMAP_GUI
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install GloMAP** (optional, but recommended)
   ```bash
   python install_glomap.py
   ```
   Or manually via conda:
   ```bash
   conda install -c conda-forge glomap
   ```

4. **Configure paths**
   - Edit `config.json` to set your COLMAP and GloMAP paths
   - Or configure via GUI on first run

### Run

```bash
python main.py
```

Or on Windows:
```bash
run.bat
```

## 📖 Usage

### Basic Workflow

1. **Select Images**: Choose your image folder
2. **Create Project**: Set output folder name
3. **Configure Camera**: 
   - Standard: Leave default settings
   - Fisheye: Enable fisheye mode and select camera model
4. **Run Pipeline**: Click "Run Complete Pipeline"
5. **View Results**: Open output folder when complete

### Dense-Only Reconstruction

If you already have a sparse model from COLMAP or GloMAP:

1. Select the sparse reconstruction folder
2. Click "Dense Only" button
3. Wait for depth map computation and fusion

### PLY Conversion Tools

Convert COLMAP PLY files for Gaussian Splatting viewers:

```bash
# Convert to Gaussian Splat format (for SuperSplat/PlayCanvas)
python convert_to_splat.py sparse.ply

# Fix PLY format issues
python fix_ply.py fused.ply --format binary
```

## 📋 Camera Models

Supported fisheye camera models:

- **OPENCV_FISHEYE**: Full fisheye model with 4 distortion parameters (fx, fy, cx, cy, k1, k2, k3, k4)
- **SIMPLE_RADIAL_FISHEYE**: Simplified model with 1 distortion parameter (f, cx, cy, k)
- **RADIAL_FISHEYE**: Similar to SIMPLE_RADIAL with additional parameters (f, cx, cy, k1, k2)
- **FOV**: Field-of-view distortion model (fx, fy, cx, cy, omega)

## 🛠️ Advanced Features

### 3D GRUT Integration (Optional)

For Gaussian Splatting reconstruction:

1. Install 3D GRUT (requires RTX 3060+ with 12GB+ VRAM)
2. Enable 3D GRUT mode in GUI
3. Configure MCMC iterations and export options

⚠️ **Note**: 3D GRUT requires significant GPU resources. See [INSTALL_3DGRUT_WINDOWS_STEP_BY_STEP.md](INSTALL_3DGRUT_WINDOWS_STEP_BY_STEP.md) for details.

### Handling Paths with Spaces

The application now properly handles:
- ✅ Spaces in folder names
- ✅ Special characters (parentheses, ampersands)
- ✅ Accented characters (á, é, ã, ç, etc.)
- ✅ Non-English characters

**Example working paths:**
```
G:/Meu Drive/PROJETOS - CHICO SOMBRA/DATA CENTER/teste
C:/Users/João Silva/Documents/Fotos (2024)/projeto
D:/Photos & Videos/Reconstruction/
```

**Previous Error (Fixed):**
```
Drive\PROJETOS foi inesperado neste momento.
```

This error occurred because paths with spaces weren't properly quoted in subprocess calls. Now fixed! ✅

## 📚 Documentation

- [Quick Start Guide](QUICKSTART.md)
- [GloMAP GUI Guide](GLOMAP_GUI_GUIDE.md)
- [3D GRUT Installation Guide](INSTALL_3DGRUT_WINDOWS_STEP_BY_STEP.md)
- [Full Documentation Index](DOCUMENTATION_INDEX.md)

## 🔧 Troubleshooting

### Common Issues

**1. "COLMAP not found"**
- Set COLMAP path in `config.json`
- Or add COLMAP to system PATH
- Check if COLMAP.bat or colmap.exe exists

**2. "Pipeline failed at feature extraction" with spaces error**
- **Fixed in latest version!** Update to get the fix
- Application now properly quotes all paths

**3. "PLY files won't open in SuperSplat"**
- Use `convert_to_splat.py` to convert to Gaussian Splat format
- COLMAP PLYs are traditional point clouds, not Gaussian Splats
- SuperSplat requires specific properties (sh_*, opacity, scale_*, rot_*)

**4. Out of memory errors**
- Reduce max image size in settings
- Reduce number of features (4096 instead of 8192)
- Use CPU mode instead of GPU
- Process fewer images at once

**5. "GloMAP not found"**
- Install via: `conda install -c conda-forge glomap`
- Or set path in `config.json`
- Application works without GloMAP (uses COLMAP mapper instead)

## 🎓 Tutorials

### Complete Pipeline Example

```bash
# 1. Start GUI
python main.py

# 2. Select your images folder
# Browse to: C:/Users/YourName/Photos/MyProject

# 3. Create project folder
# Set name: MyProject_Reconstruction

# 4. Configure (for standard cameras, use defaults)

# 5. Run Complete Pipeline
# Click "Run Complete Pipeline" button

# 6. Wait for completion
# Monitor progress in log window

# 7. View results
# Click "Open Output Folder"
# sparse/ - Sparse point cloud
# dense/ - Dense point cloud
```

### Fisheye Camera Example

```bash
# 1. Enable fisheye mode in GUI
# Check "Enable Fisheye Support"

# 2. Select camera model
# Choose: OPENCV_FISHEYE

# 3. (Optional) Set camera parameters
# If known: fx,fy,cx,cy,k1,k2,k3,k4

# 4. Enable single camera mode
# If all images from same camera

# 5. Run pipeline
# Click "Run Complete Pipeline"
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- [COLMAP](https://github.com/colmap/colmap) - Structure-from-Motion pipeline
- [GloMAP](https://github.com/colmap/glomap) - Fast global mapper
- [3D GRUT](https://github.com/nv-tlabs/3dgrut) - Gaussian Splatting with uncertainty
- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) - Modern UI library

## 📧 Contact

**Everton Braz** - [@Everton-Braz](https://github.com/Everton-Braz)

**Project Link**: [https://github.com/Everton-Braz/GloMAP_GUI](https://github.com/Everton-Braz/GloMAP_GUI)

## 🐛 Known Issues

- [ ] 3D GRUT requires significant GPU resources (RTX 3060+ recommended)
- [ ] Very large image sets (>5000 images) may require manual memory management
- [ ] Some fisheye models may require manual parameter adjustment

## 🗺️ Roadmap

- [ ] Add batch processing for multiple projects
- [ ] Implement automatic camera parameter detection
- [ ] Add mesh generation support
- [ ] Integrate texture mapping tools
- [ ] Add cloud processing support

---

<div align="center">
Made with ❤️ for the photogrammetry community
</div>
