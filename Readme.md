
# README

A website scraper specifically to scrap recipes from certain recipe websites. 
Based on [recipe_scrapers](https://github.com/hhursev/recipe-scrapers) and [peewee](https://github.com/coleifer/peewee).

Setup:
#### Prerequisites
* python 3.x
* postgresql 10+
* docker 18+
* docker-compose 1.26

#### To run the scraper
 * run `docker-compose up --build` & it should start the process
 * logs are placed in scraper-data/scraper.log
 * `docker ps` to list containers
 * `docker logs -f recipe-scraper` to check logs from the container
 * `docker exec -it recipe-scraper bin/bash` to log in to the container

To-Do:
 * Compatibility with other databases
 * Add Unit tests
 * Automating & scheduling the script using cron or some alternative
 * Website model to track progress and better scheduling
 * Better readme :p ?
