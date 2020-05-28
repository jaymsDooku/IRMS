--CREATE scripts

CREATE TABLE Impact
(
    impact_id INTEGER PRIMARY KEY AUTOINCREMENT,
    impact_level INTEGER
);

CREATE TABLE Priority
(
    priority_id INTEGER PRIMARY KEY AUTOINCREMENT,
    priority_code TEXT
);

CREATE TABLE Stage
(
    stage_id INTEGER PRIMARY KEY AUTOINCREMENT,
    stage_level TEXT
);

CREATE TABLE SystemClasification
(
    system_clasification_id INTEGER PRIMARY KEY AUTOINCREMENT,
    syste_name TEXT,
    tier INTEGER
);

CREATE TABLE Incident
(
    incident_id INTEGER PRIMARY KEY AUTOINCREMENT,
    author INTEGER REFERENCES User(user_id)
    title TEXT,
    desciption TEXT,
    sla_resolution_identification_time_frame NUMERIC,
    sla_resolution_implementation_time_frame NUMERIC,
    status INTEGER REFERENCES Stage(stage_id) ,
    system INTEGER REFERENCES SystemClasification(system_clasification_id) ,
    impact INTEGER REFERENCES Impact(impact_id) ,
    priority INTEGER REFERENCES Priority(priority_id) ,
    date_created DATETIME
);

CREATE TABLE Note
(
    note_id INTEGER PRIMARY KEY AUTOINCREMENT,
    note_title TEXT,
    date_created DATETIME,
    note_content TEXT
);

CREATE TABLE Role
(
    role_id INTEGER PRIMARY KEY AUTOINCREMENT,
    role_name TEXT,
    is_customer_facing BOOLEAN
);

CREATE TABLE Department
(
    department_id INTEGER PRIMARY KEY AUTOINCREMENT,
    department_name TEXT
);

CREATE TABLE Task
(
    task_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    content TEXT
);

CREATE TABLE IncidentValueChangeRequest
(
    incident_priority_change_request_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER REFERENCES User(user_id) ,
    incident_id INTEGER REFERENCES Incident(incident_id) ,
    old_level INTEGER,
    new_level INTEGER,
    value_type INTEGER,
    justification TEXT,
    approved BOOLEAN
    
);

CREATE TABLE Follow
(
    follow_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER REFERENCES User(user_id) ,
    incident_id INTEGER REFERENCES Incident(incident_id) 
);

CREATE TABLE Notification
(
    notification_id INTEGER PRIMARY KEY AUTOINCREMENT,
    notification_content TEXT,
    date_issued DATETIME,
    incident_id INTEGER REFERENCES Incident(incident_id) 
);

CREATE TABLE UserNotification
(
    user_notification_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER REFERENCES User(user_id) ,
    notification_id INTEGER REFERENCES Notification(notification_id) 
);

CREATE TABLE Question
(
    questiond_id INTEGER PRIMARY KEY AUTOINCREMENT,
    issuer INTEGER REFERENCES User(user_id) ,
    question_title TEXT,
    date_created DATETIME,
    question_content TEXT
);

CREATE TABLE Answer
(
    answer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    question_id INTEGER REFERENCES Question(question_id) ,
    answerer INTEGER REFERENCES User(user_id) ,
    answer_content TEXT
);

CREATE TABLE User
(
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    forename TEXT,
    surname TEXT,
    email TEXT,
    user_title TEXT,
    role INTEGER REFERENCES Role(role_id) 
);

CREATE TABLE UserSession
(
    user_session_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER REFERENCES User(user_id) ,
    session_start DATETIME,
    session_end DATETIME
);

CREATE TABLE Team
(
    team_id INTEGER PRIMARY KEY AUTOINCREMENT,
    team_name TEXT,
    department_id INTEGER REFERENCES Department(department_id) ,
);

CREATE TABLE UserTeam
(
    user_team_id INTEGER PRIMARY KEY AUTOINCREMENT,
    team_id INTEGER REFERENCES Team(team_id) ,
    user_id INTEGER REFERENCES User(user_id) 
);

CREATE TABLE TaskTeamAssignment
(
    task_team_assignment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    team_id INTEGER REFERENCES Team(team_id) ,
    task_id INTEGER REFERENCES Task(task_id) 
);

CREATE TABLE TaskTeamAssignmentRequest
(
    task_team_assignment_request_id INTEGER PRIMARY KEY AUTOINCREMENT,
    team_id INTEGER REFERENCES Team(team_id) ,
    task_id INTEGER REFERENCES Task(task_id) ,
    request_issuer INTEGER REFERENCES Users(user_id) ,
    approved BOOLEAN
);

CREATE TABLE IncidentTeamAssignmentRequest
(
    incident_team_assignment_request_id INTEGER PRIMARY KEY AUTOINCREMENT,
    team_id INTEGER REFERENCES Team(team_id) ,
    incident_id INTEGER REFERENCES Incident(incident_id) ,
    request_issuer INTEGER REFERENCES User(user_id) ,
    approved BOOLEAN
);

CREATE TABLE IncidentTeamAssignment
(
    incident_assignment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    team_id INTEGER REFERENCES Team(team_id) ,
    incident_id INTEGER REFERENCES Incident(incident_id) 
);


--DROP scripts--

DROP TABLE Impact
DROP TABLE Priority
DROP TABLE Stage
DROP TABLE SystemClasification
DROP TABLE Role
DROP TABLE Note
DROP TABLE Department
DROP TABLE Task
DROP TABLE Notification
DROP TABLE Question
DROP TABLE User
DROP TABLE UserSession
DROP TABLE Team
DROP TABLE Incident
DROP TABLE IncidentValueChangeRequest
DROP TABLE Follow
DROP TABLE UserNotification
DROP TABLE Answer
DROP TABLE UserTeam
DROP TABLE TaskTeamAssignment
DROP TABLE TaskTeamAssignmentRequest
DROP TABLE IncidentTeamAssignmentRequest
DROP TABLE IncidentTeamAssignment

--INSERT scripts

--User,Role,Team, Department

--User
INSERT INTO Role(role_id,role_name,is_customer_facing)
VALUES
(1,"Service Desk", True),
(2,"Queue Manager", FALSE),
(3,"technician", FALSE),
(4,"User", FALSE),
(5,"Resolver", FALSE),
(6,"Major Incident Response Manager", TRUE)

INSERT INTO User(user_id,forename,surname,email,user_title,role)
VALUES
(1,"Joe","Biden","JB@email.com","Service Desk", 1),
(2,"Donald","Duck","DoubleD@email.com","Queue Manager", 2),
(3,"Boris","Johnson","BJob@email.com","Technician", 3),
(4,"Frederick","William","TheGreat@email.com","User", 4),
(5,"Jim","Boston","AgainJ@email.com","Resolver", 5),
(6,"Alice","Wonderfill","AliceWhere@email.com","Major Incident Response Manager", 6)

INSERT INTO Department(department_id,department_name)
VALUES
(1,"General Management"),
(2,"Sales"),
(3,"Human Resource"),
(4,"IT Support")

INSERT INTO Team(team_id,team_name, department_id)
VALUES
(1,"Marketing Team",1),
(2,"Sales Team",1),
(3,"Finance Team",1),
(4,"Administration Team",2),
(5,"Sales Representataives Team",2),
(6,"Sales Development Reps Team",2),
(7,"HR Coordination Team",3),
(8,"HR Recruit Team",3),
(9,"HR Specialist Team",3),
(10,"Incident Response Team",4),
(11,"Development Team",4),
(12,"Maintenance Team",4)