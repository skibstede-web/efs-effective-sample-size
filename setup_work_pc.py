#!/usr/bin/env python
"""Check and prepare a Windows/VS Code workstation for the EFS notebooks.

Run from the repository root:

    python setup_work_pc.py

For automatic setup of the project virtual environment:

    python setup_work_pc.py --fix

The script checks Python packages needed by the notebooks and verifies that
Pandoc is available for exporting Word documents with editable equations.
"""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import platform
import shutil
import subprocess
import sys
import venv


REQUIRED_PACKAGES = [
    "numpy",
    "pandas",
    "matplotlib",
    "ipykernel",
    "python-docx",
    "nbformat",
]

IMPORT_NAMES = {
    "python-docx": "docx",
}


def candidate_pandoc_paths() -> list[Path]:
    candidates: list[Path] = []

    direct_path = shutil.which("pandoc")
    if direct_path:
        candidates.append(Path(direct_path))

    for scope in ("User", "Machine"):
        raw_path = os.environ.get("PATH") if scope == "Process" else None
        if scope != "Process":
            raw_path = os.environ.get("PATH")
            if platform.system().lower() == "windows":
                raw_path = os.environ.get("PATH")
        if scope == "User" and platform.system().lower() == "windows":
            raw_path = os.environ.get("PATH")
            try:
                raw_path = os.environ.get("PATH") or ""
                import winreg  # type: ignore

                hive = winreg.HKEY_CURRENT_USER if scope == "User" else winreg.HKEY_LOCAL_MACHINE
                subkey = r"Environment" if scope == "User" else r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment"
                with winreg.OpenKey(hive, subkey) as key:
                    raw_path, _ = winreg.QueryValueEx(key, "Path")
            except OSError:
                raw_path = ""
        elif scope == "Machine" and platform.system().lower() == "windows":
            try:
                import winreg  # type: ignore

                with winreg.OpenKey(
                    winreg.HKEY_LOCAL_MACHINE,
                    r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment",
                ) as key:
                    raw_path, _ = winreg.QueryValueEx(key, "Path")
            except OSError:
                raw_path = ""

        for entry in str(raw_path or "").split(os.pathsep):
            if not entry:
                continue
            candidates.append(Path(entry) / "pandoc.exe")
            candidates.append(Path(entry) / "pandoc")

    candidates.extend(
        [
            Path.home() / "AppData" / "Local" / "Pandoc" / "pandoc.exe",
            Path.home() / "AppData" / "Local" / "Pandoc" / "pandoc",
            Path("C:/Program Files/Pandoc/pandoc.exe"),
            Path("C:/Program Files/Pandoc/pandoc"),
        ]
    )

    unique_candidates: list[Path] = []
    seen: set[str] = set()
    for candidate in candidates:
        key = str(candidate).lower()
        if key in seen:
            continue
        seen.add(key)
        unique_candidates.append(candidate)
    return unique_candidates


def find_pandoc() -> Path | None:
    for candidate in candidate_pandoc_paths():
        if candidate.exists() and candidate.is_file():
            return candidate
    return None


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Check and prepare dependencies for the EFS notebooks and Pandoc Word export."
    )
    parser.add_argument(
        "--fix",
        action="store_true",
        help="Create/update .venv and install required Python packages. Also offers Pandoc install on Windows.",
    )
    parser.add_argument(
        "--no-venv",
        action="store_true",
        help="Install Python packages into the current interpreter instead of creating/updating .venv.",
    )
    parser.add_argument(
        "--upgrade",
        action="store_true",
        help="Upgrade required Python packages even if they are already installed.",
    )
    parser.add_argument(
        "--install-pandoc",
        action="store_true",
        help="Try to install Pandoc with winget if it is missing. Implied by --fix only after confirmation.",
    )
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parent
    os.chdir(repo_root)

    print("EFS workstation check")
    print(f"Repository: {repo_root}")
    print(f"System Python: {sys.executable}")
    print(f"Python version: {platform.python_version()}")
    print()

    py_ok = check_python_version()
    pandoc_ok = check_pandoc()

    if args.fix:
        target_python = sys.executable if args.no_venv else ensure_venv(repo_root)
        install_packages(target_python, REQUIRED_PACKAGES, upgrade=args.upgrade)
        register_ipykernel(target_python, "efs", "EFS (.venv)" if not args.no_venv else "EFS current Python")
        if not pandoc_ok:
            if args.install_pandoc or ask_yes_no("Pandoc is missing. Try to install it with winget now?"):
                pandoc_ok = install_pandoc_with_winget()
    else:
        target_python = current_or_repo_venv_python(repo_root)
        print("Check-only mode. Use --fix to install or update dependencies.")
        print()

    package_ok = check_packages(target_python, REQUIRED_PACKAGES)
    pandoc_ok = check_pandoc()

    print()
    print("Summary")
    print(f"Python version OK: {'yes' if py_ok else 'no'}")
    print(f"Python packages OK: {'yes' if package_ok else 'no'}")
    print(f"Pandoc available: {'yes' if pandoc_ok else 'no'}")

    if target_python:
        print(f"Recommended VS Code interpreter: {target_python}")

    if not pandoc_ok:
        print()
        print("Pandoc is required for editable Word equations.")
        print("Install manually from https://pandoc.org/installing.html or run:")
        print("    winget install --id JohnMacFarlane.Pandoc -e")

    if package_ok and pandoc_ok and py_ok:
        print()
        print("Environment is ready for the notebooks and Pandoc Word export.")
        return 0

    print()
    print("Environment still needs attention. Re-run with --fix after resolving the items above.")
    return 1


