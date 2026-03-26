import os
import sys
import shutil

torch_lib = r"C:\ovadrugx\venv\Lib\site-packages\torch\lib"
# Find all dlls in python base prefix
base = sys.base_prefix
found = 0
for root, _, files in os.walk(base):
    for f in files:
        if f.startswith("api-ms-win-crt") and f.endswith(".dll") or f.startswith("vcruntime140") or f.startswith("msvcp140"):
            src = os.path.join(root, f)
            dst = os.path.join(torch_lib, f)
            if not os.path.exists(dst):
                try:
                    shutil.copy(src, dst)
                    found += 1
                except:
                    pass
print(f"Copied {found} dlls to {torch_lib}")
