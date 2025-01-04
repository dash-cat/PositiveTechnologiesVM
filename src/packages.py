import os
import subprocess
import sys

import winreg



def get_linux_debian_packages():
    """Получить список пакетов для Debian/Ubuntu систем с версиями."""
    try:
        result = subprocess.run(['dpkg', '-l'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode == 0:
            packages = result.stdout.decode().splitlines()[5:]  # Пропускаем заголовок
            return [pkg.split()[1] + " " + pkg.split()[2] for pkg in packages]
        else:
            print("Ошибка при получении пакетов Debian.")
            return []
    except Exception as e:
        print(f"Ошибка: {e}")
        return []


def get_linux_rpm_packages():
    """Получить список пакетов для систем на базе RedHat (CentOS, Fedora) с версиями."""
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
                            package_info.append(pkg + " " + line.split(":")[1].strip())
                            break
            return package_info
        else:
            print("Ошибка при получении пакетов RPM.")
            return []
    except Exception as e:
        print(f"Ошибка: {e}")
        return []


def get_linux_arch_packages():
    """Получить список пакетов для Arch-based систем с версиями."""
    try:
        result = subprocess.run(['pacman', '-Q'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode == 0:
            packages = result.stdout.decode().splitlines()
            return packages
        else:
            print("Ошибка при получении пакетов Arch.")
            return []
    except Exception as e:
        print(f"Ошибка: {e}")
        return []


def get_mac_brew_packages():
    """Получить список пакетов, установленных через Homebrew на macOS с версиями."""
    try:
        result = subprocess.run(['brew', 'list', '--versions'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode == 0:
            packages = result.stdout.decode().splitlines()
            return packages
        else:
            print("Ошибка при получении пакетов Homebrew.")
            return []
    except Exception as e:
        print(f"Ошибка: {e}")
        return []


def get_mac_nix_packages():
    """Получить список пакетов, установленных через Nix на macOS с версиями."""
    try:
        result = subprocess.run(['nix-env', '-q'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode == 0:
            return result.stdout.decode().splitlines()
        else:
            print("Ошибка при получении пакетов Nix.")
            return []
    except Exception as e:
        print(f"Ошибка: {e}")
        return []


def get_mac_setapp_apps():
    """Проверить наличие приложений, установленных через Setapp (если доступно)."""
    try:
        setapp_path = os.path.expanduser('~/Applications/Setapp')
        if os.path.exists(setapp_path):
            return os.listdir(setapp_path)
        return []
    except Exception as e:
        print(f"Ошибка при проверке Setapp приложений: {e}")
        return []


def get_mac_applications():
    """Получить список приложений в папке /Applications на macOS."""
    try:
        applications = os.listdir('/Applications')
        return [app for app in applications if app.endswith('.app')]
    except Exception as e:
        print(f"Ошибка при получении приложений macOS: {e}")
        return []


def get_python_packages():
    """Получить список Python пакетов через pip с версиями."""
    try:
        result = subprocess.run([sys.executable, '-m', 'pip', 'list'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode == 0:
            packages = result.stdout.decode().splitlines()[2:]  # Скипаем заголовки
            return packages
        else:
            print("Ошибка при получении Python пакетов.")
            return []
    except Exception as e:
        print(f"Ошибка: {e}")
        return []

def get_windows_winget_packages():
    """Получить список приложений, установленных через winget."""
    try:
        result = subprocess.run(['winget', 'list'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode == 0:
            packages = result.stdout.decode().splitlines()
            return packages[1:]  # Пропускаем заголовок
        else:
            print("Ошибка при получении пакетов winget.")
            return []
    except Exception as e:
        print(f"Ошибка: {e}")
        return []


def get_windows_installed_programs():
    """Получить список установленных программ на Windows через реестр."""
    try:
        programs = []
        for hive in [winreg.HKEY_LOCAL_MACHINE, winreg.HKEY_CURRENT_USER]:
            key_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"
            try:
                with winreg.OpenKey(hive, key_path) as key:
                    for i in range(winreg.QueryInfoKey(key)[0]):  # Количество подкаталогов
                        subkey_name = winreg.EnumKey(key, i)
                        with winreg.OpenKey(key, subkey_name) as subkey:
                            try:
                                name = winreg.QueryValueEx(subkey, 'DisplayName')[0]
                                version = winreg.QueryValueEx(subkey, 'DisplayVersion')[0]
                                programs.append(f"{name} {version}")
                            except FileNotFoundError:
                                pass
            except FileNotFoundError:
                continue
        return programs
    except Exception as e:
        print(f"Ошибка: {e}")
        return []

def get_flatpak_packages():
    """Получить список пакетов, установленных через Flatpak."""
    try:
        result = subprocess.run(['flatpak', 'list'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode == 0:
            return result.stdout.decode().splitlines()
        else:
            print("Ошибка при получении пакетов Flatpak.")
            return []
    except Exception as e:
        print(f"Ошибка: {e}")
        return []

def get_snap_packages():
    """Получить список пакетов, установленных через Snap."""
    try:
        result = subprocess.run(['snap', 'list'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode == 0:
            packages = result.stdout.decode().splitlines()[1:]  # Пропускаем заголовок
            return packages
        else:
            print("Ошибка при получении пакетов Snap.")
            return []
    except Exception as e:
        print(f"Ошибка: {e}")
        return []

def get_docker_images():
    """Получить список Docker образов с тегами."""
    try:
        result = subprocess.run(['docker', 'images'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode == 0:
            packages = result.stdout.decode().splitlines()[1:]  # Пропускаем заголовок
            return packages
        else:
            print("Ошибка при получении Docker образов.")
            return []
    except Exception as e:
        print(f"Ошибка: {e}")
        return []

def get_helm_charts():
    """Получить список установленных Helm чартах в Kubernetes."""
    try:
        result = subprocess.run(['helm', 'list', '--all-namespaces'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode == 0:
            packages = result.stdout.decode().splitlines()[1:]  # Пропускаем заголовок
            return packages
        else:
            print("Ошибка при получении Helm чартах.")
            return []
    except Exception as e:
        print(f"Ошибка: {e}")
        return []

def get_node_packages():
    """Получить список пакетов Node.js (npm)."""
    try:
        result = subprocess.run(['npm', 'list', '-g', '--depth=0'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode == 0:
            packages = result.stdout.decode().splitlines()
            return packages[1:]  # Пропускаем заголовок
        else:
            print("Ошибка при получении пакетов npm.")
            return []
    except Exception as e:
        print(f"Ошибка: {e}")
        return []

def get_yarn_packages():
    """Получить список пакетов Yarn."""
    try:
        result = subprocess.run(['yarn', 'global', 'list'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode == 0:
            packages = result.stdout.decode().splitlines()
            return packages
        else:
            print("Ошибка при получении пакетов Yarn.")
            return []
    except Exception as e:
        print(f"Ошибка: {e}")
        return []

def get_ruby_gems():
    """Получить список установленных Ruby gems."""
    try:
        result = subprocess.run(['gem', 'list'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode == 0:
            return result.stdout.decode().splitlines()
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
        # Collect Python packages
        python_packages = get_python_packages()
        if python_packages:
            packages.extend(python_packages)

        # Collect Node.js packages (if applicable)
        try:
            node_packages = get_node_packages()
            if node_packages:
                packages.extend(node_packages)
        except Exception as e:
            print(f"Warning: Could not fetch Node.js packages. {e}")

        # Collect Ruby gems (if applicable)
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