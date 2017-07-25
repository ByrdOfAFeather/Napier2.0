# - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
# Matthew Byrd
# 5 - 12 - 17
# An automatic database manager to keep track of rankings for MathBot.
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
import sqlite3
import configparser

settings = configparser.ConfigParser()

# TODO: remove idiotic solution and replace with DB admin values.
def admin_chk(user_id):
    """checks for admin
    user_id = str"""
    if user_id == str(137974469896437760) or user_id == str(148798654688395265): return True
    else: return False


def get_guess(user_id):
    """Returns if a user has attempted to answer yet
    user_id = str"""
    db = sqlite3.connect('Ranking/Rankings.db')
    adder = db.cursor()
    adder.execute('SELECT * FROM ranks ORDER BY Points DESC')
    db_result = adder.fetchall()
    for values in db_result:
        values = str(values).replace("(", "").replace(")", "").split(',')  # Removes discords ID formatting
        if values[0] == user_id:  # Checks for the user ID
            return values[2]  # Returns the guess value
    print("ERROR: NO USER ID FOUND")
    db.close()


def add_user(user_id):
    """Adds a user to the database
    user_id - str"""
    db = sqlite3.connect('Ranking/Rankings.db')
    adder = db.cursor()
    adder.execute("INSERT INTO ranks (UserID,Points,DailyGuess) VALUES ({}, 0, 0)".format(user_id))
    db.commit()
    db.close()


def set_guess(user_id, value):
    """used to set a guess in the databased to either 0 (false) or 1 (true)
    user_id - str
    value - int"""
    db = sqlite3.connect('Ranking/Rankings.db')
    adder = db.cursor()
    adder.execute('UPDATE ranks SET DailyGuess = {} WHERE UserID = {}'.format(value, user_id))
    db.commit()
    db.close()


def check_id(user_id):
    """checks if a user is in the database yet
    user_id - str"""
    db = sqlite3.connect('Ranking/Rankings.db')
    adder = db.cursor()
    adder.execute('SELECT 1 FROM ranks WHERE UserID = {}'.format(user_id))
    result = adder.fetchall()
    if result: pass # If a non empty list is passed, there is a user
    if not result: add_user(user_id)
    db.close()


def add_points(user_id, points):
    """adds points given the user and the point amount, if the point value is less than 0, it defaults to 0
    user_id - str
    points - int"""
    db = sqlite3.connect('Ranking/Rankings.db')
    adder = db.cursor()
    if int(points) < 0:
        adder.execute('UPDATE ranks SET Points = {} WHERE UserID = {}'.format(0, user_id))
    else:
        cur_points = get_points(user_id)
        adder.execute('UPDATE ranks SET Points = {} WHERE UserID = {}'.format(points + int(cur_points), user_id))

    db.commit()
    db.close()


def get_points(user_id):
    """gets the points for the given user
    user_id - str"""
    db = sqlite3.connect('Ranking/Rankings.db')
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
    """resets the answer value (0 or 1) to 0 for the entire db"""
    db = sqlite3.connect('Ranking/Rankings.db')
    adder = db.cursor()
    adder.execute('SELECT * FROM ranks ORDER BY Points DESC')
    db_result = adder.fetchall()
    for values in db_result:
        values = str(values).replace("(", "").replace(")", "").split(',')  # Formats the returned value into ID
        adder.execute('UPDATE ranks SET DailyGuess = {} WHERE UserID = {}'.format(0, values[0]))
    db.commit()
    db.close()


def set_settings(channel_id, ques_set, no):
    """updates settings in the ini file
    channel_id - number
    ques_set - string
    number - int"""
    # Sets the passed settings in the math bot config file
    settings.clear()
    settings.read("Ranking/ranking_config.ini")
    settings.set(str(channel_id), "cur_question_set", str(ques_set))
    settings.set(str(channel_id), "cur_question", str(no))
    with open('Ranking/ranking_config.ini', 'w') as configfile:
        settings.write(configfile)


def get_question(channel_name):
    '''gets the current question and question group given the current channel information
    channel_name - string'''
    settings.read("Ranking/ranking_config.ini")
    cur_question = settings.get('{}'.format(channel_name), 'cur_question') + '.jpg'
    cur_question_group = settings.get('{}'.format(channel_name), 'cur_question_set')
    cur_settings = [cur_question, cur_question_group]
    return cur_settings


def get_aw(level, ques_set, no):
    """gets the answer for the passed question information
    level - int
    ques_set - string
    no - int"""
    # Retrieves the currents answer from the given level config file
    settings.read(r"Math Question Repo\{}\{}\answer_key.ini".format(level, ques_set))
    cur_aw = [settings.get(no.replace(".jpg", ""), 'answer'), int(settings.get(no.replace(".jpg", ""), 'point_val'))]
    return cur_aw

