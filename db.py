import sqlite3
from tabulate import tabulate

def insert_question(cur):
    volume = input("Enter volume:\t")
    maintopic = input("Enter maintopic:\t")
    subtopic = input("Enter subtopic:\t")
    question = input("Enter question:\t")

    #check if given question already exists
    cur.execute('''SELECT * 
                   FROM Questions
                   WHERE (volume = ? AND maintopic = ? 
                   AND subtopic = ? AND question = ?);
                ''', (volume, maintopic, subtopic, question))

    rows = cur.fetchall()
    if len(rows) == 0:
        #insert question
        cur.execute('''INSERT INTO Questions (volume, maintopic, subtopic, question)
                    VALUES (?, ?, ?, ?);
                    ''', (volume, maintopic, subtopic, question))
        print('{}-{}-{}-{} question added'.format(volume, maintopic, subtopic, question))
    else:
        #increment count and update datetime
        cur.execute('''UPDATE Questions
                       SET count = count + 1, last_modified = datetime('now', 'localtime')
                       WHERE (volume = ? AND maintopic = ? 
                       AND subtopic = ? AND question = ?);
        ''', (volume, maintopic, subtopic, question))
        print('{}-{}-{}-{} question already exists!, incrementing count'.format(volume, maintopic, subtopic, question))
    

    return (volume, maintopic, subtopic, question)


def insert_note(cur, inputs):
    #https://stackoverflow.com/questions/30239092/how-to-get-multiline-input-from-user
    print("Enter/Paste your notes. Ctrl-D or Ctrl-Z (windows) to save it.")
    contents = []
    while True:
        try:
            line = input()
        except EOFError:
            break
        contents.append(line)
    contents = ('\n').join(contents)
    cur.execute('''UPDATE Questions
                   SET notes = notes || ?, last_modified = datetime('now', 'localtime')
                   WHERE (volume = ? AND maintopic = ? 
                   AND subtopic = ? AND question = ?);
                ''', (contents, inputs[0], inputs[1], inputs[2], inputs[3]))
    


def view_marked_question(cur):
    volume = input("Enter volume:\t")
    maintopic = input("Enter maintopic:\t")
    subtopic = input("Enter subtopic:\t")
    question = input("Enter question:\t")

    #check if given question is marked
    cur.execute('''SELECT * 
                   FROM Questions
                   WHERE (volume = ? AND maintopic = ? 
                   AND subtopic = ? AND question = ?);
                ''', (volume, maintopic, subtopic, question))

    rows = cur.fetchall()
    if len(rows) == 0:
        print("You haven't marked the question {}-{}-{}-{} yet".format(volume, maintopic, subtopic, question))
    else:
        for row in rows:
            print('\nQ:\t{}-{}-{}-{}'.format(row[0], row[1], row[2], row[3]))
            print('Count: {}\t Last Modified: {}'.format(row[4], row[5]))
            print('Notes: ')
            notes = row[6].split('\n')
            for i in notes:
                print(i)


def view_marked_questions_volume(cur):
    cur.execute( '''SELECT volume, maintopic, subtopic, question, count, last_modified 
                    FROM Questions
                    ORDER BY volume, maintopic, subtopic, question;
                ''')
    rows = cur.fetchall()
    print_rows(rows)


def view_marked_questions_latest(cur):
    cur.execute( '''SELECT volume, maintopic, subtopic, question, count, last_modified 
                    FROM Questions
                    ORDER BY last_modified DESC;
                ''')
    rows = cur.fetchall()
    print_rows(rows)


def view_marked_question_count(cur):
    cur.execute( '''SELECT volume, maintopic, subtopic, question, count, last_modified 
                    FROM Questions
                    ORDER BY count DESC;
                ''')
    rows = cur.fetchall()
    print_rows(rows)
    


def print_rows(rows):
    print(tabulate(rows, headers=["Volume", "Maintopic", "Subtopic", 
                                "Question", "Count", "Last Modified"], 
                                tablefmt="fancy_grid"))

