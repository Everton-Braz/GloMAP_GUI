# GloMAP Photogrammetry GUI

A modern graphical user interface for photogrammetry processing using **GloMAP** (10-100x faster) and **COLMAP** with **fisheye camera support**.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey)

## Features

### ✅ Available Now
- 🚀 **Fast Processing**: GloMAP for 10-100x faster sparse reconstruction
- 🐟 **Fisheye Support**: Handle 180-220° FOV cameras (OPENCV_FISHEYE, RADIAL_FISHEYE, etc.)
- 🎨 **Modern GUI**: Dark-themed interface with CustomTkinter
- 📊 **Real-time Progress**: Live log updates and progress tracking
- ⚙️ **Configurable**: GPU acceleration, multiple matcher types, fisheye models
- 📁 **Point Cloud Export**: Automatic PLY export for sparse and dense reconstructions
- 🔷 **Dense-Only Mode**: Run dense reconstruction on existing sparse models

### ✨ Advanced Features (Optional)
- **3D GRUT Integration**: Full support for 3D Gaussian Splatting with fisheye
- Install: `git clone https://github.com/nv-tlabs/3dgrut` (Linux recommended)
- See `GUIA_3DGRUT_INSTALACAO.md` for complete installation guide (Portuguese)
- Alternatives: Nerfstudio, Fisheye-GS (see `3DGUT_AVAILABILITY_NOTE.md`)

## Prerequisites

### Required Software

1. **Python 3.8+** - [Download](https://www.python.org/downloads/)
2. **COLMAP 3.9+** - [Download](https://github.com/colmap/colmap/releases)
3. **GloMAP 1.0+** - [Download](https://github.com/colmap/glomap/releases) or install via conda

### Optional Software

- **Nerfstudio** - For 3D Gaussian Splatting (alternative to 3DGUT)
- **Fisheye-GS** - For fisheye Gaussian Splatting

### System Requirements

- **CPU**: Multi-core processor (Intel i5 or better)
- **RAM**: 16GB minimum, 32GB+ recommended for fisheye
- **GPU**: CUDA-compatible NVIDIA GPU (optional but recommended)
- **Storage**: SSD with sufficient space for datasets

## Installation

### 1. Clone or Download

```bash
git clone <repository-url>
cd GloMAP_GUI
```

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure COLMAP Path

Edit `gui/main_window.py` and set the correct path to your COLMAP installation:

```python
self.colmap_path = r"C:\path\to\your\colmap-x64-windows-cuda"
```

### 4. Verify Installations

Run the test script to verify all components are installed:

```bash
python -c "import customtkinter; print('CustomTkinter OK')"
```

## Usage

### Running the Application

```bash
python main.py
```

### Workflow

1. **Select Images Folder**: Browse and select folder containing your images
2. **Select Project Folder**: Choose where to save outputs
3. **Configure Options**:
   - Enable/disable GPU acceleration
   - Choose matcher type (sequential or exhaustive)
   - Enable dense reconstruction (optional)
4. **Run Pipeline**: Click "Run Complete Pipeline" button
5. **Monitor Progress**: Watch real-time log updates
6. **View Results**: Click "Open Output" to see generated point clouds

### Output Structure

```
project_folder/
├── images/              # Input images
├── database.db          # COLMAP database
├── sparse/
│   ├── 0/              # Sparse reconstruction
│   └── sparse.ply      # Sparse point cloud
└── dense/              # Dense reconstruction (if enabled)
    └── fused.ply       # Dense point cloud
```

## Configuration

### Default Settings

The application uses these default settings (configurable via GUI):

- **GPU Acceleration**: Enabled
- **Max Features**: 8192 per image
- **Matcher Type**: Sequential
- **Matcher Overlap**: 10 images
- **Dense Reconstruction**: Disabled (faster processing)

### Advanced Configuration

Edit `gui/main_window.py` to modify default configurations:

```python
self.config = {
    'use_gpu': True,
    'matcher_type': 'sequential',
    'include_dense': False,
    'max_features': 8192,
    'overlap': 10
}
```

## Pipeline Steps

The complete pipeline includes:

1. **Feature Extraction** - SIFT features from images
2. **Feature Matching** - Find correspondences between images
3. **Sparse Reconstruction** - GloMAP global SfM (10-100x faster!)
4. **Sparse Export** - Convert to PLY point cloud
5. **Dense Reconstruction** (optional):
   - Image undistortion
   - Stereo depth computation
   - Depth map fusion to point cloud

## Viewing Point Clouds

### CloudCompare (Recommended)

Free, open-source point cloud viewer:
- Download: [cloudcompare.org](https://cloudcompare.org)
- Open `.ply` files directly

### MeshLab

Alternative viewer with mesh processing:
- Download: [meshlab.net](http://www.meshlab.net/)

### COLMAP GUI

View within COLMAP:
```bash
colmap gui --import_path path/to/model
```

## Troubleshooting

### "COLMAP not found"
- Verify COLMAP is installed
- Check `self.colmap_path` in `main_window.py`
- Ensure `COLMAP.bat` exists in the specified directory

### "GloMAP not found"
- Install GloMAP and add to system PATH
- Or specify full path in `glomap_wrapper.py`

### "GPU initialization failed"
- Update NVIDIA drivers
- Install CUDA toolkit
- Or disable GPU: uncheck "Use GPU Acceleration"

### "Insufficient shared matches"
- Increase image overlap
- Use different matcher type
- Check image quality and lighting

### UI Freezing
- This shouldn't happen - worker threads prevent UI blocking
- If it does, report as a bug

## Project Structure

```
GloMAP_GUI/
├── main.py                  # Application entry point
├── requirements.txt         # Python dependencies
├── GLOMAP_GUI_GUIDE.md     # Complete documentation
├── gui/
│   ├── main_window.py      # Main GUI window
│   └── workers.py          # Background thread workers
├── core/
│   ├── colmap_wrapper.py   # COLMAP command wrapper
│   ├── glomap_wrapper.py   # GloMAP command wrapper
│   └── pipeline.py         # Pipeline orchestration
└── utils/
    ├── validators.py       # Input validation
    └── logger.py          # Logging utilities
```

## Performance Tips

1. **Use GloMAP** - 10-100x faster than COLMAP mapper
2. **Enable GPU** - Significantly faster feature extraction
3. **Sequential Matcher** - Faster for ordered image sequences
4. **Skip Dense** - Use sparse-only for quick previews
5. **Reduce Resolution** - Lower `max_features` for faster processing

## Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License.

## Acknowledgments

- **GloMAP**: [colmap/glomap](https://github.com/colmap/glomap)
- **COLMAP**: [colmap/colmap](https://github.com/colmap/colmap)
- **CustomTkinter**: [TomSchimansky/CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)

## References

Based on the comprehensive guide in `GLOMAP_GUI_GUIDE.md`. See that document for:
- Detailed installation instructions
- Command reference
- Alternative implementations (PyQt6)
- Deployment guidelines

## Support

For issues, questions, or feature requests:
- Check `GLOMAP_GUI_GUIDE.md` for detailed documentation
- Open an issue on GitHub
- Consult COLMAP/GloMAP documentation

---

**Note**: This application provides a GUI wrapper for COLMAP and GloMAP. The actual photogrammetry processing is performed by these external tools.
