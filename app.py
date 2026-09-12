import streamlit as st

from standards_reader import read_standards_document
from rule_extractor import extract_rules
from llm_client import LLMClient
from reviewer import review_code


# =========================================================
# Page Configuration
# =========================================================

st.set_page_config(
    page_title="PL/SQL Code Review Agent",
    page_icon="🔍",
    layout="wide"
)


# =========================================================
# Header
# =========================================================

st.title("🔍 Oracle PL/SQL Code Review Agent")

st.caption(
    "AI-powered PL/SQL code review based on "
    "standards provided through an external document."
)

st.divider()


# =========================================================
# Input Section
# =========================================================

st.subheader("Review Configuration")

col1, col2 = st.columns(2)


# ---------------------------------------------------------
# Standards Document
# ---------------------------------------------------------

with col1:

    st.markdown("### 📘 PL/SQL Standards")

    standards_file = st.file_uploader(
        "Upload standards document",
        type=["docx"],
        key="standards"
    )

    if standards_file:

        st.success(
            f"✓ {standards_file.name}"
        )


# ---------------------------------------------------------
# PL/SQL Code
# ---------------------------------------------------------

with col2:

    st.markdown("### 💻 PL/SQL Source")

    code_source = st.radio(
        "Code input method",
        [
            "Upload SQL File",
            "Paste PL/SQL Code"
        ],
        horizontal=True
    )

    plsql_code = ""


    if code_source == "Upload SQL File":

        sql_file = st.file_uploader(
            "Upload PL/SQL source",
            type=["sql", "pkb", "pks"],
            key="sql"
        )

        if sql_file:

            plsql_code = sql_file.read().decode(
                "utf-8",
                errors="ignore"
            )

            st.success(
                f"✓ {sql_file.name}"
            )


    else:

        plsql_code = st.text_area(
            "Paste PL/SQL source",
            height=250,
            placeholder=(
                "CREATE OR REPLACE PROCEDURE ..."
            ),
            key="code"
        )


# =========================================================
# Review Button
# =========================================================

st.divider()

review_button = st.button(
    "🔍 Review PL/SQL Code",
    type="primary",
    use_container_width=True
)


# =========================================================
# Review Processing
# =========================================================

if review_button:

    if not standards_file:

        st.error(
            "Please upload the PL/SQL standards document."
        )

        st.stop()


    if not plsql_code.strip():

        st.error(
            "Please provide PL/SQL source code."
        )

        st.stop()


    with st.spinner(
        "Analyzing PL/SQL against coding standards..."
    ):

        # Read standards
        content = read_standards_document(
            standards_file
        )

        # Extract rules
        standards = extract_rules(content)

        # Create LLM client
        llm_client = LLMClient()

        # Review code
        result = review_code(
            plsql_code,
            standards,
            llm_client
        )


    # Store result in session state
    st.session_state["review_result"] = result
    st.session_state["standards_count"] = len(standards)


# =========================================================
# Display Results
# =========================================================

if "review_result" in st.session_state:

    result = st.session_state["review_result"]

    summary = result["summary"]

    st.divider()

    st.subheader("📊 Review Summary")


    # -----------------------------------------------------
    # Metrics
    # -----------------------------------------------------

    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric(
        "Standards Loaded",
        st.session_state["standards_count"]
    )

    col2.metric(
        "Total Findings",
        summary["total_findings"]
    )

    col3.metric(
        "🔴 High",
        summary["high"]
    )

    col4.metric(
        "🟠 Medium",
        summary["medium"]
    )

    col5.metric(
        "🟢 Low",
        summary["low"]
    )


    # =====================================================
    # No Findings
    # =====================================================

    findings = result["findings"]

    if not findings:

        st.success(
            "✅ No standards violations found."
        )

        st.info(
            "The PL/SQL code complies with the "
            "standards provided in the uploaded document."
        )


    # =====================================================
    # Findings
    # =====================================================

    else:

        st.subheader(
            f"📋 Findings ({len(findings)})"
        )

        # =====================================================
        # Findings by Category
        # =====================================================

        categories = {}

        for finding in findings:

            category = finding["category"]

            if category not in categories:
                categories[category] = 0

            categories[category] += 1


        if categories:

            st.markdown("### Findings by Category")

            category_cols = st.columns(
                min(len(categories), 4)
            )

            for index, (category, count) in enumerate(
                categories.items()
            ):

                category_cols[index % len(category_cols)].metric(
                    category,
                    count
                )


        for index, finding in enumerate(findings, start=1):

            severity = finding["severity"]


            # ---------------------------------------------
            # Severity indicator
            # ---------------------------------------------

            if severity == "HIGH":

                severity_icon = "🔴"

            elif severity == "MEDIUM":

                severity_icon = "🟠"

            else:

                severity_icon = "🟢"


            title = (
                f"{severity_icon} "
                f"{finding['rule_id']} | "
                f"{finding['title']} | "
                f"Line {finding['line']}"
            )


            with st.expander(
                title,
                expanded=(index == 1)
            ):

                # -----------------------------------------
                # Finding metadata
                # -----------------------------------------

                col1, col2, col3 = st.columns(3)

                col1.write(
                    f"**Rule:** {finding['rule_id']}"
                )

                col2.write(
                    f"**Severity:** {severity}"
                )

                col3.write(
                    f"**Line:** {finding['line']}"
                )


                st.markdown("### Source Code")

                st.code(
                    finding["code"],
                    language="sql"
                )


                st.markdown("### Issue")

                st.write(
                    finding["message"]
                )


                st.markdown("### Applicable Standard")

                st.info(
                    finding["standard"]
                )


                st.markdown("### Recommendation")

                st.write(
                    finding["recommendation"]
                )


    # =====================================================
    # Source Code
    # =====================================================

    with st.expander(
        "💻 View Submitted PL/SQL Code"
    ):

        st.code(
            plsql_code,
            language="sql"
        )