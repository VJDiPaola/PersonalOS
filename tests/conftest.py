"""Shared pytest configuration and fixtures."""


def pytest_addoption(parser):
    parser.addoption(
        "--update-goldens",
        action="store_true",
        default=False,
        help="Update golden files instead of comparing against them.",
    )
