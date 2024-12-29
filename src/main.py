import os
import sys
import subprocess
import platform
import distro

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
            # Получаем версии пакетов с помощью rpm -qi
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

def get_installed_packages():
    system = platform.system().lower()
    
    installed_packages = []
    
    # Для разных систем выполняем разные проверки
    if system == 'linux':
        # Для Linux систем выбираем подходящий менеджер пакетов
        distro_name = distro.id().lower()  # Получаем название дистрибутива
        
        if 'debian' in distro_name or 'ubuntu' in distro_name:
            installed_packages.extend(get_linux_debian_packages())
        elif 'centos' in distro_name or 'fedora' in distro_name or 'redhat' in distro_name:
            installed_packages.extend(get_linux_rpm_packages())
        elif 'arch' in distro_name:
            installed_packages.extend(get_linux_arch_packages())
        else:
            print(f"Неизвестная Linux-дистрибуция: {distro_name}.")
    
    elif system == 'darwin':  # Для macOS
        installed_packages.extend(get_mac_brew_packages())
    
    # Получаем Python пакеты
    installed_packages.extend(get_python_packages())
    
    return installed_packages

if __name__ == "__main__":
    installed_packages = get_installed_packages()
    print("\n".join(installed_packages))
