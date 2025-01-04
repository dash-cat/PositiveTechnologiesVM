

from OS import OS, get_system
from packages import get_cross_platform_packages



if __name__ == "__main__":
    pkgs = get_system().get_packages()
    pkgs.extend(get_cross_platform_packages())
    for pkg in pkgs:
        print(pkg)
