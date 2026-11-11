# CayleyValidation

External test and validation suite for **CayleyKernel**, the high-performance
Cayley–Dickson multiplication engine.  `cayley-validation` is a separate
repository so the engine can ship lean wheels while the historical literature
companions, regression fixtures, and reproduction scripts stay under version
control in a dedicated laboratory.

## Layout

```
CayleyValidation/
  pyproject.toml      # project metadata + editable link to ../CayleyKernel
  README.md
  tests/
    __init__.py
    conftest.py       # pytest fixtures and GPU guards (mirrors the kernel's)
    papers/           # migrated literature validation suites
      arxiv_0704_0112/
      arxiv_0907_2047/
      arxiv_1505_01670/
      arxiv_1912_01351/
      arxiv_2607_23613/
      arxiv_2608_28176/
      arxiv_math_0702075/
      desktop_batch/          # 16-paper batch (2001.11797, 2205.07986, ...)
      journal_617_0702_2024/
      physletb_141078/
      quasilinear_spheres/
      type_replay.py
      test_type_replay.py
    support/              # shared oracles and GPU guards (engine-independent)
      oracles.py
      comparisons.py
      inputs.py
      gpu_support.py
      test_reference_support.py
```

## Sibling checkout assumption

`pyproject.toml` expects the engine repository to live one directory up:

```
workspace/
  CayleyKernel/         # setup.py, pyproject.toml, CayleyKernel/, tests/, cuda/, rust/
  CayleyValidation/     # this repository
```

If your layout differs, override the direct-URL reference by editing the
`dependencies` list, or point `CAYLEY_KERNEL_PATH` at the absolute path
during the editable install step below.

## Developer setup (editable)

The prerequisite dependency is a PEP 508 direct URL so `pip install .`
cannot succeed without the engine.  For a true editable workflow — kernel
source changes reflected in this suite without reinstalling — run:

```bash
# from the CayleyValidation repository root
pip install -e ../CayleyKernel   # editable engine install
pip install -e .[dev]            # editable suite + pytest
```

Then run the migrated literature validation:

```bash
# CPU-only default selection (mirrors the engine's CI selection)
pytest -q -m "cpu and not slow" tests/papers

# one companion, with verbose output
pytest -v tests/papers/arxiv_2608_28176/test_sections.py

# the 16-paper desktop batch
pytest -v tests/papers/desktop_batch
```

GPU companions require `CuPy`, the compiled kernel (`make kernel` in the
engine tree), and a visible CUDA device.  Missing prerequisites produce
skips, not failures, in the paper suites; a numerical mismatch or missing
entry point after the prerequisites succeed is a failure.

## Migration provenance

The suites under `tests/papers/` were migrated from
`CayleyKernel/tests/papers/`.  The shared oracles in `tests/support/` were
copied over so this laboratory does not import from the engine's private
`tests` package.  Saved JSON / CSV / SVG / log snapshots referenced by the
companion READMEs remain the historical evidence for the runs that
produced them — do not recompute or relabel them.
