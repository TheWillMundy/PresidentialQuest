from flask import Flask, render_template, request, redirect
from flask_ask import Ask, statement, question, session
from fuzzywuzzy import fuzz, process
import json
import random
# import requests
# import time
# import unidecode

# Dynamo Connect
import dynamo_connect as db_connect
# Quest Helper Functions
import quest_helpers

app = Flask(__name__)
ask = Ask(app, "/presidential_facts")

# Helper variables
stop_words = ['stop', 'cancel', 'end', 'finish', 'no']

# Helper Functions
def get_challenge():
    random_president = quest_helpers.random_president()
    all_facts = db_connect.get_facts(random_president)
    random_fact = random.choice(all_facts)
    return random_president, random_fact

def score_review(score, spoken_president, actual_president, villain):
    answer = "the answer was {}. ".format(actual_president)
    # Setting score
    match_spoken_president = process.extractOne(spoken_president, db_connect.get_presidents())[0]
    if match_spoken_president.lower() == actual_president.lower():
        score['player'] += 1
        player_correct = True
    else:
        score['villain'] += 1
        player_correct = False
    # Score report is common to all scenarios
    score_report = "The score is currently {} to {} - ".format(score['player'], score['villain'])
    if player_correct:
        review_score_message = "Nice! You were correct, " + answer
    else:
        review_score_message = "Sorry, you were just a bit off, " + answer
    if score['player'] == score['villain']:
        review_score_message += score_report + "it's a tie!"
    else:
        if score['player'] > score['villain']:
            review_score_message += score_report + "you're in the lead!"
        else:
            review_score_message += score_report + "oh no, {} is winning. You need to catch up!".format(villain)
    return score, review_score_message

def limit_reached(score, villain, hero, president):
    if score['player'] >= 3:
        return render_template('player_victory', villain=villain, hero=hero)
    elif score['villain'] >= 3:
        return render_template('villain_victory', villain=villain, hero=hero, president=president)
    else:
        return False

@app.route('/')
def homepage():
    return 'Greetings, this is an Alexa Skill for Kids. Now shoo, let the Alexa users have their turn.'

# @app.route('/fact_form', methods=['GET'])
# def fact_form():
#     return render_template('form.html')
#
# @app.route('/add_fact', methods=['POST'])
# def add():
#     result = request.form
#     db_connect.add_facts(result['president'], result['fact'])
#     return redirect('/fact_form')

@ask.launch
def start_skill():
    return presidential_intent()

@ask.intent("BeginFromHelpIntent")
def begin_from_help():
    return presidential_intent()

@ask.intent("PresidentialIntent")
def presidential_intent():
    random_villain, villain_backstory, villain_archenemy = quest_helpers.random_villain()
    # Setup Session
    session.attributes['villain'] = random_villain
    session.attributes['villain_backstory'] = villain_backstory
    session.attributes['hero'] = villain_archenemy
    # Setup Challenge
    random_president, random_fact = get_challenge()
    session.attributes['president'] = random_president
    # To be sent to user
    message = render_template('introduction', villain=random_villain, villain_backstory=villain_backstory, hero=villain_archenemy, random_fact=random_fact)
    reprompt = render_template('reprompt', villain=random_villain, random_fact=random_fact)
    return question(message) \
            .reprompt(reprompt)

@ask.intent("QuestStepIntent")
def quest_step_intent(spoken_president):
    # Ensures correct intent being executed
    if spoken_president.lower() in stop_words:
        return stop_intent()
    elif spoken_president.lower().count("help") >= 1:
        return help_intent()
    elif 'president' not in session.attributes:
        return presidential_intent('Player')
    # match_spoken_president = process.extractOne(spoken_president, db_connect.get_presidents())
    actual_president = session.attributes['president']
    # Setup score
    score = {'player': 0, 'villain': 0}
    if 'score' in session.attributes:
        score = session.attributes['score']
    score, score_review_msg = score_review(score, spoken_president, actual_president, session.attributes['villain'])
    # Check score
    message = limit_reached(score, session.attributes['villain'], session.attributes['hero'], actual_president)
    if message:
        return statement(message)
    else:
        session.attributes['score'] = score
    # Next challenge
    random_president, random_fact = get_challenge()
    session.attributes['president'] = random_president
    message = render_template('quest_step', villain=session.attributes['villain'], score_review=score_review_msg, random_fact=random_fact)
    reprompt = render_template('reprompt', villain=session.attributes['villain'], random_fact=random_fact)
    return question(message) \
            .reprompt(reprompt)

@ask.intent("AMAZON.HelpIntent")
def help_intent():
    help_text = render_template('help')
    return question(help_text)

@ask.intent("AMAZON.CancelIntent")
def cancel_intent():
    print("User canceled the interaction")
    return statement('')

@ask.intent("AMAZON.StopIntent")
def stop_intent():
    print("User canceled the interaction")
    return statement('')

if __name__ == '__main__':
    app.run(debug=True)
