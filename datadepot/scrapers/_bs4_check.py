#!/usr/bin/env python3
import sys
print(sys.executable)
try:
    from bs4 import BeautifulSoup
    print("bs4 OK")
except Exception as e:
    print("bs4 ERR:", e)
try:
    import lxml
    print("lxml OK")
except Exception as e:
    print("lxml ERR:", e)
