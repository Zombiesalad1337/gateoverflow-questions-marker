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
    #sqlite3 doesn't have date/time data types, last_modified is stored as text (YYYY-MM-DD HH:MM:SS.SSS)
    cur.execute('''CREATE TABLE IF NOT EXISTS Questions
                   (volume INTEGER, maintopic INTEGER, subtopic INTEGER, question INTEGER,
                    count INTEGER DEFAULT 1, last_modified TEXT DEFAULT datetime('now', 'localtime'),
                    notes TEXT DEFAULT '',
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

exited = False
while (not exited):

    print("1. Mark important questions")
    print("2. View marked questions")
    print("3. Exit")
    choice1 = int(input("Enter your choice:\t"))

    #add error handling, range of inputs
    if choice1 == 1:
        inputs = db.insert_question(cur)
        con.commit()
        while (True):
            print("1. Add a short note for the added question")
            print("2. Go back")
            choice11 = int(input("Enter your choice:\t"))
            
            if choice11 == 1:
                db.insert_note(cur, inputs)
                con.commit()
                print("Note added")
            if choice11 == 2:
                break
        

    if choice1 == 2:
        print("1. View a marked question") #add option to insert note
        print("2. View all marked questions - volume wise")
        print("3. View all marked questions - sort by latest")
        print("4. View all marked questions - sort by count")
        print("5. Go back")

    if choice1 == 3:
        con.close()
        exit()


