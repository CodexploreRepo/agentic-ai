"""Routing: send each input to the handler that suits it.

The cheapest useful pattern in this repo, and the most under-used. Most
real workloads are a mixture: nine easy cases and one hard one. Sending all ten
to your best model is slow and expensive; sending all ten to your cheapest is
wrong one time in ten. A classifier in front costs one fast call and fixes both.

Routing is also the honest answer to a lot of requests for "an agent". If the
task is really "work out which of five things the user wants, then do that
thing", a router plus five straight-line handlers will beat an autonomous loop
on cost, latency and debuggability.

Built in Module 05.

Planned interface::

    route(user_input: str, routes: dict[str, Route], ...) -> RouteDecision
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import NoReturn


@dataclass(frozen=True, slots=True)
class Route:
    """One destination a router can choose."""

    name: str
    #: Shown to the classifier. Write it as the condition under which this
    #: route is correct, not as a description of the handler.
    when: str
    handler: Callable[[str], str]


@dataclass(frozen=True, slots=True)
class RouteDecision:
    """Which route was chosen, and how confident the classifier was."""

    route: str
    confidence: float = 0.0
    reasoning: str = ""


def route(*args: object, **kwargs: object) -> NoReturn:
    """Not implemented yet -- built in Module 05.

    Raises:
        NotImplementedError: Always. See docs/patterns/routing.md.
    """
    raise NotImplementedError("route() is built in Module 05. See docs/patterns/routing.md.")
