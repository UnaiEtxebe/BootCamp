"""Topology graph utilities."""
from __future__ import annotations

from graphviz import Digraph


def export_topology(nodes, edges, path: str) -> None:
    """Export a simple topology diagram using Graphviz."""
    dot = Digraph()
    for node in nodes:
        dot.node(node)
    for start, end in edges:
        dot.edge(start, end)
    dot.render(path, format="png", cleanup=True)
