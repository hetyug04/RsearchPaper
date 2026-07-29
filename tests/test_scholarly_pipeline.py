import datetime as dt
import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


pipeline = load("scholarly_pipeline", ROOT / "scripts/scholarly_pipeline.py")
conference = load("conference_identity", ROOT / "scripts/conference_identity.py")


def test_parse_crossref_date_parts():
    assert pipeline.parse_date({"date-parts": [[2025, 5, 21]]}) == dt.date(2025, 5, 21)
    assert pipeline.parse_date([[2025, 5]]) == dt.date(2025, 5, 1)


def test_saved_crossref_fixture_separates_public_and_deposit_dates():
    fixture = json.loads(
        (ROOT / "tests/fixtures/crossref_record.json").read_text(encoding="utf-8")
    )
    assert pipeline.date_text(fixture["published-online"]) == "2025-05-21"
    assert pipeline.date_text(fixture["published-print"]) == "2025-07"
    assert pipeline.date_text(fixture["deposited"]) == "2026-01-04"
    assert pipeline.parse_date(fixture["published-online"]) < pipeline.parse_date(
        fixture["deposited"]
    )


def test_normalize_doi():
    assert pipeline.normalize_doi("https://doi.org/10.1234/ABC. ") == "10.1234/abc"


def test_title_scope_flags_prediction():
    assert pipeline.title_scope_flag("A machine learning prediction model cohort study").startswith(
        "exclude_title:"
    )
    assert pipeline.title_scope_flag("Diabetes and cardiovascular events: a cohort study") == (
        "requires_full_text_screen"
    )


def test_conference_auto_same_requires_both_axes_and_full_text():
    evidence = conference.ConferenceEvidence(
        identifier_match=3,
        source_window_match=2,
        sample_match=1,
        author_linkage=1,
        population_match=1,
        exposure_match=2,
        outcome_match=2,
        estimand_match=2,
        effect_match=1,
        adjustment_match=1,
        full_abstract_available=True,
    )
    assert conference.adjudicate(evidence) == "auto_same_study_material_analysis"


def test_conference_missing_full_abstract_is_human_review():
    evidence = conference.ConferenceEvidence(
        identifier_match=3,
        source_window_match=2,
        sample_match=1,
        exposure_match=2,
        outcome_match=2,
        estimand_match=2,
    )
    assert conference.adjudicate(evidence) == "human_review_required"


def test_conference_decisive_conflict_never_auto_excludes():
    evidence = conference.ConferenceEvidence(
        identifier_match=3,
        source_window_match=2,
        sample_match=1,
        author_linkage=1,
        population_match=1,
        exposure_match=2,
        outcome_match=2,
        estimand_match=2,
        effect_match=1,
        adjustment_match=1,
        full_abstract_available=True,
        decisive_conflict=True,
    )
    assert conference.adjudicate(evidence) == "human_review_required"
