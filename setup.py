import sqlite3

con = sqlite3.connect(".db")
cur=con.cursor()

cur.execute("CREATE TABLE implants (\
    id INTEGER PRIMARY KEY ,\
    register_date DATETIME,\
    last_seen DATETIME,\
    os VARCHAR(20),\
    domain VARCHAR(20),\
    hostname VARCHAR(20)\
);")

cur.execute("CREATE TABLE actions (\
    id INTEGER PRIMARY KEY ,\
    date DATETIME,\
    action_type INT,\
    content VARCHAR(100),\
    implant_id INT,\
    FOREIGN KEY (implant_id) REFERENCES implants(id)\
);")


cur.execute("CREATE TABLE tasks (\
    id INTEGER PRIMARY KEY ,\
    author VARCHAR(20),\
    link VARCHAR(50),\
    content VARCHAR(500),\
    tags VARCHAR(30)\
);")

cur.execute("CREATE TABLE implant_task (\
    id INTEGER PRIMARY KEY ,\
    implant_id INT ,\
    task_id INT,\
    date DATETIME,\
    executed BOOLEAN,\
    FOREIGN KEY (implant_id) REFERENCES implants(id),\
    FOREIGN KEY (task_id) REFERENCES tasks(id)\
);")