import sqlite3
import os
from shutil import copy2
import datetime
import db

#creating backup of db each time interact.py is run
NUM_BACKUPS = 10
BACKUP_DIR = "./backups/"


if 'backups' not in os.listdir():
    os.mkdir(BACKUP_DIR)
if 'questions.db' in os.listdir():
    
    #https://stackoverflow.com/questions/47739262/find-remove-oldest-file-in-directory
    #removes oldest file if NUM_BACKUPS threshold is reached
    backup_list = os.listdir(BACKUP_DIR)
    if len(backup_list) >= NUM_BACKUPS:
        oldest_backup = min(backup_list)
        os.remove(os.path.abspath(BACKUP_DIR + oldest_backup))

    copy2('./questions.db', BACKUP_DIR)
    os.rename(BACKUP_DIR + 'questions.db', 
              BACKUP_DIR + 'questions' + str(datetime.datetime.now())[:19].replace(' ', '_') + '.db')

    con = sqlite3.connect('questions.db')
    cur = con.cursor()

#else create db and questions table
else:
    con = sqlite3.connect('questions.db')
    cur = con.cursor()
    #sqlite3 doesn't have date/time data types, last_modified is stored as int (unix time)
    cur.execute('''CREATE TABLE IF NOT EXISTS Questions
                   (volume INTEGER, maintopic INTEGER, subtopic INTEGER, question INTEGER,
                    count INTEGER, last_modified INTEGER, notes TEXT,
                    PRIMARY KEY (volume, maintopic, subtopic, question));
    ''')
    con.commit()
    

os.system('clear')
print('''           ____       _        ___                  __ _               
          / ___| __ _| |_ ___ / _ \__   _____ _ __ / _| | _____      __
         | |  _ / _` | __/ _ \ | | \ \ / / _ \ '__| |_| |/ _ \ \ /\ / /
         | |_| | (_| | ||  __/ |_| |\ V /  __/ |  |  _| | (_) \ V  V / 
          \____|\__,_|\__\___|\___/  \_/ \___|_|  |_| |_|\___/ \_/\_/  
                                                                       
''')

