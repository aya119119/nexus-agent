import pytest

from tools.calculator import CalculatorTool


@pytest.mark.parametrize(
    "expression, expected",
    [
        ("2 + 3", 5),
        ("10 / 2", 5),
        ("(2 + 3) * 4", 20),
        ("2 ** 3", 8),
    ],
)
def test_valid_expressions_return_correct_results(expression, expected):
    assert CalculatorTool().run(expression=expression) == expected


def test_rejects_injection_attempts():
    result = CalculatorTool().run(expression="__import__('os').system('ls')")
    assert "invalid" in result.lower() or "not allowed" in result.lower() or "unsafe" in result.lower()
