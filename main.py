"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import Flask, render_template, request, json, jsonify
import requests
import json
from IPython.display import HTML
import matplotlib.pyplot as plt
from PIL import Image
from io import BytesIO
import pyodbc
from mailjet_rest import Client
import os

app = Flask(__name__)

subscription_key = "683934df678c4864b7d5f3ddbffffa3a"
assert subscription_key

search_url = "https://api.cognitive.microsoft.com/bing/v7.0/images/search"


@app.route('/')
def main():
    # return render_template(
    #     "index.html",
    #     title='Azure',
    #     year=datetime.now().year,
    # )
    return 'Hello, World!'

@app.route('/searchPhoto', methods=['POST'])
def searchPhoto():
    search_term = request.form['searchTab']

    headers = {"Ocp-Apim-Subscription-Key": subscription_key}
    params  = {"q": search_term, "textDecorations": True, "textFormat": "HTML"}
    response = requests.get(search_url, headers=headers, params=params)
    response.raise_for_status()
    search_results = response.json()
    thumbnail_urls = [img["thumbnailUrl"] for img in search_results["value"]]
    return json.dumps(thumbnail_urls)

@app.route("/getProp/<url>", methods=["POST"])
def getProp(url):
	print(url)
	subscription_key = "f3b511f4df724117af62d1fb82041eda"
	assert subscription_key
	vision_base_url = "https://westcentralus.api.cognitive.microsoft.com/vision/v1.0/"
	vision_analyze_url = vision_base_url + "analyze"
	
	url = "https://" + url.replace("~","/").replace("^","?")
	headers = {'Ocp-Apim-Subscription-Key': subscription_key }
	params = {'visualFeatures': 'Categories,Description,Color'}
	data = {'url': url}
	response = requests.post(vision_analyze_url, headers=headers, params=params, json=data)
	response.raise_for_status()
	analysis = response.json()
	image_caption = analysis["description"]["captions"][0]["text"].capitalize()
	return json.dumps(image_caption)

@app.route("/addInBd/<url>/<description>", methods=["POST"])
def addInBd(url, description):
    url = "https://" + url.replace("~","/").replace("^","?")
    server = 'azurebidi.database.windows.net'
    database = 'ImagesTornado'
    username = 'AzureBidi'
    password = 'Azure6598'
    driver= '{ODBC Driver 13 for SQL Server}'
    cnxn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1443;DATABASE='+database+';UID='+username+';PWD='+ password)
    cursor = cnxn.cursor()
    cursor.execute("INSERT INTO Image (ImageLink, ImageDescription) VALUES('" + url + "', '" + description.split("\"")[1] + "')")
    cnxn.commit()
    cnxn.close()
    return json.dumps("OK")

@app.route("/bd")
def changePage():
	return render_template(
		"bd.html",
		title='Azure',
		year=datetime.now().year,
    )


@app.route("/records", methods=["POST"])
def getAllRecords():
	server = 'azurebidi.database.windows.net'
	database = 'ImagesTornado'
	username = 'AzureBidi'
	password = 'Azure6598'
	driver= '{ODBC Driver 13 for SQL Server}'

	cnxn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1443;DATABASE='+database+';UID='+username+';PWD='+ password)
	cursor = cnxn.cursor()
	cursor.execute("SELECT * FROM Image")
	list = []
	for row in cursor.fetchall():
		list.append(row[1])
		list.append(row[2])
	return jsonify(list)


@app.route("/sendemail/<param>/<url>/<description>", methods=["POST"])
def sendEmail(param,url,description):
	print(param)
	print(url)
	print(description)
	url = "https://" + url.replace("~","/").replace("^","?")
	print(url)
	api_key = 'f3d6edc6f29603b8f65301bc7bbb204f'
	api_secret = '18c208510c66d1a76b65ee261920b5dd'
	mailjet = Client(auth=(api_key, api_secret), version='v3.1')
	data = {
	  'Messages': [
					{
							"From": {
									"Email": "cosmin.tofan@info.uaic.ro",
									"Name": "Greetings from Azure"
							},
							"To": [
									{
											"Email": param,
											"Name": param
									}
							],
							"Subject": "A happy image with description for a happy day!",
							"TextPart": description,
							"HTMLPart": "<h1>" + description + "</h1> <img src=\""+ url + "\" height=\"100%\" width=\"100%\">"
					}
			]
	}
	result = mailjet.send.create(data=data)
	print(result.status_code)
	print (result.json())
	return json.dumps("OK")
	
	
if __name__ == '__main__':
  app.run()
