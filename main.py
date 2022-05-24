import requests
import os
import pandas


CREATE_USER_PIXELA_ENDPOINT = "https://pixe.la/v1/users"
USERNAME = os.environ.get("USERNAME")
PIXELA_TOKEN = os.environ.get("PIXELA_TOKEN")
CREATE_GRAPH_PIXELA_ENDPOINT = f"{CREATE_USER_PIXELA_ENDPOINT}/{USERNAME}/graphs"
JAPANESE_COLOR_WORDS = ["shibafu", "momiji", "sora", "ichou", "ajisai", "kuro"]

graph_name = ""
graph_id = ""
graph_units = ""
graph_quantity_phrase = ""
graph_id_list = "codestudy1"
graph_name_and_id_list = pandas.read_csv("graphs.csv").to_dict(orient="records")
add_pixel_pixela_endpoint = f"{CREATE_GRAPH_PIXELA_ENDPOINT}/{graph_id}"


PIXELA_HEADERS = {
    "X-USER-TOKEN": PIXELA_TOKEN
}


def create_user():
    #NEEDS TO HAVE USERNAME AND TOKEN UPDATED NEED TO BE UPDATED IN THE EXECUTION ENVIRONMENT
    # FOR A NEW USER TO BE CREATED

    print("For New User to be created, please change the execution environment BEFORE running the program to reflect "
          "\nthe new username and authentication token!!")
    environment_variables_changed = input("Did you enter your new USERNAME "
                                          "and new authentication TOKEN? (yes or no) ").lower()
    if environment_variables_changed == "yes":
        global continue_program
        pixela_parameters = {
            "username": USERNAME,
            "token": PIXELA_TOKEN,
            "agreeTermsOfService": input("Do you agree to Pixela's Terms of Service? (yes or no) ".lower()),
            "notMinor": input("Are you a non-minor (an adult)? (yes or no) ").lower(),
        }

        #Create User
        pixela_response = requests.post(url=CREATE_USER_PIXELA_ENDPOINT, json=pixela_parameters)
        print(pixela_response.text)
        print("#####################\n")
    else:
        print("Please enter the new USERNAME and authentication TOKEN in "
              "the environment settings BEFORE running the program!")
        continue_program = False


def get_graph():
    global graph_id, graph_name, continue_program, add_pixel_pixela_endpoint, graph_units, graph_quantity_phrase
    count = 0
    action1 = 0
    while action1 != "exit" and int(action1) > count or int(action1) < 1:
        print("---------------------------------")
        print("Available Graphs:")
        count = 0
        for graph_pair in graph_name_and_id_list:
            count += 1
            print(f"{count}. {graph_pair['graph_name']}")
        count += 1
        print(f"{count}. Create NEW GRAPH.")
        count += 1
        print(f"{count}. Exit program.")
        action1 = input("Pick the number of the graph you'd like to work on: ")

    if int(action1) == count:
        continue_program = False
    else:
        if int(action1) == count - 1:
            create_new_graph()
        else:
            graph_name = graph_name_and_id_list[int(action1) - 1]["graph_name"]
            graph_id = graph_name_and_id_list[int(action1) - 1]["graph_id"]
            graph_units = graph_name_and_id_list[int(action1) - 1]["graph_units"]
            graph_quantity_phrase = graph_name_and_id_list[int(action1) - 1]["graph_quantity_phrase"]
            add_pixel_pixela_endpoint = f"{CREATE_GRAPH_PIXELA_ENDPOINT}/{graph_id}"


def create_new_graph():
    global graph_id, add_pixel_pixela_endpoint, graph_name, graph_units, graph_quantity_phrase
    color_number = int(input("What color should the graph be? \n"
                             "(1=green, 2=red, 3=blue, 4=yellow, 5=purple, or 6=black) "))
    color = JAPANESE_COLOR_WORDS[color_number - 1]

    graph_name = input("What is the name for the graph? ")
    graph_id = input("What should be the graphs id (Validation rule: ^[a-z][a-z0-9-]{1,16})? ")
    graph_units = input("What will the units in the graph be? ")
    graph_quantity_phrase = input(f"What phrase do you want to have in the following blank?:\nHow many {graph_units} ______________ on dayX? (eg. How many minutes did you study on dayX?)\n")
    graph_name_and_id_list.append({"graph_name": graph_name,
                                   "graph_id": graph_id,
                                   "graph_units": graph_units,
                                   "graph_quantity_phrase": graph_quantity_phrase})
    dataframe_name_and_id = pandas.DataFrame(graph_name_and_id_list)
    dataframe_name_and_id.to_csv("graphs.csv", index=False)
    add_pixel_pixela_endpoint = f"{CREATE_GRAPH_PIXELA_ENDPOINT}/{graph_id}"
    pixela_graph_create_parameter = {
        "id": graph_id,
        "name": graph_name,
        "unit": graph_units,
        "type": input("What is the type of the units? (int or float) "),
        "color": color
    }

    # Create Pixela graph
    create_graph_response = requests.post(url=CREATE_GRAPH_PIXELA_ENDPOINT,
                                          json=pixela_graph_create_parameter,
                                          headers=PIXELA_HEADERS)
    print(create_graph_response.text)
    print("#####################\n")


def add_datum():
    preprocessed_day = input("What day would you like to add?(YYYY/MM/DD) ")
    day = preprocessed_day.replace("/", "")
    # minutes = input(f"How many minutes did you study on {day}?")

    create_parameters = {
        "date": day,
        "quantity": input(f"How many {graph_units} {graph_quantity_phrase} on {preprocessed_day}? "),
    }

    # Create Pixel
    create_pixel_response = requests.post(url=add_pixel_pixela_endpoint,
                                          headers=PIXELA_HEADERS,
                                          json=create_parameters)
    print(create_pixel_response.text)
    print("#####################\n")


def delete_datum():
    preprocessed_day = input("What day would you like to change?(YYYY/MM/DD) ")
    day = preprocessed_day.replace("/", "")

    delete_pixel_response = requests.delete(url=f"{add_pixel_pixela_endpoint}/{day}", headers=PIXELA_HEADERS)

    print(delete_pixel_response.text)
    print("#####################\n")


def change_datum():
    preprocessed_day = input("What day would you like to change?(YYYY/MM/DD) ")
    day = preprocessed_day.replace("/", "")
    update_pixel_parameters = {
        "quantity": input(f"How many {graph_units} {graph_quantity_phrase} on {preprocessed_day}? ")
    }

    # Update Pixel
    update_pixel_response = requests.put(url=f"{add_pixel_pixela_endpoint}/{day}",
                                         headers=PIXELA_HEADERS,
                                         json=update_pixel_parameters)

    print(update_pixel_response.text)
    print("#####################\n")


continue_program = True
get_graph()
while continue_program:
    action = input("What would you like to do?\n1. ADD a datum\n2. DELETE a datum"
                   "\n3. CHANGE a datum\n4. EXIT program\n").lower()#\n5. Add new USER").lower()
    if action == "exit" or action == "4":
        continue_program = False
    elif action == "add" or action == "1":
        print("*************************")
        print("Adding Datum:")
        add_datum()
    elif action == "delete" or action == "2":
        print("*************************")
        print("Deleting Datum:")
        delete_datum()
    elif action == "change" or action == "3":
        print("*************************")
        print("Changing Datum:")
        change_datum()
    elif action == "user" or action == "5":
        print("*************************")
        print("Creating new User:")
        create_user()
    else:
        print(f"'{action}' is not a valid choice. Please choose: ADD, DELETE, CHANGE, or EXIT")


