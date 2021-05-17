from flask import Flask, render_template, request, redirect, url_for
from db import DBInit, deleteToReservedDB, getSeasons, getEpisodes, setEpisodeStatus, getReservedEpisodes, addToReservedDB

app = Flask(__name__, template_folder='templates')


DBInit()

@app.route('/')
def index():
    seasons = getSeasons()
    return render_template('./seasons.html', seasons=seasons)


@app.route('/episodes/<season>')
def episodes(season):
    seasons = getSeasons()
    episodes_list = getEpisodes(season)
    return render_template('./episodes.html', currentSeason=season, seasons=seasons, episodes=episodes_list)


@app.route("/allow/<season>/<number>")
def allow(season, number):
    setEpisodeStatus(number, "Available")
    deleteToReservedDB(number)
    return redirect(url_for('episodes', season=season))


@app.route("/rent/<season>/<number>")
def rent(season, number):
    setEpisodeStatus(number, "Rented")
    deleteToReservedDB(number)
    return redirect(url_for('episodes', season=season))


@app.route("/reserve/<season>/<number>")
def reserve(season, number):
    setEpisodeStatus(number, "Reserved")
    addToReservedDB(number)
    return redirect(url_for('episodes', season=season))


@app.route("/confirm_payment")
def confirmPayment():
    reserved_episodes = getReservedEpisodes()
    return render_template('./confirm_payment.html', episodes=reserved_episodes)


@app.route("/payment_confirmed", methods=['POST'])
def paymentConfirmed():
    if request.method == "POST":
        episode_number = request.form["episode"]
        setEpisodeStatus(episode_number, "Rented")
        deleteToReservedDB(episode_number)
        return redirect(url_for('confirmPayment'))



if __name__ == "__main__":
    app.run(host="localhost", port="5000", debug=True)
