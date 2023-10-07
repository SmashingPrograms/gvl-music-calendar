SETUP INSTRUCTIONS

Initial setup:
- Clone repository
- Install python (see instructions provided by CG) [TBA]
- In command line, cd into gvl-music-calendar folder
- Get required packages: ```pip3 install -r requirements.txt```

Run React frontend:
- Cd into frontend
- Npm install
- npm run dev

Running Flask server (backend):
- Tab 2
- Cd into backend
- python3 app.py

Installing ElasticSearch (“database”):
- First! Make sure you have at least 10% of your disk space free. Elasticsearch will fail a node and have an empty cluster otherwise.
- Go to the Elasticsearch (ES) downloads page
- Choose your platform (e.g. Mac 64-bit)
- enter your code directory- cd ~/code 
- untar the ES file you downloaded
- tar zxvf ~/Downloads/elasticsearch-8.10.2-darwin-x86_64.tar.gz
- enter the directory: cd elasticsearch-8.10.2
- edit the config file: code ./config/elasticsearch.yml (or manually open this file using your VSCode)
- change the cluster.name param to music-calendar-dev
- start ES: bin/elasticsearch
- open a new terminal window (change to the elastic dir again if needed), then enter this command to create a password for your elastic user:
- bin/elasticsearch-reset-password -a -u elastic
- Copy the password when it is output on the terminal
- Create file, username.txt - elastic username "elastic"
- Create file, password.txt - elastic pw the one you copied

(More to be added later: Kibana installation and setup, authorize Google applications, create mock data)