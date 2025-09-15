import json
import sys
from pathlib import Path

def notebook_to_py(ipynb_path, py_path=None):
    """
    Convierte un archivo .ipynb a .py concatenando todas las celdas de código.

    Args:
        ipynb_path (str o Path): ruta del archivo .ipynb
        py_path (str o Path, opcional): ruta de salida del archivo .py
                                        Si no se da, se usará el mismo nombre.
    """
    ipynb_path = Path(ipynb_path)
    if py_path is None:
        py_path = ipynb_path.with_suffix(".py")
    else:
        py_path = Path(py_path)

    # Leer notebook como JSON
    with open(ipynb_path, "r", encoding="utf-8") as f:
        notebook = json.load(f)

    # Extraer código
    code_lines = []
    for cell in notebook.get("cells", []):
        if cell.get("cell_type") == "code":
            code_lines.append("# In[ ]:\n")
            code_lines.extend(cell.get("source", []))
            code_lines.append("\n\n")

    # Guardar en archivo .py
    with open(py_path, "w", encoding="utf-8") as f:
        f.writelines(code_lines)

    print(f"Archivo .py guardado en: {py_path}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python ipynb_to_py.py archivo.ipynb [salida.py]")
    else:
        notebook_to_py(*sys.argv[1:])
