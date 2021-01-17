from sanic import Sanic
from sanic.response import json
from datetime import datetime
import requests
app = Sanic()


@app.route('/')
@app.route('/<path:path>')
async def index(request, path=""):
    url = "https://graphql.anilist.co"

    months = ["", "Jan", "Feb", "Mar", "Apr", "May", "June", "July", "Aug", "Sept", "Oct", "Nov", "Dec"]

    month_to_season = {
        "Jan": "WINTER",
        "Feb": "WINTER",
        "Mar": "SPRING",
        "Apr": "SPRING",
        "May": "SPRING",
        "June": "SUMMER",
        "July": "SUMMER",
        "Aug": "SUMMER",
        "Sept": "FALL",
        "Oct": "FALL",
        "Nov": "FALL",
        "Dec": "WINTER"
    }

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
                status
                nextAiringEpisode {
                    airingAt
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
    return json(animeList)
