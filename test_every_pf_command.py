#!/usr/bin/env python3

import json
import os
import re
import subprocess
import sys
from pathlib import Path


PF_FILE = '.pf'
RESULTS_FILE = 'pf_test_results_detailed.json'
TASK_LINE_RE = re.compile(r'^\s{2}([a-zA-Z0-9_.-]+)\s+-\s+')
PREFERRED_TASK_ORDER = [
    'setup',
    'default',
    'generate',
    'typecheck',
    'test',
    'test-cdp',
    'test-generate',
    'test-import',
    'docs',
    'validate',
    'rebuild',
    'check',
]


def resolve_workspace() -> Path:
    workspace_override = os.environ.get('PF_WORKSPACE')
    if workspace_override:
        return Path(workspace_override).resolve()

    script_dir = Path(__file__).resolve().parent
    return script_dir


def list_pf_tasks(workspace: Path) -> list[str]:
    result = subprocess.run(
        ['pf', '-f', PF_FILE, 'list'],
        cwd=workspace,
        capture_output=True,
        text=True,
        timeout=120,
        check=False,
    )

    if result.returncode != 0:
        raise RuntimeError(f'Failed to list pf tasks: {result.stderr.strip()}')

    tasks: list[str] = []
    for line in result.stdout.splitlines():
        match = TASK_LINE_RE.match(line)
        if match:
            tasks.append(match.group(1))

    return tasks


def order_tasks(tasks: list[str]) -> list[str]:
    if not tasks:
        return []

    order_rank = {
        name: index
        for index, name in enumerate(PREFERRED_TASK_ORDER)
    }
    max_rank = len(PREFERRED_TASK_ORDER)

    return sorted(
        tasks,
        key=lambda task: (order_rank.get(task, max_rank), task)
    )


def run_task(workspace: Path, task: str, max_attempts: int = 2) -> dict:
    attempts = []
    result = None

    for attempt_number in range(1, max_attempts + 1):
        result = subprocess.run(
            ['pf', '-f', PF_FILE, task],
            cwd=workspace,
            capture_output=True,
            text=True,
            timeout=900,
            check=False,
        )
        attempts.append({
            'attempt': attempt_number,
            'returncode': result.returncode,
            'stdout': result.stdout,
            'stderr': result.stderr,
        })
        if result.returncode == 0:
            break

    assert result is not None
    return {
        'task': task,
        'success': result.returncode == 0,
        'returncode': result.returncode,
        'stdout': result.stdout,
        'stderr': result.stderr,
        'attempt_count': len(attempts),
        'flaky_pass': len(attempts) > 1 and result.returncode == 0,
        'attempts': attempts,
    }


def main() -> int:
    workspace = resolve_workspace()

    print('=' * 60)
    print('TESTING ALL PF TASKS - COMPREHENSIVE')
    print('=' * 60)
    print("Rule target: 'ALL PF FILES MUST BE TESTED BEFORE YOU STOP WORKING. Every entry.'")
    print()
    print(f'Workspace: {workspace}')
    print(f'PF file: {workspace / PF_FILE}')
    print()

    try:
        tasks = order_tasks(list_pf_tasks(workspace))
    except Exception as error:
        print(f'ERROR: {error}')
        return 1

    if not tasks:
        print('ERROR: no tasks were discovered from pf list output.')
        return 1

    print(f'Found {len(tasks)} pf task(s): {", ".join(tasks)}')
    print()

    results = []
    for task in tasks:
        print(f'Running task: {task}')
        task_result = run_task(workspace, task)
        results.append(task_result)
        status = 'PASS' if task_result['success'] else 'FAIL'
        retry_suffix = ''
        if task_result.get('attempt_count', 1) > 1:
            retry_suffix = f', attempts={task_result["attempt_count"]}'
        print(f'  {task}: {status} (exit={task_result["returncode"]}{retry_suffix})')
        if not task_result['success'] and task_result['stderr']:
            print('  stderr (first 300 chars):')
            print(task_result['stderr'][:300])

    output_payload = {
        'workspace': str(workspace),
        'pf_file': PF_FILE,
        'tasks': results,
    }
    output_path = workspace / RESULTS_FILE
    output_path.write_text(json.dumps(output_payload, indent=2))

    total = len(results)
    passed = sum(1 for item in results if item['success'])
    print()
    print('=' * 60)
    print('FINAL RESULTS - ALL PF TASKS')
    print('=' * 60)
    print(f'Overall: {passed}/{total} task entries passed')
    print(f'Detailed results saved to: {output_path}')

    return 0 if passed == total else 1


if __name__ == '__main__':
    sys.exit(main())
