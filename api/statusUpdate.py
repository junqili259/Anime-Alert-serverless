from sanic import Sanic
from sanic.response import json
import requests

app = Sanic()

@app.route('/')
@app.route('/<path:path>')
async def getShow(request, path=""):

    id = int(request.args.get('id'))

    url = "https://graphql.anilist.co"
    
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

    return json(response.json())