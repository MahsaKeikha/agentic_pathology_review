# F57 Agentic Pathology Review

**Maturity:** L3 reference candidate  
**Version:** 1.0.0

A six-agent reference architecture for governed pathology workflow support across specimen tracking, metadata validation, case completeness, quality review, escalation, and qualified human review.

F57 focuses on the operational, information-quality, and governance layers surrounding pathology workflows. It is deliberately non-diagnostic. The system can help organize specimens and cases, validate identifiers and metadata, identify missing workflow elements, apply structured quality checks, surface operational concerns, and route cases for human review. It does not interpret slides, diagnose disease, assign tumor grade or stage, determine margins, or replace a pathologist.

## Why pathology workflow requires explicit orchestration

Pathology depends on the integrity of the full specimen-to-report chain. Errors can arise from accession mismatches, incomplete requisitions, specimen-label discrepancies, missing blocks or slides, incomplete case material, unavailable ancillary studies, quality-control problems, workflow delays, or unresolved communication requirements.

F57 separates these concerns into specialist responsibilities:

```text
specimen / pathology case
          |
          v
 Specimen Workflow Agent
          |
          v
 Metadata Validator Agent
          |
          v
 Case Completeness Agent
          |
          v
      Quality Agent
          |
          v
    Escalation Agent
          |
          v
 Qualified Human Reviewer
```

This separation makes it clear whether a case is blocked because of identity, completeness, quality, or escalation concerns rather than collapsing all issues into one narrative output.

## Six-agent architecture

| Agent | Responsibility | Core question |
|---|---|---|
| Specimen Workflow Agent | Tracks specimen and case workflow state | Is the specimen accounted for through the expected operational stages? |
| Metadata Validator Agent | Checks identifiers and case metadata | Are patient, accession, specimen, site, and procedure references complete and internally consistent? |
| Case Completeness Agent | Reviews expected materials and workflow elements | Does the case contain the required operational materials for qualified review? |
| Quality Agent | Applies structured quality-control checks | Are there quality issues that should block or qualify workflow progression? |
| Escalation Agent | Routes unresolved or safety-relevant workflow concerns | Does this case require higher-priority human attention or manual resolution? |
| Human Reviewer Agent | Represents the qualified human authority boundary | Has an authorized pathology professional reviewed the case where required? |

## Repository structure

```text
AGENTS/
├── specimen_workflow_agent.py
├── metadata_validator_agent.py
├── case_completeness_agent.py
├── quality_agent.py
├── escalation_agent.py
└── human_reviewer_agent.py

SKILLS/
├── specimen_workflow.py
├── metadata_validation.py
├── case_completeness.py
├── quality_review.py
└── escalation_review.py

TOOLS/
├── specimen_tracker.py
├── metadata_checker.py
├── case_completeness_checker.py
├── quality_checklist.py
└── escalation_router.py

benchmarks/
├── benchmark.py
└── RESULTS.md

evals/
├── evaluator.py
└── heldout_suite.py

orchestration/
memory/
observability/
schemas/
prompts/
config/
safety/
examples/
tests/
docs/
.github/workflows/ci.yml
run.py
pyproject.toml
README.md
```

## Specimen workflow

The Specimen Workflow Agent supports the operational path from specimen receipt through case readiness.

A specimen record can include:

```text
case_id
accession_number
patient_reference
specimen_id
specimen_type
anatomic_site
collection_time
received_time
container_count
block_count
slide_count
workflow_status
location
processing_state
```

`TOOLS/specimen_tracker.py` provides the reference abstraction for specimen and case tracking.

Production pathology systems may contain more detailed state for grossing, processing, embedding, sectioning, staining, scanning, ancillary testing, review, sign-out, and archival workflows.

## Chain of custody and specimen identity

Specimen identity is a core safety requirement.

The system should preserve explicit links between:

```text
patient
  |
  v
procedure / encounter
  |
  v
accession
  |
  v
specimen container
  |
  v
cassette / block
  |
  v
slide / image
  |
  v
pathology case
```

Production implementations should rely on authoritative laboratory systems and validated identifiers rather than inferred identity.

