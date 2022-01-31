# to run this website and watch for changes: 
# $ export FLASK_ENV=development; flask run


from flask import Flask, g, render_template, request

import matplotlib.pyplot as plt
import numpy as np
import pickle
import sqlite3




# Create web app, run with flask run
# (set "FLASK_ENV" variable to "development" first!!!)

app = Flask(__name__)

# Create main page

@app.route('/')
# after running
# $ export FLASK_ENV=development; flask run
# site will be available at 
# http://localhost:5000

def main():
    # return render_template('main_better.html')
    return render_template('main.html')

#submit page
@app.route('/submit/', methods=['POST', 'GET'])
def submit():
    if request.method == 'GET':
        return render_template('submit.html')
    else:
        try:
            insert_message(request)
            return render_template('submit.html', thanks=True)
        except:
            return render_template('submit.html', error=True)

def get_message_db():
    try:
        return g.message_db
    except:
        g.message_db = sqlite3.connect("messages_db.sqlite")
        cmd = \
        '''
        CREATE TABLE IF NOT EXISTS `messages` (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            handle TEXT NOT NULL,
            message TEXT NOT NULL
        );
        '''

        cursor = g.message_db.cursor()
        cursor.execute(cmd)
        return g.message_db

def insert_message(request):
    conn = get_message_db()
    cmd = \
    f'''
    INSERT INTO messages (handle, message)
        VALUES ('{request.form["handle"]}', '{request.form["message"]}'); 
    '''

    cursor = conn.cursor()
    cursor.execute(cmd)
    conn.commit()
    conn.close()


@app.route('/view/')
def view():
    return render_template('view.html', messages = random_messages(5))

def random_messages(n):
    conn = get_message_db()
    cursor = conn.cursor()
    cursor.execute(f"SELECT handle, message FROM messages ORDER BY RANDOM() LIMIT {n}")
    # cursor.execute("SELECT MAX(id) FROM messages")
    # max_id = cursor.fetchone()[0]
    #
    #
    # if max_id <= 1:
    #     cursor.execute(f"SELECT handle, message FROM messages WHERE id=max_id")
    # else:
    #     ids = np.arange(1, max_id + 1)
    #     np.random.shuffle(ids)
    #     rand_ids = tuple(ids[:n])
    #     cursor.execute(f"SELECT handle, message FROM messages WHERE id IN {rand_ids}")
    # # elif n <= max_id:
    # #     rand_ids = tuple(np.random.choice(np.arange(1, max_id+1), n, replace=False))
    # #     cursor.execute(f"SELECT handle, message FROM messages WHERE id IN {rand_ids}")
    # # else:
    # #     rand_ids = tuple(np.random.choice(np.arange(1, max_id+1), max_id, replace=False))
    # #     cursor.execute(f"SELECT handle, message FROM messages WHERE id IN {rand_ids}")
    msg = cursor.fetchall()
    return msg




