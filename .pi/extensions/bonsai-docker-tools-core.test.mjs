import { test } from 'node:test';
import assert from 'node:assert/strict';
import { installLifecycleTools, lifecycleArgs, pythonCommand } from './bonsai-docker-tools-core.mjs';

test('Python argv preserves executable boundaries', () => {
  assert.deepEqual(pythonCommand('win32'), { command: 'py', prefixArgs: ['-3'] });
  assert.deepEqual(pythonCommand('linux'), { command: 'python3', prefixArgs: [] });
  assert.deepEqual(pythonCommand('linux', '/a b/python'), { command: '/a b/python', prefixArgs: [] });
  assert.throws(() => pythonCommand('linux', 'bad\nexe'), /control/);
});
test('managed argv requires explicit identity and separates stop, restart and upgrade', () => {
  assert.deepEqual(lifecycleArgs('stop', { installation: 'ui' }), ['--json', '--installation', 'ui', 'stop']);
  assert.deepEqual(lifecycleArgs('restart', { installation: 'ui', operation: 'b'.repeat(32) }),
    ['--json', '--installation', 'ui', 'restart', '--operation', 'b'.repeat(32)]);
  assert.throws(() => lifecycleArgs('stop', {}), /installation/);
  assert.throws(() => lifecycleArgs('upgrade', { installation: 'ui', revision: 'main' }), /exact revision/);
  assert.throws(() => lifecycleArgs('upgrade', { installation: 'ui', operation: 'b'.repeat(32), start: true }), /new upgrade/);
  assert.throws(() => lifecycleArgs('logs', { operation: 'b'.repeat(32), tail: 201 }), /Tail/);
});
test('registered mutation cannot execute without confirmation; status forwards only to adapter', async () => {
  const definitions = new Map(), calls = [];
  const Type = Object.fromEntries(['Optional','String','Integer','Boolean','Object'].map(name => [name, value => ({ name, value })]));
  installLifecycleTools({ registerTool: tool => definitions.set(tool.name, tool),
    exec: async (...args) => { calls.push(args); return { code: 0, stdout: '{"status":"observed"}', stderr: '' }; } }, Type);
  const stop = definitions.get('bonsai_stop_worker');
  assert.equal(stop.defaultActive, false);
  await assert.rejects(stop.execute('', { installation: 'ui' }, undefined, undefined, { hasUI: false }), /confirmation/);
  assert.equal(calls.length, 0);
  await stop.execute('', { installation: 'ui' }, undefined, undefined, { hasUI: true, ui: { confirm: async () => true } });
  assert.ok(calls[0][1].some(value => value.endsWith('tools/containers.py') || value.endsWith('tools\\containers.py')));
  assert.deepEqual(calls[0][1].slice(-4), ['--json', '--installation', 'ui', 'stop']);
  await definitions.get('bonsai_worker_status').execute('', { installation: 'ui' }, undefined, undefined, {});
  assert.equal(calls.at(-1)[1].at(-1), 'inspect');
  assert.equal(definitions.has('bonsai_build_image'), false);
});