def check_python_version() -> bool:
    if sys.version_info < (3, 10):
        print("Python check: FAIL. Python 3.10 or newer is recommended.")
        return False
    print("Python check: OK")
    return True


def current_or_repo_venv_python(repo_root: Path) -> str:
    venv_python = repo_root / ".venv" / "Scripts" / "python.exe"
    if venv_python.exists():
        return str(venv_python)
    return sys.executable


def ensure_venv(repo_root: Path) -> str:
    venv_dir = repo_root / ".venv"
    python_exe = venv_dir / "Scripts" / "python.exe"
    if not python_exe.exists():
        print(f"Creating virtual environment: {venv_dir}")
        venv.EnvBuilder(with_pip=True).create(venv_dir)
    else:
        print(f"Using existing virtual environment: {venv_dir}")
    return str(python_exe)


def install_packages(python_exe: str, packages: list[str], upgrade: bool = False) -> None:
    print()
    print("Installing Python dependencies")
    subprocess.check_call([python_exe, "-m", "pip", "install", "--upgrade", "pip"])
    command = [python_exe, "-m", "pip", "install"]
    if upgrade:
        command.append("--upgrade")
    requirements = Path("requirements.txt")
    if requirements.exists():
        command.extend(["-r", str(requirements)])
    else:
        command.extend(packages)
    subprocess.check_call(command)


def register_ipykernel(python_exe: str, kernel_name: str, display_name: str) -> None:
    print()
    print("Registering VS Code/Jupyter kernel")
    subprocess.check_call(
        [
            python_exe,
            "-m",
            "ipykernel",
            "install",
            "--user",
            "--name",
            kernel_name,
            "--display-name",
            display_name,
        ]
    )


def check_packages(python_exe: str, packages: list[str]) -> bool:
    print()
    print(f"Checking Python packages with: {python_exe}")
    missing: list[str] = []
    for package in packages:
        if package_installed(python_exe, package):
            version = package_version(python_exe, package)
            suffix = f" ({version})" if version else ""
            print(f"  OK      {package}{suffix}")
        else:
            missing.append(package)
            print(f"  MISSING {package}")
    return not missing


def package_installed(python_exe: str, package: str) -> bool:
    import_name = IMPORT_NAMES.get(package, package.replace("-", "_"))
    code = f"import {import_name}"
    completed = subprocess.run([python_exe, "-c", code], capture_output=True, text=True)
    return completed.returncode == 0


def package_version(python_exe: str, package: str) -> str:
    code = (
        "import importlib.metadata as m\n"
        f"print(m.version({package!r}))\n"
    )
    completed = subprocess.run([python_exe, "-c", code], capture_output=True, text=True)
    if completed.returncode != 0:
        return ""
    return completed.stdout.strip()


def check_pandoc() -> bool:
    print()
    print("Checking Pandoc")
    pandoc_path = find_pandoc()
    pandoc = str(pandoc_path) if pandoc_path else None
    if not pandoc:
        print("  MISSING pandoc")
        return False
    pandoc_dir = str(Path(pandoc).parent)
    if pandoc_dir not in os.environ.get("PATH", ""):
        os.environ["PATH"] = os.environ.get("PATH", "") + os.pathsep + pandoc_dir
    completed = subprocess.run([pandoc, "--version"], capture_output=True, text=True, check=False)
    first_line = completed.stdout.splitlines()[0] if completed.stdout else pandoc
    print(f"  OK      {first_line}")
    return True


def install_pandoc_with_winget() -> bool:
    if platform.system().lower() != "windows":
        print("Automatic Pandoc install is only implemented for Windows winget.")
        return False
    if shutil.which("winget") is None:
        print("winget was not found. Install Pandoc manually from https://pandoc.org/installing.html")
        return False
    command = ["winget", "install", "--id", "JohnMacFarlane.Pandoc", "-e"]
    print("Running:", " ".join(command))
    completed = subprocess.run(command, check=False)
    return completed.returncode == 0


def ask_yes_no(prompt: str) -> bool:
    if not sys.stdin.isatty():
        return False
    answer = input(f"{prompt} [y/N] ").strip().lower()
    return answer in {"y", "yes"}


if __name__ == "__main__":
    raise SystemExit(main())
