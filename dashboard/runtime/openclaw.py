"""OpenClaw subprocess-based agent runtime."""
import subprocess
from pathlib import Path
from .base import AgentRuntime


class OpenClawRuntime(AgentRuntime):
    """Executes agents via the `openclaw` CLI subprocess."""

    def run(self, agent_id: str, session_id: str, prompt: str,
            timeout: int = 120, model: str = 'zai/glm-5-turbo') -> str:
        """Run a prompt through openclaw and return raw stdout."""
        cmd = ['openclaw', 'agent', '--agent', agent_id,
             '--session-id', session_id, '--local', '-m', prompt]
        if model:
            cmd.extend(['--model', model])
        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        )
        try:
            stdout, _ = proc.communicate(timeout=timeout)
        except subprocess.TimeoutExpired:
            proc.kill()
            proc.wait(timeout=5)
            raise
        if proc.returncode != 0:
            # Return empty string; caller decides retry strategy
            return ''
        return stdout.decode().strip()

    def register(self, agent_id: str, workspace: str,
                 soul_content: str = '') -> bool:
        """Register an agent workspace with openclaw."""
        try:
            result = subprocess.run(
                ['openclaw', 'agents', 'add', agent_id,
                 '--workspace', workspace, '--non-interactive'],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=15,
            )
            return result.returncode == 0
        except Exception:
            return False

    def delete(self, agent_id: str) -> bool:
        """Remove an agent from openclaw."""
        try:
            result = subprocess.run(
                ['openclaw', 'agents', 'delete', agent_id, '--force'],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=15,
            )
            return result.returncode == 0
        except Exception:
            return False

    def list_registered(self) -> str:
        """Return raw output of `openclaw agents list`."""
        try:
            result = subprocess.run(
                ['openclaw', 'agents', 'list'],
                capture_output=True, text=True, timeout=20,
            )
            return result.stdout or ''
        except Exception:
            return ''
