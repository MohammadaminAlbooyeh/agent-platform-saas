"""Unit tests for real agent logic (query/processor/research)."""

import asyncio
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from agents.processor_agent import ProcessorAgent, apply_transform  # noqa: E402
from agents.query_agent import QueryAgent  # noqa: E402
from agents.research_agent import ResearchAgent  # noqa: E402


def test_apply_transform_sum():
    assert apply_transform("sum", [1, 2, 3]) == {"sum": 6.0}


def test_apply_transform_uppercase_keys():
    assert apply_transform("uppercase_keys", {"a": "x"}) == {"a": "X"}


def test_apply_transform_unsupported_raises():
    import pytest

    with pytest.raises(ValueError):
        apply_transform("not-a-real-op", {})


def test_processor_agent_runs_real_transform():
    agent = ProcessorAgent()
    result = asyncio.run(agent.run({"operation": "sum", "data": [1, 2, 3]}, "tenant-1"))
    assert result["transformed"] == {"sum": 6.0}
    assert result["tokens_used"] > 0
    assert result["tool_calls"] == 0


def test_processor_agent_invalid_operation_errors():
    agent = ProcessorAgent()
    result = asyncio.run(agent.run({"operation": "sum", "data": {"not": "a list"}}, "tenant-1"))
    assert "error" in result


def test_query_agent_requires_query():
    agent = QueryAgent()
    result = asyncio.run(agent.run({}, "tenant-1"))
    assert "error" in result


def test_research_agent_requires_topic_or_url():
    agent = ResearchAgent()
    result = asyncio.run(agent.run({}, "tenant-1"))
    assert "error" in result
