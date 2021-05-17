import redis
from data import seasons, episodes


# DB configurations
# HOST = "localhost"
HOST = "db-redis"
PORT = 6379


def connect_db(database=0):
    '''Create conection to DB'''
    conexion = redis.StrictRedis(host=HOST, port=PORT, db=database, charset="utf-8", decode_responses=True)
    if(conexion.ping()):
        print("Conectado a servidor de redis")
    else:
        print("error")
    return conexion


# DB Acceses
conexion = connect_db()
conexionReserved = connect_db(1)


def DBInit():
    # Reset BBDD
    conexion.flushall()

    # Stores seasons's list. >> seasons : ["1", "2"]
    for season in seasons:
        conexion.rpush("seasons", str(season))

    # Stores number of episodes's list for each season. >> seasonX : ["1", "2", ....] 
    for i in range(1, 9):
        conexion.rpush("season1", str(i))
    for i in range(8, 17):
        conexion.rpush("season2", str(i))

    # Stores episodes's data. >> numero_ep : {season, status, number, name}
    for episode in episodes:
        conexion.hmset(episode['number'], episode)


def getSeasons():
    '''return list of seasons numbers'''
    seasons = conexion.lrange("seasons", 0, -1)
    return seasons


def getEpisodes(season):
    '''return array with episodes. Each index is a dict with number, name and status keys'''
    list_episodes = []
    episodes_number = conexion.lrange("season" + str(season), 0, -1)

    for number in episodes_number:
        list_episodes.append(getEpisodeData(number))

    return list_episodes


def getEpisodeData(number):
    '''return episode data as dictionary'''
    data = conexion.hgetall(number)
    return data


def setEpisodeStatus(number, newStatus):
    '''Set status's episode'''
    data = getEpisodeData(number)
    currentStatus = data["status"]
    if currentStatus != newStatus:
        conexion.hset(number, "status", newStatus)

def getReservedEpisodes():
    conRes = connect_db(1)
    number_list = conRes.keys("*")
    episodes_list = []
    if number_list:
        for number in number_list:
            episode = getEpisodeData(number)
            episodes_list.append(episode)
        episodes_list.sort(key=lambda e: int(e['number']))
    return episodes_list


# ReservedDB's functions

def addToReservedDB(number):
    conexionReserved.setex(number, 15, "Reserved")


def deleteToReservedDB(number):
    conexionReserved.delete(number)
