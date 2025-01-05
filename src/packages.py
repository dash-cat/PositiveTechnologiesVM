import os
import plistlib
import re
import subprocess
import sys
import asyncio

import time
from typing import Callable, Dict, List, TypedDict
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filename="package_scanner.log",
    filemode="w",
)
logger = logging.getLogger(__name__)

class Package(TypedDict):
    name: str
    version: str
    source: str

def is_command_available(command: str) -> bool:
    try:
        result = subprocess.run(
            ["which", command],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        return result.returncode == 0
    except Exception as e:
        logger.error(f"Error checking availability of command '{command}': {e}")
        return False

async def run_command_async(command: list[str]) -> list[str]:
    if not is_command_available(command[0]):
        logger.warning(f"Command '{command[0]}' is not available. Skipping.")
        return []

    try:
        process = await asyncio.create_subprocess_exec(
            *command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()
        if process.returncode == 0:
            return stdout.decode().splitlines()
        else:
            logger.warning(f"Command '{' '.join(command)}' failed with return code {process.returncode}")
            return []
    except Exception as e:
        logger.error(f"Error executing command '{' '.join(command)}': {e}")
        return []



async def get_packages_generic_async(
    command: list[str],
    source: str,
    stdout_mapper: Callable[[list[str]], list[str]],
    get_name: Callable[[str], str],
    get_version: Callable[[str], str],
) -> list[Package]:
    lines = await run_command_async(command)
    if lines:
        mapped_stdout = stdout_mapper(lines)
        return [
            {"name": get_name(line), "version": get_version(line), "source": source}
            for line in mapped_stdout
        ]
    return []

def get_packages_generic(
    command: list[str],
    source: str,
    stdout_mapper: Callable[[list[str]], list[str]],
    get_name: Callable[[str], str],
    get_version: Callable[[str], str],
) -> list[Package]:
    try:
        logger.info(f"Executing command: {' '.join(command)}")
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode == 0:
            mapped_stdout = stdout_mapper(result.stdout.decode().splitlines())
            logger.info(f"Command executed successfully: {' '.join(command)}")
            return [
                {"name": get_name(line), "version": get_version(line), "source": source}
                for line in mapped_stdout
            ]
        else:
            logger.warning(f"Command {command} failed with return code {result.returncode}")
            return []
    except Exception as e:
        logger.error(f"Error executing command {command} for {source}: {e}")
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
        logger.info("Fetching installed programs from Windows registry")
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
        logger.info(f"Found {len(programs)} installed programs in Windows registry")
        return programs
    except Exception as e:
        logger.error(f"Error fetching Windows installed programs: {e}")
        return []

def get_mac_nix_packages() -> List[Package]:
    return get_packages_generic(
        command=["nix-env", "-q"],
        source="Nix",
        stdout_mapper=lambda lines: lines,
        get_name=lambda line: line.split()[0],
        get_version=lambda line: line.split()[1],
    )

def get_app_version_openstep(app_path: str) -> str:
    info_plist_path = os.path.join(app_path, 'Contents', 'Info.plist')
    if os.path.exists(info_plist_path):
        try:
            with open(info_plist_path, 'rb') as plist_file:
                plist_data = plistlib.load(plist_file, fmt=plistlib.FMT_XML)
                return plist_data.get('CFBundleShortVersionString', 'Unknown version')
        except Exception as e:
            logger.error(f"Error reading Info.plist for {app_path}: {e}")
            return 'Error reading version'
    else:
        logger.warning(f"Info.plist not found for {app_path}")
        return 'Info.plist not found'

def get_mac_setapp_apps() -> List[Dict[str, str]]:
    try:
        logger.info("Fetching Setapp applications")
        setapp_path = os.path.expanduser('~/Applications/Setapp')
        if os.path.exists(setapp_path):
            apps = []
            for app in os.listdir(setapp_path):
                app_path = os.path.join(setapp_path, app)
                version = get_app_version_openstep(app_path) if app.endswith('.app') else ''
                apps.append({"name": app, "version": version, "source": "Setapp"})
            logger.info(f"Found {len(apps)} Setapp applications")
            return apps
        logger.warning("Setapp directory not found")
        return []
    except Exception as e:
        logger.error(f"Error fetching Setapp applications: {e}")
        return []

def get_mac_applications() -> List[Dict[str, str]]:
    try:
        logger.info("Fetching macOS applications")
        applications = os.listdir('/Applications')
        apps = []
        for app in applications:
            app_path = os.path.join('/Applications', app)
            if app.endswith('.app'):
                version = get_app_version_openstep(app_path)
                apps.append({"name": app, "version": version, "source": "/Applications"})
        logger.info(f"Found {len(apps)} macOS applications")
        return apps
    except Exception as e:
        logger.error(f"Error fetching macOS applications: {e}")
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
    logger.info("Fetching npm packages")
    return get_packages_generic(
        command=["npm", "list", "-g", "--depth=0"],
        source="npm",
        stdout_mapper=lambda lines: [line for line in lines if line.strip()],
        get_name=lambda line: line.split("@")[0],
        get_version=lambda line: line.split("@")[1] if "@" in line else "unknown",
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
    version_regex = re.compile(r'\(([^:]+):?\s*([^)]+)\)')
    return get_packages_generic(
        command=["gem", "list"],
        source="RubyGems",
        stdout_mapper=lambda lines: lines,
        get_name=lambda line: line.split()[0],
        get_version=lambda line: (
            version_match.group(2)
            if (version_match := version_regex.search(line)) 
            else ""
        ),
    )

def get_conda_packages() -> List[Package]:
    return get_packages_generic(
        command=["conda", "list", "--json"],
        source="conda",
        stdout_mapper=lambda lines: eval("".join(lines)),  # Преобразование JSON в Python-объект
        get_name=lambda pkg: pkg["name"],
        get_version=lambda pkg: pkg["version"],
    )


def get_flatpak_apps() -> List[Package]:
    return get_packages_generic(
        command=["flatpak", "list", "--app"],
        source="Flatpak Apps",
        stdout_mapper=lambda lines: lines,
        get_name=lambda line: line.split()[0],
        get_version=lambda line: line.split()[1],
    )


def get_appimage_apps() -> List[Package]:
    try:
        logger.info("Searching for AppImage applications")
        appimage_paths = subprocess.run(
            ["find", "/opt", "-type", "f", "-name", "*.AppImage"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=30
        ).stdout.decode().splitlines()

        packages = []
        for path in appimage_paths:
            name = os.path.basename(path)
            version = "unknown"
            try:
                version_output = subprocess.run(
                    [path, "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE
                ).stdout.decode()
                version = version_output.splitlines()[0] if version_output else "unknown"
            except Exception as e:
                logger.warning(f"Could not fetch version for AppImage: {name}. {e}")
            packages.append({"name": name, "version": version, "source": "AppImage"})
        logger.info(f"Found {len(packages)} AppImage applications")
        return packages
    except Exception as e:
        logger.error(f"Error fetching AppImage applications: {e}")
        return []


def get_kde_store_apps() -> List[Package]:
    return get_packages_generic(
        command=["plasma-discover", "--list-installed"],
        source="KDE Store",
        stdout_mapper=lambda lines: lines,
        get_name=lambda line: line.split()[0],
        get_version=lambda line: line.split()[1],
    )


def get_snap_classic_apps() -> List[Package]:
    return get_packages_generic(
        command=["snap", "list", "--classic"],
        source="Snap Classic",
        stdout_mapper=lambda lines: lines[1:],  # Пропустить заголовок
        get_name=lambda line: line.split()[0],
        get_version=lambda line: line.split()[1],
    )


def get_flatpak_runtime_packages() -> List[Package]:
    return get_packages_generic(
        command=["flatpak", "list", "--runtime"],
        source="Flatpak Runtime",
        stdout_mapper=lambda lines: lines,
        get_name=lambda line: line.split()[0],
        get_version=lambda line: line.split()[1],
    )

async def get_cross_platform_packages() -> list[str]:
    tasks = [
        get_packages_generic_async(["dpkg", "-l"], "deb", lambda lines: lines[5:], lambda line: line.split()[1], lambda line: line.split()[2]),
        get_packages_generic_async([sys.executable, "-m", "pip", "list"], "pip", lambda lines: lines[2:], lambda line: line.split()[0], lambda line: line.split()[1]),
        # get_packages_generic_async(["npm", "list", "-g", "--depth=0"], "npm", lambda lines: [line.strip() for line in lines if line.strip()], lambda line: line.split("@")[0], lambda line: line.split("@")[1] if "@" in line else "unknown"),
        get_packages_generic_async(["gem", "list"], "RubyGems", lambda lines: lines, lambda line: line.split()[0], lambda line: (re.search(r'\(([^:]+):?\s*([^)]+)\)', line).group(2) if re.search(r'\(([^:]+):?\s*([^)]+)\)', line) else "")),
        get_packages_generic_async(["conda", "list", "--json"], "conda", lambda lines: eval("".join(lines)), lambda pkg: pkg["name"], lambda pkg: pkg["version"]),
        get_packages_generic_async(["flatpak", "list"], "Flatpak", lambda lines: lines, lambda line: line.split()[0], lambda line: line.split()[1]),
        get_packages_generic_async(["snap", "list"], "Snap", lambda lines: lines[1:], lambda line: line.split()[0], lambda line: line.split()[1]),
        get_packages_generic_async(["docker", "images"], "Docker", lambda lines: lines[1:], lambda line: line.split()[0], lambda line: line.split()[1]),
        get_packages_generic_async(["helm", "list", "--all-namespaces"], "Helm", lambda lines: lines[1:], lambda line: line.split()[0], lambda line: line.split()[1]),
        get_packages_generic_async(["find", "/opt", "-type", "f", "-name", "*.AppImage"], "AppImage", lambda lines: lines, lambda line: os.path.basename(line), lambda line: "unknown"),
        get_packages_generic_async(["brew", "list", "--versions"], "brew", lambda lines: lines, lambda line: line.split()[0], lambda line: line.split()[1]),
        # get_packages_generic_async(["ls", "/Applications"], "macOS Apps", lambda lines: lines, lambda line: line.split()[0], lambda line: "unknown")
        get_packages_generic_async(
            ["npm", "list", "-g", "--depth=0"],
            "npm",
            lambda lines: [
                line.strip() 
                for line in lines 
                if line.strip() and re.search(r"(?:──\s+|^)(@?.*?)\s*@", line) and re.search(r"@([\d.]+)$", line)
            ],
            lambda line: re.search(r"(?:──\s+|^)(@?.*?)\s*@", line).group(1).strip(),
            lambda line: re.search(r"@([\d.]+)$", line).group(1).strip()
        )

    ]
    start_time = time.time()
    results = await asyncio.gather(*tasks)
    elapsed_time = time.time() - start_time
    logger.info(f"All tasks completed in {elapsed_time:.2f} seconds.")

    packages = [pkg for result in results for pkg in result]
    return packages