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

CREATE TABLE SystemClassification
(
    system_classification_id INTEGER PRIMARY KEY AUTOINCREMENT,
    system_name TEXT,
    tier INTEGER
);

CREATE TABLE Incident
(
    incident_id INTEGER PRIMARY KEY AUTOINCREMENT,
    author INTEGER REFERENCES User(user_id),
    title TEXT,
    description TEXT,
    sla_identification_deadline DATETIME,
    sla_implementation_deadline DATETIME,
    status INTEGER REFERENCES Stage(stage_id),
    system INTEGER REFERENCES SystemClasification(system_clasification_id),
    impact INTEGER REFERENCES Impact(impact_id),
    priority INTEGER REFERENCES Priority(priority_id),
    date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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
    username TEXT,
    password TEXT,
    role INTEGER REFERENCES Role(role_id) 
);

CREATE TABLE UserSession
(
    user_session_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER REFERENCES User(user_id) ,
    session_start TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    session_end TIMESTAMP
);

CREATE TABLE Team
(
    team_id INTEGER PRIMARY KEY AUTOINCREMENT,
    team_name TEXT,
    department_id INTEGER REFERENCES Department(department_id)
);

CREATE TABLE UserTeam
(
    user_team_id INTEGER PRIMARY KEY AUTOINCREMENT,
    team_id INTEGER REFERENCES Team(team_id),
    user_id INTEGER REFERENCES User(user_id) 
);

CREATE TABLE TaskTeamAssignment
(
    task_team_assignment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    team_id INTEGER REFERENCES Team(team_id),
    task_id INTEGER REFERENCES Task(task_id) 
);

CREATE TABLE TaskTeamAssignmentRequest
(
    task_team_assignment_request_id INTEGER PRIMARY KEY AUTOINCREMENT,
    team_id INTEGER REFERENCES Team(team_id),
    task_id INTEGER REFERENCES Task(task_id),
    request_issuer INTEGER REFERENCES User(user_id),
    approved BOOLEAN
);

CREATE TABLE IncidentTeamAssignmentRequest
(
    team_id INTEGER REFERENCES Team(team_id),
    incident_id INTEGER REFERENCES Incident(incident_id),
    request_issuer INTEGER REFERENCES User(user_id),
    approved BOOLEAN,
    date_issued TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (team_id, incident_id)
);

CREATE TABLE IncidentTeamAssignment
(
    team_id INTEGER REFERENCES Team(team_id),
    incident_id INTEGER REFERENCES Incident(incident_id),
    PRIMARY KEY (team_id, incident_id)
);
