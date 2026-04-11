"""Unit tests for parsers/guardrails.py."""
from parsers.guardrails import is_prep_only, has_required_action, needs_retry


def test_prep_short_korean():
    assert is_prep_only("확인하겠습니다") is True
    assert is_prep_only("상황을 파악하겠습니다") is True


def test_prep_short_english():
    assert is_prep_only("let me check") is True
    assert is_prep_only("I will analyze first") is True


def test_not_prep_when_long():
    long_text = "확인하겠습니다." + "x" * 200
    assert is_prep_only(long_text, max_len=150) is False


def test_not_prep_when_actionable():
    """Even if text is short, real work words are not prep."""
    assert is_prep_only("API 서버 구축 완료") is False


def test_has_required_action_with_command():
    assert has_required_action("[TASK_ADD:foo:high]") is True


def test_has_required_action_with_mention():
    assert has_required_action("@CEO 보고드립니다") is True


def test_has_required_action_neither():
    assert has_required_action("그냥 인사") is False


def test_needs_retry_pure_prep():
    """Short prep text with no command/mention should be retried."""
    assert needs_retry("확인하겠습니다") is True


def test_needs_retry_prep_but_has_mention():
    """If there's a mention, accept even if short."""
    assert needs_retry("@CEO 확인하겠습니다") is False


def test_needs_retry_prep_but_has_command():
    assert needs_retry("[TASK_ADD:check:high] 확인하겠습니다") is False


def test_needs_retry_long_text_no_action():
    """Long text without commands is borderline; we accept it (not pure prep)."""
    long = "x" * 300
    assert needs_retry(long) is False
