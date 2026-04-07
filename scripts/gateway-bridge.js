#!/usr/bin/env node
/**
 * OpenClaw Gateway WebSocket bridge.
 * Reads messages from stdin (JSON lines), sends to gateway WS, returns replies.
 * Keeps WS connection alive — no reconnection overhead per message.
 *
 * Usage: node gateway-bridge.js
 * Stdin:  {"agent":"id","session":"sid","message":"text","timeout":120000}
 * Stdout: {"ok":true,"reply":"..."} or {"ok":false,"error":"..."}
 */
const WebSocket = require('ws');
const GATEWAY_URL = process.env.GATEWAY_WS || 'ws://127.0.0.1:18789';
const TOKEN = process.env.GATEWAY_TOKEN || '';

let ws;
let pending = new Map(); // id -> {resolve, reject, timer}
let msgId = 0;

function connect() {
  const headers = TOKEN ? { Authorization: `Bearer ${TOKEN}` } : {};
  ws = new WebSocket(GATEWAY_URL, { headers });

  ws.on('open', () => {
    process.stderr.write('[bridge] connected\n');
  });

  ws.on('message', (data) => {
    try {
      const msg = JSON.parse(data.toString());
      // Try to match with pending requests
      for (const [id, p] of pending) {
        if (msg.id === id || msg.reply_to === id) {
          clearTimeout(p.timer);
          pending.delete(id);
          p.resolve(msg);
          return;
        }
      }
      // Unmatched message — could be a push
    } catch (e) {}
  });

  ws.on('close', () => {
    process.stderr.write('[bridge] disconnected, reconnecting...\n');
    for (const [id, p] of pending) {
      clearTimeout(p.timer);
      p.reject(new Error('ws closed'));
    }
    pending.clear();
    setTimeout(connect, 2000);
  });

  ws.on('error', (err) => {
    process.stderr.write(`[bridge] error: ${err.message}\n`);
  });
}

function send(agentId, sessionId, message, timeoutMs = 120000) {
  return new Promise((resolve, reject) => {
    if (!ws || ws.readyState !== WebSocket.OPEN) {
      reject(new Error('not connected'));
      return;
    }
    const id = `bridge-${++msgId}`;
    const payload = {
      id,
      agent: agentId,
      session: sessionId,
      message,
      type: 'agent_turn'
    };
    const timer = setTimeout(() => {
      pending.delete(id);
      resolve({ ok: false, error: 'timeout', reply: '' });
    }, timeoutMs);

    pending.set(id, { resolve, reject, timer });
    ws.send(JSON.stringify(payload));
  });
}

// Read JSON lines from stdin
process.stdin.setEncoding('utf8');
let buffer = '';
process.stdin.on('data', async (chunk) => {
  buffer += chunk;
  const lines = buffer.split('\n');
  buffer = lines.pop(); // keep incomplete line

  for (const line of lines) {
    const trimmed = line.trim();
    if (!trimmed) continue;
    try {
      const req = JSON.parse(trimmed);
      const result = await send(
        req.agent || '',
        req.session || '',
        req.message || '',
        req.timeout || 120000
      );
      process.stdout.write(JSON.stringify(result) + '\n');
    } catch (e) {
      process.stdout.write(JSON.stringify({ ok: false, error: e.message }) + '\n');
    }
  }
});

connect();
