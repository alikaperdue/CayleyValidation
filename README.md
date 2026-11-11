# CayleyValidation

Reproduce selected calculations from the Cayley–Dickson literature using
[CayleyKernel](https://github.com/alikaperdue/CayleyKernel). The
[paper index](docs/papers/README.md) lists the papers, the claims each suite
checks, and the evidence saved from earlier runs.

## Quickstart

Clone both repositories side by side. Use an editable kernel checkout because
some companions use research scripts from the kernel source tree.

```bash
git clone https://github.com/alikaperdue/CayleyKernel.git
git clone https://github.com/alikaperdue/CayleyValidation.git
cd CayleyValidation
git -C ../CayleyKernel checkout --detach 12850af9feab89b5fb9993feeae2d8f8b0e3c0e5

python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e ../CayleyKernel -e '.[test,research-test]'
python -m pytest -q -m 'cpu and not slow' tests/
```

You can substitute the absolute path to a different kernel checkout in the
install command. The [CPU workflow](.github/workflows/cpu.yml) uses the same
pinned kernel revision as this example.

## Run one paper, slow cases, or GPU cases

Run these commands from CayleyValidation:

```bash
python -m pytest -v -m 'cpu and not slow' tests/papers/arxiv_2608_28176/
python -m pytest -q -m 'cpu and slow' tests/papers/
```

For GPU checks, install the CuPy extra for your CUDA version and build the
kernel in the CayleyKernel checkout. For example, with CUDA 12:

```bash
python -m pip install -e '../CayleyKernel[cuda12]'
make -C ../CayleyKernel kernel
python -m pytest -q -m 'not cpu and not slow' tests/papers/
```

The GPU checks may skip when CuPy, a CUDA device, or the compiled library is
unavailable. Inspect skip reasons with `-rs`. Standalone report runners use
their own test selection. See each paper's reproduction instructions and run
`python -m tests.papers.<companion>.run --help` for the runner options.

The paper guides also include commands starting with `python -m scripts`.
Run those from the CayleyKernel checkout with the same virtual environment
active, or set `PYTHONPATH` to the absolute path of that checkout.

## Evidence and provenance

The companions and historical evidence were migrated from CayleyKernel.
Published results record the original run and should remain byte-for-byte
stable. Write new reports to a fresh path under `validation-output/`.
Report runners record the validation and kernel Git revisions and source
hashes. When using a kernel outside a Git checkout, the kernel revision is
unavailable. Tests run without the original PDFs. Some report runners can
hash a local copy using `--paper`.

The repository is distributed under the [Apache License 2.0](LICENSE).
