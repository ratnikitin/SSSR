import os

abs_path = os.path.abspath(__file__)

base_path = os.path.abspath(os.curdir)

rel_path = os.path.relpath(abs_path, base_path)

print(rel_path)
