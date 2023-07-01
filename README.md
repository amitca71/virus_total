installation (on mac or linux):
1. install python 3.7 +
2. install virtual env (pip install virtualenv)
3. python -m venv . (on project folder)
4. . ./bin/activate
5. pip install -r requirements.txt

pre requisite:
1. save site files as: /tmp/sites/my_sites.csv
2. have running redis locally, using default port (docker-compose up )

execution:
python app.py

comments:
- the records are stored on redis database and expires after 30 minutes
(this is for the excercise, for time saving... real life would use timetsmp on the record)
in order to have data up to date, need to execute frequency every less than 30 minutes (every 5 minutes)
- events log are written to file system, in real life, would be collected by logstash





