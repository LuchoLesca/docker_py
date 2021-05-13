import redis
from json import dumps, loads

data = {
    "season":{
        "1": {
            "episode": {
                "1": {"name": "The Mandalorian", "status": "Rent"},
                "2": {"name": "The Child", "status": "Allow"},
                "3": {"name": "The Sin", "status": "Reserve"},
                "4": {"name": "Sanctuary", "status": "Allow"},
                "5": {"name": "The Gunslinger", "status": "Allow"},
                "6": {"name": "The Prisioner", "status": "Allow"},
                "7": {"name": "The Reckoling", "status": "Allow"},
                "8": {"name": "Redemption", "status": "Allow"}
            },
        },
        "2": {
            "episode": {
                "9": {"name": "The Marshal", "status": "Reserve"},
                "10": {"name": "The Passanger", "status": "Rent"},
                "11": {"name": "The Heiress", "status": "Allow"},
                "12": {"name": "The Siege", "status": "Allow"},
                "13": {"name": "The Jedi", "status": "Allow"},
                "14": {"name": "The Tradegy", "status": "Allow"},
                "15": {"name": "The Believer", "status": "Allow"},
                "16": {"name": "The Rescue", "status": "Allow"}
            }
        }
    }
}



def connect_db(database=0):
    '''Crea conexion a baea de datos'''
    # Esta conexion para db-redis en docker
    # conexion = redis.StrictRedis(host="db-redis", port="6379", db=0)
    
    # Esta conexion para db-redis en mi pc
    conexion = redis.StrictRedis(host="127.0.0.1", port="6379", db=database)
    if(conexion.ping()):
        print("Conectado a servidor de redis")
    else:
        print("error")
    return conexion

 
conexion = connect_db()
db_status = {"Available": 1, "Rented": 2, "Reserved": 3}
databases_pointers = {
    "Available": redis.StrictRedis(host="localhost", port=6379, db=1, charset="utf-8", decode_responses=True),
    "Rented": redis.StrictRedis(host="localhost", port=6379, db=2, charset="utf-8", decode_responses=True),
    "Reserved": redis.StrictRedis(host="localhost", port=6379, db=3, charset="utf-8", decode_responses=True)
}

def DBInit():

    conexion.flushall()

    seasons = ["1", "2"]
    conexion.set("seasons", dumps(seasons))
    # seasons : listasesonies(numeros)

    episodes_season_one = []
    episodes_season_two = []

    for num in range(1, 9):
        episodes_season_one.append(str(num))
    conexion.set("season1", dumps(episodes_season_one))
    # season1 : listaepisodios1(numeros)

    for num in range(9, 17):
        episodes_season_two.append(str(num))
    conexion.set("season2", dumps(episodes_season_two))
    # season2 : listaepisodios2(numeros)

    episodes = [
        {"season": "1", "status": "Available", "number": "1", "name": "The Mandalorian"},
        {"season": "1", "status": "Available", "number": "2", "name": "The Child"},
        {"season": "1", "status": "Available", "number": "3", "name": "The Sin"},
        {"season": "1", "status": "Available", "number": "4", "name": "Sanctuary"},
        {"season": "1", "status": "Available", "number": "5", "name": "The Gunslinger"},
        {"season": "1", "status": "Available", "number": "6", "name": "The Prisioner"},
        {"season": "1", "status": "Available", "number": "7", "name": "The Reckoling"},
        {"season": "1", "status": "Available", "number": "8", "name": "Redemption"},
        {"season": "2", "status": "Available", "number": "9", "name": "The Marshal"},
        {"season": "2", "status": "Available", "number": "10", "name": "The Passanger"},
        {"season": "2", "status": "Available", "number": "11", "name": "The Heiress"},
        {"season": "2", "status": "Available", "number": "12", "name": "The Siege"},
        {"season": "2", "status": "Available", "number": "13", "name": "The Jedi"},
        {"season": "2", "status": "Available", "number": "14", "name": "The Tradegy"},
        {"season": "2", "status": "Available", "number": "15", "name": "The Believer"},
        {"season": "2", "status": "Available", "number": "16", "name": "The Rescue"}
    ]

    # Seteo numeroepisodio : nombreepisodio
    for episode in episodes:
        conexion.set(episode["number"], dumps(episode["name"]))

    # Seteo nombreepisodio : diccionario con datos
    for episode in episodes:
        conexion.set(episode["name"], dumps({"status": episode["status"], "season": episode["season"], "number": episode["number"]}))

    conexion1 = connect_db(1)
    for episode in episodes:
        conexion1.set(episode["name"], "")


def getSeasons():
    '''return list of seasons numbers'''
    seasons = conexion.get("seasons")
    if seasons:
        return loads(seasons)
    else:
        return []


def getEpisodes(season):
    '''return array with episodes. Each index is a dict with number, name and status keys'''
    
    episodes = []

    episodes_number = conexion.get("season" + str(season))
    episodes_number = loads(episodes_number)

    for number in episodes_number:
        name = getEpisodeName(number)
        status = getEpisodeData(name)["status"]
        episodes.append({"number": number, "name": name, "status": status})
    return episodes

def getEpisodeData(name):
    '''return episode data (status, season) as dictionary'''
    data = conexion.get(name)
    data_json = loads(data)
    return data_json

def getEpisodeName(number):
    name_episode = loads(conexion.get(str(number)))
    return name_episode

# Este lo cree para el confirm_payment
def getEpisodeSeason(name):
    '''returns the season to which the episode belongs'''
    return getEpisodeData(name)["season"]

def getEpisodeStatus(name):
    '''returns the season to which the episode belongs'''
    return getEpisodeData(name)["season"]

def setEpisodeStatus(name, newStatus):
    '''Set status's episode'''
    data = getEpisodeData(name)
    currentStatus = data["status"]
    if currentStatus != newStatus:
        # Change attribute status in object
        data["status"] = newStatus
        conexion.set(name, dumps(data))
        # Move to corresponding db
        pointer = databases_pointers[currentStatus]
        pointer.move(name, db_status[newStatus])

def getReservedEpisodes():
    episodes_list = []

    puntero = databases_pointers["Reserved"]
    keys = puntero.keys("*")
    
    for name in keys:
        episode = getEpisodeData(name)
        episode["name"] = name
        episodes_list.append(episode)

    episodes_list.sort(key=lambda e: int(e['number']))

    return episodes_list
