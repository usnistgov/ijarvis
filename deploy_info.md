# Docker page: https://hub.docker.com/repository/docker/nistodi/cdcs_jarvis/general

cd  /data/workspace/cdcsstage/build/jarvis

STEP: 1 cd ../../build/jarvis, change CDCS_VERSION in ENV then copy ENV to .env

STEP: 2 ./docker_clean.sh

To redeploy all containers:

STEP: 1 cd  /data/workspace/cdcsstage/deploy/jarvis

change CDCS_VERSION in settings/ENV  and then cp settings/ENV  to .env

STEP: 2 ./docker_clean_all.sh

Wait for app to come up by checking URL.

docker_logs

Once up:

STEP3: ./add_users.sh, /.add_social_user.sh, ./load_optimade.sh

When change urls.py tell Karen (for others not jarvis)


First go to Jumpobox
Then go to phasedata
Go to deploy/jarvis directory
change CDCS_VERSION in settings/ENV  and then cp settings/ENV  to .env


docker_clean.sh (no docker_clean_all.sh because preserves the user data)



