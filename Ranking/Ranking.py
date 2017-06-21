# Matthew Byrd #
# 12 - 5 - 17 #
#
# Desc: #
# A Automatic Database manager file to keep track of rankings for math bot #
import sqlite3
import configparser

settings = configparser.ConfigParser()


def admin_chk(user_id):
    if user_id == str(137974469896437760) or user_id == str(148798654688395265): return True
    else: return False


def get_guess(user_id):
    db = sqlite3.connect('Rankings.db')
    adder = db.cursor()
    adder.execute('SELECT * FROM ranks ORDER BY Points DESC')
    db_result = adder.fetchall()
    for values in db_result:
        values = str(values).replace("(", "").replace(")", "").split(',')  # Formats the returned value into ID
        if values[0] == user_id:  # Checks for the user ID
            return values[2]  # Returns the guess value
    print("ERROR: NO USER ID FOUND")
    db.close()


def add_user(user_id):
    db = sqlite3.connect('Rankings.db')
    adder = db.cursor()
    adder.execute("INSERT INTO ranks (UserID,Points,DailyGuess) VALUES ({}, 0, 0)".format(user_id))
    db.commit()
    db.close()


def set_guess(user_id, value):
    db = sqlite3.connect('Rankings.db')
    adder = db.cursor()
    adder.execute('UPDATE ranks SET DailyGuess = {} WHERE UserID = {}'.format(value, user_id))
    db.commit()
    db.close()


def attempt_answer(user_id):
    db = sqlite3.connect('Rankings.db')
    adder = db.cursor()
    adder.execute('UPDATE ranks SET DailyGuess = {} WHERE UserID = {}'.format(1, user_id))
    db.commit()
    db.close()


def check_id(user_id):
    db = sqlite3.connect('Rankings.db')
    adder = db.cursor()
    adder.execute('SELECT 1 FROM ranks WHERE UserID = {}'.format(user_id))
    result = adder.fetchall()
    if result: pass # If a non empty list is passed, there is a user
    if not result: add_user(user_id)
    db.close()


def add_points(user_id, points):
    db = sqlite3.connect('Rankings.db')
    adder = db.cursor()
    if int(points) < 0:
        db = sqlite3.connect('Rankings.db')
        adder = db.cursor()
        adder.execute('UPDATE ranks SET Points = {} WHERE UserID = {}'.format(0, user_id))
    else:
        cur_points = get_points(user_id)
        adder.execute('UPDATE ranks SET Points = {} WHERE UserID = {}'.format(points + int(cur_points), user_id))

    db.commit()
    db.close()


def get_points(user_id):
    db = sqlite3.connect('Rankings.db')
    adder = db.cursor()
    adder.execute('SELECT * FROM ranks ORDER BY Points DESC')
    db_result = adder.fetchall()
    for values in db_result:
        values = str(values).replace("(", "").replace(")", "").split(',')  # Formats the returned value into ID
        if values[0] == user_id:  # Checks for the user ID
            return values[1]  # Returns the user points
    print("ERROR: NO USER ID FOUND")
    db.close()


def reset_guess():
    # Resets all guesses in the database of a question it properly answered
    db = sqlite3.connect('Rankings.db')
    adder = db.cursor()
    adder.execute('SELECT * FROM ranks ORDER BY Points DESC')
    db_result = adder.fetchall()
    for values in db_result:
        values = str(values).replace("(", "").replace(")", "").split(',')  # Formats the returned value into ID
        adder.execute('UPDATE ranks SET DailyGuess = {} WHERE UserID = {}'.format(0, values[0]))
    db.commit()
    db.close()


def set_settings(channel_id, ques_set, number):
    # Sets the passed settings in the math bot config file
    settings.clear()
    settings.read("ranking_config.ini")
    settings.set(channel_id, "cur_question_set", ques_set)
    settings.set(channel_id, "cur_question", number)
    with open('ranking_config.ini', 'w') as configfile:
        settings.write(configfile)


def get_question(channel_id):
    # Retrieves the question for the passed id and current settings
    settings.read("ranking_config.ini")
    cur_question = settings.get('{}'.format(channel_id), 'cur_question') + '.jpg'
    cur_question_group = settings.get('{}'.format(channel_id), 'cur_question_set')
    cur_settings = [cur_question, cur_question_group]
    return cur_settings


def get_answer(level, ques_set, no):
    # Retrieves the currents answer from the given level config file
    settings.read(r"Math Question Repo\{}\{}\answer_key.ini".format(level, ques_set))
    cur_answer = settings.get(no, 'answer')
    return cur_answer


def get_weight(level, ques_set, no):
    # Retrieves the current weight
    settings.read(r"Math Question Repo\{}\{}\answer_key.ini".format(level, ques_set))
    cur_answer = settings.get(no, 'point_val')
    print(cur_answer)
    return cur_answer
