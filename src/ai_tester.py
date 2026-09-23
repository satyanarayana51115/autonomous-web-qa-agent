"""
src/ai_tester.py: Google GenAI SDK with robust retry logic for 503 server spikes.
"""
import os
import time
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

class AITester:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        self.client = genai.Client(api_key=api_key)
        self.model_name = "gemini-3.6-flash"

    def _call_model_with_retry(self, prompt: str, max_retries: int = 4) -> str:
        """503 తాత్కాలిక సర్వర్ ట్రాఫిక్ వస్తే వేచి చూసి మళ్లీ ప్రయత్నించే పటిష్టమైన లాజిక్"""
        for attempt in range(max_retries):
            try:
                response = self.client.models.generate_content(
                    model=self.model_name,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        temperature=0.2,
                    )
                )
                return response.text.replace("```python", "").replace("```", "").strip()
            except Exception as e:
                err_text = str(e)
                # సర్వర్ ఓవర్‌లోడ్ లేదా బిజీగా ఉంటే (503 లేదా 429)
                if ("503" in err_text or "429" in err_text or "UNAVAILABLE" in err_text) and attempt < max_retries - 1:
                    sleep_time = (attempt + 1) * 4  # 4 సెకన్లు, 8 సెకన్లు, 12 సెకన్లు వేచి చూస్తుంది
                    time.sleep(sleep_time)
                    continue
                raise e

    def generate_test_suite(self, url: str, page_title: str, elements: list) -> str:
        prompt = f"""
        You are an expert QA Automation Engineer using Playwright and Pytest.
        Target URL: {url}
        Page Title: {page_title}
        Interactive Elements: {elements}

        Write a concise, resilient Pytest script using playwright.sync_api.
        Rules:
        1. Test function signature: `def test_autonomous_generated_suite(page):`.
        2. First line: `page.goto("{url}")`.
        3. Do NOT use page.fill(). To make typing visible on screen, MUST use:
           - `page.locator("#username").click()`
           - `page.keyboard.type("tomsmith", delay=150)`
           - `page.wait_for_timeout(1000)`
           - `page.locator("#password").click()`
           - `page.keyboard.type("SuperSecretPassword!", delay=150)`
           - `page.wait_for_timeout(1000)`
        4. Click submit:
           - `page.locator("button[type='submit']").click()`
           - `page.wait_for_timeout(4000)`
        5. Return ONLY executable raw Python code without markdown blocks or backticks.
        """
        return self._call_model_with_retry(prompt)

    def heal_broken_test(self, failed_code: str, error_trace: str, current_dom_elements: list) -> str:
        prompt = f"""
        Fix broken selector in this Playwright test:
        ERROR: {error_trace}
        FAILED CODE: {failed_code}
        CURRENT ELEMENTS: {current_dom_elements}

        Return ONLY valid fixed Python code.
        """
        return self._call_model_with_retry(prompt)