CREATE TABLE IF NOT EXISTS Impact
(
    impact_id INTEGER PRIMARY KEY AUTOINCREMENT,
    impact_level INTEGER
);

CREATE TABLE IF NOT EXISTS Priority
(
    priority_id INTEGER PRIMARY KEY AUTOINCREMENT,
    priority_code TEXT
);

CREATE TABLE IF NOT EXISTS Stage
(
    stage_id INTEGER PRIMARY KEY AUTOINCREMENT,
    stage_level TEXT
);

CREATE TABLE IF NOT EXISTS SystemClassification
(
    system_classification_id INTEGER PRIMARY KEY AUTOINCREMENT,
    system_name TEXT,
    tier INTEGER
);

CREATE TABLE IF NOT EXISTS Incident
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

CREATE TABLE IF NOT EXISTS Note
(
    note_id INTEGER PRIMARY KEY AUTOINCREMENT,
    note_title TEXT,
    date_created DATETIME,
    note_content TEXT
);

CREATE TABLE IF NOT EXISTS Role
(
    role_id INTEGER PRIMARY KEY AUTOINCREMENT,
    role_name TEXT,
    is_customer_facing BOOLEAN
);

CREATE TABLE IF NOT EXISTS Department
(
    department_id INTEGER PRIMARY KEY AUTOINCREMENT,
    department_name TEXT
);

CREATE TABLE IF NOT EXISTS Task
(
    task_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    content TEXT
);

CREATE TABLE IF NOT EXISTS IncidentValueChangeRequest
(
    change_request_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER REFERENCES User(user_id) ,
    incident_id INTEGER REFERENCES Incident(incident_id) ,
    old_value INTEGER,
    new_value INTEGER,
    value_type INTEGER,
    justification TEXT,
    status INTEGER DEFAULT -1,
    date_requested TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS Follow
(
    follow_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER REFERENCES User(user_id) ,
    incident_id INTEGER REFERENCES Incident(incident_id) 
);

CREATE TABLE IF NOT EXISTS Notification
(
    notification_id INTEGER PRIMARY KEY AUTOINCREMENT,
    notification_content TEXT,
    date_issued DATETIME,
    incident_id INTEGER REFERENCES Incident(incident_id) 
);

CREATE TABLE IF NOT EXISTS UserNotification
(
    user_notification_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER REFERENCES User(user_id) ,
    notification_id INTEGER REFERENCES Notification(notification_id) 
);

CREATE TABLE IF NOT EXISTS Question
(
    questiond_id INTEGER PRIMARY KEY AUTOINCREMENT,
    issuer INTEGER REFERENCES User(user_id) ,
    question_title TEXT,
    date_created DATETIME,
    question_content TEXT
);

CREATE TABLE IF NOT EXISTS Answer
(
    answer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    question_id INTEGER REFERENCES Question(question_id) ,
    answerer INTEGER REFERENCES User(user_id) ,
    answer_content TEXT
);

CREATE TABLE IF NOT EXISTS User
(
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    forename TEXT,
    surname TEXT,
    email TEXT,
    username TEXT,
    password TEXT,
    role INTEGER REFERENCES Role(role_id) 
);

CREATE TABLE IF NOT EXISTS UserSession
(
    user_session_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER REFERENCES User(user_id) ,
    session_start TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    session_end TIMESTAMP
);

CREATE TABLE IF NOT EXISTS Team
(
    team_id INTEGER PRIMARY KEY AUTOINCREMENT,
    team_name TEXT,
    department_id INTEGER REFERENCES Department(department_id)
);

CREATE TABLE IF NOT EXISTS UserTeam
(
    user_team_id INTEGER PRIMARY KEY AUTOINCREMENT,
    team_id INTEGER REFERENCES Team(team_id),
    user_id INTEGER REFERENCES User(user_id) 
);

CREATE TABLE IF NOT EXISTS TaskTeamAssignment
(
    task_team_assignment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    team_id INTEGER REFERENCES Team(team_id),
    task_id INTEGER REFERENCES Task(task_id) 
);

CREATE TABLE IF NOT EXISTS TaskTeamAssignmentRequest
(
    team_id INTEGER REFERENCES Team(team_id),
    task_id INTEGER REFERENCES Task(task_id),
    request_issuer INTEGER REFERENCES User(user_id),
    approved BOOLEAN,
    date_issued TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (team_id, task_id)
);

CREATE TABLE IF NOT EXISTS IncidentTeamAssignmentRequest
(
    team_id INTEGER REFERENCES Team(team_id),
    incident_id INTEGER REFERENCES Incident(incident_id),
    request_issuer INTEGER REFERENCES User(user_id),
    status INTEGER,
    date_issued TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (team_id, incident_id)
);

CREATE TABLE IF NOT EXISTS IncidentTeamAssignment
(
    team_id INTEGER REFERENCES Team(team_id),
    incident_id INTEGER REFERENCES Incident(incident_id),
    PRIMARY KEY (team_id, incident_id)
);
