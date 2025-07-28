"""
Build Package Script
===================

This script builds the Dragon's Lair RPG package for distribution.
It creates the necessary files for uploading to PyPI or other repositories.

RESOURCE: This automates the package building process.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def print_banner():
    """Print the dragon banner"""
    banner = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                    🐉 DRAGON'S LAIR RPG 🐉                    ║
    ║                                                              ║
    ║                    📦 PACKAGE BUILDER                        ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)

def check_requirements():
    """Check if required tools are installed"""
    print("🔍 Checking requirements...")
    
    required_tools = ['python', 'pip', 'setuptools', 'wheel', 'twine']
    missing_tools = []
    
    for tool in required_tools:
        try:
            subprocess.run([tool, '--version'], capture_output=True, check=True)
            print(f"✅ {tool} is available")
        except (subprocess.CalledProcessError, FileNotFoundError):
            print(f"❌ {tool} is missing")
            missing_tools.append(tool)
    
    if missing_tools:
        print(f"\n❌ Missing required tools: {', '.join(missing_tools)}")
        print("Please install them with: pip install setuptools wheel twine")
        return False
    
    return True

def clean_build():
    """Clean previous build files"""
    print("🧹 Cleaning previous build files...")
    
    build_dirs = ['build', 'dist', '*.egg-info']
    for pattern in build_dirs:
        for path in Path('.').glob(pattern):
            if path.is_dir():
                shutil.rmtree(path)
                print(f"🗑️  Removed {path}")
            elif path.is_file():
                path.unlink()
                print(f"🗑️  Removed {path}")

def build_package():
    """Build the package"""
    print("🔨 Building package...")
    
    try:
        # Build the package
        result = subprocess.run([
            sys.executable, 'setup.py', 'sdist', 'bdist_wheel'
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Package built successfully!")
            return True
        else:
            print(f"❌ Build failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Build error: {e}")
        return False

def check_package():
    """Check the built package"""
    print("🔍 Checking built package...")
    
    try:
        result = subprocess.run([
            'twine', 'check', 'dist/*'
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Package check passed!")
            return True
        else:
            print(f"❌ Package check failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Package check error: {e}")
        return False

def list_package_files():
    """List the built package files"""
    print("📦 Built package files:")
    
    dist_dir = Path('dist')
    if dist_dir.exists():
        for file in dist_dir.iterdir():
            size = file.stat().st_size / 1024  # Size in KB
            print(f"   📄 {file.name} ({size:.1f} KB)")
    else:
        print("   ❌ No dist directory found")

def upload_instructions():
    """Show upload instructions"""
    print("\n📤 Upload Instructions:")
    print("=" * 50)
    print("1. Test upload to TestPyPI:")
    print("   twine upload --repository testpypi dist/*")
    print()
    print("2. Upload to PyPI (production):")
    print("   twine upload dist/*")
    print()
    print("3. Install from TestPyPI:")
    print("   pip install --index-url https://test.pypi.org/simple/ dragons-lair-rpg")
    print()
    print("4. Install from PyPI:")
    print("   pip install dragons-lair-rpg")
    print()
    print("5. Run the game:")
    print("   dragons-lair-rpg")

def main():
    """Main build process"""
    print_banner()
    
    print("🐉 Building Dragon's Lair RPG Package")
    print("=" * 50)
    
    # Check requirements
    if not check_requirements():
        return False
    
    # Clean previous builds
    clean_build()
    
    # Build package
    if not build_package():
        return False
    
    # Check package
    if not check_package():
        return False
    
    # List built files
    list_package_files()
    
    # Show upload instructions
    upload_instructions()
    
    print("\n🎉 Package build completed successfully!")
    print("🐉 Dragon's Lair RPG is ready for distribution!")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 