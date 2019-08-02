import json
with open('train.json', 'r') as f:
    distros_dict = json.load(f)

    print(distros_dict)