"""Safe calculator tool for basic arithmetic.

This intentionally supports only a small, explicit subset of arithmetic so input
from the model remains safe and predictable. It does not use raw eval().
"""
import ast

from tools.base import Tool


_ALLOWED_BIN_OPS = {
    ast.Add: lambda a, b: a + b,
    ast.Sub: lambda a, b: a - b,
    ast.Mult: lambda a, b: a * b,
    ast.Div: lambda a, b: a / b,
    ast.Pow: lambda a, b: a ** b,
}

_ALLOWED_UNARY_OPS = {
    ast.UAdd: lambda a: +a,
    ast.USub: lambda a: -a,
}


class CalculatorTool(Tool):
    name = "calculator"
    description = "Evaluate safe arithmetic expressions with +, -, *, /, ** and parentheses."
    input_schema = {
        "type": "object",
        "properties": {
            "expression": {"type": "string", "description": "A numeric expression to evaluate."}
        },
        "required": ["expression"],
    }

    def _eval_node(self, node):
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return node.value
        if isinstance(node, ast.BinOp):
            left = self._eval_node(node.left)
            right = self._eval_node(node.right)
            op = type(node.op)
            if op not in _ALLOWED_BIN_OPS:
                raise ValueError(f"Unsupported operation: {ast.dump(node.op)}")
            return _ALLOWED_BIN_OPS[op](left, right)
        if isinstance(node, ast.UnaryOp):
            operand = self._eval_node(node.operand)
            op = type(node.op)
            if op not in _ALLOWED_UNARY_OPS:
                raise ValueError(f"Unsupported unary operation: {ast.dump(node.op)}")
            return _ALLOWED_UNARY_OPS[op](operand)
        if isinstance(node, ast.Expression):
            return self._eval_node(node.body)
        raise ValueError(f"Unsupported expression node: {type(node).__name__}")

    def run(self, **kwargs) -> str:
        expression = kwargs.get("expression")
        if not expression or not isinstance(expression, str):
            return "Calculator error: expression must be a non-empty string."

        try:
            parsed = ast.parse(expression, mode="eval")
            result = self._eval_node(parsed)
        except Exception as exc:
            return f"Calculator error: invalid or unsafe expression: {exc}"

        if isinstance(result, float) and result.is_integer():
            result = int(result)

        return str(result)
