"""
src/scanner.py: Playwright ద్వారా పేజీని నావిగేట్ చేసి ఇంటరాక్టివ్ ఎలిమెంట్స్ సేకరిస్తుంది.
"""
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import json

class WebScanner:
    def __init__(self, headless: bool = True):
        self.headless = headless

    def inspect_page(self, url: str) -> dict:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=self.headless, slow_mo=1000 if not self.headless else 0)
            page = browser.new_page()
            
            # పేజీ లోడ్ అయ్యేదాకా నెట్‌వర్క్ ఐడిల్ స్టేట్ కోసం వేచి చూస్తుంది
            page.goto(url, wait_until="networkidle", timeout=30000)

            if not self.headless:
                page.wait_for_timeout(3000)  # పేజీ లోడ్ అయ్యాక 3 సెకన్లు ఆగుతుంది
                
            title = page.title()
            html_content = page.content()
            browser.close()

        # కేవలం ముఖ్యమైన ఎలిమెంట్స్ (Form, Input, Button, A) మాత్రమే ఫిల్టర్ చేస్తాం
        soup = BeautifulSoup(html_content, "html.parser")
        interactive_elements = []

        for tag in soup.find_all(['button', 'input', 'a', 'textarea', 'select']):
            # ఎలిమెంట్ యొక్క ముఖ్యాంశాలు
            elem_data = {
                "tag": tag.name,
                "type": tag.get("type", ""),
                "id": tag.get("id", ""),
                "name": tag.get("name", ""),
                "placeholder": tag.get("placeholder", ""),
                "text": tag.get_text(strip=True),
                "aria_label": tag.get("aria-label", "")
            }
            # ఖాళీగా లేని ఎలిమెంట్లను మాత్రమే తీసుకుంటాం
            if any(elem_data.values()):
                interactive_elements.append(elem_data)

        return {
            "url": url,
            "title": title,
            "elements_count": len(interactive_elements),
            "elements": interactive_elements[:30] # టాప్ 30 ఎలిమెంట్స్ మాత్రమే LLM కి పంపుతాం
        }