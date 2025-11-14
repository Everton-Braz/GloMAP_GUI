# Quick Start: Installing 3D GRUT for GloMAP GUI

## Prerequisites Check

Before installing, verify you have:

```bash
# Check NVIDIA GPU
nvidia-smi

# Check CUDA version (need 11.8 or newer)
nvcc --version

# Check GCC version (need 11 or 12)
gcc --version

# Check Python version (need 3.10+)
python --version
```

---

## Installation Steps

### 1. Clone Repository
```bash
cd ~
git clone https://github.com/nv-tlabs/3dgrut
cd 3dgrut
```

### 2. Install (Choose Your Method)

#### A. Easy Install (CUDA 11.8 or 12.8)
```bash
./install.sh
```

#### B. Custom CUDA Version
```bash
# Set your CUDA path
export CUDA_HOME=/usr/local/cuda-12.1  # Example for CUDA 12.1
./install.sh
```

#### C. Install with GUI Viewer
```bash
./install.sh --with-viewer
```

### 3. Verify Installation
```bash
# Check if Python package installed
python -c "import dgut; print('3D GRUT OK!')"

# Check if scripts exist
ls train.py render.py viewer.py
```

---

## Windows (WSL2) Installation

### 1. Install WSL2 with Ubuntu
```powershell
# In PowerShell (Administrator)
wsl --install -d Ubuntu-22.04
```

### 2. Setup NVIDIA CUDA in WSL2
```bash
# Inside WSL2 Ubuntu
wget https://developer.download.nvidia.com/compute/cuda/repos/wsl-ubuntu/x86_64/cuda-keyring_1.1-1_all.deb
sudo dpkg -i cuda-keyring_1.1-1_all.deb
sudo apt-get update
sudo apt-get -y install cuda-toolkit-12-8
```

### 3. Install GCC 11
```bash
sudo apt update
sudo apt install gcc-11 g++-11
sudo update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-11 100
sudo update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-11 100
```

### 4. Install 3D GRUT
```bash
cd ~
git clone https://github.com/nv-tlabs/3dgrut
cd 3dgrut
export CUDA_HOME=/usr/local/cuda-12
./install.sh
```

---

## Docker Installation (Alternative)

### 1. Pull Image
```bash
docker pull nvidia/3dgrut:latest
```

### 2. Run Container
```bash
docker run --gpus all -v /path/to/data:/data -it nvidia/3dgrut:latest
```

### 3. Inside Container
```bash
cd /workspace
python train.py --config_name colmap --data.path /data/your_project
```

---

## Common Installation Issues

### Issue: "CUDA not found"
**Solution**:
```bash
# Find CUDA installation
find /usr/local -name "nvcc" 2>/dev/null

# Set CUDA_HOME
export CUDA_HOME=/usr/local/cuda-12.8  # Use your path
echo 'export CUDA_HOME=/usr/local/cuda-12.8' >> ~/.bashrc
source ~/.bashrc
```

### Issue: "GCC version incompatible"
**Solution**:
```bash
# Install GCC 11 or 12
sudo apt install gcc-11 g++-11

# Set as default
sudo update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-11 100
sudo update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-11 100
```

### Issue: "CMake too old"
**Solution**:
```bash
# Install newer CMake
sudo apt remove cmake
pip install cmake --upgrade
```

### Issue: "pip install fails"
**Solution**:
```bash
# Install dependencies first
sudo apt install python3-dev python3-pip

# Try installing with verbose output
pip install -e . -v
```

---

## Verification Test

### 1. Prepare Test Data
```bash
# Create test structure
mkdir -p ~/test_3dgrut/images
mkdir -p ~/test_3dgrut/sparse/0

# Copy some images to images/
# Run COLMAP to generate sparse/0/ (or use sample data)
```

### 2. Run Quick Training Test
```bash
cd ~/3dgrut
python train.py \
  --config_name colmap \
  --data.path ~/test_3dgrut \
  --output_dir ~/test_3dgrut/output \
  --down_sample_factor 4 \
  --iterations 1000
```

### 3. Check Results
```bash
# Should see output files
ls ~/test_3dgrut/output/

# Should include:
# - *.ply (point cloud)
# - checkpoints/
# - training logs
```

---

## Integration with GloMAP GUI

### 1. Location Detection
The GUI automatically searches for 3D GRUT in:
- `~/3dgrut/`
- `~/3DGUT/`
- `C:/3dgrut/` (Windows)
- `C:/3DGUT/` (Windows)
- Local project directory

### 2. Manual Path Configuration (if needed)
If auto-detection fails, edit `core/dgut_wrapper.py`:
```python
def _locate_dgut(self):
    # Add your custom path
    custom_path = Path("/your/custom/path/3dgrut")
    if custom_path.exists():
        return custom_path
    # ... rest of code
```

### 3. Test from GUI
1. Open GloMAP GUI
2. Check startup log for "3DGUT: ✓" or "3DGUT: ✗"
3. If ✗, error message shows installation instructions

---

## Performance Tips

### GPU Memory Optimization
```bash
# Use lower resolution
--down_sample_factor 4  # Instead of 2

# Reduce batch size (in config file)
# Edit configs/mcmc.yaml:
# batch_size: 1  # Instead of 4
```

### Speed Optimization
```bash
# Use colmap config (faster)
--config_name colmap  # Instead of mcmc

# Reduce iterations
--iterations 15000  # Instead of 30000

# Skip validation
--eval false
```

### Quality Optimization
```bash
# Use MCMC config (better quality)
--config_name mcmc

# More iterations
--iterations 50000

# Full resolution
--down_sample_factor 1
```

---

## Next Steps

After successful installation:

1. **Test with GloMAP GUI**:
   - Launch GUI: `python main.py`
   - Check 3DGUT status in startup log
   - Run a test reconstruction

2. **Read Full Documentation**:
   - `GUIA_3DGRUT_INSTALACAO.md` (Portuguese comprehensive guide)
   - `3DGRUT_IMPLEMENTATION_COMPLETE.md` (Implementation details)

3. **Explore 3D GRUT Features**:
   - Interactive viewer: `python viewer.py --model path/to/model`
   - Custom rendering: `python render.py --model path/to/model`
   - Export options: PLY, OBJ, mesh formats

---

## Support Resources

- **GitHub Issues**: https://github.com/nv-tlabs/3dgrut/issues
- **NVIDIA Forum**: https://forums.developer.nvidia.com/
- **Discord**: [3D Gaussian Splatting Community]
- **Reddit**: r/computervision, r/3Dprinting

---

**Installation Time**: 10-30 minutes  
**Difficulty**: Intermediate (Linux experience helpful)  
**Success Rate**: High (with correct CUDA/GCC versions)

---

*Quick Start Guide v1.0*  
*Last Updated: 2025-01-15*
