import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def get_title_from_index(index):
	return df[df.index == index]["title"].values[0]

def get_index_from_title(title):
	return df[df.title == title]["index"].values[0]


df = pd.read_csv("movie_dataset.csv")


features = ['keywords','cast','genres','director']

for feature in features:
	df[feature] = df[feature].fillna('')

def combine_features(row):
	try:
		return row['keywords'] +" "+row['cast']+" "+row["genres"]+" "+row["director"]
	except:
		print ("Error:", row)	

df["combined_features"] = df.apply(combine_features,axis=1)


cv = CountVectorizer()

count_matrix = cv.fit_transform(df["combined_features"])


cosine_sim = cosine_similarity(count_matrix)
def movieRec(movie):
	movie_user_likes = movie

	movie_index = get_index_from_title(movie_user_likes)

	similar_movies =  list(enumerate(cosine_sim[movie_index]))


	sorted_similar_movies = sorted(similar_movies,key=lambda x:x[1],reverse=True)


	i=0
	sortedMovie = {}
	for element in sorted_similar_movies:
		temp = {i:get_title_from_index(element[0])}
		sortedMovie.update(temp)
		print (get_title_from_index(element[0]))
		i=i+1
		if i>4:
			break
	return sortedMovie




import flask
from flask import request, jsonify,render_template, Response, request, redirect, url_for
from flask_cors import CORS
from flask import send_file

import json
import io



# y = json.dumps(x)
#
app = flask.Flask(__name__)
CORS(app)
app.config["DEBUG"] = True



@app.route('/', methods=['GET'])
def home():
	return "welcome"

@app.route('/getmovie', methods=['GET'])
def getmovie():
	movie = request.args.get("movie", "")
	recom = movieRec(movie)
	print(recom)
	return jsonify(recom)


app.run()