import os
import importlib

package_dir = os.path.dirname(__file__)

for root, dirs, files in os.walk(package_dir):
    for file in files:
        if file.endswith('.py') and file != '__init__.py':
            rel_dir = os.path.relpath(root, package_dir)
            module_name = file[:-3]
            if rel_dir == '.':
                import_path = f".{module_name}"
            else:
                import_path = "." + ".".join(rel_dir.split(os.sep)) + f".{module_name}"
            importlib.import_module(import_path, package=__package__)