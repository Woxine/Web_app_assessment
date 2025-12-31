"""
WSGI Configuration File (for PythonAnywhere deployment)
"""
import sys

# Add project path to Python path
path = '/home/yourusername/cw2'  # Change to your actual path
if path not in sys.path:
    sys.path.insert(0, path)

from app import create_app

application = create_app('production')

if __name__ == "__main__":
    application.run()

