# MMO RPG from scratch


## Starting the server
The server can be started using the docker-compose file
    
    cd server
    docker-compose up --build

or running the `srv.py` after starting the mongodb
(to add persistent storage add `-v /my/own/datadir:/data/db` to the docker run command)

    cd server
    docker run --network=host --name mongo -p 27017:27017 MONGO_INITDB_DATABASE=mmorpg_db -d mongo
    python srv.py

Server will listen to port 1060 on your localhost

## Connecting the client
Just run `clt_game.py`
    
    python clt_game.py
