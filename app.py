"""Flask"""

from flask import Flask, jsonify, request

app = Flask(__name__)

stores = [
    {
     'name': 'primary',
     'items': [
         {
             'name': 'book',
             'price': 53
             }
         ]
     }
]


# get
@app.route('/stores', methods = ['GET'])
def get_stores():
    return jsonify({'all stores': stores})


# get
@app.route('/store/<string:name>', methods = ['GET'])
def get_store(name):
    for store in stores:
        if store['name'] == name:
            return jsonify(stores)
        return jsonify({'error': 'store not found'})


# get items in the store
@app.route('/store/<string:name>/item')
def get_items_in_store(name):
    for store in stores:
        if store['name'] == name:
            return jsonify({'items': store['items']})
    return jsonify({'error': 'store not found'})


# post
@app.route('/store', methods = ['POST'])
def create_store():
    request_data = request.get_json()
    new_store = {
        'name': request_data['name'],
        'items': []
        }
    stores.append(new_store)
    return jsonify(new_store)


# post
@app.route('/store/<string:name>/item', methods = ['POST'])
def create_item_in_store(name):
    request_data = request.get_json()
    for store in stores:
        if store['name'] == name:
            new_item = {
                'name': request_data['name'],
                'price': request_data['price']
                }
            store['items'].append(new_item)
            return jsonify(new_item)
    return {'error': 'store not found'}


# delete
@app.route('/store/<string:name>', methods = ['DELETE'])
def delete_store(name):
    for store in stores:
        if store['name'] == name:
            stores.remove(name)
        return {'message': 'item deleted'}
    return {'error': 'item not found'}


if __name__ == '__main__':
    app.run(host = '127.0.0.8', port = 4000, debug = False)