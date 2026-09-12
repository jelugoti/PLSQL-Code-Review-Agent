CREATE OR REPLACE PROCEDURE update_employee_salary (
    p_employee_id NUMBER,
    p_new_salary  NUMBER
)
AS
    l_employee_name employee.employee_name%TYPE;
BEGIN

    SELECT employee_name
    INTO l_employee_name
    FROM employee
    WHERE employee_id = p_employee_id;

EXCEPTION
    WHEN NO_DATA_FOUND THEN
        RAISE_APPLICATION_ERROR(
            -20001,
            'Employee not found: ' || p_employee_id
        );

    WHEN TOO_MANY_ROWS THEN
        RAISE_APPLICATION_ERROR(
            -20002,
            'Multiple employees found for ID: ' || p_employee_id
        );
END;
/