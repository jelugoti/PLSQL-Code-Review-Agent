CREATE OR REPLACE PROCEDURE process_employees (
    p_department_id NUMBER
)
AS

    CURSOR cur_employees IS
        SELECT employee_id,
               first_name
        FROM employees
        WHERE department_id = p_department_id;

    l_employee_id employees.employee_id%TYPE;
    l_employee_name employees.first_name%TYPE;

BEGIN

    OPEN cur_employees;

    LOOP

        FETCH cur_employees
        INTO l_employee_id,
             l_employee_name;

        EXIT WHEN cur_employees%NOTFOUND;

        DBMS_OUTPUT.PUT_LINE(
            l_employee_name
        );

    END LOOP;

END process_employees;
/