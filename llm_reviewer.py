from models import StandardRule


def build_review_prompt(code: str, standards: list[StandardRule]) -> str:

    standards_text = ""

    for rule in standards:

        standards_text += f"""
            Rule ID: {rule.id}
            Section: {rule.section}
            Title: {rule.title}
            Severity: {rule.severity}
            Standard: {rule.standard}

            """

    prompt = f"""
Review the following Oracle PL/SQL code against the
provided coding standards.

IMPORTANT REVIEW RULES:

1. Use ONLY the standards supplied in this prompt.

2. Do NOT invent additional coding standards.

3. Evaluate every supplied standard against the PL/SQL code.

4. Report ONLY genuine violations.

5. If the code complies with a standard, DO NOT report it.

6. If a standard is not applicable to the code, DO NOT report it.

7. Consider the PL/SQL context before reporting a violation.

8. Every finding MUST reference the Rule ID from the
   supplied standards.

9. Every finding MUST identify the relevant source-code line.

10. The "standard" field MUST contain the actual standard
    from the supplied document.

11. Explain clearly why the code violates the standard.

12. Provide a practical recommendation to fix the violation.

13. Do not report general PL/SQL best practices unless
    they are explicitly present in the supplied standards.

14. Do not modify or rewrite the supplied source code.

15. If there are no violations, return an empty findings array.

=========================
PL/SQL STANDARDS
=========================

{standards_text}


=========================
PL/SQL CODE
=========================

{code}

Review the code now.
"""

    return prompt