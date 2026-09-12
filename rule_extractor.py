from models import StandardRule


def extract_rules(content):

    rules = []

    rule_number = 1
    current_section = "General"

    for item in content:

        # ==================================================
        # Paragraph
        # ==================================================

        if item["type"] == "paragraph":

            text = item["text"].strip()

            # Detect major sections
            if "Naming Conventions" in text:
                current_section = "Naming Conventions"

            elif "Formatting & Layout" in text:
                current_section = "Formatting & Layout"

            elif "Data Types & Declarations" in text:
                current_section = "Data Types & Declarations"

            elif "SQL & Collection Operations" in text:
                current_section = "SQL & Collection Operations"

            elif "Exception & Error Handling" in text:
                current_section = "Exception & Error Handling"

            elif "Performance & Compiler Enhancements" in text:
                current_section = "Performance & Compiler Enhancements"

            elif "Security & Code Integrity" in text:
                current_section = "Security & Code Integrity"

            continue


        # ==================================================
        # Table
        # ==================================================

        if item["type"] == "table":

            rows = item["rows"]

            if not rows:
                continue


            # ------------------------------------------------
            # Get table header
            # ------------------------------------------------

            header = [
                cell.strip().lower()
                for cell in rows[0]
            ]


            # ------------------------------------------------
            # Naming prefix table
            # ------------------------------------------------

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


                    # Build standard description

                    standard_text = (
                        f"{scope} must use the "
                        f"'{prefix}' prefix."
                    )


                    if example:

                        standard_text += (
                            f" Example: {example}"
                        )


                    # Create rule

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