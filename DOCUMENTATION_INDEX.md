# GloMAP GUI + 3D GRUT - Documentation Index

Quick reference guide to all documentation in this project.

---

## 🚀 Quick Start (Start Here!)

| Document | Purpose | Audience |
|----------|---------|----------|
| **`QUICKSTART.md`** | Get GloMAP GUI running in 5 minutes | All users |
| **`README.md`** | Project overview and features | All users |
| **`IMPLEMENTATION_SUMMARY.md`** | 3D GRUT implementation status | Developers & Users |

---

## 📦 Installation Guides

### GloMAP + COLMAP
| Document | Content | Platform |
|----------|---------|----------|
| `README.md` (Installation section) | Install GUI, COLMAP, GloMAP | Windows/Linux/macOS |
| `BUILDING_GLOMAP_WINDOWS.md` | Build GloMAP from source | Windows |
| `install_glomap.py` | Automated GloMAP installer | All platforms |

### 3D GRUT
| Document | Language | Detail Level | Time to Complete |
|----------|----------|--------------|------------------|
| **`INSTALL_3DGRUT_QUICKSTART.md`** | English | Quick reference | 10-30 minutes |
| **`INSTALLATION_CHECKLIST.md`** | Portuguese | Step-by-step with checkboxes | 30-60 minutes |
| **`GUIA_3DGRUT_INSTALACAO.md`** | Portuguese | Comprehensive (400+ lines) | Full understanding |

---

## 📚 User Guides

### Basic Usage
| Document | Content | Users |
|----------|---------|-------|
| `GLOMAP_GUI_GUIDE.md` | Complete GUI usage guide | All users |
| `QUICKSTART.md` | Fast introduction | New users |

### Advanced Features
| Document | Content | Users |
|----------|---------|-------|
| `GLOMAP_GUI_+3DGUT_GUIDE.md` | Fisheye + 3D GRUT features | Advanced users |
| `3DGRUT_IMPLEMENTATION_COMPLETE.md` | 3D GRUT technical details | Power users & developers |

---

## 🔧 Technical Documentation

### Implementation Details
| Document | Focus | Audience |
|----------|-------|----------|
| `3DGRUT_IMPLEMENTATION_COMPLETE.md` | Complete 3D GRUT implementation | Developers |
| `IMPLEMENTATION_SUMMARY.md` | Executive summary | Project managers |
| `3DGUT_IMPLEMENTATION_STATUS.md` | Earlier status (archive) | Reference |

### Code Reference
| File | Purpose |
|------|---------|
| `core/dgut_wrapper.py` | 3D GRUT Python wrapper |
| `core/pipeline.py` | Photogrammetry pipeline |
| `core/colmap_wrapper.py` | COLMAP integration |
| `gui/main_window.py` | Main GUI application |
| `gui/workers.py` | Background processing |

---

## ℹ️ Reference Information

### Software Availability
| Document | Content |
|----------|---------|
| `3DGUT_AVAILABILITY_NOTE.md` | 3D GRUT repository and availability status |
| `BUILD_TOOLS_STATUS.md` | Build tools and dependencies |

### Configuration
| File | Purpose |
|------|---------|
| `config.json` | GUI configuration (auto-generated) |
| `requirements.txt` | Python dependencies |
| `.gitignore` | Git exclusions |

---

## 📁 Project Structure

```
GloMAP_GUI/
├── 📖 Documentation (You are here!)
│   ├── README.md                           # Main project readme
│   ├── QUICKSTART.md                       # 5-minute quick start
│   ├── IMPLEMENTATION_SUMMARY.md           # Executive summary ⭐
│   │
│   ├── 🎓 User Guides
│   │   ├── GLOMAP_GUI_GUIDE.md            # Basic usage
│   │   ├── GLOMAP_GUI_+3DGUT_GUIDE.md     # Advanced features
│   │   └── INSTALLATION_CHECKLIST.md       # Step-by-step install ⭐
│   │
│   ├── 🚀 3D GRUT Guides
│   │   ├── INSTALL_3DGRUT_QUICKSTART.md   # Quick install (English) ⭐
│   │   ├── GUIA_3DGRUT_INSTALACAO.md      # Full guide (Portuguese)
│   │   └── 3DGRUT_IMPLEMENTATION_COMPLETE.md  # Technical details
│   │
│   ├── 🔧 Technical Docs
│   │   ├── 3DGUT_AVAILABILITY_NOTE.md      # Software status
│   │   ├── BUILDING_GLOMAP_WINDOWS.md      # Build from source
│   │   └── BUILD_TOOLS_STATUS.md           # Dependencies
│   │
│   └── 📝 Archive
│       ├── 3DGUT_IMPLEMENTATION_STATUS.md  # Earlier status
│       ├── IMPLEMENTATION_COMPLETE.md      # Milestone marker
│       └── INSTALLATION_COMPLETE.md        # Setup completion
│
├── 🐍 Source Code
│   ├── main.py                             # Application entry point
│   ├── core/                               # Backend logic
│   │   ├── pipeline.py                     # Main pipeline
│   │   ├── colmap_wrapper.py               # COLMAP integration
│   │   ├── glomap_wrapper.py               # GloMAP integration
│   │   └── dgut_wrapper.py                 # 3D GRUT integration ⭐
│   ├── gui/                                # User interface
│   │   ├── main_window.py                  # Main window
│   │   └── workers.py                      # Background threads
│   └── utils/                              # Helper functions
│
├── ⚙️ Configuration
│   ├── requirements.txt                    # Python packages
│   ├── config.json                         # App settings
│   ├── setup.py                            # Package setup
│   └── .gitignore                          # Git exclusions
│
└── 🎬 Execution
    ├── main.py                             # Run GUI
    ├── run.bat                             # Windows launcher
    └── install_glomap.py                   # GloMAP installer
```

