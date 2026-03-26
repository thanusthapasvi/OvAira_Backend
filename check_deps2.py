import pefile
import os

def check_dll(pe_path):
    pe = pefile.PE(pe_path)
    missing = []
    for entry in pe.DIRECTORY_ENTRY_IMPORT:
        dll = entry.dll.decode('utf-8')
        found = False
        paths = [
            r"C:\Windows\System32",
            r"C:\ovadrugx\venv\Lib\site-packages\torch\lib",
            r"C:\ovadrugx\venv\Scripts"
        ]
        for p in paths:
            if os.path.exists(os.path.join(p, dll)):
                found = True
                break
        if not found:
            missing.append(dll)
    return missing

lib_dir = r"C:\ovadrugx\venv\Lib\site-packages\torch\lib"
print("Missing for c10:")
print(check_dll(os.path.join(lib_dir, "c10.dll")))

print("Missing for torch_cpu:")
print(check_dll(os.path.join(lib_dir, "torch_cpu.dll")))
