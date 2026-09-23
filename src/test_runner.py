"""
src/test_runner.py: Pytest ను గరిష్టంగా 15 సెకన్ల టైమౌట్‌తో రన్ చేస్తుంది.
"""
import sys
import subprocess
import os

class TestRunner:
    @staticmethod
    def save_and_run_test(test_code: str, file_path: str = "generated_tests/test_dynamic_suite.py") -> dict:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(test_code)      

        # cmd లో కేవలం "pytest" బదులు sys.executable వాడాలి:
        cmd = [sys.executable, "-m", "pytest", file_path, "-v", "--tb=short", "--headed", "--slowmo", "1000"]  
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            is_passed = (result.returncode == 0)
            return {
                "passed": is_passed,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "code_run": test_code
            }
        except subprocess.TimeoutExpired:
            return {
                "passed": False,
                "stdout": "",
                "stderr": "Pytest execution timed out after 60 seconds.",
                "code_run": test_code
            }