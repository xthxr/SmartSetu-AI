import json

with open('credentials.json', 'r') as f:
    content = f.read()

print(json.dumps(content))
