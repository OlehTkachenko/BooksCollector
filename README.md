# BooksCollector
Test pet-project for practice Docker and Docker-Swarm

### Test pet-project for practice Docker and Docker-Swarm

![alt text](docs/Diagram.png)

### Plan 
- [x] Create script which will collect best books form [Yakaboo](https://www.yakaboo.ua/ua/knigi/dobirki-yakaboo.html)
- [X] Create docker/docker compose file which will create 2 containers. One for python script. Second one for PostgressDB.
- [X] Make collect python script save all datas in DB.
- [] Add logging to code
- [] Optimize, rewrite code, change all todo places.
- [] Add docker volume for logs.
- [] Create script for getting data from DB in CSV format.
- [] change diagram.
- [] add description to project, and describe stack.

### How to run
1. Create file `.env` and add this 2 lines to this file:
    - `POSTGRES_PASSWORD=1123` (Change the password to whatever you want)
    - `POSTGRES_PORT=5432 ` (If port 5432 closed for you change value)
2. run `docker-compose build`
3. run `docker-compose up`
4. Now you can check collected logs in DB.`psql -h localhost -p {your_port} -U collector BooksDB` and enter your pass.
5. Select all records from table books. `select * from books;` 