from clarifai.rest import ClarifaiApp
from clarifai.rest import Image as ClImage
import os
import json
import urllib.request as urllib2
from flask import redirect
app = ClarifaiApp()
model = app.models.get('food-items-v1.0')


def get_ingredients(image_url=None, image_path=None):
    if image_url:
        image = ClImage(url= image_url)
    else:
        image = ClImage(file_obj=open(image_path, 'rb'))
    response= model.predict([image])
    ingredients = []
    cnt = 0
    if (response['status']['code'] == 10000):
        for i in response['outputs']:
            for j in i['data']['concepts']:
                if j['value'] > .7 and cnt < 3:
                    ingredients.append(j['name'])
                    cnt += 1
                else:
                    return ingredients
        return ingredients


def food2fork_util(query, mode):
    if mode == 'search':
        url = "http://food2fork.com/api/search?key=" + os.environ['FOOD_2_FORK_API_KEY'] + "&q=" + query + "&sort=r"
    else:
        url = "http://food2fork.com/api/get?key=" + os.environ['FOOD_2_FORK_API_KEY'] + "&rId=" + query + "&sort=r"
    url_req = urllib2.Request(url, headers={'User-Agent': 'Chrome/69', 'Content-Type': 'application/json'},
                              method='GET')
    response = urllib2.urlopen(url_req).read().decode('utf8')
    response_json = json.loads(response)
    return response_json


def get_recipe(image_url=None, filename=None, flag=None):
    if flag == 'url':
        ingredients = get_ingredients(image_url)
    else:
        ingredients = get_ingredients(image_path='static/uploads/' + filename)
    ing = ",".join(ingredients)
    print(ing)
    search_response = food2fork_util(ing, mode='search')
    result = []
    if search_response['count'] == 0:
        return "No recipes found! "
    else:
        for i in range(min(5, search_response['count'])):
            get_response = food2fork_util(search_response['recipes'][i]['recipe_id'], mode='get')
            search_response['recipes'][i]['ingredients'] = ",".join(get_response['recipe']['ingredients'])
            result.append(search_response['recipes'][i])
        return result

if __name__ == "__main__":
    main()