import sqlite3

con = sqlite3.connect(".db")
cur=con.cursor()

cur.execute("CREATE TABLE implants (\
    id INT AUTO_INCREMENT PRIMARY KEY ,\
    register_date DATETIME,\
    last_seen DATETIME,\
    os VARCHAR(20),\
    domain VARCHAR(20),\
    hostname VARCHAR(20)\
);")

cur.execute("CREATE TABLE actions (\
    action_id INT AUTO_INCREMENT PRIMARY KEY ,\
    date DATETIME,\
    action_type INT,\
    content VARCHAR(100),\
    implant_id INT,\
    FOREIGN KEY (implant_id) REFERENCES implants(id)\
);")


cur.execute("CREATE TABLE tasks (\
    task_id INT AUTO_INCREMENT PRIMARY KEY ,\
    author VARCHAR(20),\
    link VARCHAR(50),\
    content VARCHAR(200),\
    tags VARCHAR(30)\
);")