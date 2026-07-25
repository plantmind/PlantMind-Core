import json


def to_json(data):
    return json.dumps(data, indent=4)


def from_json(data):
    return json.loads(data)