F57 must not:

- guess a patient identity
- merge specimens because names appear similar
- silently reconcile conflicting accession numbers
- assume unlabeled or ambiguously labeled material belongs to a case
- create a missing chain-of-custody link without evidence

Potential states include:

```text
SPECIMEN IDENTITY UNRESOLVED
ACCESSION MISMATCH
CONTAINER COUNT MISMATCH
BLOCK / SLIDE LINKAGE INCOMPLETE
MANUAL REVIEW REQUIRED
```

## Metadata validation

The Metadata Validator Agent checks whether required case information is present and internally consistent.

Relevant metadata can include:

- patient reference
- accession number
- ordering or submitting service
- collection date/time
- receipt date/time
- procedure type
- specimen source
- anatomic site
- laterality where applicable
- fixation information where applicable
- container designation
- clinical history field
- requested studies
- case priority or service type

`TOOLS/metadata_checker.py` provides deterministic support for completeness and consistency checks.

Metadata validation is not diagnostic interpretation. It confirms that the workflow package is coherent enough to progress.

## Case completeness

The Case Completeness Agent determines whether expected operational material is available.

Depending on workflow and local policy, completeness can include:

- requisition or order present
- expected specimen containers accounted for
- required blocks present
- required slides present
- recuts or deeper levels completed when ordered
- ancillary tests available when required for workflow completion
- external material received when expected
- consultation material documented
- digital images available where relevant
- required clinical information present
- pending work clearly identified

`TOOLS/case_completeness_checker.py` provides the deterministic reference layer.

A case can be operationally complete without any statement about whether the eventual diagnosis is correct.

## Quality review

The Quality Agent applies structured checks to workflow and material quality.

`TOOLS/quality_checklist.py` provides the reference checklist abstraction.

Possible quality dimensions include:

- specimen labeling consistency
- container integrity
- processing completeness
- slide or image availability
- stain quality status
- digital scan completeness
- ancillary-test status
- document completeness
- source-system consistency
- outstanding corrective action

The exact quality criteria depend on the laboratory, specimen type, accreditation context, technology, and local SOPs.

The system should never invent a passing quality result when no quality assessment occurred.

## Digital pathology boundary

F57 can be extended to integrate with whole-slide image and digital pathology systems, but the base repository remains non-diagnostic.

It may support:

- confirming that a scan exists
- checking that expected image files are available
- validating metadata associated with a digital slide
- identifying missing or failed scans
- routing incomplete digital cases

It must not autonomously:

- interpret morphology
- identify malignancy
- assign histologic type
- assign grade
- determine margins
- quantify biomarkers for clinical use
- issue a final diagnostic report

Any diagnostic image-analysis capability would require a separately defined intended use, validation strategy, regulatory analysis, and clinical governance.

## Ancillary studies

Pathology cases can depend on additional studies such as immunohistochemistry, special stains, molecular tests, cytogenetics, flow cytometry, or external consultation.

F57 can track whether an expected ancillary result is:

- ordered
- pending
- completed
- unavailable
- failed
- received from an external source
- requiring manual reconciliation

The system should not infer the meaning of an ancillary result or use it to generate a diagnosis.

## Escalation

The Escalation Agent surfaces workflow conditions requiring timely human attention.

Examples can include:

- unresolved specimen identity
- accession conflict
- missing expected specimen or slide
- incomplete chain of custody
- failed or unavailable required ancillary material
- significant workflow delay
- source-system outage
- unresolved quality concern
- required manual reconciliation
- pending case exceeding configured operational thresholds

`TOOLS/escalation_router.py` provides the reference routing abstraction.

Escalation should use approved laboratory and hospital channels. F57 does not determine clinical urgency from microscopic findings.

## Human review boundary

The Human Reviewer Agent represents the qualified professional authority layer.

F57 must not autonomously:

- diagnose cancer or any other disease
- interpret microscopic morphology
- determine benign versus malignant status
- assign histologic grade
- assign pathologic stage
- determine margin status
- interpret immunohistochemistry
- interpret molecular or cytogenetic findings
- determine treatment implications
- sign a pathology report
- communicate a diagnostic critical result as if it were a pathologist

