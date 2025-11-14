"""
PLY File Fixer - Convert and repair PLY files for better compatibility
Fixes common issues with PLY files from COLMAP/GloMAP
"""
import argparse
import struct
import sys
from pathlib import Path


def read_ply_header(file_path):
    """Read and parse PLY header."""
    with open(file_path, 'rb') as f:
        # Read header
        header_lines = []
        while True:
            line = f.readline().decode('ascii', errors='ignore').strip()
            header_lines.append(line)
            if line == 'end_header':
                break
        
        data_start = f.tell()
        
    # Parse header
    vertex_count = 0
    properties = []
    format_type = 'ascii'
    
    for line in header_lines:
        if line.startswith('element vertex'):
            vertex_count = int(line.split()[-1])
        elif line.startswith('property'):
            parts = line.split()
            prop_type = parts[1]
            prop_name = parts[2]
            properties.append((prop_name, prop_type))
        elif line.startswith('format'):
            format_type = line.split()[1]
    
    return {
        'vertex_count': vertex_count,
        'properties': properties,
        'format': format_type,
        'data_start': data_start
    }


def read_binary_ply(file_path, header_info):
    """Read binary PLY data."""
    vertices = []
    
    with open(file_path, 'rb') as f:
        f.seek(header_info['data_start'])
        
        # Determine data types
        type_map = {
            'float': ('f', 4),
            'double': ('d', 8),
            'uchar': ('B', 1),
            'uint': ('I', 4),
            'int': ('i', 4)
        }
        
        # Build format string
        fmt_parts = []
        byte_size = 0
        for prop_name, prop_type in header_info['properties']:
            if prop_type in type_map:
                fmt_char, size = type_map[prop_type]
                fmt_parts.append(fmt_char)
                byte_size += size
        
        fmt = '<' + ''.join(fmt_parts)  # Little endian
        
        # Read all vertices
        for _ in range(header_info['vertex_count']):
            data = f.read(byte_size)
            if len(data) < byte_size:
                break
            vertex = struct.unpack(fmt, data)
            vertices.append(vertex)
    
    return vertices


def read_ascii_ply(file_path, header_info):
    """Read ASCII PLY data."""
    vertices = []
    
    with open(file_path, 'r') as f:
        # Skip header
        for line in f:
            if line.strip() == 'end_header':
                break
        
        # Read vertices
        for line in f:
            parts = line.strip().split()
            if len(parts) == len(header_info['properties']):
                vertex = [float(x) for x in parts]
                vertices.append(tuple(vertex))
    
    return vertices


def write_ply_ascii(output_path, vertices, properties):
    """Write PLY in ASCII format (most compatible)."""
    with open(output_path, 'w') as f:
        # Write header
        f.write("ply\n")
        f.write("format ascii 1.0\n")
        f.write("comment Fixed by PLY Fixer\n")
        f.write(f"element vertex {len(vertices)}\n")
        
        # Write properties
        for prop_name, prop_type in properties:
            # Standardize type names
            if prop_type in ['uchar', 'uint8']:
                prop_type = 'uchar'
            elif prop_type in ['float', 'float32']:
                prop_type = 'float'
            f.write(f"property {prop_type} {prop_name}\n")
        
        f.write("end_header\n")
        
        # Write data
        for vertex in vertices:
            # Format each value appropriately
            formatted = []
            for i, (val, (prop_name, prop_type)) in enumerate(zip(vertex, properties)):
                if 'uchar' in prop_type or prop_name in ['red', 'green', 'blue']:
                    # Color values as integers 0-255
                    formatted.append(str(int(val)))
                else:
                    # Floating point with reasonable precision
                    formatted.append(f"{val:.6f}")
            
            f.write(" ".join(formatted) + "\n")


