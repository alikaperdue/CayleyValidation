"""Make the engine's source-only scripts available to the validation suites."""

import sys
from pathlib import Path

import CayleyKernel

KERNEL_ROOT = Path(CayleyKernel.__file__).resolve().parents[1]

# Editable installs can expose the engine package without its sibling scripts/.
if (KERNEL_ROOT / "scripts").is_dir() and str(KERNEL_ROOT) not in sys.path:
    sys.path.append(str(KERNEL_ROOT))
