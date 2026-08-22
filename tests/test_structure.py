from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_layers():
    layers = [
        "AGENTS",
        "TOOLS",
        "SKILLS",
        "orchestration",
        "memory",
        "state",
        "schemas",
        "prompts",
        "config",
        "safety",
        "observability",
        "evals",
        "benchmarks",
        "examples",
        "docs",
    ]
    for layer in layers:
        assert (ROOT / layer).exists(), layer


def test_counts():
    assert len(list((ROOT / "AGENTS").glob("*_agent.py"))) >= 6
    assert len(list((ROOT / "TOOLS").glob("*.py"))) >= 5
    assert len(list((ROOT / "SKILLS").glob("*.py"))) >= 5
