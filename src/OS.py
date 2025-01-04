import platform
import distro
from dataclasses import dataclass
from packages import (
    get_linux_arch_packages,
    get_linux_debian_packages,
    get_linux_rpm_packages,
    get_mac_applications,
    get_mac_brew_packages,
    get_windows_winget_packages,
    get_windows_installed_programs,
)


@dataclass
class OS:
    family: str
    get_packages: callable[[], list[str]]


# Define OS configurations for each supported type
debian = OS(family="linux", get_packages=get_linux_debian_packages)
rpm_based = OS(family="linux", get_packages=get_linux_rpm_packages)
arch_based = OS(family="linux", get_packages=get_linux_arch_packages)
macos = OS(family="darwin", get_packages=lambda: get_mac_brew_packages() + get_mac_applications())
windows = OS(
    family="windows",
    get_packages=lambda: get_windows_winget_packages() + get_windows_installed_programs(),
)


def get_system() -> OS:
    system_name = platform.system().lower()
    system = None

    match system_name:
        case 'linux':
            distro_name = distro.id().lower()  # Get the Linux distribution name
            match distro_name:
                case name if 'debian' in name or 'ubuntu' in name:
                    system = debian
                case name if 'centos' in name or 'fedora' in name or 'redhat' in name:
                    system = rpm_based
                case name if 'arch' in name:
                    system = arch_based
                case _:
                    raise RuntimeError(f"Unknown Linux distribution: {distro_name}.")
        case 'darwin':
            system = macos
        case 'windows':
            system = windows
        case _:
            raise RuntimeError(f"Unsupported operating system: {system_name}.")

    return system
