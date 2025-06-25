from pathlib import Path
import shutil
from configuration import *

def clear_directory(path):
    p = Path(path)
    for child in p.iterdir():
        if child.is_file() or child.is_symlink():
            child.unlink()
        elif child.is_dir():
            shutil.rmtree(child)

def borrar_programas():
    for path in program_families:
        clear_directory(f"./programas_generados/{path}")

if __name__ == "__main__":
    borrar_programas()