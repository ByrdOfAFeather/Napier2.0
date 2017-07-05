import sqlite3
from discord.ext import commands
from sympy.parsing.sympy_parser import parse_expr
from Math_Modules import trigonometric as tr
from Math_Modules import polynomials as pn
from Ranking import Ranking as r
import censor
import secrets

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
# Matthew Byrd
# 2016 - 2018
# A Discord Bot designed for educational use, to inspire people to learn mathematics more so than now.
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - #

description = '''A Magical Bot Used To Do More Than Magical Things'''
napier = commands.Bot(command_prefix=">", description=description, pm=True)
censor_list = censor.arrBad


@napier.event
async def on_ready():
    print("Logged in as\n"
          "{}\n"
          "{}\n"
          "-----".format(napier.user.name, napier.user.id))

################################################TRIGONOMETRY############################################################

# Trigonometric Functions #
# Uses Module Trigonometric (tr) #


@napier.command(pass_context=True)
async def sin(ctx):
    """Returns the sine value in degrees of the given angle. >sin x"""
    form_val = ctx.message.content.replace(">sin", "")
    await napier.say(tr.sin_deg(parse_expr(form_val)))
    

@napier.command(pass_context=True)
async def cos(ctx):
    """Returns the cosine value in degrees of the given angle. >cos x"""
    form_val = ctx.message.content.replace("cos", "")
    await napier.say(tr.cos_deg(parse_expr(form_val)))


@napier.command(pass_context=True)
async def tan(ctx):
    """Returns the tangent value in degrees of the given angle. >tan x"""
    form_val = ctx.message.content.replace("tan", "")
    await napier.say(tr.tan_deg(parse_expr(form_val)))


@napier.command(pass_context=True)
async def solve_right_triangle(ctx):
    """Solves a right triangle, given that the right triangle is possible.
    >solve_triangle angle(deg) | angle(deg) | leg | leg | hypo"""
    await napier.say("I am on it!")
    form_val = ctx.message.content.replace("solve_triangle", "")
    form_val = form_val.split('|')
    i = 0
    for values in form_val:
        if values == "None":
            form_val[i] = None
        else:
            form_val[i] = float(values)
        i += 1

    infinite = tr.solve_that_triangle(form_val[0], form_val[1], form_val[2], form_val[3], form_val[4])

    if not infinite: await napier.send_file(ctx.message.channel, 'image.svg')
    if infinite: await napier.say("The triangle has infinitely many solutions")

########################################POLYNOMIAL MANIPULATION#########################################################

@napier.command(pass_context=True)
async def factor(ctx):
    """Factors a given function, >factor x^2 + 3*x^2...etc. Multiplication symbol required (3x != 3*x)"""
    formatted = ctx.message.content.replace(">factor", "")
    try: await napier.say("```{}```".format(pn.factor(formatted)))

    except (SyntaxError, TypeError) as e:
        await napier.say("The given function does not make sense to me. 0_0")
        print("wrong {}".format(e))


@napier.command(pass_context=True)
async def simplify(ctx):
    """Simplifies a given function, Similar to >factor, but is limited in certain aspects of factorization"""
    formatted = ctx.message.content.replace(">simplify", "")
    try: await napier.say("```{}```".format(pn.simplify(formatted)))

    except (SyntaxError, TypeError) as e:
        await napier.say("The given function does not make sense to me. 0_0")
        print("wrong {}".format(e))


@napier.command(pass_context=True)
async def roots(ctx):
    """finds all real roots of a given function.
    >roots x**2 + 3*x^2...etc. Multiplication symbol is required (3x != 3*x)"""
    formatted = ctx.message.content.replace(">roots", "")
    try: await napier.say("```{}```".format(pn.get_roots(formatted)))

    except (SyntaxError, TypeError) as e:
        await napier.say("The given function does not make sense to me. 0_0")
        print("wrong {}".format(e))

#######################################CONIC SECTIONS###################################################################

#@bot.command(pass_context=True)
#async def conic_section_simplification(ctx):
#    pass

####################################RANKING SYSTEM######################################################################

@napier.command(pass_context=True)
async def ranks(ctx):
    """Returns a top 10 list of current math point ranks"""
    # Returns a discord-formatted string containing the ranks in order
    db = sqlite3.connect('Ranking/Rankings.db')
    adder = db.cursor()
    adder.execute('SELECT * FROM ranks ORDER BY Points DESC')
    db_result = adder.fetchall()

    rank_list = ""  # Note not actaully a list, but a string.
    i = 0
    while i < 10:
        try:
            # First item in the array is ID, Second is Points, Third is True/False answer check.
            final_row = str(db_result[i]).replace("(", "").replace(")", "").replace(" ", "").split(',')
            user_name = await napier.get_user_info(final_row[0])  # Loose typed language problems
            rank_list += "{} is rank {} with {} points\n".format(user_name.display_name, i + 1, final_row[1])
            i += 1
        except IndexError:  # Breaks in case there isn't 10 users yet.
            break

    db.close()
    await napier.say("\nTop 10:\n{}\n".format(rank_list))


