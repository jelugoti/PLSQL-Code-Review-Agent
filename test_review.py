from standards_reader import read_standards_document
from rule_extractor import extract_rules
from llm_client import LLMClient
from reviewer import review_code
import config


# -------------------------------------------------
# 1. Read standards document
# -------------------------------------------------

standards_file = config.standards_file

content = read_standards_document(
    standards_file
)


# -------------------------------------------------
# 2. Extract structured rules
# -------------------------------------------------

standards = extract_rules(
    content
)


# -------------------------------------------------
# 3. Create LLM client
# -------------------------------------------------

llm_client = LLMClient()


# -------------------------------------------------
# 4. Sample PL/SQL
# -------------------------------------------------

plsql_code = """
CREATE OR REPLACE PROCEDURE update_employee (
    p_employee_id NUMBER
)
AS

    l_employee_name VARCHAR2(100);
    l_bad_count NUMBER;

BEGIN

    SELECT *
    INTO employee_name
    FROM employees
    WHERE employee_id = employee_id;

EXCEPTION

    WHEN OTHERS THEN
        NULL;

END update_employee;
/
"""


# -------------------------------------------------
# 5. Review code
# -------------------------------------------------

result = review_code(
    plsql_code,
    standards,
    llm_client
)


# -------------------------------------------------
# 6. Display result
# -------------------------------------------------

print("\n")
print("=" * 70)
print("PL/SQL CODE REVIEW RESULT")
print("=" * 70)

print("\nSUMMARY")
print("-" * 70)

print(result["summary"])


print("\nFINDINGS")
print("-" * 70)

for finding in result["findings"]:

    print(f"\nRule ID     : {finding['rule_id']}")
    print(f"Category    : {finding['category']}")
    print(f"Severity    : {finding['severity']}")
    print(f"Title       : {finding['title']}")
    print(f"Line        : {finding['line']}")
    print(f"Code        : {finding['code']}")
    print(f"Message     : {finding['message']}")
    print(f"Standard    : {finding['standard']}")
    print(
        f"Recommendation: "
        f"{finding['recommendation']}"
    )