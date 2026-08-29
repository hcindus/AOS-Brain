import sys
print("EXE:", sys.executable)
print("VERSION:", sys.version_info)
for p in sys.path:
    print("PATH:", p)
try:
    import requests; print("requests OK:", requests.__version__)
except Exception as e:
    print("requests ERR:", e)
try:
    import playwright; print("playwright OK")
except Exception as e:
    print("playwright ERR:", e)
