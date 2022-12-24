# FotMobscraper

This script extracts expected goals (xG) data from FotMob and stores it in a PostgreSQL database. It allows users to access and analyze xG data from various soccer leagues and tournaments around the world.

FotMob is a website and mobile app that provides real-time soccer scores, statistics, news, and updates for various leagues and tournaments around the world. It covers a wide range of soccer leagues and tournaments, including the major leagues in Europe, South America, and other regions, as well as international competitions such as the World Cup and the European Championship.

The FotMob.py file outlines how it scrapes the data and then inputs it into a PostgreSQL database. 

A user can input a team name and the number of weeks of data they would like to retrieve and the program will store this data it in a PostgreSQL database. The data stored is as follows:

| Player Name | Home Team | Away Team | Date of Game | Minute | xG | Shot type | Situation | Result | Locx | Locy |   

| Foden | Manchester City | Liverpool | December 22, 2022 | 84 | 0.05 | Left foot | Regular play | Attempt saved | 10.035 | 46.383 |


