#!/usr/bin/env python3
"""Score whether an earlier conference abstract is the same study/analysis.

The rule has two independent 0–8 axes. It never decides from a title or search
snippet alone; absent full abstract evidence is routed to human review.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ConferenceEvidence:
    identifier_match: int = 0       # 0 or 3
    source_window_match: int = 0    # 0..2
    sample_match: int = 0           # 0 or 1
    author_linkage: int = 0         # 0 or 1
    population_match: int = 0       # 0 or 1
    exposure_match: int = 0         # 0..2
    outcome_match: int = 0          # 0..2
    estimand_match: int = 0         # 0..2
    effect_match: int = 0           # 0 or 1
    adjustment_match: int = 0       # 0 or 1
    full_abstract_available: bool = False
    decisive_conflict: bool = False
    unexplained_sample_change: bool = False

    @property
    def identity_score(self) -> int:
        return sum(
            (
                self.identifier_match,
                self.source_window_match,
                self.sample_match,
                self.author_linkage,
                self.population_match,
            )
        )

    @property
    def analysis_score(self) -> int:
        return sum(
            (
                self.exposure_match,
                self.outcome_match,
                self.estimand_match,
                self.effect_match,
                self.adjustment_match,
            )
        )


def adjudicate(evidence: ConferenceEvidence) -> str:
    """Return auto_same, auto_not_same, or human_review_required."""
    if not evidence.full_abstract_available:
        return "human_review_required"
    if evidence.decisive_conflict or evidence.unexplained_sample_change:
        return "human_review_required"
    mandatory = evidence.exposure_match == 2 and evidence.outcome_match == 2
    if evidence.identity_score >= 6 and evidence.analysis_score >= 6 and mandatory:
        return "auto_same_study_material_analysis"
    if evidence.identity_score <= 3 or evidence.analysis_score <= 3:
        return "auto_not_same_material_analysis"
    return "human_review_required"
