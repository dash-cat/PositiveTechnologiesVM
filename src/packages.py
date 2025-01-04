import os
import subprocess
import sys

from typing import TypedDict
import winreg

class Package(TypedDict):
    name: str
    version: str
    source: str

def get_linux_debian_packages() -> list[Package]:
    try:
        result = subprocess.run(['dpkg', '-l'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode == 0:
            packages = result.stdout.decode().splitlines()[5:]
            return [
                {"name": pkg.split()[1], "version": pkg.split()[2], "source": "deb"}
                for pkg in packages
            ]
        else:
            print("Error retrieving Debian packages.")
            return []
    except Exception as e:
        print(f"Error: {e}")
        return []


def get_linux_rpm_packages() -> list[Package]:
    try:
        result = subprocess.run(['rpm', '-qa'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode == 0:
            packages = result.stdout.decode().splitlines()
            package_info = []
            for pkg in packages:
                info_result = subprocess.run(['rpm', '-qi', pkg], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                if info_result.returncode == 0:
                    pkg_info = info_result.stdout.decode().splitlines()
                    for line in pkg_info:
                        if line.startswith("Version"):
                            package_info.append({"name": pkg, "version": line.split(":")[1].strip(), "source": "rpm"})
                            break
            return package_info
        else:
            print("Error retrieving RPM packages.")
            return []
    except Exception as e:
        print(f"Error: {e}")
        return []

def get_linux_arch_packages() -> list[Package]:
    try:
        result = subprocess.run(['pacman', '-Q'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode == 0:
            packages = result.stdout.decode().splitlines()
            return [
                {"name": pkg.split()[0], "version": pkg.split()[1], "source": "arch"}
                for pkg in packages
            ]
        else:
            print("Error retrieving Arch packages.")
            return []
    except Exception as e:
        print(f"Error: {e}")
        return []


def get_mac_brew_packages() -> list[Package]:
    try:
        result = subprocess.run(['brew', 'list', '--versions'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode == 0:
            packages = result.stdout.decode().splitlines()
            return [
                {"name": pkg.split()[0], "version": pkg.split()[1], "source": "brew"}
                for pkg in packages
            ]
        else:
            print("Error retrieving Homebrew packages.")
            return []
    except Exception as e:
        print(f"Error: {e}")
        return []
    
def get_windows_winget_packages() -> list[Package]:
    try:
        result = subprocess.run(['winget', 'list'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode == 0:
            packages = result.stdout.decode().splitlines()[1:]
            return [
                {"name": line.split()[0], "version": line.split()[1], "source": "winget"}
                for line in packages if len(line.split()) >= 2
            ]
        else:
            print("Error retrieving winget packages.")
            return []
    except Exception as e:
        print(f"Error: {e}")
        return []

def get_windows_installed_programs() -> list[Package]:
    try:
        programs = []
        for hive in [winreg.HKEY_LOCAL_MACHINE, winreg.HKEY_CURRENT_USER]:
            key_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"
            try:
                with winreg.OpenKey(hive, key_path) as key:
                    for i in range(winreg.QueryInfoKey(key)[0]):
                        subkey_name = winreg.EnumKey(key, i)
                        with winreg.OpenKey(key, subkey_name) as subkey:
                            try:
                                name = winreg.QueryValueEx(subkey, 'DisplayName')[0]
                                version = winreg.QueryValueEx(subkey, 'DisplayVersion')[0]
                                programs.append({"name": name, "version": version, "source": "winreg"})
                            except FileNotFoundError:
                                pass
            except FileNotFoundError:
                continue
        return programs
    except Exception as e:
        print(f"Error: {e}")
        return []

def get_mac_nix_packages() -> list[Package]:
    try:
        result = subprocess.run(['nix-env', '-q'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode == 0:
            return [
                {"name": pkg.split()[0], "version": pkg.split()[1], "source": "Nix"}
                for pkg in result.stdout.decode().splitlines()
            ]
        else:
            print("Ошибка при получении пакетов Nix.")
            return []
    except Exception as e:
        print(f"Ошибка: {e}")
        return []


def get_mac_setapp_apps() -> list[Package]:
    try:
        setapp_path = os.path.expanduser('~/Applications/Setapp')
        if os.path.exists(setapp_path):
            return [{"name": app, "version": "", "source": "Setapp"} for app in os.listdir(setapp_path)]
        return []
    except Exception as e:
        print(f"Ошибка при проверке Setapp приложений: {e}")
        return []


def get_mac_applications() -> list[Package]:
    try:
        applications = os.listdir('/Applications')
        return [
            {"name": app, "version": "", "source": "/Applications"}
            for app in applications if app.endswith('.app')
        ]
    except Exception as e:
        print(f"Ошибка при получении приложений macOS: {e}")
        return []


def get_python_packages() -> list[Package]:
    try:
        result = subprocess.run([sys.executable, '-m', 'pip', 'list'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode == 0:
            packages = result.stdout.decode().splitlines()[2:]  # Skip headers
            return [
                {"name": line.split()[0], "version": line.split()[1], "source": "pip"}
                for line in packages
            ]
        else:
            print("Ошибка при получении Python пакетов.")
            return []
    except Exception as e:
        print(f"Ошибка: {e}")
        return []


def get_flatpak_packages() -> list[Package]:
    try:
        result = subprocess.run(['flatpak', 'list'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode == 0:
            return [
                {"name": pkg.split()[0], "version": pkg.split()[1], "source": "Flatpak"}
                for pkg in result.stdout.decode().splitlines()
            ]
        else:
            print("Ошибка при получении пакетов Flatpak.")
            return []
    except Exception as e:
        print(f"Ошибка: {e}")
        return []

def get_snap_packages() -> list[Package]:
    try:
        result = subprocess.run(['snap', 'list'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode == 0:
            packages = result.stdout.decode().splitlines()[1:]  # Skip header
            return [
                {"name": line.split()[0], "version": line.split()[1], "source": "Snap"}
                for line in packages
            ]
        else:
            print("Ошибка при получении пакетов Snap.")
            return []
    except Exception as e:
        print(f"Ошибка: {e}")
        return []

def get_docker_images() -> list[Package]:
    try:
        result = subprocess.run(['docker', 'images'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode == 0:
            packages = result.stdout.decode().splitlines()[1:]  # Skip header
            return [
                {"name": line.split()[0], "version": line.split()[1], "source": "Docker"}
                for line in packages
            ]
        else:
            print("Ошибка при получении Docker образов.")
            return []
    except Exception as e:
        print(f"Ошибка: {e}")
        return []

def get_helm_charts() -> list[Package]:
    try:
        result = subprocess.run(['helm', 'list', '--all-namespaces'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode == 0:
            packages = result.stdout.decode().splitlines()[1:]  # Skip header
            return [
                {"name": line.split()[0], "version": line.split()[1], "source": "Helm"}
                for line in packages
            ]
        else:
            print("Ошибка при получении Helm чартах.")
            return []
    except Exception as e:
        print(f"Ошибка: {e}")
        return []

def get_node_packages() -> lambdaist[Package]:
    try:
        result = subprocess.run(['npm', 'list', '-g', '--depth=0'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode == 0:
            packages = result.stdout.decode().splitlines()[1:]  # Skip header
            return [
                {"name": line.split()[0], "version": line.split()[1], "source": "npm"}
                for line in packages if " " in line
            ]
        else:
            print("Ошибка при получении пакетов npm.")
            return []
    except Exception as e:
        print(f"Ошибка: {e}")
        return []

def get_yarn_packages() -> list[Package]:
    try:
        result = subprocess.run(['yarn', 'global', 'list'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode == 0:
            packages = result.stdout.decode().splitlines()
            return [
                {"name": line.split()[0], "version": line.split()[1], "source": "Yarn"}
                for line in packages
            ]
        else:
            print("Ошибка при получении пакетов Yarn.")
            return []
    except Exception as e:
        print(f"Ошибка: {e}")
        return []

def get_ruby_gems() -> List[Package]:
    try:
        result = subprocess.run(['gem', 'list'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode == 0:
            packages = result.stdout.decode().splitlines()
            return [
                {"name": line.split()[0], "version": line.split()[1][1:-1], "source": "RubyGems"}
                for line in packages
            ]
        else:
            print("Ошибка при получении Ruby gems.")
            return []
    except Exception as e:
        print(f"Ошибка: {e}")
        return []

def get_cross_platform_packages() -> list[str]:
    """
    Collect all cross-platform packages (e.g., Python, Node.js, Ruby gems).
    Returns:
        list[str]: A combined list of cross-platform packages with their versions.
    """
    try:
        packages = []
        python_packages = get_python_packages()
        if python_packages:
            packages.extend(python_packages)

        try:
            node_packages = get_node_packages()
            if node_packages:
                packages.extend(node_packages)
        except Exception as e:
            print(f"Warning: Could not fetch Node.js packages. {e}")

        try:
            ruby_gems = get_ruby_gems()
            if ruby_gems:
                packages.extend(ruby_gems)
        except Exception as e:
            print(f"Warning: Could not fetch Ruby gems. {e}")

        return packages

    except Exception as e:
        print(f"Error collecting cross-platform packages: {e}")
        return []