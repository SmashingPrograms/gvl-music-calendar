# Music Calendar
This is a simple event aggregation app. 

## Setup

### Prerequisites
- Python 3.11

### Python packages
- Install required packages: `pip3 install -r requirements.txt`

### Install ElasticSearch
> Before starting, make sure you have more than 10% of your disk space free. Elasticsearch will fail a node and have an empty cluster otherwise. 

- [Download Elasticsearch](https://www.elastic.co/downloads/elasticsearch)
  - Choose your platform (e.g. `macOS x86_64` for Intel Macs, `macOS aarch64` for Apple silicon)
- enter your code directory- cd ~/code 
- untar the ES file you downloaded
- `tar zxvf ~/Downloads/elasticsearch-VERSION-darwin-x86_64.tar.gz`
- enter the directory: `cd elasticsearch-VERSION`
- edit the config file: `code ./config/elasticsearch.yml` (or your editor of choice)
- change the `cluster.name` param to `music-calendar-dev`
- on terminal, start ES: `bin/elasticsearch`
- open a new terminal window (change to the elastic dir again if needed), then enter this command to create a password for your elastic user:
  - `bin/elasticsearch-reset-password -a -u elastic`
- Copy the password when it is output on the terminal
- Create file, `username.txt` - elastic username "elastic"
- Create file, `password.txt` - elastic pw the one you copied

### Google API access
- Open [Google Cloud Console](https://console.cloud.google.com/) and select a project or create a new one
- Navigate to the API & Credentials section
- Click the button at the top + Enable APIs and Services
- Ensure the following APIs are enabled on the project:
  - Calendar
  - Drive
- Select OAuth Consent Screen from the sidebar nav
  - Follow the prompts to set it up (probably start with Internal)
- Select Credentials from the sidebar nav
- Click + Create Credentials and then choose Create OAuth Client ID
- Follow the prompts and finally download the `credentials.json` file
- Place the `credentials.json` file in the root of your application

#### TODO: Kibana installation and setup, create mock data
> Kibana is useful for observability of your Elasticsearch data, but isn't strictly necessary to run the app. Mock data is also helpful for having some data for development, again not required.

## Running 
### Frontend
- `cd frontend`
- `npm install`
- `npm run dev`

### Backend
- `cd backend`
- `python3 app.py`
