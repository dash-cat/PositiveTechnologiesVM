import os
import subprocess
import sys

from typing import Callable, List, TypedDict

class Package(TypedDict):
    name: str
    version: str
    source: str

def get_packages_generic(
    command: list[str],
    source: str,
    stdout_mapper: Callable[[list[str]], list[str]],
    get_name: Callable[[str], str],
    get_version: Callable[[str], str],
) -> list[Package]:
    try:
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode == 0:
            mapped_stdout = stdout_mapper(result.stdout.decode().splitlines())
            return [
                {"name": get_name(line), "version": get_version(line), "source": source}
                for line in mapped_stdout
            ]
        else:
            print(f"failed to retrieve packages from {source}.")
            return []
    except Exception as e:
        print(f"Error: {e}")
        return []

def get_linux_debian_packages() -> List[Package]:
    return get_packages_generic(
        command=["dpkg", "-l"],
        source="deb",
        stdout_mapper=lambda lines: lines[5:],
        get_name=lambda line: line.split()[1],
        get_version=lambda line: line.split()[2],
    )



def get_linux_rpm_packages() -> List[Package]:
    return get_packages_generic(
        command=["rpm", "-qa"],
        source="rpm",
        stdout_mapper=lambda lines: lines,
        get_name=lambda line: line,
        get_version=lambda line: subprocess.run(
            ["rpm", "-q", "--qf", "%{VERSION}", line],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        ).stdout.decode().strip(),
    )

def get_linux_arch_packages() -> List[Package]:
    return get_packages_generic(
        command=["pacman", "-Q"],
        source="arch",
        stdout_mapper=lambda lines: lines,
        get_name=lambda line: line.split()[0],
        get_version=lambda line: line.split()[1],
    )


def get_mac_brew_packages() -> List[Package]:
    return get_packages_generic(
        command=["brew", "list", "--versions"],
        source="brew",
        stdout_mapper=lambda lines: lines,
        get_name=lambda line: line.split()[0],
        get_version=lambda line: line.split()[1],
    )


def get_windows_winget_packages() -> List[Package]:
    return get_packages_generic(
        command=["winget", "list"],
        source="winget",
        stdout_mapper=lambda lines: lines[1:],  # Skip header
        get_name=lambda line: line.split()[0],
        get_version=lambda line: line.split()[1] if len(line.split()) > 1 else "",
    )


def get_windows_installed_programs() -> List[Package]:
    import winreg

    try:
        programs = []
        for hive in [winreg.HKEY_LOCAL_MACHINE, winreg.HKEY_CURRENT_USER]:
            key_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"
            with winreg.OpenKey(hive, key_path) as key:
                for i in range(winreg.QueryInfoKey(key)[0]):
                    subkey_name = winreg.EnumKey(key, i)
                    with winreg.OpenKey(key, subkey_name) as subkey:
                        try:
                            name = winreg.QueryValueEx(subkey, "DisplayName")[0]
                            version = winreg.QueryValueEx(subkey, "DisplayVersion")[0]
                            programs.append({"name": name, "version": version, "source": "winreg"})
                        except FileNotFoundError:
                            continue
        return programs
    except Exception as e:
        print(f"Error: {e}")
        return []

def get_mac_nix_packages() -> List[Package]:
    return get_packages_generic(
        command=["nix-env", "-q"],
        source="Nix",
        stdout_mapper=lambda lines: lines,
        get_name=lambda line: line.split()[0],
        get_version=lambda line: line.split()[1],
    )



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
            # XXX
            {"name": app, "version": "", "source": "/Applications"}
            for app in applications if app.endswith('.app')
        ]
    except Exception as e:
        print(f"Ошибка при получении приложений macOS: {e}")
        return []


def get_python_packages() -> List[Package]:
    return get_packages_generic(
        command=[sys.executable, "-m", "pip", "list"],
        source="pip",
        stdout_mapper=lambda lines: lines[2:],  # Skip headers
        get_name=lambda line: line.split()[0],
        get_version=lambda line: line.split()[1],
    )


def get_flatpak_packages() -> List[Package]:
    return get_packages_generic(
        command=["flatpak", "list"],
        source="Flatpak",
        stdout_mapper=lambda lines: lines,
        get_name=lambda line: line.split()[0],
        get_version=lambda line: line.split()[1],
    )

def get_snap_packages() -> List[Package]:
    return get_packages_generic(
        command=["snap", "list"],
        source="Snap",
        stdout_mapper=lambda lines: lines[1:],  # Skip header
        get_name=lambda line: line.split()[0],
        get_version=lambda line: line.split()[1],
    )

def get_docker_images() -> List[Package]:
    return get_packages_generic(
        command=["docker", "images"],
        source="Docker",
        stdout_mapper=lambda lines: lines[1:],  # Skip header
        get_name=lambda line: line.split()[0],
        get_version=lambda line: line.split()[1],
    )

def get_helm_charts() -> List[Package]:
    return get_packages_generic(
        command=["helm", "list", "--all-namespaces"],
        source="Helm",
        stdout_mapper=lambda lines: lines[1:],  # Skip header
        get_name=lambda line: line.split()[0],
        get_version=lambda line: line.split()[1],
    )

def get_node_packages() -> List[Package]:
    return get_packages_generic(
        command=["npm", "list", "-g", "--depth=0"],
        source="npm",
        stdout_mapper=lambda lines: lines[1:],  # Skip header
        get_name=lambda line: line.split()[0],
        get_version=lambda line: line.split()[1] if len(line.split()) > 1 else "",
    )

def get_yarn_packages() -> List[Package]:
    return get_packages_generic(
        command=["yarn", "global", "list"],
        source="Yarn",
        stdout_mapper=lambda lines: lines,
        get_name=lambda line: line.split()[0],
        get_version=lambda line: line.split()[1] if len(line.split()) > 1 else "",
    )

def get_ruby_gems() -> List[Package]:
    return get_packages_generic(
        command=["gem", "list"],
        source="RubyGems",
        stdout_mapper=lambda lines: lines,
        get_name=lambda line: line.split()[0],
        get_version=lambda line: line.split()[1][1:-1] if len(line.split()) > 1 else "",
    )


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