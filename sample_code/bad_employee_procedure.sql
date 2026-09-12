CREATE OR REPLACE PROCEDURE update_employee_salary (
    p_employee_id NUMBER,
    p_new_salary NUMBER
)
AS
    employee_name VARCHAR2(100);
BEGIN

    SELECT *
    INTO employee_name
    FROM employees
    WHERE employee_id = employee_id;

    UPDATE employees
    SET salary = new_salary
    WHERE employee_id = employee_id;

EXCEPTION
    WHEN OTHERS THEN NULL;

END;
/