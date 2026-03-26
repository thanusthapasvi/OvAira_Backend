import pefile
pe = pefile.PE(r"C:\ovadrugx\venv\Lib\site-packages\torch\lib\c10.dll")
print("Dependencies of c10.dll:")
for entry in pe.DIRECTORY_ENTRY_IMPORT:
    print(entry.dll.decode('utf-8'))
