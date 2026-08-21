# Agentic Pathology Review

F57 standalone multi-agent pathology workflow support system.

## Agents

- [`specimen_workflow_agent.py`](AGENTS/specimen_workflow_agent.py)
- [`metadata_validator_agent.py`](AGENTS/metadata_validator_agent.py)
- [`case_completeness_agent.py`](AGENTS/case_completeness_agent.py)
- [`quality_agent.py`](AGENTS/quality_agent.py)
- [`escalation_agent.py`](AGENTS/escalation_agent.py)
- [`human_reviewer_agent.py`](AGENTS/human_reviewer_agent.py)

## Tools

- [`specimen_tracker.py`](TOOLS/specimen_tracker.py)
- [`metadata_checker.py`](TOOLS/metadata_checker.py)
- [`case_completeness_checker.py`](TOOLS/case_completeness_checker.py)
- [`quality_checklist.py`](TOOLS/quality_checklist.py)
- [`escalation_router.py`](TOOLS/escalation_router.py)

## Skills

- [`specimen_workflow.py`](SKILLS/specimen_workflow.py)
- [`metadata_validation.py`](SKILLS/metadata_validation.py)
- [`case_completeness.py`](SKILLS/case_completeness.py)
- [`quality_review.py`](SKILLS/quality_review.py)
- [`escalation_review.py`](SKILLS/escalation_review.py)

Supporting layers include orchestration, memory, state, schemas, prompts, config, safety, observability, evals, benchmarks, examples, tests, docs, and CI.

This system is non-diagnostic and requires qualified human review.
