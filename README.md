# Server
Server-side scripts to be run on the same instance as MongoDB

## Server Requirements:
- NodeJS
- NPM
- Python 2.7
- pip
- MongoDB

## ToDo (on Server):
- Add Tweepy & Twitter access codes to config.py
- Modify permission of initScript `chmod 700 initScript`, and run `./initScript`
- Save/Copy [mongod.conf](https://gist.github.com/vanshdassani/b59c035829f5a30d7095894c19ad7bab) to /etc/mongod.conf on your server
- Start mongoDB `sudo service mongod start`
- Create user accounts with read/write access (see [MongoDB Docs](https://docs.mongodb.com/manual/tutorial/create-users/) and details below)
- Add username & password (tweetUploader) to index.js file
- Modify permission of tweetScript `chmod 700 tweetScript`, and run in background `nohup ./tweetScript > tweetScript.out 2>&1 &`

### MongoDB Users to create
- admin: roles [ userAdminAnyDB, dbOwner; database: admin, meteor, local ]
- ventisApp: roles [ readWrite; database: meteor ]
- tweetUploader: roles [ readWrite; database: meteor ]

### Additional MongoDB commands (on Server)
- start MongoDB: `sudo service mongod start`
- stop MongoDB: `sudo service mongod stop`
- restart MongoDB: `sudo service mongod restart`
- check status: `vi /var/log/mongodb/mongod.log`
- edit config: `sudo vi /etc/mongod.conf`
- enter mongo console w/admin: `mongo --port 3000 -u "<USERNAME>" -p "<PASSWORD>" --authenticationDatabase "admin"`
- enter mongo console w/out admin: in terminal -> `mongo --port 3000` ; in mongoshell -> `use admin; db.auth("<USERNAME>","<PASSWORD>")`
