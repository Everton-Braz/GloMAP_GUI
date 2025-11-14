# Quick Start Guide

## Installation (5 minutes)

### 1. Install Python Dependencies

```bash
cd C:\Users\User\Documents\APLICATIVOS\GloMAP_GUI
python setup.py
```

This will:
- Check Python version
- Install CustomTkinter
- Verify COLMAP and GloMAP installations
- Create necessary directories

### 2. Run the Application

```bash
python main.py
```

## First Use

### Step 1: Prepare Your Images
- Place all your photos in a single folder
- Use at least 3 images (10+ recommended)
- Supported formats: JPG, PNG, BMP, TIFF

### Step 2: Run Processing
1. Click **"Browse"** next to "Images Folder"
2. Select your images folder
3. Click **"Browse"** next to "Project Folder"
4. Select/create an output folder
5. Adjust settings (optional):
   - ✅ Use GPU Acceleration (recommended if you have NVIDIA GPU)
   - Matcher: Sequential (for ordered photos) or Exhaustive
   - ✅ Include Dense Reconstruction (slower but creates detailed point cloud)
6. Click **"▶ Run Complete Pipeline"**

### Step 3: View Results
- Monitor progress in the log window
- When complete, click **"📁 Open Output"**
- Find your point clouds:
  - `sparse/sparse.ply` - Fast sparse reconstruction
  - `dense/fused.ply` - Detailed dense point cloud (if enabled)

## Opening Point Clouds

### CloudCompare (Free)
1. Download from https://cloudcompare.org
2. Install and open CloudCompare
3. Drag and drop `.ply` files

### Windows 3D Viewer
1. Right-click `.ply` file
2. Select "Open with" → "3D Viewer"

### COLMAP GUI
```bash
cd C:\Users\User\Documents\colmap-x64-windows-cuda
COLMAP.bat gui --import_path "path/to/sparse/0"
```

## Tips for Best Results

### Image Capture
- ✅ Overlap: 60-80% between consecutive images
- ✅ Lighting: Consistent, avoid harsh shadows
- ✅ Focus: Sharp images, avoid motion blur
- ✅ Coverage: Photograph object from all angles
- ❌ Avoid: Reflective surfaces, featureless areas

### Processing Settings
- **Fast Preview**: Disable dense reconstruction
- **Best Quality**: Enable dense, use GPU, exhaustive matcher
- **Large Dataset** (100+ images): Use sequential matcher, may need more RAM

### Troubleshooting
- **"No images found"**: Check folder contains JPG/PNG files
- **"GPU failed"**: Uncheck "Use GPU Acceleration"
- **"Insufficient matches"**: Check image overlap and quality
- **Long processing time**: Normal for dense reconstruction

## Performance Expectations

| Dataset Size | Sparse (GloMAP) | Dense (Optional) |
|--------------|-----------------|------------------|
| 10-20 images | 1-2 minutes     | 5-10 minutes     |
| 50-100 images| 5-10 minutes    | 30-60 minutes    |
| 200+ images  | 15-30 minutes   | 2-4 hours        |

*Times with GPU acceleration. CPU-only is slower.*

## Example Workflow

### Urban Scene Reconstruction
1. Images: 50 photos of a building
2. Settings: Sequential matcher, GPU enabled, no dense
3. Time: ~5 minutes
4. Result: Sparse point cloud showing building structure

### Object Scanning
1. Images: 30 photos around an object
2. Settings: Exhaustive matcher, GPU enabled, with dense
3. Time: ~20 minutes
4. Result: Detailed 3D point cloud

## Next Steps

After creating point clouds:
1. **Mesh Generation**: Use CloudCompare or MeshLab
2. **Texture Mapping**: Use COLMAP's dense reconstruction
3. **Export**: Convert to other formats (OBJ, STL, etc.)

## Need Help?

- Read `README.md` for detailed documentation
- Check `GLOMAP_GUI_GUIDE.md` for complete reference
- Verify installations: `python setup.py`

---

**Note**: First run may take longer as COLMAP builds feature databases.
