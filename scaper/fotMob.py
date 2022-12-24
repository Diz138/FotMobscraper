# Libraries
from selenium import webdriver
import time
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import pandas as pd
import numpy as np
import psycopg2
from sqlalchemy import create_engine


# Creating a scraping function that allows the user to input teams and it will return xG data from their games
def scrape(team, weeks):
    # Setting up driver and url
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.maximize_window()

    # Creating Lists to store scraped data
    loc_x = []
    loc_y = []
    player = []
    xG = []
    shot_type = []
    situation = []
    result = []
    home = []
    away = []
    date = []
    minute = []
    player_shot = pd.DataFrame()

    # Retrieving Fotmob website
    driver.get('https://www.fotmob.com/')

    # Finding search bar
    input = driver.find_element(By.XPATH, value='// *[ @ id = "__next"] / header / section / div / section / div / \
    input')

    # Searching for given team
    input.send_keys(team)
    input.send_keys(Keys.RETURN)
    time.sleep(5)
    team_url = driver.find_element(By.XPATH, value='// *[ @ id = "__next"] / main / div[2] / section / div[3] / div[2] \
    / a[1]').get_attribute('href')

    # Storing team name
    team_name = driver.find_element(By.XPATH, value='// *[ @ id = "__next"] / main / div[2] / section / div[3] / div[2] \
    / a[1]').text

    # Going given number of previous games
    for i in range(weeks):
        # Getting to the fixture page of the given team
        driver.get(team_url[:34] + 'fixtures' + team_url[42:])

        # Making sure the game has been played
        if driver.find_element(By.XPATH, value='//*[@id="__next"]/main/section/section/div/section/div[2]/a[' + str(
                i + 1) + ']/div[2]/div/div/span').text.__contains__(':') == False:
            time.sleep(5)

            # Retrieving link to game page
            game_url = driver.find_element(By.XPATH, value='//*[@id="__next"]/main/section/section/div/section/div[2]/a\
            [1]').get_attribute('href')
            driver.get(game_url)

            home_team = driver.find_element(By.XPATH, value='//*[@id="MatchFactsWrapper"]/div/div[1]/div[1]/section/div\
            [2]/section[2]/header/a[1]/div/span/span').text

            away_team = driver.find_element(By.XPATH, value='//*[@id="MatchFactsWrapper"]/div/div[1]/div[1]/section/div[\
            2]/section[2]/header/a[2]/div/span/span').text

            date_game = driver.find_element(By.XPATH, value='//*[@id="MatchFactsWrapper"]/div/div[1]/div[1]/section/div[\
            2]/div[3]/section/ul/li[1]/div/time/span[1]').text

            # Getting data if given team was at home for game
            if home_team == team_name:
                for my_elem in driver.find_elements(By.ID, value='circle'):
                    if float(my_elem.get_attribute('cx')) < 50:
                        try:
                            my_elem.click()
                            home.append(home_team)
                            away.append(away_team)
                            date.append(date_game)
                            minute.append(int(my_elem.find_element(By.XPATH, value='//*[@id="MatchFactsWrapper"]/div/\
                            div[1]/div[5]/section/section/div[3]/div/div/div[1]/div[2]/div/span').text[:2]))

                            player.append(my_elem.find_element(By.XPATH, value='//*[@id="MatchFactsWrapper"]/div/div[1]\
                            /div[5]/section/section/div[3]/div/div/div[1]/div[1]/a/span').text)

                            xG.append(float(my_elem.find_element(By.XPATH, value='//*[@id="MatchFactsWrapper"]/div/div[\
                            1]/div[5]/section/section/div[3]/div/div/div[2]/div[2]/div[2]/span[1]').text))

                            shot_type.append(my_elem.find_element(By.XPATH, value='//*[@id="MatchFactsWrapper"]/div/div[\
                            1]/div[5]/section/section/div[3]/div/div/div[2]/div[1]/ul/li[1]/span[2]').text)

                            situation.append(my_elem.find_element(By.XPATH, value='//*[@id="MatchFactsWrapper"]/div/div\
                            [1]/div[5]/section/section/div[3]/div/div/div[2]/div[1]/ul/li[2]/span[2]').text)

                            result.append(my_elem.find_element(By.XPATH, value='//*[@id="MatchFactsWrapper"]/div/div[1]\
                            /div[5]/section/section/div[3]/div/div/div[2]/div[1]/ul/li[3]/span[2]').text)

                            loc_x.append(float(my_elem.get_attribute('cx')))
                            loc_y.append(float(my_elem.get_attribute('cy')))

                        except:
                            print("Non-clickable element")

            # Getting data if given team was away for game
            else:
                for my_elem in driver.find_elements(By.ID, value='circle'):
                    if float(my_elem.get_attribute('cx')) > 50:
                        try:
                            my_elem.click()
                            home.append(home_team)
                            away.append(away_team)
                            date.append(date_game)
                            minute.append(int(my_elem.find_element(By.XPATH, value='//*[@id="MatchFactsWrapper"]/div/\
                            div[1]/div[5]/section/section/div[3]/div/div/div[1]/div[2]/div/span').text[:2]))

                            player.append(my_elem.find_element(By.XPATH, value='//*[@id="MatchFactsWrapper"]/div/div[1]\
                            /div[5]/section/section/div[3]/div/div/div[1]/div[1]/a/span').text)

                            xG.append(float(my_elem.find_element(By.XPATH, value='//*[@id="MatchFactsWrapper"]/div/div[\
                            1]/div[5]/section/section/div[3]/div/div/div[2]/div[2]/div[2]/span[1]').text))

                            shot_type.append(my_elem.find_element(By.XPATH, value='//*[@id="MatchFactsWrapper"]/div/div[\
                            1]/div[5]/section/section/div[3]/div/div/div[2]/div[1]/ul/li[1]/span[2]').text)

                            situation.append(my_elem.find_element(By.XPATH, value='//*[@id="MatchFactsWrapper"]/div/div\
                            [1]/div[5]/section/section/div[3]/div/div/div[2]/div[1]/ul/li[2]/span[2]').text)

                            result.append(my_elem.find_element(By.XPATH, value='//*[@id="MatchFactsWrapper"]/div/div[1]\
                            /div[5]/section/section/div[3]/div/div/div[2]/div[1]/ul/li[3]/span[2]').text)

                            loc_x.append(float(my_elem.get_attribute('cx')))
                            loc_y.append(float(my_elem.get_attribute('cy')))

                        except:
                            print("Non-clickable element")

    # Adding data to dataframe
    player_shot['lastName'] = np.array(player)
    player_shot['home'] = np.array(home[:len(player)])
    player_shot['away'] = np.array(away[:len(player)])
    player_shot['date'] = np.array(date[:len(player)])
    player_shot['minute'] = np.array(minute)
    player_shot['xG'] = np.array(xG)
    player_shot['shot_type'] = np.array(shot_type)
    player_shot['situation'] = np.array(situation)
    player_shot['result'] = np.array(result)
    player_shot['locx'] = np.array(loc_x)
    player_shot['locy'] = np.array(loc_y)
    print(player_shot.head())
    driver.close()
    return player_shot


def pgConnection():
    conn_string = 'postgresql://zrlfhmhqeibxzu:5873169306599f59ad392397d506a6d6cc1f81e0b828c02a8b4accd84834347c@ec2-54-161-255-125.compute-1.amazonaws.com:5432/d4jkr1fqnjl76s'
    db = create_engine(conn_string)
    conn = db.connect()
    # Establishing the connection
    conn1 = psycopg2.connect(
        database="d4jkr1fqnjl76s", user='username',
        password='password',
        host='ec2-54-161-255-125.compute-1.amazonaws.com', port='5432'
    )
    conn1.autocommit = True
    # cursor
    cur = conn1.cursor()
    return cur, conn


if __name__ == '__main__':
    # Connecting to PG database
    cursor, conn = pgConnection()

    # Taking input from user
    team = input("Input team: ")
    games = int(input("Input number of games to pull data: "))

    # Inputting data returned from scrape into database
    scrape(team, games).to_sql('shots', conn, if_exists='replace')

    # testing = scrape(team, games)
    # testing.to_csv('testing.csv')
