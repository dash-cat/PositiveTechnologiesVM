import os
import subprocess
import sys


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