Qualified pathology professionals remain responsible for interpretation, diagnosis, final reporting, and clinically consequential communication.

## Workflow state and provenance

The orchestration and `memory/` layers preserve structured state across agents.

Useful state includes:

```text
case_id
accession_number
specimen_tracking_state
metadata_validation_state
case_completeness_state
quality_state
pending_material
escalation_state
human_review_state
unresolved_questions
```

Production systems should preserve provenance for every field, including source system, timestamp, version, and operator or interface where applicable.

## LIS and laboratory integration

F57 is platform-neutral but can be adapted to systems such as:

- laboratory information systems (LIS)
- anatomic pathology systems
- EHR/EMR systems
- specimen tracking systems
- slide printers and scanners
- digital pathology platforms
- molecular laboratory systems
- document management systems
- quality management systems
- external consultation and image-exchange systems

Production adapters should preserve identifiers, timestamps, access controls, audit logs, and authoritative source hierarchy.

## Privacy and security

Pathology data can contain protected health information, genomic information, images, and highly sensitive diagnostic records.

Production deployments should apply:

- authenticated identity
- least privilege
- role-based or attribute-based access
- minimum-necessary data access
- encryption in transit
- encryption at rest where required
- audit logging
- secure export controls
- retention policies
- secure disposal
- appropriate handling of genomic or molecular data

Reference testing should use synthetic or appropriately governed datasets.

## Downtime and degraded operation

Pathology laboratories require explicit workflows for source-system outages or incomplete data.

Examples include:

- LIS unavailable
- scanner unavailable
- digital slide unavailable
- ancillary system unavailable
- network outage
- interface delay
- stale tracking state

F57 should surface uncertainty instead of treating cached information as authoritative.

Useful states include:

```text
SOURCE UNAVAILABLE
DATA STALE
SPECIMEN STATE UNKNOWN
ANCILLARY STATUS UNKNOWN
MANUAL WORKFLOW REQUIRED
```

Local downtime SOPs remain authoritative.

## Fail-closed workflow gates

A pathology case should not be represented as operationally ready when critical evidence is unresolved.

Potential blockers include:

- unresolved specimen identity
- accession mismatch
- missing required metadata
- incomplete specimen chain
- missing expected material
- incomplete case package
- unresolved quality failure
- stale source data
- required ancillary status unknown
- unresolved escalation
- required human review incomplete

Human review should not silently erase data-integrity or chain-of-custody problems. The underlying issue should be resolved or handled explicitly according to laboratory policy.

## End-to-end reference workflow

A typical F57 run follows this sequence:

1. Receive an authorized pathology case.
2. Confirm accession, patient reference, and specimen identifiers.
3. Track specimen and material state.
4. Validate case metadata.
5. Check whether expected materials and ancillary items are present.
6. Apply structured quality checks.
7. Surface unresolved discrepancies or delays.
8. Route escalation when required.
9. Preserve workflow evidence and provenance.
10. Require qualified human review for diagnostic interpretation and final sign-out.

## Observability

The `observability/` layer supports traceable workflow operations.

Useful operational metrics include:

- specimen receipt-to-processing time
- processing-to-slide time
- case age
- metadata failure count
- accession mismatch count
- missing-material count
- ancillary turnaround time
- incomplete-case count
- quality-failure count
- escalation count
- escalation acknowledgement time
- source-system outage events
- human-review state

These metrics can support laboratory operations and quality improvement but should not substitute for formal clinical quality programs or accreditation requirements.

## Benchmarks and evaluation

The repository includes:

```text
benchmarks/benchmark.py
benchmarks/RESULTS.md
evals/evaluator.py
evals/heldout_suite.py
```

Evaluation should focus on workflow integrity and safety rather than diagnostic accuracy.

Useful dimensions include:

- identity-conflict detection
- accession-mismatch detection
- missing-metadata detection
- specimen-tracking completeness
- missing-material detection
- case-completeness detection
- quality-failure detection
- ancillary-status handling
- stale-data handling
- source-outage behavior
- escalation routing
- unresolved-state propagation
- human-review enforcement

