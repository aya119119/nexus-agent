"""Agent package exports.

We avoid importing Agent eagerly here because the DB layer imports the package
configuration module, and importing .core at package import time creates a circular
reference during startup.
"""

__all__ = ["Agent"]


def __getattr__(name):
    if name == "Agent":
        from .core import Agent
        return Agent
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
