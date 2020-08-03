FROM python:3

# install psycopg2 library with PIP
RUN pip3 install psycopg2
RUN pip3 install recipe_scrapers bs4 peewee

ADD . ./recipe-scraper

CMD [ "python", "./recipe-scraper/scraper.py" ]
