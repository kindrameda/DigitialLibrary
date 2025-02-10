show databases;
create database test;
use test;
show tables;
create table testtable(Name varchar(100), Date int);
insert into testtable (Name, Date) values('Urvashi', 0906);
insert into testtable (Name, Date) values('Kindra', 2403);
select * from testtable;
CREATE TABLE students (
ID INT AUTO_INCREMENT PRIMARY KEY,
Name VARCHAR(255),
Score DECIMAL(5, 2)
);
INSERT INTO students (Name, Score) VALUES
('John Doe', 85.5),
('Jane Smith', 92.0),
('Alice Johnson', 78.3),
('Bob Williams', 90.2),
('Emily Brown', 88.7),
('Michael Davis', 79.8),
('Sarah Wilson', 87.1),
('James Taylor', 91.5),
('Emma Martinez', 82.4),
('Matthew Thompson', 94.6),
('Olivia Garcia', 76.9),
('David Hernandez', 83.2),
('Sophia Lopez', 89.3),
('Daniel Hill', 85.7),
('Isabella Scott', 93.8),
('Alexander Green', 81.2),
('Mia Adams', 87.9),
('Ethan Baker', 90.4),
('Chloe Hall', 84.6),
('William King', 88.1);
select * from students;
select * from students where Score > 90;
select * from students where Score between 80 and 90;
select * from students order by Score desc;
select count(*) as TotalStudents from students;
select count(*) as From80to90 from students where Score between 80 and 90;
select avg(Score) from students;
select max(Score) from students;
select min(Score) from students;
SET SQL_SAFE_UPDATES = 0;
update Students set Score = 100 where name = 'John Doe';
select * from students;
delete from students where name = "Bob Williams";
select * from students order by Score desc limit 5;
select * from students where name like 'J%';
select * from students where name like '%son';
select * from students order by Score desc limit 1;
select * from students where name like '%son' order by Score desc limit 1;
select sum(Score) from students;
update Students set Score = Score+5;
select avg(Score) from Students;
select * from students where Score > (select avg(Score) from Students);  
select max(Score) from Students;
select * from students where Score < (select max(Score) from Students) order by Score desc limit 3;
select sum(Score) from students where name like 'M%';
select max(Score), min(Score), avg(Score) from Students;
-- List the bottom 5 students with the lowest scores.
select * from students order by Score limit 5;

-- Display students sorted alphabetically by their names.
select * from students order by Name;

-- Find the students who scored the second-highest score.
select * from students where Score < (select max(Score) from students) order by Score desc limit 1;

-- Update the scores of students whose names start with "J" by adding 10 points.
update Students set Score = Score + 10 where name like "J%";

-- Delete all students with scores below 50. 
delete from students where Score < 50;

update book set status = 'read' where title = %s