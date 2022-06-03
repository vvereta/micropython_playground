import ujson as json

def read_config(config_file='config.json'):
    with open(config_file) as json_file:
        return json.load(json_file)
