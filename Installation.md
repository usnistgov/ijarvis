```
# Installation instructions for WSL Linux
sudo vi /etc/resolv.conf #[Change to 8.8.8.8]
wget -qO - https://www.mongodb.org/static/pgp/server-5.0.asc | sudo apt-key add -
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/5.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-5.0.list
sudo apt-get update
sudo apt-get install -y mongodb-org
mongod --version
cd / && cd home
mkdir -p ~/data/db
sudo mongod --dbpath ~/data/db
ps -e | grep 'mongod' [In a different terminal]
sudo apt install redis-server
(One time only)
>mongo
    use mgi
	db.createUser(
	{
	 user: "mdb_user1",
	 pwd: "AsdfgZxcvb1878",
	 roles: ["readWrite"], 
	 mechanisms:[  
     "SCRAM-SHA-1"
     ]
	}
	)
sudo service redis-server start
redis-server
pip install -r requirements.core.txt
pip install -r requirements.txt
cp .env_kc .env (In mdcs folder)
export DJANGO_SETTINGS_MODULE=mdcs.dev_settings
celery --app=mdcs worker -E -l info
celery --app=mdcs beat -l info
turned off oaipmh, saml2

python manage.py migrate --settings=mdcs.dev_settings
python manage.py runserver --settings=mdcs.dev_settings
Or,
python manage.py runserver --settings=mdcs.dev_settings localhost:8000

Other details:

My mdcs/.env

DJANGO_SECRET_KEY=YOUR_SECRET_KEY
SERVER_URI=http://127.0.0.1:8000
SERVER_NAME=MDCS
MONGO_HOST=localhost
MONGO_PORT=27017
MONGO_USER=mdb_user1
MONGO_PASS=AsdfgZxcvb1878
MONGO_DB=mgi
REDIS_HOST=localhost
REDIS_PORT=6379

My prod_settings.py
""" Development Settings
"""


from .settings import *
USE_EMAIL = True
SERVER_EMAIL = &#39; kamal.choudhary@nist.gov&#39;
ADMINS = [(&#39;knc6&#39;, &#39; kamal.choudhary@nist.gov&#39;),(&#39;blong&#39;, &#39;benjamin.long@nist.gov&#39;)]
MANAGERS = [(&#39;knc6&#39;, &#39; kamal.choudhary@nist.gov&#39;),(&#39;blong&#39;, &#39;benjamin.long@nist.gov&#39;)]
EMAIL_SUBJECT_PREFIX = "[JARVIS]"
EMAIL_HOST = "smtp.nist.gov"
EMAIL_POST = 25
```

python manage.py  dumpdata socialaccount --exclude contenttypes --indent 2 --settings=mdcs.dev_settings >social_users.json

python manage.py  loaddata social_users.json

##############

Newton

1) go to /data/workspace/cdcsstage/deploy/jarvis on the production server, 

2) change CDCS_VERSION to 3.4.0-2023-9-11 in settings/ENV, then copy ENV to .env 

3) and then run "./docker_clean.sh". 

 

If that doesn't work, you can try 

"docker_clean_all.sh" 

then we'll have to run ./add_users.sh, 

./add_social_users.sh, 

./load_optimade_db.sh.
