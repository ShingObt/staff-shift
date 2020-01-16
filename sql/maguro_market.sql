CREATE ROLE maguro LOGIN PASSWORD 'password';

CREATE DATABASE maguro_market OWNER maguro;

\c maguro_market

CREATE TABLE employees (
	employee_id CHAR(6) NOT NULL,
	nickname TEXT NOT NULL,
	PRIMARY KEY (employee_id)
);
ALTER TABLE employees OWNER TO maguro;

CREATE TABLE shifts (
	day DATE NOT NULL,
	employee_id CHAR(6) NOT NULL,
	start_time TIME NOT NULL,
	end_time TIME NOT NULL,
	PRIMARY KEY (day, employee_id)
);
ALTER TABLE shifts ADD FOREIGN KEY (employee_id) REFERENCES employees (employee_id);
ALTER TABLE shifts OWNER TO maguro;
