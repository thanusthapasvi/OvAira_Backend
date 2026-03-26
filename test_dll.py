import ctypes
import os

lib_dir = r"C:\ovadrugx\venv\Lib\site-packages\torch\lib"
os.add_dll_directory(lib_dir)

dlls = [f for f in os.listdir(lib_dir) if f.endswith(".dll")]
for dll in dlls:
    try:
        ctypes.CDLL(os.path.join(lib_dir, dll))
        print(f"Loaded {dll}")
    except Exception as e:
        print(f"FAILED {dll}: {e}")
