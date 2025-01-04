

from OS import OS, get_system
from packages import get_cross_platform_packages



if __name__ == "__main__":
    print("\n".join(get_system().get_packages().extend(get_cross_platform_packages())))
