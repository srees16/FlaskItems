from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required

from security import authentication, identify

app = Flask(__name__)
app.secret_key = 'mysecretkeyherecantbebroken'
api = Api(app = app)

jwt = JWT(app, authentication, identify) # JWT creates new end point /auth

items = []

class Item(Resource):
    
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True, help='mandatory field')
        
    @jwt_required()
    def get(self, name):
        '''for item in items:
            if item['name'] == name:
                return item'''
        item = next(filter(lambda x: x['name'] == name, items), None)
        return {'item': item}, 200 if item else 404
        return {'error': 'item not found'}, 404
    
    @jwt_required()
    def post(self, name): # force=True doesn't need content-type header, format as per payload
        if next(filter(lambda x: x['name'] == name, items), None):
            return {'message': 'item {} already exists'.format(name)}, 400
        #data = request.get_json(force=True) # returns none instead of error
        data = Item.parser.parse_args()
        item = {'name': name, 'price': data['price']}
        items.append(item)
        return item, 201
    
    @jwt_required()
    def put(self, name):
        data = Item.parser.parse_args()
        #data = request.get_json(force=True)
        for item in items:
            if item['name'] == name:
                item.update(data)
            else:
                item = {'name': name, 'price': data['price']}
                items.append(item)
            return item
    
    @jwt_required()
    def delete(self, name):
        global items
        items = list(filter(lambda x: x['name'] != name, items))
        return {'message': 'item deleted'}


class Item_List(Resource):
    
    def get(self):
        return {'items': items}

api.add_resource(Item, '/item/<string:name>')
api.add_resource(Item_List, '/items')

if __name__ == '__main__':
    app.run(host='127.0.0.4', port=3000, debug=False)