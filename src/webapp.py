from flask import Flask, request, session, g, url_for, redirect, abort
import database
import bot
import _thread as thread

app = Flask(__name__)
with open('src/secrets/flask_key.txt') as flask_key_file:
    app.secret_key = bytes(flask_key_file.readline(), "utf-8").decode("unicode_escape")
thread.start_new_thread(bot.init_bot, tuple())


@app.route('/')
def index():
    return 'Placeholder text'


PAIR_ID = 'id'
DISCORD_ID = 'discord_id'
DISCORD_NAME = 'discord_name'


@app.route('/pair', methods=['POST'])
def handle_pair():
    pair_id = request.form[PAIR_ID]
    user_id = database.get_user_id_from_pair_id(pair_id)
    if user_id is not None:
        database.delete_pair_id(pair_id)
        user_data = database.get_user_data(user_id)
        session[DISCORD_ID] = user_id
        session[DISCORD_NAME] = user_data.user_name
    else:
        abort(401, description="Invalid or expired pair code")


@app.route('/logout', methods=['POST'])
def handle_logout():
    session.pop(DISCORD_NAME, None)
    session.pop(DISCORD_ID, None)
    return redirect(url_for('index'))


@app.route('/data', methods=['POST'])
def handle_data():
    speed = request.form['speed']
    user_id = session[DISCORD_ID]
    user_data = database.get_user_data(user_id)
    if user_data:
        min_speed = user_data.min_speed
        if not min_speed:
            database.store_settings_data(user_id, min_speed=0)
        if speed < min_speed:
            bot.client.punish(user_data)


@app.route('/settings', methods=['GET', 'POST'])
def handle_settings():
    method = request.method
    if method == 'GET':
        pass
    elif method == 'POST':
        min_speed = request.form['min_speed']
        database.store_settings_data(min_speed=min_speed)

