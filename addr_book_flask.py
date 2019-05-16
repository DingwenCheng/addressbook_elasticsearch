from flask import Flask, request, jsonify, make_response
from elasticsearch import Elasticsearch
import json
import elasticsearch
import hashlib

# creating flask instance
app = Flask(__name__)
# connecting to elasticsearch
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

# default hello world endpoint
@app.route("/")
def hello():
    return "Hello World!"

"""
/contact
Endpoint for /contact?pageSize={}&page={}&query={} and POST /contact requests
The get request will query the elasticsearch for all document with the given
query parameter.
The post request will add new item to the elasticsearch, and use the unique name
to generate id using hash function
"""
@app.route("/contact", methods=['GET', 'POST'])
def contact_all():
    # get section
    if request.method == 'GET':
        if 'pageSize' in request.args:
            pageSize = int(request.args['pageSize'])
            if pageSize < 1:
                return make_response(jsonify({'error': 'Bad Request Parameter'}), 400)
        else:
            pageSize = 20

        if 'page' in request.args:
            page = int(request.args['page'])
            if page < 1:
                return make_response(jsonify({'error': 'Bad Request Parameter'}), 400)
        else:
            page = 1

        if 'query' in request.args:
            query = {'query': {'query_string': {'default_field': 'name', 'query': request.args['query']}}}
        else:
            query = {'query': {'match_all': {}}}

        res = es.search(index='addrbook', body=query)
        if page > 1:
            start = (page - 1) * pageSize
        else:
            start = 0
        if start > len(res['hits']['hits']):
            return make_response(jsonify({'error': 'Bad Request Parameter'}), 400)
        end = start + pageSize
        return make_response(jsonify(res['hits']['hits'][start:end]), 200)

    # post section
    elif request.method == 'POST':
        if 'name' in request.form and 'address' in request.form and 'phone' in request.form:
            name = str(request.form['name'])
            addr = str(request.form['address'])
            phone = str(request.form['phone'])
            if len(phone) >= 15 or not phone.isdigit():
                return make_response(jsonify({'error': 'Request Parameter Invalid'}), 400)
            hash_id = int(hashlib.sha1(name.encode()).hexdigest(), 16) % (10 ** 8)
            # duplicate check here
            try:
                res = es.get(index='addrbook', doc_type='address', id=hash_id)
                return make_response(jsonify({'error': 'Address already in database'}), 400)
            except elasticsearch.exceptions.NotFoundError:
                data = {"name": name, "address": addr, "phone": phone}
                res = es.index(index='addrbook', doc_type='address', id=hash_id, body=data)
                return make_response(jsonify(res), 200)
        else:
            return make_response(jsonify({'error': 'Request Parameter Missing'}), 400)
    else:
        return make_response(jsonify({'error': 'Method Not found'}), 400)


"""
/contact/<name>
Endpoint for GET/PUT/DELET /contact/{name} requests
The get request will return one document based on the unique name it provided
The put request will update one document if it is already exsiting in database
The delete request will delete one document if it is already exsiting in databse
"""
@app.route("/contact/<name>", methods=['GET', 'PUT', 'DELETE'])
def contact_name(name):
    try:
        hash_id = int(hashlib.sha1(name.encode()).hexdigest(), 16) % (10 ** 8)
        res = es.get(index='addrbook', doc_type='address', id=hash_id)
        # get section
        if request.method == 'GET':
            return make_response(jsonify(res['_source']), 200)
        # put section
        elif request.method == 'PUT':
            if 'address' in request.form or 'phone' in request.form:
                if 'address' in request.form:
                    addr = str(request.form['address'])
                else:
                    addr = res['_source']['address']
                if 'phone' in request.form:
                    phone = str(request.form['phone'])
                else:
                    phone = res['_source']['phone']
                # error checking
                if len(phone) >= 15 or not phone.isdigit():
                    return make_response(jsonify({'error': 'Request Parameter Invalid'}), 401)

                data = {"name": name, "address": addr, "phone": phone}
                res = es.index(index='addrbook', doc_type='address', id=hash_id, body=data)
                return make_response(jsonify(res), 200)
            else:
                return make_response(jsonify({'error': 'Request Parameter Missing'}), 402)
        # delete section
        elif request.method == 'DELETE':
            res = es.delete(index='addrbook', doc_type='address', id=hash_id)
            return make_response(jsonify(res), 200)
        else:
            return make_response(jsonify({'error': 'Method Not found'}), 400)
    except elasticsearch.exceptions.NotFoundError:
        return make_response(jsonify({'error': 'Not Found'}), 400)



if __name__ == '__main__':
    app.run(debug = True, host = 'localhost', port = 5000)
