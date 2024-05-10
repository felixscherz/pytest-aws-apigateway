import pytest


def test_plugin(pytester: pytest.Pytester):
    pytester.copy_example("test_handler.py")
    result = pytester.runpytest("-k", "test_handler")
    assert result.ret == 0
    ...
