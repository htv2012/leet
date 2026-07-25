import argparse
import importlib.metadata
import os
import pathlib
import subprocess

from . import data
from .data import SETTINGS
from .parse import extract_details
from .version import __version__

CLI_NAME = "leet"

try:
    __version__ = importlib.metadata.version(CLI_NAME)
except importlib.metadata.PackageNotFoundError:
    __version__ = "0.0.0-dev"


def create_uv_project(root, name, description):
    os.chdir(root)
    subprocess.run(
        ["uv", "init", "--name", name, "--description", description], check=False
    )
    subprocess.run(["uv", "add", "--dev", "pytest", "ruff", "ty"], check=False)


def main():
    """Entry"""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-r",
        "--root",
        type=pathlib.Path,
        default=pathlib.Path("~/Projects/interview-questions/leetcode").expanduser(),
    )
    parser.add_argument("-d", "--dump")
    parser.add_argument(
        "-V", "--version", action="version", version=f"%(prog)s {__version__}"
    )
    parser.add_argument("url")
    parser.add_argument(
        "-V", "--version", action="version", version=f"{CLI_NAME} v{__version__}"
    )
    options = parser.parse_args()

    details = extract_details(options.url, options.dump)

    # Determine the root: leetcode dir
    assert options.root.exists()
    os.chdir(options.root)

    # Create the directories
    project_dir = options.root / details["dir"]
    project_dir.mkdir()
    vscode_dir = project_dir / ".vscode"
    vscode_dir.mkdir()

    # Create the project using uv, we don't need main.py
    create_uv_project(project_dir, details["project_id"], details["description"])
    main_script = project_dir / "main.py"
    main_script.unlink()

    # Create the files
    data.update_pyproject(project_dir)
    data.write_file(project_dir, "README.md", details["readme"])
    data.write_file(project_dir, "Makefile")
    data.write_file(project_dir, "solution.py", details["code"])
    data.write_file(project_dir, "test_solution.py", details["test"])
    data.write_file(vscode_dir, "settings.json", SETTINGS)
    pathlib.Path("/tmp/leetdir").write_text(f"cd {project_dir}")
