# SPDX-License-Identifier: Apache-2.0
"""Shared pytest fixtures for the external paper suites."""

import CayleyKernel
import numpy as np
import pytest

from tests.support.gpu_support import GPUUnavailable, check_compiled_kernel, device_count


def pytest_addoption(parser):
    parser.addoption(
        "--require-gpu",
        action="store_true",
        help="Fail selected GPU tests if their device or compiled kernel is unavailable.",
    )


def _gpu_unavailable(config, reason):
    if config.getoption("--require-gpu"):
        pytest.fail(f"--require-gpu: {reason}", pytrace=False)
    pytest.skip(str(reason))


@pytest.fixture(scope="session")
def gpu_device_count(pytestconfig):
    try:
        return device_count()
    except GPUUnavailable as exc:
        _gpu_unavailable(pytestconfig, exc)


@pytest.fixture(scope="session")
def compiled_kernel():
    """Host-only ABI checks can use the library without a device."""
    try:
        check_compiled_kernel()
    except GPUUnavailable as exc:
        pytest.skip(str(exc))


@pytest.fixture(scope="session")
def gpu_kernel(pytestconfig, gpu_device_count):
    try:
        check_compiled_kernel()
    except GPUUnavailable as exc:
        _gpu_unavailable(pytestconfig, exc)
    return CayleyKernel.cp


@pytest.fixture(autouse=True)
def _prepare_gpu_test(request):
    """Skip GPU-marked tests when prerequisites are missing.

    Mirrors the engine's conftest: a test marked `cpu` runs unconditionally;
    anything else must present a usable device and compiled kernel.
    """
    if request.node.get_closest_marker("cpu"):
        return
    if request.node.get_closest_marker("gpu_device"):
        request.getfixturevalue("gpu_device_count")
    else:
        request.getfixturevalue("gpu_kernel")
    np.random.seed(0)
    if CayleyKernel.cp is not None:
        CayleyKernel.cp.random.seed(0)