---

## 🎯 Common Tasks Quick Reference

### "I want to start using the GUI"
1. Read `QUICKSTART.md`
2. Install dependencies from `README.md`
3. Run `python main.py`

### "I want to install 3D GRUT"
1. Read `IMPLEMENTATION_SUMMARY.md` (overview)
2. Follow `INSTALL_3DGRUT_QUICKSTART.md` (English)
3. OR use `INSTALLATION_CHECKLIST.md` (Portuguese, detailed)

### "I want to understand fisheye support"
1. Read `GLOMAP_GUI_+3DGUT_GUIDE.md` (section 2)
2. Check camera models in `core/colmap_wrapper.py`

### "I want to understand the code"
1. Read `3DGRUT_IMPLEMENTATION_COMPLETE.md` (architecture)
2. Study `core/pipeline.py` (main workflow)
3. Review `gui/main_window.py` (UI logic)

### "I'm having installation problems"
1. Check `INSTALLATION_CHECKLIST.md` (troubleshooting section)
2. Read `3DGUT_AVAILABILITY_NOTE.md` (system requirements)
3. Review `GUIA_3DGRUT_INSTALACAO.md` (comprehensive guide)

### "I want to contribute"
1. Understand architecture: `3DGRUT_IMPLEMENTATION_COMPLETE.md`
2. Check code structure: `core/` and `gui/` folders
3. Review existing issues and features

---

## 🌐 Language Guide

| Language | Documents Available |
|----------|---------------------|
| **English** | All documentation (primary) |
| **Portuguese** | `GUIA_3DGRUT_INSTALACAO.md`, `INSTALLATION_CHECKLIST.md` |

---

## ⭐ Recommended Reading Order

### For New Users
1. `README.md` - Understand what the project does
2. `QUICKSTART.md` - Get it running fast
3. `GLOMAP_GUI_GUIDE.md` - Learn the features
4. `INSTALL_3DGRUT_QUICKSTART.md` - Add 3D GRUT (optional)

### For Advanced Users
1. `IMPLEMENTATION_SUMMARY.md` - Current status
2. `GLOMAP_GUI_+3DGUT_GUIDE.md` - Advanced features
3. `3DGRUT_IMPLEMENTATION_COMPLETE.md` - Technical depth
4. `GUIA_3DGRUT_INSTALACAO.md` - Complete 3D GRUT guide

### For Developers
1. `3DGRUT_IMPLEMENTATION_COMPLETE.md` - Architecture
2. `core/pipeline.py` - Main workflow
3. `gui/main_window.py` - UI implementation
4. `core/dgut_wrapper.py` - 3D GRUT wrapper
5. `gui/workers.py` - Threading model

---

## 🔍 Find By Topic

### Installation
- GloMAP: `README.md` → Installation section
- COLMAP: `README.md` → Prerequisites section
- 3D GRUT: `INSTALL_3DGRUT_QUICKSTART.md` OR `INSTALLATION_CHECKLIST.md`

### Usage
- Basic: `QUICKSTART.md` OR `GLOMAP_GUI_GUIDE.md`
- Fisheye: `GLOMAP_GUI_+3DGUT_GUIDE.md` → Section 2
- 3D GRUT: `GLOMAP_GUI_+3DGUT_GUIDE.md` → Section 3

### Troubleshooting
- General: `GLOMAP_GUI_GUIDE.md` → Troubleshooting section
- 3D GRUT: `INSTALLATION_CHECKLIST.md` → Solução de Problemas
- Build issues: `BUILDING_GLOMAP_WINDOWS.md`

### Technical Details
- Architecture: `3DGRUT_IMPLEMENTATION_COMPLETE.md`
- Commands: `INSTALL_3DGRUT_QUICKSTART.md` → Quick Commands
- Configuration: `3DGRUT_IMPLEMENTATION_COMPLETE.md` → Configuration Options

---

## 📊 Documentation Statistics

- **Total Documents**: 15 markdown files
- **Total Lines**: ~5,000+ lines of documentation
- **Languages**: English (primary) + Portuguese (select guides)
- **Code Files**: 20+ Python modules
- **Last Updated**: 2025-01-15

---

## 🆘 Getting Help

1. **Read the docs**: Start with `IMPLEMENTATION_SUMMARY.md`
2. **Check checklist**: `INSTALLATION_CHECKLIST.md` for step-by-step
3. **Review code**: Check relevant files in `core/` or `gui/`
4. **Search issues**: https://github.com/nv-tlabs/3dgrut/issues

---

## 🎓 Learning Path

### Beginner → Intermediate (1-2 hours)
```
README.md 
  → QUICKSTART.md 
    → GLOMAP_GUI_GUIDE.md 
      → First successful reconstruction! 🎉
```

### Intermediate → Advanced (2-4 hours)
```
IMPLEMENTATION_SUMMARY.md 
  → INSTALL_3DGRUT_QUICKSTART.md 
    → GLOMAP_GUI_+3DGUT_GUIDE.md 
      → First 3D GRUT training! 🎉
```

### Advanced → Expert (4-8 hours)
```
3DGRUT_IMPLEMENTATION_COMPLETE.md 
  → Study core/*.py files 
    → GUIA_3DGRUT_INSTALACAO.md 
      → Custom pipeline development! 🎉
```

---

**Index Version**: 1.0  
**Last Updated**: 2025-01-15  
**Maintainer**: GitHub Copilot + User

---

*This index helps you navigate the comprehensive documentation. Start with the "Quick Start" section above!*
