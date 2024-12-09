import importlib
import os


def load_tools(package: str, *additional_packages: str) -> list:
    package_list = [package] + list(additional_packages)
    tools = []
    for package_ in package_list:
        dir = package_.replace('.', '/')
        package_ = package_.replace('/', '.')

        for file in os.listdir(dir):
            if not (not file.startswith("__") and file.startswith("_") and file.endswith(".py")):
                continue
                
            name = os.path.splitext(file)[0]
            module = importlib.import_module(f'{package_}.{name}')
            tools.extend(module.tools)
    return tools
