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
    
