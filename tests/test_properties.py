from hypothesis import given, strategies as st
import app as seance_app


@given(st.text(alphabet=" \t\n\r", min_size=0, max_size=50))
def test_whitespace_input_always_rejected(blank_text):
    valid, msg = seance_app.validate_code_payload(blank_text, "Python")
    assert valid is False
    assert len(msg) > 0


@given(
    st.characters(blacklist_categories=("Cs",)).filter(lambda c: c.strip() != ""),
    st.integers(min_value=1, max_value=500),
)
def test_oversized_payload_always_rejected(char, extra_len):
    huge_text = char * (seance_app.MAX_CODE_LENGTH + extra_len)
    valid, _ = seance_app.validate_code_payload(huge_text, "Python")
    assert valid is False


@given(
    st.text(min_size=1, max_size=300).filter(lambda s: s.strip() != ""),
    st.sampled_from(["Python", "JavaScript", "SQL", "PHP"]),
)
def test_fallback_exorcist_preserves_schema_invariants(code_snippet, lang):
    result = seance_app.fallback_static_exorcist(code_snippet, lang)
    assert isinstance(result["curse_name"], str) and len(result["curse_name"]) > 0
    assert result["severity"] in {"Minor Poltergeist", "Vengeful Wraith", "Eldritch Horror"}
    assert isinstance(result["astral_nodes"], list) and len(result["astral_nodes"]) >= 1
    assert isinstance(result["purified_code"], str) and len(result["purified_code"]) > 0