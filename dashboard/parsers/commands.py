"""Pure regex parsers for agent system commands.

These are extracted from server.process_task_commands() so they can be
unit-tested without DB or LLM dependencies. Each function returns a list
of structured dicts; mutations to DB happen in the caller.
"""
import re

# ─── Pattern constants ───
RE_TASK_ADD = re.compile(r'\[TASK_ADD:([^:]+):([^\]]+)\]')
RE_TASK_DONE = re.compile(r'\[TASK_DONE:([^\]]+)\]')
RE_TASK_START = re.compile(r'\[TASK_START:([^\]]+)\]')
RE_TASK_BLOCK = re.compile(r'\[TASK_BLOCK:([^:]+):([^\]]+)\]')
RE_CRON_ADD = re.compile(r'\[CRON_ADD:([^:]+):(\d+):([^\]]+)\]')
RE_CRON_DEL = re.compile(r'\[CRON_DEL:([^\]]+)\]')
RE_APPROVAL = re.compile(r'\[APPROVAL:([^:\]]+):([^:\]]+)(?::([^\]]*))?\]')
RE_MENTION = re.compile(r'@([A-Za-z\w]+)')
RE_HAS_COMMAND = re.compile(r'\[TASK_|\[APPROVAL:|\[CRON_')

APPROVAL_CATEGORIES = {
    '예산', '구매', '프로젝트', '인사', '정책', '기타',
    'budget', 'purchase', 'project', 'hr', 'policy', 'general',
}


def parse_task_add(text):
    """Returns: list of {'title': str, 'priority': str}"""
    return [{'title': m.group(1).strip(), 'priority': m.group(2).strip()}
            for m in RE_TASK_ADD.finditer(text)]


def parse_task_done(text):
    """Returns: list of titles to mark done"""
    return [m.group(1).strip() for m in RE_TASK_DONE.finditer(text)]


def parse_task_start(text):
    return [m.group(1).strip() for m in RE_TASK_START.finditer(text)]


def parse_task_block(text):
    """Returns: list of {'title': str, 'reason': str}"""
    return [{'title': m.group(1).strip(), 'reason': m.group(2).strip()}
            for m in RE_TASK_BLOCK.finditer(text)]


def parse_cron_add(text):
    """Returns: list of {'title': str, 'interval': int, 'prompt': str}"""
    return [{'title': m.group(1).strip(),
             'interval': int(m.group(2)),
             'prompt': m.group(3).strip()}
            for m in RE_CRON_ADD.finditer(text)]


def parse_cron_del(text):
    return [m.group(1).strip() for m in RE_CRON_DEL.finditer(text)]


def parse_approval(text):
    """Returns: list of {'category': str, 'title': str, 'detail': str}.

    Supports both [APPROVAL:cat:title:detail] and [APPROVAL:title:detail].
    """
    out = []
    for m in RE_APPROVAL.finditer(text):
        parts = [m.group(1).strip(), m.group(2).strip(), (m.group(3) or '').strip()]
        if len(parts[0]) <= 10 and parts[0] in APPROVAL_CATEGORIES:
            cat, title, detail = parts[0], parts[1], parts[2]
        else:
            cat, title, detail = 'general', parts[0], parts[1]
        out.append({'category': cat, 'title': title, 'detail': detail})
    return out


def extract_mentions(text):
    """Extract @mentions, e.g. ['CEO', 'CTO']."""
    return [m.group(1) for m in RE_MENTION.finditer(text)]


def has_system_command(text):
    """True if text contains any [TASK_|[APPROVAL:|[CRON_ command."""
    return bool(RE_HAS_COMMAND.search(text))


def has_mention(text):
    """True if text contains @mention."""
    return bool(RE_MENTION.search(text))