def write_ply_binary(output_path, vertices, properties):
    """Write PLY in binary format (smaller file size)."""
    with open(output_path, 'wb') as f:
        # Write header (ASCII)
        header = []
        header.append("ply\n")
        header.append("format binary_little_endian 1.0\n")
        header.append("comment Fixed by PLY Fixer - Compatible format\n")
        header.append(f"element vertex {len(vertices)}\n")
        
        # Write properties with correct types
        type_map = {
            'uchar': 'B',
            'float': 'f',
            'double': 'd',
            'uint': 'I',
            'int': 'i',
            'uint8': 'B',
            'float32': 'f'
        }
        
        fmt_parts = []
        for prop_name, prop_type in properties:
            # Normalize type names for better compatibility
            normalized_type = prop_type
            if prop_type in ['uchar', 'uint8']:
                normalized_type = 'uchar'
            elif prop_type in ['float', 'float32']:
                normalized_type = 'float'
            elif prop_type in ['double', 'float64']:
                normalized_type = 'float'  # Convert double to float for compatibility
            
            header.append(f"property {normalized_type} {prop_name}\n")
            
            # Map to struct format
            struct_format = type_map.get(prop_type, 'f')
            if prop_type in ['double', 'float64']:
                struct_format = 'f'  # Pack as float instead of double
            fmt_parts.append(struct_format)
        
        header.append("end_header\n")
        
        # Write header
        f.write(''.join(header).encode('ascii'))
        
        # Write binary data
        fmt = '<' + ''.join(fmt_parts)
        for vertex in vertices:
            # Convert data if needed (e.g., double to float)
            converted = []
            for i, val in enumerate(vertex):
                prop_type = properties[i][1]
                if prop_type in ['double', 'float64']:
                    converted.append(float(val))  # Ensure it's float32
                else:
                    converted.append(val)
            f.write(struct.pack(fmt, *converted))


def fix_ply_file(input_path, output_path=None, format_type='ascii'):
    """
    Fix PLY file for better compatibility.
    
    Args:
        input_path: Path to input PLY file
        output_path: Path to output file (if None, adds '_fixed' suffix)
        format_type: 'ascii' or 'binary'
    
    Returns:
        Path to fixed file
    """
    input_path = Path(input_path)
    
    if output_path is None:
        output_path = input_path.parent / f"{input_path.stem}_fixed.ply"
    else:
        output_path = Path(output_path)
    
    print(f"Reading: {input_path}")
    
    # Read header
    header_info = read_ply_header(input_path)
    print(f"  Vertices: {header_info['vertex_count']:,}")
    print(f"  Format: {header_info['format']}")
    print(f"  Properties: {len(header_info['properties'])}")
    
    # Read data
    if 'binary' in header_info['format']:
        vertices = read_binary_ply(input_path, header_info)
    else:
        vertices = read_ascii_ply(input_path, header_info)
    
    print(f"  Read {len(vertices):,} vertices")
    
    # Write fixed file
    print(f"Writing: {output_path}")
    if format_type == 'ascii':
        write_ply_ascii(output_path, vertices, header_info['properties'])
        print("  Format: ASCII (most compatible)")
    else:
        write_ply_binary(output_path, vertices, header_info['properties'])
        print("  Format: Binary (smaller size)")
    
    # Show file sizes
    input_size = input_path.stat().st_size / 1024 / 1024
    output_size = output_path.stat().st_size / 1024 / 1024
    print(f"  Input size: {input_size:.2f} MB")
    print(f"  Output size: {output_size:.2f} MB")
    
    return output_path


def main():
    """Command line interface."""
    parser = argparse.ArgumentParser(
        description='Fix PLY files for better compatibility with various programs',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  # Fix single file (ASCII format, most compatible)
  python fix_ply.py input.ply

  # Fix to binary format (smaller size)
  python fix_ply.py input.ply --format binary

  # Specify output path
  python fix_ply.py input.ply --output fixed.ply

  # Fix all PLY files in a directory
  python fix_ply.py project_folder/*.ply
        '''
    )
    
    parser.add_argument('input', nargs='+', help='Input PLY file(s) or pattern')
    parser.add_argument('--output', '-o', help='Output file path (for single file)')
    parser.add_argument('--format', '-f', choices=['ascii', 'binary'], default='ascii',
                       help='Output format (default: ascii for best compatibility)')
    
    args = parser.parse_args()
    
    # Process files
    input_files = []
    for pattern in args.input:
        from glob import glob
        matched = glob(pattern)
        if matched:
            input_files.extend(matched)
        else:
            input_files.append(pattern)
    
    if not input_files:
        print("Error: No input files specified")
        return 1
    
    if len(input_files) > 1 and args.output:
        print("Error: Cannot specify --output with multiple input files")
        return 1
    
    print(f"\n{'='*60}")
    print("PLY File Fixer")
    print(f"{'='*60}\n")
    
    fixed_files = []
    for input_file in input_files:
        try:
            output_file = fix_ply_file(input_file, args.output, args.format)
            fixed_files.append(output_file)
            print("✓ Success!\n")
        except Exception as e:
            print(f"✗ Error: {e}\n")
            continue
    
    if fixed_files:
        print(f"{'='*60}")
        print(f"Fixed {len(fixed_files)} file(s):")
        for f in fixed_files:
            print(f"  • {f}")
        print(f"{'='*60}\n")
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
