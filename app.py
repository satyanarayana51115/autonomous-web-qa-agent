import streamlit as st
import os
import json
from src.scanner import WebScanner
from src.ai_tester import AITester
from src.test_runner import TestRunner

st.set_page_config(
    page_title="Autonomous Web QA Agent",
    page_icon="🧪",
    layout="wide"
)

# --- CENTER ALIGNED HEADER & TECH STACK ---
st.markdown("""
    <div style="text-align: center; padding-bottom: 1.5rem;">
        <h1 style="margin-bottom: 0.2rem;">🧪 Autonomous Web QA & Self-Healing Testing Agent</h1>
        <p style="font-size: 1.15rem; color: #888; margin-bottom: 0.8rem;">
            Zero-Scripting Autonomous Testing Suite powered by Playwright + Pytest + Gemini Reasoning
        </p>
        <div>
            <span style="background-color: #262730; color: #00FFCC; padding: 4px 10px; border-radius: 4px; font-weight: bold; margin: 2px;">Python</span>
            <span style="background-color: #262730; color: #45ba4b; padding: 4px 10px; border-radius: 4px; font-weight: bold; margin: 2px;">Playwright</span>
            <span style="background-color: #262730; color: #0a9edc; padding: 4px 10px; border-radius: 4px; font-weight: bold; margin: 2px;">Pytest</span>
            <span style="background-color: #262730; color: #ff4b4b; padding: 4px 10px; border-radius: 4px; font-weight: bold; margin: 2px;">Google Gemini SDK</span>
            <span style="background-color: #262730; color: #ffa421; padding: 4px 10px; border-radius: 4px; font-weight: bold; margin: 2px;">Self-Healing AST</span>
        </div>
    </div>
    <hr style="margin-top: 0.5rem; margin-bottom: 1.5rem; border: 0.5px solid #333;">
""", unsafe_allow_html=True)

# Sidebar Configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    target_url = st.text_input(
        "Target Website URL:",
        value="https://example.com",
        help="Enter the full URL including https://"
    )
    headless_mode = st.checkbox("Headless Browser Mode", value=False) # వీడియో రికార్డింగ్ కోసం డిఫాల్ట్‌గా False (Headed) ఉంచాం
    run_btn = st.button("🚀 Run Autonomous Test Suite", type="primary", use_container_width=True)


if run_btn:
    if not target_url:
        st.error("Please enter a valid target URL.")
    else:
        scanner = WebScanner(headless=headless_mode)
        tester = AITester()
        runner = TestRunner()

        col1, col2 = st.columns([1, 1])

        # Step 1: Autonomous Discovery (Page Scanning)
        with st.status("🔍 Scanning Website & Extracting DOM...", expanded=True) as status:
            st.write("Navigating target URL via Playwright and inspecting interactive elements...")
            try:
                scan_data = scanner.inspect_page(target_url)
                st.write(f"Page Title: **{scan_data['title']}**")
                st.write(f"Interactive Elements Detected: **{scan_data['elements_count']}**")
            except Exception as e:
                st.error(f"Page scanning failed: {e}")
                st.stop()

            # Step 2: AI Test Generation
            st.write("🤖 Generating resilient Pytest script using Gemini...")
            try:
                test_code = tester.generate_test_suite(
                    url=scan_data["url"],
                    page_title=scan_data["title"],
                    elements=scan_data["elements"]
                )
            except Exception as e:
                st.error(f"Test generation failed: {e}")
                st.stop()

            # Step 3: Test Execution
            st.write("⚡ Executing generated tests via Pytest runner...")
            run_result = runner.save_and_run_test(test_code)

            # Step 4: Self-Healing Mechanism (If Test Fails)
            if not run_result["passed"]:
                st.warning("⚠️ Test assertion failed. Initiating Self-Healing Agent...")
                healed_code = tester.heal_broken_test(
                    failed_code=test_code,
                    error_trace=run_result["stderr"] + "\n" + run_result["stdout"],
                    current_dom_elements=scan_data["elements"]
                )
                st.write("🔄 Re-executing suite with healed locators...")
                run_result = runner.save_and_run_test(healed_code)
                test_code = healed_code

            status.update(label="✅ Autonomous QA Pipeline Completed!", state="complete", expanded=False)

        # Output Display Columns
        with col1:
            st.subheader("📊 Execution Results")
            if run_result["passed"]:
                st.success("✅ All Generated Test Cases Passed Successfully (100% Passed)!")
            else:
                st.error("❌ Test suite execution failed. Review execution trace below.")

            with st.expander("View Raw Pytest Terminal Output", expanded=True):
                st.code(run_result["stdout"] if run_result["stdout"] else run_result["stderr"], language="text")

        with col2:
            st.subheader("📝 Autonomous Pytest Code")
            st.code(test_code, language="python")