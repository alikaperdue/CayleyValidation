"""Record source identities for reports produced by the two checkouts."""

import hashlib
import subprocess
from pathlib import Path

from tests import KERNEL_ROOT

VALIDATION_ROOT = Path(__file__).resolve().parents[2]


def _git_head(root):
    # An installed wheel may live inside a venv in an unrelated Git checkout.
    prefix = subprocess.run(
        ["git", "rev-parse", "--show-prefix"],
        cwd=root,
        capture_output=True,
        text=True,
        check=False,
    )
    if prefix.returncode or prefix.stdout.strip():
        return None
    return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root, text=True).strip()


def source_provenance(files):
    hashes = {}
    for path in sorted(files):
        path = path.resolve()
        # Keep the historical repository-relative labels, including
        # CayleyKernel/__init__.py for the separately installed engine.
        root = KERNEL_ROOT if path.is_relative_to(KERNEL_ROOT / "CayleyKernel") else VALIDATION_ROOT
        hashes[path.relative_to(root).as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()
    return {
        "git_head": _git_head(VALIDATION_ROOT),
        "kernel_git_head": _git_head(KERNEL_ROOT),
        "source_sha256": hashes,
    }
