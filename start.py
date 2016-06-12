import requests
import config
import yaml
import os


def start():
    table_name = input("Enter the name of table you want to download file: ")
    enc_query = input("Enter the encoded query you want to query for: ")

    get_url = config.instance["get_api"] + table_name + "?sysparm_query=" + enc_query

    print "making a call to URL {0}".format(get_url)
    # make the get call.
    user_name = config.creds["user_name"]
    password = config.creds["password"]

    r = requests.get(get_url, auth = (user_name,password))

    print r.status_code

    json_returned = yaml.safe_load(r.text)
    folder_name = config.folder_location[table_name]

    results_array = json_returned["result"]

    for i in results_array:
        file_name = i["name"]
        script = i["script"]
        createFile(folder_name,file_name,script)




def createFile(folder_name, name,content):
    if name in config.exclude_file_name:
        print "Skipping the file name {0}".format(name)
        return
    try:
        print "writing file_name = {0}".format(name)
        name = name + ".js"
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

        with open(os.path.join(folder_name,name), 'wb') as temp_file:
            temp_file.write(content)
    except Exception as e:
        print "Error with the file name {0}".format(name)



start()