@napier.command(pass_context=True)
async def points(ctx):
    """Checks the point value of yourself or another user"""
    if len(ctx.message.content.split(" ")) > 1:
        search_id = ctx.message.content.split(" ")[1]
        search_id = search_id.replace("<", "").replace(">", "").replace("@", "").replace("!", "")
        r.check_id(search_id)
        point_val = r.get_points(search_id)
        await napier.say("<@{}> has {} points".format(search_id, point_val))
    else:
        r.check_id(ctx.message.author.id)
        point_val = r.get_points(ctx.message.author.id)
        await napier.say("<@{}> has {} points".format(ctx.message.author.id, point_val))


@napier.command(pass_context=True)
async def add_points(ctx):
    """Adds points to the passed user"""
    if r.admin_chk(ctx.message.author.id):
        r.check_id(ctx.message.author.id)
        r.add_points(ctx.message.author.id, int(ctx.message.content.replace(">add_points", "").replace(" ", "")))
    else: await napier.say("<@{}> Admin commands are for admins only!".format(ctx.message.author.id))


@napier.command(pass_context=True)
async def answer(ctx):
    """USE THIS COMMAND TO ANSWER - IMPORTANT - YOU ONLY GET ONE CHANCE PER QUESTION"""
    response = ctx.message.content.replace('>answer', '').replace(' ', '')
    r.check_id(ctx.message.author.id)  # Checks if the user exists yet
    guess = int(r.get_guess(ctx.message.author.id))  # Returns if the user has responded yet
    cur_settings = r.get_question(ctx.message.channel.id)
    cur_aw = r.get_aw(ctx.message.channel, cur_settings[1], cur_settings[0])

    if response in cur_aw[0] and guess == 0:
        r.add_points(ctx.message.author.id, int(cur_aw[1]))
        r.set_settings(ctx.message.channel.id, cur_settings[1], str(cur_settings[0] + 1))
        await napier.say("Congratulations <@{}> you gained {} points".format(ctx.message.author.id, cur_aw[1]))
        await next_question(ctx)

    elif response not in cur_aw[0] and guess == 0:
        r.set_guess(ctx.message.author.id, 1)
        await napier.say("Sorry <@{}> try again next question!".format(ctx.message.author.id))

    elif guess == 1:
        await napier.say("You already tried this question <@{}>!".format(ctx.message.author.id))


@napier.command(pass_context=True)
async def set_guess(ctx):
    """Sets the guess of the called of the command to the specified number"""
    if r.admin_chk(ctx.message.author.id):
        r.check_id(ctx.message.author.id)
        r.set_guess(ctx.message.author.id, int(ctx.message.content.replace(">set_guess", "").replace(" ", "")))
    else: await napier.say("<@{}> Admin commands are for admins only!".format(ctx.message.author.id))


@napier.command(pass_context=True)                                                                                                                                                                  
async def start_challenge(ctx):
    """Starts the question specified question set"""
    formatted = ctx.message.content.replace(">start_challenge", "").split("|")
    if r.admin_chk(ctx.message.author.id):
        question_set = formatted[0]
        question_no = formatted[1]
        r.set_settings(ctx.message.channel.id, question_set, question_no)
        await next_question(ctx)

    else: await napier.say("<@{}> Admin commands are for admins only!".format(ctx.message.author.id))

async def next_question(ctx):
    """For internal bot use only, moves to the next question in the set"""
    try:
        cur_settings = r.get_question(ctx.message.channel.id)
        cur_channel = napier.get_channel(ctx.message.channel.id)
        await napier.send_file(ctx.message.channel,
                               r"Math Question Repo\{}\{}\{}".format(cur_channel.name, cur_settings[1], cur_settings[0]))
        r.reset_guess()
    except Exception as e:
        print(e)
        await napier.say("It appears that I've run out of questions!")

#####################################GENERAL FUNCTIONS##################################################################

@napier.command(pass_context=True)
async def wot(ctx): await wotloc(ctx)


async def wotloc(ctx):
    """Local version of the command so it can be used both by the bot and user, changes This to ThIs"""
    try: # Loose solution allowing the bot to pass the literal message or for the command to pass the context message.
        message = ctx.message.content.replace(">wot", "")
        channel = ctx.message.channel
    except AttributeError:
        message = ctx.content.replace(">wot", "")
        channel = ctx.channel
    i = 1
    formatted_message = ""
    for items in message:
        if i % 2 != 0: items = items.upper()
        else: items = items.lower()
        formatted_message += items
        if items == " ": continue
        i += 1
    await napier.send_message(channel, formatted_message)



@napier.event
async def on_message(message):
    if message.content in censor.arrBad: await napier.delete_message(message)  # Primitive censorship
    if message.author.id == "138367390185553920" or message.author.id == '138392070724255744': await wotloc(message)
    await napier.process_commands(message)




napier.run(secrets.token)
