# Per-Vertex Colored OBJ Importer

This script is used to import OBJ files with per-vertex coloring into Maya. It was originally built to import the OBJ output of the 3D Face Reconstruction Tool (<a href="https://github.com/AaronJackson/vrn">https://github.com/AaronJackson/vrn</a>). For OBJ files that do not have per-vertex coloring you can use Maya's built-in OBJ importer.

## Usage

Install the script into your Maya script directory, then from within Maya use the following:

For versions of Maya BEFORE 2022:
```
import convert_face_obj
reload(convert_face_obj)
convert_face_obj.run()
```

For versions of Maya 2022 or higher:
```
import convert_face_obj
import importlib
importlib.reload(convert_face_obj)
convert_face_obj.run()
```
