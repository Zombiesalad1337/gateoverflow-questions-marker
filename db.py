import sqlite3

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
                    ''')
    else:
        #increment count and update datetime
        cur.execute('''UPDATE Questions
                       SET count = count + 1, last_modified = datetime('now', 'localtime')
                       WHERE (volume = ? AND maintopic = ? 
                       AND subtopic = ? AND question = ?);
        ''', (volume, maintopic, subtopic, question))
    print('{}-{}-{}-{} question added'.format(volume, maintopic, subtopic, question))

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
    
    
    
