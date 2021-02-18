Minesweeper API

Important considerations:

- Authtoken was used to manage users with the front end 

- Maximum and minimum were set for the game board considering the gameplay and the screen in which it would be used. These variables can be modified in the settings file 

- El api esta preparada para ser consumida localmente desde 127.0.0.1:3000. This can be modified in the variable CORS_ORIGIN_WHITELIST in the settings file 

Local deploy:

- Dependencies: Docker, docker-compose

- Instruction:
    - Build the images: `docker-compose -f local.yml build`
    - Up the images: `docker-compose -f local.yml up`

    - Send command to django api:  `docker-compose -f local.yml run --rm django <COMMAND>`
    - Run tests: `docker-compose -f local.yml run --rm django python manage.py test`