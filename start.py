from Math_Modules import trigonometric as tr
from Math_Modules import conversion_funcs as cf
from Math_Modules import polynomials as pn
from Ranking import Ranking as r
import censor
import secrets
from discord.ext import commands
from sympy.parsing.sympy_parser import parse_expr
from datetime import datetime
import sqlite3
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
# Matthew Byrd
# 2016 -2018
# A Discord Bot designed for educational use, to inspire people to learn mathematics more so than now.
# Part of FIX DHS 2018.
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - #

# TO DO LIST #
# https://cdn.discordapp.com/attachments/272896747385258004/313147123656949760/416b412.gif #


description = '''A Magical Bot Used To Do More Than Magical Things'''
napier = commands.Bot(command_prefix=">", description=description, pm=True)
censor_list = censor.arrBad


@napier.event
async def on_ready():
    print("Logged in as\n"
          "{}\n"
          "{}\n"
          "-----".format(napier.user.name, napier.user.id))
    start_time = datetime.time


########################################################################################################################

# Trigonometric Functions #
@napier.command(pass_context=True)
async def sin(ctx):
    form_val = cf.format_msg(ctx.message.content, "sin")
    await napier.say(tr.sin_call(parse_expr(form_val)))  # tr = trigonometric
    

@napier.command(pass_context=True)
async def cos(ctx):
    form_val = cf.format_msg(ctx.message.content, "cos")
    await napier.say(tr.cos_call(parse_expr(form_val)))


@napier.command(pass_context=True)
async def tan(ctx):
    form_val = cf.format_msg(ctx.message.content, "tan")
    await napier.say(tr.tan_call(parse_expr(form_val)))


@napier.command(pass_context=True)
async def solve_triangle(ctx):
    await napier.say("I am on it!")
    form_val = cf.format_msg(ctx.message.content, "solve_triangle")
    form_val = form_val.split()
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

# End of Trigonometric Functions #

########################################################################################################################

# Polynomial Manipulation #


@napier.command(pass_context=True)
async def factor(ctx):
    formatted = cf.format_msg(ctx.message.content, "factor")
    try:
        await napier.say("```{}```".format(pn.factor(formatted)))

    except (SyntaxError, TypeError):
        await napier.say("The given function does not make sense to me.")


@napier.command(pass_context=True)
async def simplify(ctx):
    formatted = cf.format_msg(ctx.message.content, "simplify")
    try:await napier.say("```{}```".format(pn.simplify(formatted)))

    except (SyntaxError, TypeError) as e:
        await napier.say("The given function does not make sense to me")
        print("wrong {}".format(e))


@napier.command(pass_context=True)
async def roots(ctx):
    formatted = cf.format_msg(ctx.message.content, "roots")
    try: await napier.say("```{}```".format(pn.get_dem_roots(formatted)))

    except (SyntaxError, TypeError) as e:
        await napier.say("The given function does not make sense to me.")
        print("wrong {}".format(e))


# End of Manipulation #

########################################################################################################################

# Conic Sections #

#@bot.command(pass_context=True)
#async def conic_section_simplification(ctx):
#    pass


# End Of Conic Sections #

########################################################################################################################

# Ranking System - WIP #

@napier.command(pass_context=True)
async def ranks(ctx):
    db = sqlite3.connect('SQL Manager/Rankings.db')
    adder = db.cursor()

    adder.execute('SELECT * FROM ranks ORDER BY Points DESC')
    db_result = adder.fetchall()

    i = 0
    rank_list = ""  # Note not actaully a list, but a string.
    while i < 10:
        try:
            final_row = str(db_result[i]).replace("(", "").replace(")", "").replace(" ", "").split(',')
            rank_list += "<@{}> is rank {} with {} points\n".format(final_row[0], i + 1, final_row[1])
            i += 1
        except IndexError:
            break
    await napier.say("\nTop 10:\n{}\n".format(rank_list))
    db.close()


@napier.command(pass_context=True)
async def points(ctx):
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
    if r.admin_chk(ctx.message.author.id):
        r.check_id(ctx.message.author.id)
        r.add_points(ctx.message.author.id, int(ctx.message.content.replace(">add_points", "").replace(" ", "")))
    else: await napier.say("<@{}> Admin commands are for admins only!".format(ctx.message.author.id))


@napier.command(pass_context=True)
async def answer(ctx):
    response = ctx.message.content.replace('>answer', '').replace(' ', '')
    r.check_id(ctx.message.author.id)  # Checks if the user exists yet
    guess = r.get_guess(ctx.message.author.id)  # Checks if the user has responded yet
    cur_settings = r.get_question(ctx.message.channel.id)
    cur_answer = r.get_answer(ctx.message.channel, cur_settings[1], cur_settings[0].replace(".jpg", ""))
    cur_weight = r.get_weight(ctx.message.channel, cur_settings[1], cur_settings[0].replace(".jpg", ""))
    if response in cur_answer and int(guess) == 0:
        r.add_points(ctx.message.author.id, int(cur_weight))
        r.set_settings(ctx.message.channel.id, cur_settings[1], str(int(cur_settings[0].replace(".jpg", "")) + 1))
        await napier.say("Congratulations <@{}> you gained {} points".format(ctx.message.author.id, cur_weight))
        await next_question(ctx)

    elif response not in cur_answer and int(guess) == 0:
        await napier.say("Sorry <@{}> try again next question!".format(ctx.message.author.id))
        r.attempt_answer(ctx.message.author.id)

    elif int(guess) == 1:
        await napier.say("You already tried this question <@{}>!".format(ctx.message.author.id))


@napier.command(pass_context=True)
async def set_guess(ctx):
    if r.admin_chk(ctx.message.author.id):
        r.check_id(ctx.message.author.id)
        r.set_guess(ctx.message.author.id, int(ctx.message.content.replace(">set_guess", "").replace(" ", "")))
    else: await napier.say("<@{}> Admin commands are for admins only!".format(ctx.message.author.id))


@napier.command(pass_context=True)                                                                                                                                                                  
async def start_challenge(ctx):
    formatted = ctx.message.content.replace(">start_challenge", "").split("|")
    if r.admin_chk(ctx.message.author.id):
        question_set = formatted[0]
        question_no = formatted[1]
        r.set_settings(ctx.message.channel.id, question_set, question_no)
        await next_question(ctx)

    else: await napier.say("<@{}> Admin commands are for admins only!".format(ctx.message.author.id))

async def next_question(ctx):
    try:
        cur_settings = r.get_question(ctx.message.channel.id)
        cur_channel = napier.get_channel(ctx.message.channel.id)
        await napier.send_file(ctx.message.channel,
                               r"Math Question Repo\{}\{}\{}".format(cur_channel.name,
                                                                     cur_settings[1], cur_settings[0]))
        r.reset_guess()
    except Exception as e:
        print(e)
        await napier.say("It appears that I've run out of questions!")





# End of Ranking System - WIP #

########################################################################################################################
@napier.event
async def on_message(message):
    if message.content in censor.arrBad:
        await napier.delete_message(message)
    await napier.process_commands(message)

# @bot.event
# async def on_message(message):
#    print(message.content)


napier.run(secrets.token)
