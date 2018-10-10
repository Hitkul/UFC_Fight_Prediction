import json

def get_names_of_faulty_files():
    with open("failed_history/files_with_different_template.txt", "r") as in_file:
        files = in_file.readlines()
    return files

def get_string_json_from_file(file_location):
    with open(file_location) as f:
        data = json.load(f)
    return str(data)

for file in get_names_of_faulty_files():
    str_json = get_string_json_from_file("data/fight_json/"+file.replace("\n",""))
    str_json = str_json.replace("[","{")
    str_json = str_json.replace("]","}")
    with open('data/fixed_json/'+file.replace("\n",""),w) as out:
        json.dump(eval(str_json),out, indent=4)

