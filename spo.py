#!/usr/bin/env python

import requests
import psycopg2

# Connect to the database
conn = psycopg2.connect("dbname=voornameninliedjes user=remco")
cur = conn.cursor()
cur.execute("SELECT * FROM song;")
results = cur.fetchall()

for row in results:
    artist = row[1]
    a_id = str(row[0])
    question = {'q' : artist, 'type' : 'artist'}
    r = requests.get("https://api.spotify.com/v1/search", params=question)
    data = r.json()
    if len(data["artists"]["items"]) > 0:
        artist_id = data["artists"]["items"][0]["id"]
        SQL = "UPDATE song SET artist_spotify_id = %s WHERE id = %s;"
        cur.execute(SQL, [artist_id, row[0]])
    else:
    	artist_id = "unknown"
    print(artist + " with id " + a_id + " has spotify id " + artist_id)

conn.commit()

cur.close()
conn.close()

# Generate request to find artist
# question = {'q' : 'paul simon', 'type' : 'artist'}
# r = requests.get("https://api.spotify.com/v1/search", params=question)
# data = r.json()

# Extract the artist id
# artist_id = data["artists"]["items"][0]["id"]
# print(artist_id)

# Get the artist information based on the artist id
# r2 = requests.get("https://api.spotify.com/v1/artists/" + artist_id)
# print(r2.text)

