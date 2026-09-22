"""
src/test_runner.py: Pytest ను గరిష్టంగా 15 సెకన్ల టైమౌట్‌తో రన్ చేస్తుంది.
"""
import subprocess
import os

class TestRunner:
    @staticmethod
    def save_and_run_test(test_code: str, file_path: str = "generated_tests/test_dynamic_suite.py") -> dict:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(test_code)

        # గరిష్టంగా 15 సెకన్ల టైమౌట్
        cmd = ["pytest", file_path, "-v", "--tb=short"]
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
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
                "stderr": "Pytest execution timed out after 15 seconds.",
                "code_run": test_code
            }