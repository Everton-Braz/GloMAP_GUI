"""
Convert COLMAP/GloMAP PLY to Gaussian Splat PLY format
For SuperSplat, PlayCanvas and other Gaussian Splatting viewers
"""
import struct
import sys
from pathlib import Path
import numpy as np


def read_colmap_ply(file_path):
    """Read COLMAP PLY file (x,y,z,r,g,b)."""
    vertices = []
    
    with open(file_path, 'rb') as f:
        # Read header
        header_end = False
        vertex_count = 0
        is_binary = False
        
        while not header_end:
            line = f.readline().decode('ascii').strip()
            if line.startswith('element vertex'):
                vertex_count = int(line.split()[-1])
            elif line.startswith('format binary'):
                is_binary = True
            elif line == 'end_header':
                header_end = True
                break
        
        # Read vertices
        if is_binary:
            # Binary: x,y,z (float), r,g,b (uchar)
            for _ in range(vertex_count):
                x, y, z = struct.unpack('<fff', f.read(12))
                r, g, b = struct.unpack('<BBB', f.read(3))
                vertices.append((x, y, z, r/255.0, g/255.0, b/255.0))
        else:
            # ASCII
            for _ in range(vertex_count):
                line = f.readline().decode('ascii').strip()
                parts = line.split()
                x, y, z = float(parts[0]), float(parts[1]), float(parts[2])
                r, g, b = int(parts[3])/255.0, int(parts[4])/255.0, int(parts[5])/255.0
                vertices.append((x, y, z, r, g, b))
    
    return np.array(vertices, dtype=np.float32)


def write_gaussian_splat_ply(output_path, vertices):
    """
    Write Gaussian Splat PLY format.
    Required properties for SuperSplat/PlayCanvas:
    - x, y, z (position)
    - nx, ny, nz (normal - can be dummy)
    - f_dc_0, f_dc_1, f_dc_2 (color in spherical harmonics - DC component)
    - opacity
    - scale_0, scale_1, scale_2 (scale)
    - rot_0, rot_1, rot_2, rot_3 (rotation quaternion)
    """
    num_points = len(vertices)
    
    with open(output_path, 'wb') as f:
        # Write header
        header = f"""ply
format binary_little_endian 1.0
comment Converted from COLMAP to Gaussian Splat format
element vertex {num_points}
property float x
property float y
property float z
property float nx
property float ny
property float nz
property float f_dc_0
property float f_dc_1
property float f_dc_2
property float opacity
property float scale_0
property float scale_1
property float scale_2
property float rot_0
property float rot_1
property float rot_2
property float rot_3
end_header
"""
        f.write(header.encode('ascii'))
        
        # Write binary data
        for vertex in vertices:
            x, y, z, r, g, b = vertex
            
            # Convert RGB to spherical harmonics DC component
            # The RGB values are already normalized [0,1]
            # For SH: color = SH_C0 * sh_dc, where SH_C0 = 0.28209479177387814
            # So: sh_dc = color / SH_C0
            SH_C0 = 0.28209479177387814
            f_dc_0 = (r - 0.5) / SH_C0
            f_dc_1 = (g - 0.5) / SH_C0
            f_dc_2 = (b - 0.5) / SH_C0
            
            # Default values for Gaussian properties
            nx, ny, nz = 0.0, 0.0, 1.0  # Normal pointing up
            
            # Opacity in logit space: logit(0.9) ≈ 2.2
            # High opacity for point cloud visualization
            opacity = 2.2
            
            # Scale in log space: exp(-7) ≈ 0.0009 units
            # Very small splats to approximate point cloud
            scale_0, scale_1, scale_2 = -7.0, -7.0, -7.0
            
            # Identity quaternion (no rotation)
            rot_0, rot_1, rot_2, rot_3 = 1.0, 0.0, 0.0, 0.0
            
            # Pack as binary (17 floats)
            data = struct.pack('<fffffffffffffffff',
                             x, y, z,
                             nx, ny, nz,
                             f_dc_0, f_dc_1, f_dc_2,
                             opacity,
                             scale_0, scale_1, scale_2,
                             rot_0, rot_1, rot_2, rot_3)
            f.write(data)


def convert_to_gaussian_splat(input_path, output_path=None):
    """Convert COLMAP PLY to Gaussian Splat PLY."""
    input_path = Path(input_path)
    
    if output_path is None:
        output_path = input_path.parent / f"{input_path.stem}_splat.ply"
    else:
        output_path = Path(output_path)
    
    print(f"Reading COLMAP PLY: {input_path}")
    vertices = read_colmap_ply(input_path)
    print(f"  Points: {len(vertices):,}")
    
    print(f"Writing Gaussian Splat PLY: {output_path}")
    write_gaussian_splat_ply(output_path, vertices)
    
    input_size = input_path.stat().st_size / 1024 / 1024
    output_size = output_path.stat().st_size / 1024 / 1024
    print(f"  Input size: {input_size:.2f} MB")
    print(f"  Output size: {output_size:.2f} MB")
    print("✓ Conversion complete!")
    print(f"\nYou can now open '{output_path.name}' in:")
    print("  • SuperSplat (https://supersplat.playcanvas.com)")
    print("  • PlayCanvas Editor")
    print("  • Any Gaussian Splatting viewer")
    
    return output_path


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Convert COLMAP PLY to Gaussian Splat PLY format',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  python convert_to_splat.py sparse.ply
  python convert_to_splat.py fused.ply --output scene_splat.ply
  python convert_to_splat.py *.ply
        '''
    )
    
    parser.add_argument('input', nargs='+', help='Input PLY file(s)')
    parser.add_argument('--output', '-o', help='Output file path (for single file)')
    
    args = parser.parse_args()
    
    if len(args.input) > 1 and args.output:
        print("Error: Cannot specify --output with multiple input files")
        sys.exit(1)
    
    print("\n" + "="*60)
    print("COLMAP to Gaussian Splat PLY Converter")
    print("="*60 + "\n")
    
    for input_file in args.input:
        try:
            convert_to_gaussian_splat(input_file, args.output)
            print()
        except Exception as e:
            print(f"✗ Error converting {input_file}: {e}\n")
            continue
