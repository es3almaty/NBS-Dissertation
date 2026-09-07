from __future__ import annotations

from dataclasses import dataclass, field, asdict
from enum import Enum
from pathlib import Path
from typing import Any


class ComponentStatus(str, Enum):
    PRESENT_COMPLIANT = "PRESENT_COMPLIANT"
    PRESENT_NONCOMPLIANT = "PRESENT_NONCOMPLIANT"
    MISSING = "MISSING"


class SubmissionStatus(str, Enum):
    READY = "READY"
    CONDITIONAL = "CONDITIONAL"
    RESUBMIT = "RESUBMIT"


class CitationSystem(str, Enum):
    APA_AUTHOR_DATE = "APA_AUTHOR_DATE"
    NUMERIC = "NUMERIC"
    FOOTNOTE = "FOOTNOTE"
    MIXED = "MIXED"
    NO_DETECTABLE_SYSTEM = "NO_DETECTABLE_SYSTEM"


class TableRisk(str, Enum):
    SIMPLE_SAFE = "SIMPLE_SAFE"
    COMPLEX_SAFE_TO_PRESERVE = "COMPLEX_SAFE_TO_PRESERVE"
    BROKEN_REQUIRES_REVIEW = "BROKEN_REQUIRES_REVIEW"


class Severity(str, Enum):
    CRITICAL = "CRITICAL"
    MAJOR = "MAJOR"
    MINOR = "MINOR"
    ADVISORY = "ADVISORY"


class Action(str, Enum):
    AUTO_FIX = "AUTO_FIX"
    FLAG = "FLAG"
    BLOCK_FORMATTING = "BLOCK_FORMATTING"
    MANUAL_REVIEW = "MANUAL_REVIEW"


@dataclass
class ComponentResult:
    name: str
    status: ComponentStatus
    critical: bool = True
    applicable: bool = True
    evidence: list[str] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)


@dataclass
class Finding:
    code: str
    title: str
    message: str
    severity: Severity
    action: Action = Action.FLAG
    location: str | None = None
    evidence: dict[str, Any] = field(default_factory=dict)


@dataclass
class TableAssessment:
    index: int
    caption: str | None
    number: int | None
    risk: TableRisk
    reasons: list[str] = field(default_factory=list)
    rows: int = 0
    cols: int = 0


@dataclass
class PreflightResult:
    paragraphs: int = 0
    tables: int = 0
    images: int = 0
    hyperlinks: int = 0
    sections: int = 0
    headers: int = 0
    footers: int = 0
    page_fields: int = 0
    duplicate_page_fields: bool = False
    footnotes_present: bool = False
    endnotes_present: bool = False
    equations_present: bool = False
    fields_present: bool = False
    automatic_numbering_paragraphs: list[int] = field(default_factory=list)
    heading_paragraphs: list[dict[str, Any]] = field(default_factory=list)
    section_breaks: int = 0
    package_parts: list[str] = field(default_factory=list)


@dataclass
class ReferenceAssessment:
    system: CitationSystem
    references_present: bool
    numeric_citations: list[int] = field(default_factory=list)
    author_date_citations: list[str] = field(default_factory=list)
    unmatched_citations: list[str] = field(default_factory=list)
    uncited_reference_entries: list[str] = field(default_factory=list)
    duplicate_entries: list[str] = field(default_factory=list)


@dataclass
class AuditResult:
    input_path: str
    language: str
    status: SubmissionStatus
    missing_critical_count: int
    components: dict[str, ComponentResult]
    preflight: PreflightResult
    references: ReferenceAssessment
    tables: list[TableAssessment] = field(default_factory=list)
    findings: list[Finding] = field(default_factory=list)
    auto_fixes: list[str] = field(default_factory=list)
    formatted_path: str | None = None
    report_path: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        def cv(v: Any) -> Any:
            if isinstance(v, Enum):
                return v.value
            if isinstance(v, Path):
                return str(v)
            if hasattr(v, "__dataclass_fields__"):
                return {k: cv(val) for k, val in asdict(v).items()}
            if isinstance(v, dict):
                return {k: cv(val) for k, val in v.items()}
            if isinstance(v, list):
                return [cv(x) for x in v]
            return v
        return cv(self)
