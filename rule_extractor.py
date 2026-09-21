from models import StandardRule


def extract_rules(content):
    rules = []
    rule_number = 1

    current_section = "General"

    section_names = [
        "Naming Conventions",
        "Formatting & Layout",
        "Data Types & Declarations",
        "SQL & Collection Operations",
        "Exception & Error Handling",
        "Performance & Compiler Enhancements",
        "Security & Code Integrity"
    ]

    for item in content:

        # --------------------------------------------------
        # PARAGRAPHS
        # --------------------------------------------------

        if item["type"] == "paragraph":

            text = item["text"].strip()

            if not text:
                continue

            # Detect section
            for section in section_names:
                if section in text:
                    current_section = section
                    break

            # Ignore section headings
            if text in section_names:
                continue

            # Ignore document title
            if text.startswith("PL/SQL Coding Standards"):
                continue

            # Ignore obvious explanatory text
            if (
                text.startswith("Consistent naming conventions")
                or text.startswith("sql")
                or text == "Use code with caution."
            ):
                continue

            # --------------------------------------------------
            # Detect bullet-style standards
            # --------------------------------------------------

            cleaned_text = text

            # Remove common bullet characters
            for bullet in ["-", "•", "–", "—"]:
                if cleaned_text.startswith(bullet):
                    cleaned_text = cleaned_text[1:].strip()

            # Detect cursor rule
            if (
                "Explicit cursors must be closed"
                in cleaned_text
            ):
                rule = StandardRule(
                    id=f"DOC-{rule_number:03d}",
                    section=current_section,
                    title="Cursor Management",
                    severity="MEDIUM",
                    standard=cleaned_text
                )

                rules.append(rule)
                rule_number += 1
                continue

            # Detect other meaningful standards
            # starting with common rule indicators.
            if any(
                cleaned_text.lower().startswith(prefix)
                for prefix in [
                    "tables:",
                    "packages:",
                    "file architecture:",
                    "case consistency:",
                    "indentation:",
                    "block labels:",
                    "anchored declarations:",
                    "native arithmetic:",
                    "string character semantics:",
                    "boolean evaluations:",
                    "bulk processing:",
                    "19c qualified expressions:",
                    "explicit column lists:",
                    "no blank handlers:",
                    "centralized logging:",
                    "modern diagnostic tracking:",
                    "udf pragma:",
                    "nocopy hint:",
                    "compiler optimization level:",
                    "dynamic sql binding:",
                    "privilege control:"
                ]
            ):
                rule = StandardRule(
                    id=f"DOC-{rule_number:03d}",
                    section=current_section,
                    title=cleaned_text.split(":")[0].strip(),
                    severity="MEDIUM",
                    standard=cleaned_text
                )

                rules.append(rule)
                rule_number += 1

                continue

        # --------------------------------------------------
        # TABLES
        # --------------------------------------------------

        if item["type"] == "table":

            rows = item["rows"]

            if not rows:
                continue

            header = [
                cell.strip().lower()
                for cell in rows[0]
            ]

            if (
                "prefix" in header
                and "scope / type" in header
            ):

                for row in rows[1:]:

                    if len(row) < 2:
                        continue

                    prefix = row[0].strip()
                    scope = row[1].strip()

                    example = ""

                    if len(row) >= 3:
                        example = row[2].strip()

                    if not prefix or not scope:
                        continue

                    standard_text = (
                        f"{scope} must use the "
                        f"'{prefix}' prefix."
                    )

                    if example:
                        standard_text += (
                            f" Example: {example}"
                        )

                    rule = StandardRule(
                        id=f"DOC-{rule_number:03d}",
                        section=current_section,
                        title=f"{scope} Naming",
                        severity="MEDIUM",
                        standard=standard_text
                    )

                    rules.append(rule)
                    rule_number += 1

    return rules