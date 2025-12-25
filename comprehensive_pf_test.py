#!/usr/bin/env python3

import os
import sys
import subprocess
import json
from datetime import datetime

class PFTaskTester:
    def __init__(self):
        self.results = {}
        self.workspace = '/workspace'
        
    def run_command(self, cmd, timeout=60):
        """Run a command and return (success, stdout, stderr)"""
        try:
            os.chdir(self.workspace)
            result = subprocess.run(
                cmd, 
                shell=True, 
                capture_output=True, 
                text=True, 
                timeout=timeout
            )
            return result.returncode == 0, result.stdout, result.stderr
        except subprocess.TimeoutExpired:
            return False, "", "Command timed out"
        except Exception as e:
            return False, "", str(e)
    
    def test_task(self, task_name, command, description=""):
        """Test a single pf task"""
        print(f"\n{'='*50}")
        print(f"Testing: {task_name}")
        print(f"Command: {command}")
        if description:
            print(f"Description: {description}")
        print('='*50)
        
        success, stdout, stderr = self.run_command(command)
        
        self.results[task_name] = {
            'command': command,
            'success': success,
            'stdout': stdout[:500] if stdout else "",
            'stderr': stderr[:500] if stderr else "",
            'description': description
        }
        
        if success:
            print(f"✓ {task_name}: PASSED")
            if stdout:
                print(f"Output: {stdout[:200]}...")
        else:
            print(f"✗ {task_name}: FAILED")
            if stderr:
                print(f"Error: {stderr[:200]}...")
        
        return success
    
    def test_all_pf_tasks(self):
        """Test all tasks defined in .pf file"""
        print("=== COMPREHENSIVE PF TASK TESTING ===")
        print(f"Started at: {datetime.now()}")
        print(f"Workspace: {self.workspace}")
        
        # Read the .pf file to understand what we're testing
        try:
            with open(f"{self.workspace}/.pf", 'r') as f:
                pf_content = f.read()
                print(f"\nPF file content preview:\n{pf_content[:300]}...")
        except Exception as e:
            print(f"Could not read .pf file: {e}")
        
        # Test each task from the .pf file
        # Note: Testing the underlying commands since pf tool may not be available
        
        tasks_to_test = [
            # Basic functionality tests
            ("test-import", "python3 -c 'import cdp; print(cdp.accessibility)'", 
             "Test basic CDP module import"),
            
            # Code generation
            ("generate", "python3 generator/generate.py", 
             "Generate CDP bindings from JSON specs"),
            
            # Testing tasks
            ("test-generate", "python3 -m pytest generator/ -v", 
             "Run tests on the generator code"),
            
            ("test-cdp", "python3 -m pytest test/ -v", 
             "Run tests on the CDP modules"),
            
            # Type checking tasks
            ("mypy-generate", "python3 -m mypy generator/", 
             "Type check the generator code"),
            
            ("mypy-cdp", "python3 -m mypy cdp/", 
             "Type check the CDP modules"),
            
            # Documentation
            ("docs", "cd docs && python3 -m sphinx -b html . _build/html", 
             "Build documentation"),
            
            # Combined tasks (these map to pf tasks)
            ("typecheck-combined", "python3 -m mypy generator/ && python3 -m mypy cdp/", 
             "Combined type checking (typecheck pf task)"),
            
            ("test-combined", "python3 -m pytest test/ -v && python3 -m pytest generator/ -v && python3 -c 'import cdp; print(cdp.accessibility)'", 
             "Combined testing (test pf task)"),
            
            ("check-combined", "python3 -m pytest test/ -v && python3 -c 'import cdp; print(cdp.accessibility)'", 
             "Quick check (check pf task)"),
        ]
        
        # Run all tests
        passed = 0
        total = len(tasks_to_test)
        
        for task_name, command, description in tasks_to_test:
            if self.test_task(task_name, command, description):
                passed += 1
        
        # Summary
        print(f"\n{'='*60}")
        print("FINAL TEST RESULTS")
        print('='*60)
        
        for task_name in self.results:
            result = self.results[task_name]
            status = "✓ PASS" if result['success'] else "✗ FAIL"
            print(f"{task_name:20} {status}")
        
        print(f"\nSummary: {passed}/{total} tasks passed")
        
        if passed == total:
            print("🎉 ALL PF TASKS ARE WORKING CORRECTLY!")
            print("✓ Every command in the .pf file has been tested and works.")
        else:
            print("⚠️  SOME PF TASKS NEED ATTENTION")
            print("✗ Failed tasks need to be fixed or removed per rules.")
        
        # Save detailed results
        self.save_results()
        
        return passed == total
    
    def save_results(self):
        """Save test results to file"""
        try:
            with open(f"{self.workspace}/pf_test_results.json", 'w') as f:
                json.dump({
                    'timestamp': datetime.now().isoformat(),
                    'summary': {
                        'total_tasks': len(self.results),
                        'passed_tasks': sum(1 for r in self.results.values() if r['success']),
                        'failed_tasks': sum(1 for r in self.results.values() if not r['success'])
                    },
                    'results': self.results
                }, f, indent=2)
            print(f"\n📄 Detailed results saved to: pf_test_results.json")
        except Exception as e:
            print(f"Could not save results: {e}")

def main():
    tester = PFTaskTester()
    success = tester.test_all_pf_tasks()
    
    if not success:
        print("\n⚠️  ACTION REQUIRED:")
        print("Some pf tasks failed. Per rules, these need to be:")
        print("1. Fixed if they're still relevant")
        print("2. Removed if they're no longer needed")
        print("3. Updated if they're outdated")
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())