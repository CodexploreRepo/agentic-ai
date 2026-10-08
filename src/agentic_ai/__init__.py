"""A reference library for building agentic AI systems.

The public surface is deliberately small. Most code needs four things::

    from agentic_ai import Message, get_client, tool
    from agentic_ai.patterns import run_agent

Everything else lives in a subpackage named after what it does: ``patterns``,
``tools``, ``evals``, ``obs``, ``llm``.
"""

from __future__ import annotations

from agentic_ai.errors import (
    AgenticError,
    BudgetExceeded,
    ConfigError,
    MaxStepsExceeded,
    ProviderError,
    ToolExecutionError,
)
from agentic_ai.llm.base import (
    ChatResponse,
    LLMClient,
    Message,
    ToolCall,
    ToolSpec,
    Usage,
)
from agentic_ai.llm.registry import get_client
from agentic_ai.settings import get_settings

__version__ = "0.1.0"

__all__ = [
    "AgenticError",
    "BudgetExceeded",
    "ChatResponse",
    "ConfigError",
    "LLMClient",
    "MaxStepsExceeded",
    "Message",
    "ProviderError",
    "ToolCall",
    "ToolExecutionError",
    "ToolSpec",
    "Usage",
    "__version__",
    "get_client",
    "get_settings",
]
