

from OS import OS, get_system
from packages import get_python_packages



if __name__ == "__main__":
    system = get_system()
    installed_packages = system.get_packages()
    installed_packages.extend(get_python_packages())
    
    print("\n".join(installed_packages))
