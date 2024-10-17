-- SQL script that creates a view need_meeting that lists all students that have a score under 80 (strict) and no last_meeting or more than 1 month.
CREATE VIEW need_meeting AS SELECT name FROM students s WHERE s.score < 80
AND (s.last_meeting IS  NUll OR s.last_meeting <  NOW() - INTERVAL 1 MONTH);
