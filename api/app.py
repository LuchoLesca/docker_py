from flask import Flask, render_template, request, redirect, url_for
from db import DBInit, getSeasons, getEpisodes, setEpisodeStatus, getEpisodeSeason, getReservedEpisodes

app = Flask(__name__, template_folder='templates')
app.config['DEBUG'] = True


# DBInit()


@app.route('/')
def index():
    seasons = getSeasons()
    return render_template('./seasons.html', seasons=seasons)

@app.route('/episodes/<season>')
def episodes(season):
    episodes_list = getEpisodes(season)
    return render_template('./episodes.html', season=season, episodes=episodes_list)

@app.route("/allow/<season>/<name>")
def allow(season, name):
    setEpisodeStatus(name, "Available")
    return redirect(url_for('episodes', season=season))

@app.route("/rent/<season>/<name>")
def rent(season, name):
    setEpisodeStatus(name, "Rented")
    return redirect(url_for('episodes', season=season))

@app.route("/reserve/<season>/<name>")
def reserve(season, name):
    setEpisodeStatus(name, "Reserved")
    return redirect(url_for('episodes', season=season))

@app.route("/confirm_payment")
def confirmPayment():
    reserved_episodes = getReservedEpisodes()
    return render_template('./confirm_payment.html', episodes=reserved_episodes)

@app.route("/payment_confirmed", methods=['POST'])
def paymentConfirmed():
    if request.method == "POST":
        episode_name = request.form["episode"]
        setEpisodeStatus(episode_name, "Rented")
        return redirect(url_for('confirmPayment'))


if __name__ == "__main__":
    app.run(host="localhost", port="5000", debug=True)
