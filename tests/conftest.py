# tests/conftest.py
import sys
import os

# Agregar la ruta del proyecto al PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))