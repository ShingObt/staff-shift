CREATE ROLE manager LOGIN PASSWORD 'password';

CREATE DATABASE staff_shift;

\c staff_shift

CREATE TABLE staffs (
	staff_id CHAR(6) NOT NULL,
	nickname TEXT NOT NULL,
	PRIMARY KEY (staff_id)
);
ALTER TABLE staffs OWNER TO manager;

CREATE TABLE shifts (
	day DATE NOT NULL,
	staff_id CHAR(6) NOT NULL,
	start_time TIME NOT NULL,
	end_time TIME NOT NULL,
	PRIMARY KEY (day, staff_id)
);
ALTER TABLE shifts ADD FOREIGN KEY (staff_id) REFERENCES staffs (staff_id);
ALTER TABLE shifts OWNER TO manager;
