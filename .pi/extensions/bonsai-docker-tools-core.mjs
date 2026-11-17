/** Thin adapters for the runtime-owned managed lifecycle CLI. No Docker calls here. */
import { fileURLToPath } from 'node:url';

export function pythonCommand(platform, configured) {
  if (configured !== undefined && configured !== '') {
    if (typeof configured !== 'string' || /[\x00-\x1f]/.test(configured)) throw new Error('Python executable contains control characters');
    return { command: configured, prefixArgs: [] };
  }
  return platform === 'win32' ? { command: 'py', prefixArgs: ['-3'] } : { command: 'python3', prefixArgs: [] };
}

export function lifecycleArgs(action, params) {
  if (!['inspect', 'stop', 'restart', 'upgrade', 'logs'].includes(action)) throw new Error('Unsupported lifecycle action');
  const args = [];
  if (params.platformRoot) args.push('--platform-root', params.platformRoot);
  if (params.wslDistro) args.push('--wsl-distro', params.wslDistro);
  args.push('--json');
  if (params.stateDir) args.push('--state-dir', params.stateDir);
  if (action !== 'logs') {
    if (!/^[A-Za-z0-9][A-Za-z0-9_.-]{0,63}$/.test(params.installation ?? '')) throw new Error('Specify a registered installation');
    args.push('--installation', params.installation);
  }
  args.push(action);
  if (params.operation) {
    if (!/^[a-f0-9]{32}$/.test(params.operation)) throw new Error('Invalid operation id');
    if (action === 'logs') args.push(params.operation);
    else if (action !== 'inspect') args.push('--operation', params.operation);
    else throw new Error('Inspection does not resume an operation');
  } else if (action === 'logs') throw new Error('Logs require an operation id');
  if (action === 'upgrade' && !params.operation) {
    if (!/^[a-f0-9]{40}$/.test(params.revision ?? '')) throw new Error('Upgrade requires an exact revision');
    args.push('--revision', params.revision);
    if (params.start) args.push('--start');
  } else if (params.revision || params.start) throw new Error('Revision/start apply only to a new upgrade');
  if (action === 'logs') {
    const tail = params.tail ?? 40;
    if (!Number.isInteger(tail) || tail < 1 || tail > 200) throw new Error('Tail must be 1..200');
    args.push('--tail', String(tail));
  }
  return args;
}

export function installLifecycleTools(pi, Type) {
  const base = {
    platformRoot: Type.Optional(Type.String({ description: 'Trusted runtime checkout path' })),
    wslDistro: Type.Optional(Type.String()),
    stateDir: Type.Optional(Type.String({ description: 'Private Linux lifecycle registry directory' })),
  };
  const actions = [
    ['bonsai_worker_status', 'inspect', 'Inspect one registered worker installation'],
    ['bonsai_stop_worker', 'stop', 'Stop an idle installation; unknown work blocks the operation'],
    ['bonsai_restart_worker', 'restart', 'Restart the same installed release without an upgrade'],
    ['bonsai_upgrade_worker', 'upgrade', 'Build, check and install an exact runtime revision; leave stopped unless start is selected'],
    ['bonsai_worker_events', 'logs', 'Read bounded managed lifecycle operation logs; these are not worker task events'],
  ];
  for (const [name, action, description] of actions) {
    const readOnly = action === 'inspect' || action === 'logs';
    const fields = { ...base, ...(action === 'logs' ? {
      operation: Type.String(), tail: Type.Optional(Type.Integer({ minimum: 1, maximum: 200 })),
    } : { installation: Type.String(), ...(action === 'inspect' ? {} : { operation: Type.Optional(Type.String()) }) }),
      ...(action === 'upgrade' ? { revision: Type.Optional(Type.String()), start: Type.Optional(Type.Boolean()) } : {}),
    };
    pi.registerTool({ name, label: name.replaceAll('_', ' '), description, parameters: Type.Object(fields),
      defaultActive: readOnly, annotations: { readOnlyHint: readOnly }, executionMode: 'sequential',
      async execute(_id, params, signal, _onUpdate, ctx) {
        signal?.throwIfAborted();
        const args = lifecycleArgs(action, params);
        if (!readOnly && (ctx.hasUI !== true || typeof ctx.ui?.confirm !== 'function' ||
          !(await ctx.ui.confirm('Authorize worker ' + action + '?', 'Installation: ' + params.installation +
            '\nRevision: ' + (params.revision ?? 'installed/recorded release') + '\nStartup: ' +
            (action === 'restart' || params.start === true ? 'authorized' : 'leave stopped'))))) throw new Error('Operator confirmation required');
        const runner = pythonCommand(process.platform, process.env.BONSAI_PYTHON);
        const script = fileURLToPath(new URL('../../tools/containers.py', import.meta.url));
        const result = await pi.exec(runner.command, [...runner.prefixArgs, script, ...args], { signal });
        if (result.code !== 0) throw new Error('Lifecycle ' + action + ' failed: ' + (result.stderr || result.stdout));
        const text = result.stdout.trim();
        if (!text) throw new Error('Lifecycle returned no observation');
        if (Buffer.byteLength(text) > 32768) throw new Error('Lifecycle observation exceeds output bound; narrow the request');
        return { content: [{ type: 'text', text }], details: { action, installation: params.installation ?? null } };
      },
    });
  }
  pi.registerTool({ name: 'verify_commit_branch', label: 'Verify Commit Branch',
    description: 'Verify the expected Git branch and optional commit ancestry after a commit',
    parameters: Type.Object({ repo: Type.Optional(Type.String()), expectedBranch: Type.String(),
      initialSha: Type.Optional(Type.String()), commitSha: Type.Optional(Type.String()) }),
    async execute(_id, params, signal) {
      const runner = pythonCommand(process.platform, process.env.BONSAI_PYTHON);
      const args = [fileURLToPath(new URL('../skills/pr-submission/scripts/verify_branch.py', import.meta.url)),
        '--repo', params.repo ?? '.', '--expected-branch', params.expectedBranch];
      if (params.initialSha) args.push('--initial-sha', params.initialSha);
      if (params.commitSha) args.push('--commit-sha', params.commitSha);
      const result = await pi.exec(runner.command, [...runner.prefixArgs, ...args], { signal });
      if (result.code !== 0) throw new Error(result.stderr || result.stdout);
      return { content: [{ type: 'text', text: result.stdout }], details: {} };
    },
  });
}
