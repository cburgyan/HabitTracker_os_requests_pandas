import requests
import os


CREATE_USER_PIXELA_ENDPOINT = "https://pixe.la/v1/users"
USERNAME = os.environ.get("USERNAME")
PIXELA_TOKEN = os.environ.get("PIXELA_TOKEN")
CREATE_GRAPH_PIXELA_ENDPOINT = f"{CREATE_USER_PIXELA_ENDPOINT}/{USERNAME}/graphs"

pixela_parameters = {
    "token": PIXELA_TOKEN,
    "username": USERNAME,
    "agreeTermsOfService": "yes",
    "notMinor": "yes",
}

# #Create User
# pixela_response = requests.post(url=CREATE_USER_PIXELA_ENDPOINT, json=pixela_parameters)
# print(pixela_response.text)

pixela_graph_create_parameter = {
    "id": "codestudy1",
    "name": "Code Study",
    "unit": "minutes",
    "type": "int",
    "color": "ajisai"
}

pixela_headers = {
    "X-USER-TOKEN": PIXELA_TOKEN
}

# Create Pixela graph
create_graph_response = requests.post(url=CREATE_GRAPH_PIXELA_ENDPOINT,
                                      json=pixela_graph_create_parameter,
                                      headers=pixela_headers)
print(create_graph_response.text)
