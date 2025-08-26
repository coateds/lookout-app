# Multi environment DEVOps pipeline for Flask App with SQL Database

CoPilot thread:  GitHub actions deploy lookout app

## Checkpoint: flask configured to start new configuration, lookout db is built, flask migrate creates one table
- This works in both local and codespaces environment

## Need to make my last direct check in to Master
  - todo: tag it

## Lifecycle of the environments

### Local Dev
- Do major dev work here
- Start Procedure
  - From the lookout-app workspace: `docker compose up --build`
  - From the lookout-app workspace: vscode ctrl+shft+p > Dev Containers: Attach to running...  > lookout-app-flask-app-1
  - From the opened container in VSCode (purple): `flask run --host=0.0.0.0 --port=5000`
    - This will build the "lookout" database
  - From local browser, validate
    - http://localhost:5000/ > Simple Message:  Welcome to the website!
    - http://localhost:5000/env
    - http://localhost:5000/db-check
  - Note that the lookout database will be empty
  - From the opened container in VSCode (purple) sync db objects to models
    - run `flask db migrate -m "[comment]"`
    - make adjustments to the python file created in versions (like comment out system tables that should not be dropped)
    - finally run `flask db upgrade`
  - Changes to models.py > migrate to database
    - put new talbe(s) in models.py
    - in __init__.py edit from .models import User to include new tables e.g. `from .models import User, Event`
    - run `flask db migrate -m "[comment]"`
    - make adjustments to the python file created in versions (like comment out system tables that should not be dropped)
    - finally run `flask db upgrade`
    - I assume these changes will automatically be there the next time I build? (yes, but still need to `flask db migrate/upgrade`)
- Shutdown procedure
  - From the lookout-app workspace: ctrl + c, [enter], wait for everything to stop
  - `docker compose down`

### Codespaces Dev
- codespaces are built from any branch
- Make sure all changes to that branch are commited and pushed to the branch
- In the GitHub webpage, on the desired branch, click the grean CODE button, then click Create codespace on [branch]
  - Wait for five min
- Codespaces opens in a Web VSCode interface
- In the terminal run `flask run --host=0.0.0.0 --port=5000`
- Go to the ports tab of the bottom pane
- click the open in browser icon next to the forwarded port to 5000??
- The database will need to be sync'd to modesl using the same process as for local dev

in codespaces: Error: No such command 'db'. means I still have to run export FLASK_APP=website:create_app for that shell
ps aux | grep flask

### CI Dev
- GitHub Action Workflow that builds the dev environment in GitHub "cloud", then tears it down
- triggered by push to dev and master
- View result on GitHub webpage actions tab
- capable of running pytest
  - in lookout-app\tests\test_smoke.py


## Dev environment - Local
- Two Linux containers
  - Custom Flask app container with code and connection to ...
  - A pre-built SQL server container
- From VSCode on laptop
  - ctrl + Shft + P
  - dev containers: attach to running container
  - Select the dev container
- Dev process using two contaners
  - Docker-Desktop must be running!
  - Open the lookout-app Workspace. (CL\dev\lookout app)
  - Run docker compose up --build
  - dev containers: attach to running container
  - http://localhost:5000/[route]
- Shutting down:
  - Option 1 > docker compose down
  - Option 2 > in the terminal where docker compose up --build was run, press ctrl + c and then enter to see the containers shutting down.
- Use docker ps -a to see the containers that are running (or exited):
  - if the containers show as exited and they need to be rebuilt, use docker compose down first.

## Dev Environment - codespaces
export FLASK_APP=app/main.py  No!!  S/B export FLASK_APP=website:create_app
flask run --host=0.0.0.0 --port=5000

This should produce an output in the terminal indicating that Flask is running

go to the ports tab of the codespaces terminal pane
for a link to the Flask app in a browser

## GitHub Secrets

🧭 Environment Overview
| Environment    | Secrets Source | Notes                            | Secret Type
| Dev Local      | .env file      | Local-only, not synced to GitHub | .env
| Dev Codespaces | GitHub Secrets | Injected via devcontainer.json   | GH repository secret
| Staging        | GitHub Secrets | Used in GitHub Actions workflows | GH environment secret (stg)
| Production     | GitHub Secrets | Used in GitHub Actions workflows | GH environment secret (prod)


## Debugging in the codespaces environment
It is possible to simply write code in the codespaces VSCode like normal. To Rerun the Flask application:
- export FLASK_APP=app.main:app
- Running on http://0.0.0.0:5000



## tagged a "good" build
- git add .
- git commit -m "Stable local dev setup: Dockerfile, .env handling, requirements.txt"
- git tag -a local-dev-stable-v1 -m "Stable local dev environment with working Docker build"
- git push origin master
- git push origin local-dev-stable-v1

- To checkout this exact state later: git checkout local-dev-v1


SSMS access to Azure SQL DB
coateds-sql-server.database.windows.net
SQL Server Authentication
Username: coateds
Password: sqH***B***

SSMS Access to database on Dev Container
localhost,1433
SQL Server Authentication
sa
YourStrong!Passw0rd
- Check the box: Trust server certificate

