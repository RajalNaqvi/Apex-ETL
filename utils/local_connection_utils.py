import os
import json

directory = f'{os.getcwd()}/.local'
json_files_data = None

def create_con_directory():
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Directory '{directory}' created successfully.")
    else:
        print(f"Directory '{directory}' already exists.")


def read_all_configs(configs):
    json_files_data=[]
    for config in configs:
        file_path = os.path.join(directory, f"{config}.json")
        with open(file_path) as json_file:
            json_data = json.load(json_file)
            json_data_with_filename = {
                'filename': config,
                'data': json_data
            }
            json_files_data.append(json_data_with_filename)
    return json_files_data


def store_connection_config(filename,json_data):
    try:
        with open(f"{directory}/{filename}.json", 'w') as file:
            json.dump(json_data, file, indent=4)
            return True
    except Exception as e:
        return False


def get_all_connection_configs():
    return [
        filename.replace(".json", "")
        for filename in os.listdir(directory)
        if filename.endswith('.json')
    ]
    
def read_config(config):
    json_data_with_filename = {}
    file_path = os.path.join(directory, f"{config}.json")
    try:
        with open(file_path) as json_file:
            json_data = json.load(json_file)
            json_data_with_filename = {
                'filename': config,
                'data': json_data
            }
    except Exception as e:
        return json_data_with_filename
    return json_data_with_filename


def read_all_configs():
    configs = get_all_connection_configs()
    for config in configs:
        with open(f"{directory}/{config}.json") as json_file:
            data = json.load(json_file)

        python_data = []
        jdbc_data = []

        if data.get('connection_type') == 'python':
            python_data.append({"connection_name":config,"connection":data})
        elif data.get('connection_type') == 'jdbc':
            jdbc_data.append({"connection_name":config,"connection":data})
                
        return {"python": python_data,"java": jdbc_data}