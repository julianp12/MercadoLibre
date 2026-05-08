# main.py
import sys
import os

# Agrega la carpeta 'src' al PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from src.boston_housing.application import app
def main():
    app.start_server()

if __name__ == "__main__":
    main()

