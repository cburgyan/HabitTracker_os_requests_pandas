import requests
import os
import datetime


CREATE_USER_PIXELA_ENDPOINT = "https://pixe.la/v1/users"
USERNAME = os.environ.get("USERNAME")
PIXELA_TOKEN = os.environ.get("PIXELA_TOKEN")
CREATE_GRAPH_PIXELA_ENDPOINT = f"{CREATE_USER_PIXELA_ENDPOINT}/{USERNAME}/graphs"
GRAPH_NAME = "codestudy1"
POST_PIXEL_PIXELA_ENDPOINT = f"{CREATE_GRAPH_PIXELA_ENDPOINT}/{GRAPH_NAME}"

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

# # Create Pixela graph
# create_graph_response = requests.post(url=CREATE_GRAPH_PIXELA_ENDPOINT,
#                                       json=pixela_graph_create_parameter,
#                                       headers=pixela_headers)
# print(create_graph_response.text)

today = datetime.datetime.now()
print(type(today))
previous_day = int(today.strftime("%Y%m%d")) - 2
previous_day2 = datetime.datetime(year=2022, month=5, day=20)
prev_day2 = previous_day2.strftime("%Y%m%d")
print(prev_day2)
post_parameters = {
    "date": str(prev_day2),
    "quantity": "310",
}

# # Create Pixel
# create_pixel_response = requests.post(url=POST_PIXEL_PIXELA_ENDPOINT,
#                                       headers=pixela_headers,
#                                       json=post_parameters)
# print(create_pixel_response.text)

update_pixel_parameters = {
    "quantity": "197"
}
update_date_full = datetime.datetime(year=2022, month=5, day=20)
update_date_wo_hours_and_minutes = update_date_full.strftime("%Y%m%d")
UPDATE_PIXEL_ENDPOINT = f"{POST_PIXEL_PIXELA_ENDPOINT}/{update_date_wo_hours_and_minutes}"

# Update Pixel
update_pixel_response = requests.put(url=UPDATE_PIXEL_ENDPOINT,
                                     headers=pixela_headers,
                                     json=update_pixel_parameters)

print(update_pixel_response.text)
