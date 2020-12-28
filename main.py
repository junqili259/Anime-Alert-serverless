from typing import Optional
from fastapi import FastAPI, HTTPException
from datetime import datetime
from seasons import months, month_to_season
import requests


app = FastAPI()

url = "https://graphql.anilist.co"


@app.get("/")
def allShowsInSeason():
    
    # Automatically get the current season by month (WINTER, SPRING, SUMMER, FALL)
    current_month = int(datetime.today().strftime("%m"))
    month = months[current_month]
    season_now = month_to_season[month]

    year = int(datetime.today().strftime("%Y"))

    # Prevents displaying previous Winter seasonal shows due to year difference
    if month == "Dec":
        year = year + 1

    query = """query($season: MediaSeason, $seasonYear: Int, $page: Int) {
        Page(page: $page) {
            pageInfo {
                total
                perPage
                currentPage
                lastPage
                hasNextPage
            }
            media(season: $season, seasonYear: $seasonYear, type: ANIME){
                id
                title {
                    romaji
                    english
                }
                coverImage {
                    medium
                    large
                    extraLarge
                }
                episodes
                status
                nextAiringEpisode {
                    airingAt
                    timeUntilAiring
                    episode
                }
            }
        }
    }"""

    variables = {
        "season": season_now,
        "seasonYear": year,
        "page": 1
    }


    try:
        response = requests.post(url, json= {"query": query, "variables": variables})
    except requests.exceptions.ConnectionError as error:
        print("A Connection Error occured", error)

    currentPage = response.json()["data"]["Page"]["pageInfo"]["currentPage"]
    lastPage = response.json()["data"]["Page"]["pageInfo"]["lastPage"]
    animes = response.json()["data"]["Page"]["media"]

    
    for i in range(currentPage, lastPage + 1):

        currentPage = currentPage + 1
        variables["page"] = currentPage

        try:
            response = requests.post(url, json = {"query": query, "variables": variables})
        except requests.exceptions.ConnectionError as error:
            print("A Connection Error occured", error)
        
        currentPageAnime = response.json()["data"]["Page"]["media"]

        # Add anime on this page into anime list
        animes = animes + currentPageAnime
    
    animeList = {
        "media": animes
    }

    # return a list of ALL animes in the current season
    return animeList




@app.get("/season")
def anySeason(season: str, seasonYear: int, page: Optional[int] = 1):

    seasons = ['WINTER', 'SPRING', 'SUMMER', 'FALL']

    if season not in seasons:
        raise HTTPException(status_code= 400, detail= "Season syntax error. Example seasons: WINTER, SPRING, SUMMER, FALL")

    query = """query($season: MediaSeason, $seasonYear: Int, $page: Int) {
        Page(page: $page) {
            pageInfo {
                total
                perPage
                currentPage
                lastPage
                hasNextPage
            }
            media(season: $season, seasonYear: $seasonYear, type: ANIME){
                id
                title {
                    romaji
                    english
                }
                coverImage {
                    medium
                    large
                    extraLarge
                }
                episodes
            }
        }
    }"""

    variables = {
        "season": season,
        "seasonYear": seasonYear,
        "page": page
    }

    try:
        response = requests.post(url, json= {"query": query, "variables": variables})
    except requests.exceptions.ConnectionError as error:
        print("A Connection Error occured", error)

    return response.json()



@app.get("/statusUpdate")
def getShow(id: int):
    
    query = """query($id: Int) {
        Media(id: $id) {
            status
            episodes
            title {
                romaji
                english
            }
            nextAiringEpisode {
                airingAt
                timeUntilAiring
                episode
            }
        }
    }
    """

    variables = {
        "id": id
    }

    try:
        response = requests.post(url, json={"query": query, "variables": variables})
    except requests.exceptions.ConnectionError as error:
        print("A Connection Error occured", error)
    except requests.exceptions.InvalidURL as urlerr:
        print("Invalid Url error", urlerr)

    return response.json()
