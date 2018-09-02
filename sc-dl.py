#!/usr/bin/env python3

import requests
import argparse
import re
import codecs
import json
import urllib.request
import os

def get_id(data):
    try:
        song_id = re.findall('soundcloud://sounds:(.*?)"',data)[0]
        return song_id
    except Error:
        print('Could not find song')
        sys.exit()

def get_info(data):
    title = re.findall('"title":"(.*?)",',data)[0]
    title = codecs.getdecoder("unicode_escape")(title)[0]

    artist = re.findall('"username":"(.*?)",',data)[0]
    artist = codecs.getdecoder("unicode_escape")(artist)[0]

    return title, artist

def main():
    #create parser for url
    parser = argparse.ArgumentParser(description = "Download Soundcloud music")
    parser.add_argument("url", help = "Soundcloud url of the song")
    parser.add_argument("path", help = "Path where song will be saved")
    args = parser.parse_args()

    #fetch the data from the url
    r = requests.get(args.url)
    print("Fetched data")
    
    data = r.text

    song_id = get_id(data)
    print("Song id:",song_id)
    song_title, song_artist = get_info(data)
    print("Song title:",song_title)
    print("Song arist:",song_artist)

    CLIENT_ID = "kLve5Sh7JUSsPl5cCgQ7znRpV2fpzzu8"
    REQUEST_URL = "https://api.soundcloud.com/i1/tracks/{0}/streams?client_id={1}"

    json_url = REQUEST_URL.format(song_id,CLIENT_ID)
    json_data = requests.get(json_url)
    json_data = json.loads(json_data.text)

    file_url = json_data["http_mp3_128_url"]

    file_name = str(song_artist + " - " + song_title + ".mp3")
    file_name = os.path.join(args.path, file_name)
    urllib.request.urlretrieve(file_url,file_name)
    print("Downloaded song",file_name)

if __name__ == "__main__":
    main()
