import json
import werkzeug



def read_js(name):
    with open(name, 'r', encoding='utf-8') as f:
        return json.load(f)

def write_js(name, data):
    with open(name, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)

def set_key(method, key):
    data = read_js('data/api_keys.json')
    data[method] = werkzeug.security.generate_password_hash(key)
    write_js('data/api_keys.json', data)

def check_key(method, key):
    try:
        hashed_key = read_js('data/api_keys.json')[method]
    except KeyError:
        return 'unknown key'
    return werkzeug.security.check_password_hash(hashed_key, key)


if __name__ == '__main__':
    print(write_js('api_keys.json', {'register': ['lalala']}))