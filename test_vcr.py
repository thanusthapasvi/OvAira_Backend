import os
import sys
import shutil

torch_lib = r"C:\ovaira\venv\Lib\site-packages\torch\lib"
base = sys.base_prefix
found = False
for root, _, files in os.walk(base):
    for f in files:
        if f.lower() == "vcruntime140_1.dll":
            try:
                shutil.copy(os.path.join(root, f), torch_lib)
                print(f"Copied {f}")
                found = True
            except Exception as e:
                print(e)
                pass

if not found:
    print("Could not find vcruntime140_1.dll in python base")

print("Testing torch...")
try:
    import torch
    print("Torch loaded successfully! Version:", torch.__version__)
except Exception as e:
    print("Error:", e)
