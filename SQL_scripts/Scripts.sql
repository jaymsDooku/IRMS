--CREATE scripts

CREATE TABLE Incident
(
    incident_id INTEGER PRIMARY KEY,
    title TEXT,
    desciption TEXT,
    sla_resolution_identification_time_frame NUMERIC,
    sla_resolution_implementation_time_frame NUMERIC,
    status INTEGER REFERENCES Stage(stage_id) DEFERRABLE INITIALLY DEFERRED,
    system INTEGER REFERENCES SystemClasification(system_clasification_id) DEFERRABLE INITIALLY DEFERRED,
    impact INTEGER REFERENCES Impact(impact_id) DEFERRABLE INITIALLY DEFERRED,
    priority INTEGER REFERENCES Priority(priority_id) DEFERRABLE INITIALLY DEFERRED,
    date_created DATETIME
);

CREATE TABLE Impact
(
    impact_id INTEGER PRIMARY KEY,
    impact_level INTEGER
);

CREATE TABLE Priority
(
    priority_id INTEGER PRIMARY KEY,
    priority_code TEXT
);

CREATE TABLE Stage
(
    stage_id INTEGER PRIMARY KEY,
    stage_level TEXT
);

CREATE TABLE SystemClasification
(
    system_clasification_id INTEGER PRIMARY KEY,
    syste_name TEXT,
    tier INTEGER
);

CREATE TABLE IncidentValueChangeRequest
(
    incident_priority_change_request_id INTEGER PRIMARY KEY,
    user_id INTEGER REFERENCES User(user_id) DEFERRABLE INITIALLY DEFERRED,
    incident_id INTEGER REFERENCES Incident(incident_id) DEFERRABLE INITIALLY DEFERRED,
    old_level INTEGER,
    new_level INTEGER,
    value_type INTEGER,
    justification TEXT,
    approved BOOLEAN
    
);

CREATE TABLE Follow
(
    follow_id INTEGER PRIMARY KEY,
    user_id INTEGER REFERENCES User(user_id) DEFERRABLE INITIALLY DEFERRED,
    incident_id INTEGER REFERENCES Incident(incident_id) DEFERRABLE INITIALLY DEFERRED
);

CREATE TABLE Notification
(
    notification_id INTEGER PRIMARY KEY,
    notification_content TEXT,
    date_issued DATETIME,
    incident_id INTEGER REFERENCES Incident(incident_id) DEFERRABLE INITIALLY DEFERRED
);

CREATE TABLE UserNotification
(
    user_notification_id INTEGER PRIMARY KEY,
    user_id INTEGER REFERENCES User(user_id) DEFERRABLE INITIALLY DEFERRED,
    notification_id INTEGER REFERENCES Notification(notification_id) DEFERRABLE INITIALLY DEFERRED
);

CREATE TABLE Note
(
    note_id INTEGER PRIMARY KEY,
    note_title TEXT,
    date_created DATETIME,
    note_content TEXT
);

CREATE TABLE Question
(
    questiond_id INTEGER PRIMARY KEY,
    issuer INTEGER REFERENCES User(user_id) DEFERRABLE INITIALLY DEFERRED,
    question_title TEXT,
    date_created DATETIME,
    question_content TEXT
);

CREATE TABLE Answer
(
    answer_id INTEGER PRIMARY KEY,
    question_id INTEGER REFERENCES Question(question_id) DEFERRABLE INITIALLY DEFERRED,
    answerer INTEGER REFERENCES User(user_id) DEFERRABLE INITIALLY DEFERRED,
    answer_content TEXT
);

CREATE TABLE User
(
    user_id INTEGER PRIMARY KEY,
    forename TEXT,
    surname TEXT,
    email TEXT,
    user_title TEXT,
    role INTEGER REFERENCES Role(role_id) DEFERRABLE INITIALLY DEFERRED
);

CREATE TABLE UsersSession
(
    user_session_id INTEGER PRIMARY KEY,
    user_id INTEGER REFERENCES User(user_id) DEFERRABLE INITIALLY DEFERRED,
    session_start DATETIME,
    session_end DATETIME
);

CREATE TABLE Role
(
    role_id INTEGER PRIMARY KEY,
    role_name TEXT,
    is_customer_facing BOOLEAN
);

CREATE TABLE Team
(
    team_id INTEGER PRIMARY KEY,
    team_name TEXT,
    department_id INTEGER REFERRENCES Department(department_id) DEFERRABLE INITIALLY DEFERRED,
);

CREATE TABLE UserTeam
(
    user_team_id INTEGER PRIMARY KEY,
    team_id INTEGER REFERENCES Team(team_id) DEFERRABLE INITIALLY DEFERRED,
    user_id INTEGER REFERENCES User(user_id) DEFERRABLE INITIALLY DEFERRED
);

CREATE TABLE Department
(
    department_id INTEGER PRIMARY KEY,
    department_name TEXT
);

CREATE TABLE Task
(
    task_id INTEGER PRIMARY KEY,
    name TEXT,
    content TEXT
);

CREATE TABLE TaskTeamAssignment
(
    task_team_assignment_id INTEGER PRIMARY KEY,
    team_id INTEGER REFERENCES Team(team_id) DEFERRABLE INITIALLY DEFERRED,
    task_id INTEGER REFERENCES Task(task_id) DEFERRABLE INITIALLY DEFERRED
);

CREATE TABLE TaskTeamAssignmentRequest
(
    task_team_assignment_request_id INTEGER PRIMARY KEY,
    team_id INTEGER REFERENCES Team(team_id) DEFERRABLE INITIALLY DEFERRED,
    task_id INTEGER REFERENCES Task(task_id) DEFERRABLE INITIALLY DEFERRED,
    request_issuer INTEGER REFERENCES Users(user_id) DEFERRABLE INITIALLY DEFERRED,
    approved BOOLEAN
);

CREATE TABLE IncidentTeamAssignmentRequest
(
    incident_team_assignment_request_id INTEGER PRIMARY KEY,
    team_id INTEGER REFERENCES Team(team_id) DEFERRABLE INITIALLY DEFERRED,
    incident_id INTEGER REFERENCES Incident(incident_id) DEFERRABLE INITIALLY DEFERRED,
    request_issuer INTEGER REFERENCES User(user_id) DEFERRABLE INITIALLY DEFERRED,
    approved BOOLEAN
);

CREATE TABLE IncidentTeamAssignment
(
    incident_assignment_id INTEGER PRIMARY KEY,
    team_id INTEGER REFERENCES Team(team_id) DEFERRABLE INITIALLY DEFERRED,
    incident_id INTEGER REFERENCES Incident(incident_id) DEFERRABLE INITIALLY DEFERRED
);

--DROP scripts

DROP TABLE User
DROP TABLE UserSession
DROP TABLE UserNotification
DROP TABLE Team
DROP TABLE UserTeam
DROP TABLE Department
DROP TABLE Role
DROP TABLE Task
DROP TABLE TaskTeamAssignment
DROP TABLE TaskTeamAssignmentRequest
DROP TABLE Note
DROP TABLE Question
DROP TABLE Answer
DROP TABLE Incident
DROP TABLE IncidentValueChangeRequest
DROP TABLE IncidentTeamAssignmentRequest
DROP TABLE IncidentTeamAssignment
DROP TABLE Impact
DROP TABLE Priority
DROP TABLE Stage
DROP TABLE SystemClasification

--INSERT scripts