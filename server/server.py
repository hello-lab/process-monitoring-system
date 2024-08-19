import mysql.connector
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# MySQL Database configuration
db_config = {
    'user': 'root',
    'password': 'niyosan42',
    'host': 'localhost',  # 'localhost' if the database is hosted locally
    'database': 'mydb'
}

def fetch_logs(connection, computer_name=None):
    '''
    Fetch logs from the database based on the computer name.

    Args:
    - connection: MySQL database connection
    - computer_name: Filter logs based on the computer name

    Returns:
    - logs: List of logs
    '''
    cursor = connection.cursor()

    # Create the "logs" table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS logs (
            id INT AUTO_INCREMENT PRIMARY KEY,
            computer_name VARCHAR(255),
            log_message TEXT,
            event_start VARCHAR(255),
            event_end VARCHAR(255)
        )
    ''')
    
    # Fetch logs based on the provided computer name
    if computer_name:
        cursor.execute('SELECT DISTINCT id, computer_name, log_message, MAX(event_start), event_end FROM logs WHERE computer_name = "'+computer_name+'" GROUP BY log_message')
    else:
        cursor.execute('SELECT id, computer_name, log_message, event_start, event_end FROM logs')

    logs = cursor.fetchall()
    print(logs)
    return logs

@app.route('/')
def index():
    '''
    Default route to render the index.html template.
    '''
    return render_template('index.html')

@app.route('/update', methods=['GET'])
def updatit():
    '''
    Route to fetch and return logs.
    '''
    db_connection = mysql.connector.connect(**db_config)
    computer_name = ""
    logs = fetch_logs(db_connection, computer_name)
    db_connection.close()
    print(logs)
    return jsonify(logs)

@app.route('/login/', methods=['POST'])
def my_test_endpoint():
    '''
    Route to handle a POST request for logging information.
    '''
    input_json = request.get_json(force=True)
    print('data from client:', input_json["APPS-OPENNED"])
    dictToReturn = 'good'

    # Logging
    db_connection = mysql.connector.connect(**db_config)
    computer_name = input_json['Computer Name']
    log_message = input_json["APPS-OPENNED"]
    insert_log(db_connection, computer_name, log_message)
    db_connection.close()
    return jsonify(dictToReturn)

def showlog():
    '''
    Function to retrieve all logs from the database.
    '''
    db_connection = mysql.connector.connect(**db_config)
    cursor = db_connection.cursor()
    cursor.execute('SELECT * FROM logs')
    logs = cursor.fetchall()
    print(logs)
    db_connection.close()
    return logs

def insert_log(connection, computer_name_value, log_message_value):
    '''
    Function to insert logs into the database.

    Args:
    - connection: MySQL database connection
    - computer_name_value: Computer name for the log
    - log_message_value: Log message

    Returns:
    - None
    '''
    cursor = connection.cursor()
    import time

    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)

    if '-' not in log_message_value:
        try:
            # Check if the log entry already exists
            cursor.execute("SELECT COUNT(*) FROM logs WHERE computer_name = '"+computer_name_value+"' AND log_message = '"+log_message_value+"'")
            row_count = cursor.fetchone()[0]

            if row_count > 0:
                # If the computer name already exists, update the event end time
                cursor.execute("UPDATE logs SET event_end = '"+current_time+"' WHERE computer_name = '"+computer_name_value+"' AND log_message = '"+log_message_value+"'")
            else:
                # If the computer name is not a duplicate, insert a new row into the "logs" table
                cursor.execute("INSERT INTO logs (computer_name, log_message, event_start, event_end) VALUES ('"+computer_name_value+"','"+log_message_value+"' , '"+current_time+"', '"+current_time+"')")

            # Commit the transaction
            connection.commit()

        except Exception as e:
            print(f"Error occurred: {e}")
            create_log_table(connection)
            cursor = connection.cursor()
            cursor.execute('''
                INSERT INTO logs (computer_name, log_message, event_start, event_end)
                VALUES (%s, %s, %s, %s)
            ''', (computer_name_value, log_message_value, current_time, current_time))

            connection.commit()

def create_log_table(connection):
    '''
    Function to create the log table if it doesn't exist.

    Args:
    - connection: MySQL database connection

    Returns:
    - None
    '''
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS logs (
            id INT AUTO_INCREMENT PRIMARY KEY,
            computer_name VARCHAR(255),
            log_message TEXT,
            event_start VARCHAR(255),
            event_end VARCHAR(255)
        )
    ''')
    connection.commit()

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)