Strong held-out cases should intentionally contain conflicting specimen identifiers, missing blocks or slides, stale states, incomplete requisitions, ancillary delays, and unresolved quality issues.

## Reproduce the reference implementation

Install development dependencies:

```bash
python -m pip install -e '.[dev]'
```

Run checks and tests:

```bash
ruff check .
pytest -q
```

Run held-out evaluation:

```bash
python evals/heldout_suite.py
```

Run the example:

```bash
python examples/example_run.py
```

Run the main entry point:

```bash
python run.py
```

The repository includes CI under `.github/workflows/ci.yml`.

## CI and reproducibility

Production-oriented pathology workflow testing should additionally cover:

- specimen identifier fixtures
- accession conflicts
- duplicate labels
- missing containers
- missing blocks or slides
- ancillary-test delays
- digital-slide failures
- LIS adapter contracts
- interface outages
- stale-state handling
- access-control tests
- audit-log integrity

Version schemas, workflow policies, adapters, prompts, quality checklists, fixtures, and benchmark cases so behavior can be reproduced after changes.

## L3 reference candidate

F57 follows the library's L3-oriented structure through specialist agents, deterministic tools, orchestration, observability, held-out evaluation, CI, explicit safety boundaries, and human authority.

This maturity designation describes the engineering structure of the reference repository. It is not diagnostic validation, laboratory accreditation, FDA clearance or approval, CLIA certification, CAP accreditation, clinical validation, or authorization for autonomous pathology interpretation.

## Failure states

Useful explicit states include:

```text
SPECIMEN IDENTITY UNRESOLVED
ACCESSION MISMATCH
METADATA INCOMPLETE
SPECIMEN CHAIN INCOMPLETE
CASE MATERIAL MISSING
ANCILLARY STATUS UNKNOWN
QUALITY REVIEW FAILED
SOURCE DATA STALE
AUTHORITATIVE SYSTEM UNAVAILABLE
ESCALATION REQUIRED
HUMAN REVIEW REQUIRED
```

The system should never fabricate specimen identity, chain-of-custody evidence, ancillary results, slide availability, quality results, diagnostic findings, or human approval.

## Extending F57

Common extensions include:

- LIS integration
- barcode and specimen tracking
- cassette and slide printer integration
- digital pathology systems
- whole-slide image repositories
- molecular laboratory integration
- external consultation workflows
- laboratory quality systems
- turnaround-time dashboards
- case-routing dashboards
- document management
- archival and retention workflows

Extensions that add diagnostic image analysis or clinical interpretation should be treated as a separate intended-use system with appropriate validation, governance, and regulatory review.

## Example use cases

F57 can serve as a reference for:

- pathology specimen tracking
- accession quality checks
- case-completeness review
- ancillary-study workflow tracking
- laboratory quality operations
- escalation workflows
- LIS integration research
- digital pathology operations
- teaching multi-agent healthcare architecture

## Design principles

1. Treat specimen identity and chain of custody as foundational safety controls.
2. Never infer missing accession or patient identity.
3. Separate operational completeness from diagnostic interpretation.
4. Make ancillary-study status explicit.
5. Use deterministic tools for deterministic workflow checks.
6. Surface stale or unavailable source systems.
7. Escalate unresolved quality and identity issues through approved channels.
8. Preserve privacy, provenance, and auditability.
9. Fail closed when required case evidence is incomplete.
10. Keep diagnostic authority and final sign-out with qualified pathology professionals.

## Documentation

Additional architecture documentation is available under `docs/`, including `docs/ARCHITECTURE.md`.

## Citation and reuse

Use the repository metadata and citation information provided by the project when referencing this implementation. The code and documentation can be studied and adapted subject to the repository license.

## Responsible use

Use F57 as a pathology workflow and multi-agent architecture reference. Validate identifiers, specimen tracking, quality checks, source-system integrations, privacy controls, escalation procedures, and human-review boundaries against the actual laboratory environment before deployment. Final pathology interpretation, diagnosis, sign-out, and patient-care decisions remain with appropriately qualified healthcare professionals.