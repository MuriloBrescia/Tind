#!/usr/bin/env python3
"""
Tind AI Application Runner

This script provides an easy way to run the Tind AI application from the project root.
It handles path setup and provides different running modes.
"""

import os
import sys
import subprocess
from pathlib import Path

def main():
    """Main runner function."""
    # Ensure we're in the project root
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # Add src to Python path
    src_path = project_root / "src"
    sys.path.insert(0, str(src_path))
    
    print("🚀 Starting Tind AI Application...")
    print("=" * 40)
    
    # Check if Flask is available
    try:
        import flask
        print(f"✅ Flask {flask.__version__} found")
    except ImportError:
        print("❌ Flask not found. Installing...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "flask", "werkzeug"])
            print("✅ Flask installed successfully")
        except subprocess.CalledProcessError:
            print("❌ Failed to install Flask. Please install manually:")
            print("   pip install flask werkzeug")
            return 1
    
    # Import and run the app
    try:
        from src.app import app
        print("✅ Application loaded successfully")
        print("🌐 Starting web server...")
        print("📱 Open your browser to: http://localhost:5000")
        print("⚠️  Press Ctrl+C to stop the server")
        print("=" * 40)
        
        # Run the Flask app
        app.run(host='0.0.0.0', port=5000, debug=True)
        
    except Exception as e:
        print(f"❌ Error starting application: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())