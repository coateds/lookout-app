# Multi environment DEVOps pipeline for Flask App with SQL Database

CoPilot thread:  GitHub actions deploy lookout app

## Dev environment
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

