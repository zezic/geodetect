from netaddr import IPAddress
from flask import Flask, request, jsonify

with open('cidr_optim.txt', 'r') as f:
    ranges = f.read().splitlines()
ranges = [r.split('\t') for r in ranges]
ranges = [{
    'ip1': r[2].split(' - ')[0],
    'ip2': r[2].split(' - ')[1],
    'city_id': r[4]
} for r in ranges]

with open('cities.txt', 'r') as f:
    cities = f.read().splitlines()
cities = [c.split('\t') for c in cities]
cities = dict([(c[0], c[1]) for c in cities])

cache = {}

def get_city_by_ip(my_ip):
    from_cache = cache.get(my_ip)
    if from_cache:
        return from_cache
    for r in ranges:
        if IPAddress(r.get('ip1')) < IPAddress(my_ip) < IPAddress(r.get('ip2')):
            city_id = r.get('city_id')
            city = cities.get(city_id)
            cache[my_ip] = city
            return city
    cache[my_ip] = 'Москва'

app = Flask(__name__)

@app.route('/api/my_city')
def get_city():
    my_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    city = get_city_by_ip(my_ip)
    print('IP:', my_ip, 'CITY:', city)
    if city:
        return city
    else:
        return 'Москва'

@app.route('/api/my_city/<my_ip>')
def get_city_custom(my_ip):
    city = get_city_by_ip(my_ip)
    print('CUSTOM IP:', my_ip, 'CITY:', city)
    if city:
        return city
    else:
        return 'Москва'

app.run(port=7341, debug=True)
