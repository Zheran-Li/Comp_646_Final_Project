# -*- coding: utf-8 -*-
"""Untitled8.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1UrEc_OZNJVHDf9VWSANKU_ZLDo7RM_hW
"""

!pip install replicate

# using API token to open replicate to get access to the model
from getpass import getpass
import os

REPLICATE_API_TOKEN = getpass()
os.environ["REPLICATE_API_TOKEN"] = REPLICATE_API_TOKEN

# Load the data file
import json

# Open the text file
with open('youtube_data.txt', 'r') as f:
    # Load the JSON data from the file
    data = json.load(f)

# Using the pretrained model to generate captions
for data_dict in data:
  for video in data_dict['items']:
    image_url = video['snippet']['thumbnails']['high']['url']
    img_data = requests.get(image_url).content
    with open('image_name.jpg', 'wb') as handler:
      handler.write(img_data)
    import replicate
    output = replicate.run(
        "rmokady/clip_prefix_caption:9a34a6339872a03f45236f114321fb51fc7aa8269d38ae0ce5334969981e4cd8",
        input={"image": open('image_name.jpg', "rb")}
    )
    # save the predicted caption
    video['snippet']['predict_title'] = output

# Dump the data into a json file for further similarity test
with open('data.json', 'w') as f:
    json.dump(data, f)