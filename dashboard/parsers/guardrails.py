"""Pure guardrail validators (no DB / LLM).

Used by server.nudge_agent() to decide if an agent response is acceptable.
"""
from .commands import has_system_command, has_mention

PREP_PATTERNS = [
    '파악하겠', '확인하겠', '상황을 파악', '상황부터', '먼저 현재',
    'check', 'assess', 'analyze first', 'let me',
    '검토하겠', '분석하겠', '살펴보겠', '조사하겠', '정리하겠',
    '계획을 세우', '방안을 마련',
]


def is_prep_only(text, max_len=150):
    """True if response looks like preparation talk (no real work)."""
    if not text:
        return True
    if len(text) >= max_len:
        return False
    low = text.lower()
    return any(p in low for p in PREP_PATTERNS)


def has_required_action(text):
    """A valid response must contain a system command OR @mention."""
    return has_system_command(text) or has_mention(text)


def needs_retry(text, max_len=150):
    """Combined check: rejects responses that are pure prep talk and have no action."""
    if has_required_action(text):
        return False
    return is_prep_only(text, max_len=max_len)
