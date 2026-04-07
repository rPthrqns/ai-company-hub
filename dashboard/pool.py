#!/usr/bin/env python3
"""
Persistent agent process pool.
Instead of spawning a new `openclaw agent` process per nudge,
keep a warm process running and reuse it via stdin/stdout JSON lines.
"""
import subprocess, json, threading, queue, time, sys

class AgentPool:
    def __init__(self, max_workers=1):
        self.max_workers = max_workers
        self.workers = []  # list of (process, queue)
        self.lock = threading.Lock()
        self._q = queue.Queue()

    def _spawn(self):
        """Spawn a persistent openclaw process that reads JSON from stdin."""
        # We can't easily make openclaw persistent, so this is a placeholder
        # The real optimization would need Gateway WS support
        return None

    def execute(self, agent_id, session_id, message, timeout=120):
        """Execute agent turn. Falls back to subprocess if pool unavailable."""
        # Pool not implemented yet - use direct subprocess
        proc = subprocess.Popen(
            ['openclaw', 'agent', '--agent', agent_id,
             '--session-id', session_id, '--local', '-m', message],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        try:
            stdout, stderr = proc.communicate(timeout=timeout)
            return stdout.decode().strip(), proc.returncode
        except subprocess.TimeoutExpired:
            proc.kill()
            proc.wait(timeout=5)
            return '', -1

# Singleton
pool = AgentPool()
