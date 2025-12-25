#!/usr/bin/env python3

import os
import sys
import subprocess
import json
from pathlib import Path

def test_pf_task_commands():
    """
    Test every single command in the .pf file as required by rules.
    Rules state: "ALL PF FILES MUST BE TESTED BEFORE YOU STOP WORKING. Every entry."
    """
    
    print("=" * 60)
    print("TESTING ALL PF TASKS - COMPREHENSIVE")
    print("=" * 60)
    print("Per rules: 'ALL PF FILES MUST BE TESTED BEFORE YOU STOP WORKING. Every entry.'")
    print()
    
    # Change to workspace
    os.chdir('/workspace')
    
    # Read and parse the .pf file
    pf_file = Path('.pf')
    if not pf_file.exists():
        print("✗ ERROR: .pf file not found!")
        return False
    
    print("📄 Reading .pf file...")
    with open(pf_file, 'r') as f:
        pf_content = f.read()
    
    print(f"📄 .pf file content:\n{pf_content}\n")
    
    # Extract tasks from .pf file
    # The .pf file has tasks in format: task_name:\n    command
    tasks = {}
    current_task = None
    
    for line in pf_content.split('\n'):
        line = line.rstrip()
        if line and not line.startswith('#') and ':' in line and not line.startswith(' '):
            # This is a task definition
            current_task = line.split(':')[0].strip()
            tasks[current_task] = []
        elif line.startswith('    ') and current_task:
            # This is a command for the current task
            command = line.strip()
            if command:
                tasks[current_task].append(command)
    
    print(f"📋 Found {len(tasks)} tasks in .pf file:")
    for task_name, commands in tasks.items():
        print(f"  - {task_name}: {len(commands)} command(s)")
    print()
    
    # Test each task
    results = {}
    total_commands = 0
    passed_commands = 0
    
    for task_name, commands in tasks.items():
        print(f"\n{'='*40}")
        print(f"TESTING TASK: {task_name}")
        print('='*40)
        
        task_success = True
        task_results = []
        
        for i, command in enumerate(commands, 1):
            total_commands += 1
            print(f"\n  Command {i}/{len(commands)}: {command}")
            
            # Test the command
            try:
                result = subprocess.run(
                    command, 
                    shell=True, 
                    capture_output=True, 
                    text=True, 
                    timeout=120,  # 2 minute timeout
                    cwd='/workspace'
                )
                
                if result.returncode == 0:
                    print(f"  ✓ SUCCESS")
                    passed_commands += 1
                    task_results.append({
                        'command': command,
                        'success': True,
                        'output': result.stdout[:200] if result.stdout else "",
                        'error': ""
                    })
                else:
                    print(f"  ✗ FAILED (exit code: {result.returncode})")
                    if result.stderr:
                        print(f"  Error: {result.stderr[:200]}...")
                    task_success = False
                    task_results.append({
                        'command': command,
                        'success': False,
                        'output': result.stdout[:200] if result.stdout else "",
                        'error': result.stderr[:200] if result.stderr else ""
                    })
                    
            except subprocess.TimeoutExpired:
                print(f"  ✗ TIMEOUT (>120s)")
                task_success = False
                task_results.append({
                    'command': command,
                    'success': False,
                    'output': "",
                    'error': "Command timed out after 120 seconds"
                })
                
            except Exception as e:
                print(f"  ✗ ERROR: {e}")
                task_success = False
                task_results.append({
                    'command': command,
                    'success': False,
                    'output': "",
                    'error': str(e)
                })
        
        results[task_name] = {
            'success': task_success,
            'commands': task_results
        }
        
        # Task summary
        task_passed = sum(1 for cmd in task_results if cmd['success'])
        task_total = len(task_results)
        status = "✓ PASS" if task_success else "✗ FAIL"
        print(f"\n  Task Summary: {status} ({task_passed}/{task_total} commands passed)")
    
    # Final summary
    print(f"\n{'='*60}")
    print("FINAL RESULTS - ALL PF TASKS")
    print('='*60)
    
    for task_name, result in results.items():
        status = "✓ PASS" if result['success'] else "✗ FAIL"
        cmd_count = len(result['commands'])
        passed_count = sum(1 for cmd in result['commands'] if cmd['success'])
        print(f"{task_name:15} {status} ({passed_count}/{cmd_count} commands)")
    
    print(f"\nOverall: {passed_commands}/{total_commands} commands passed")
    
    # Save detailed results
    with open('pf_test_results_detailed.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"📄 Detailed results saved to: pf_test_results_detailed.json")
    
    # Determine final status
    all_passed = passed_commands == total_commands
    
    if all_passed:
        print("\n🎉 SUCCESS: All pf tasks are working correctly!")
        print("✅ Every single command in the .pf file has been tested and passes.")
    else:
        print("\n⚠️  ISSUES FOUND: Some pf tasks have problems.")
        print("❌ Failed commands need to be fixed or removed per rules.")
        print("\nPer rules: 'check all pf tasks and fix them OR remove them if they are no longer relevant'")
    
    return all_passed

if __name__ == "__main__":
    success = test_pf_task_commands()
    sys.exit(0 if success else 1)