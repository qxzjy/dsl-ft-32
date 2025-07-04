import pytest

# Sample DataFrame as a fixture
@pytest.fixture
def sample_set():
    return {1, 2, 3, -4, -5, 6}