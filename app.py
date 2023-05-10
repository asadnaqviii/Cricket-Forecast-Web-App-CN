from flask import Flask, render_template, request, jsonify
from bs4 import BeautifulSoup
import requests
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('predictions.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS predictions (id INTEGER PRIMARY KEY, user TEXT, match_link TEXT, player TEXT, predicted_score INTEGER, upvotes INTEGER, downvotes INTEGER, ridiculous_votes INTEGER)''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_live_players', methods=['GET'])
def get_live_players():
    match_link = request.args.get('match_link')
    if match_link:
        response = requests.get(match_link)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the scorecard container
        scorecard_container = soup.select_one('div[id^="innings_"]')

        players = []
        if scorecard_container:
            # Find all the rows containing player names and their runs
            player_rows = scorecard_container.select('div.cb-col.cb-col-100.cb-scrd-itms')

            for row in player_rows:
                player_name = row.select_one('div:nth-child(1)')
                player_runs = row.select_one('div.text-right.text-bold')

                if player_name and player_runs:
                    player = {}
                    player['name'] = player_name.text.strip()
                    player['runs'] = player_runs.text.strip()
                    players.append(player)
        return jsonify(players)
    else:
        return jsonify([])



@app.route('/add_prediction', methods=['POST'])
def add_prediction():
    data = request.json
    conn = sqlite3.connect('predictions.db')
    c = conn.cursor()
    c.execute("INSERT INTO predictions (user, match_link, player, predicted_score, upvotes, downvotes, ridiculous_votes) VALUES (?, ?, ?, ?, ?, ?, ?)", (data['user'], data['match_link'], data['player'], data['predicted_score'], 0, 0, 0))
    conn.commit()
    conn.close()
    return jsonify({'status': 'success'})

@app.route('/cast_vote', methods=['POST'])
def cast_vote():
    data = request.json
    conn = sqlite3.connect('predictions.db')
    c = conn.cursor()

    if data['vote_type'] == 'upvote':
        c.execute("UPDATE predictions SET upvotes = upvotes + 1 WHERE id = ?", (data['prediction_id'],))
    elif data['vote_type'] == 'downvote':
        c.execute("UPDATE predictions SET downvotes = downvotes + 1 WHERE id = ?", (data['prediction_id'],))
    elif data['vote_type'] == 'ridiculous':
        c.execute("UPDATE predictions SET ridiculous_votes = ridiculous_votes + 1 WHERE id = ?", (data['prediction_id'],))

    conn.commit()
    conn.close()
    return jsonify({'status': 'success'})

@app.route('/get_predictions', methods=['GET'])
def get_predictions():
    conn = sqlite3.connect('predictions.db')
    c = conn.cursor()
    c.execute("SELECT * FROM predictions")
    predictions = c.fetchall()
    conn.close()
    return jsonify(predictions)

if __name__ == '__main__':
    app.run(debug=True)


