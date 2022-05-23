import requests
import os


PIXELA_ENDPOINT = "https://pixe.la/v1/users"
USERNAME = os.environ.get("USERNAME")
PIXELA_TOKEN = os.environ.get("PIXELA_TOKEN")

pixela_parameters = {
    "token": PIXELA_TOKEN,
    "username": USERNAME,
    "agreeTermsOfService": "yes",
    "notMinor": "yes",
}

#Create User
pixela_response = requests.post(url=PIXELA_ENDPOINT, json=pixela_parameters)
print(pixela_response.text)