#!/usr/bin/python3
from flask import Flask, jsonify, abort, make_response, request
from flask_cors import CORS
# from flask_restful import Api
import DB_main
import os

app = Flask(__name__)
# api = Api(app)
dbs = {}

for name in os.listdir('datasource/'):
    db = DB_main.DB()
    db.import_DB(name)
    dbs[name] = db

CORS(app, origins="http://127.0.0.1:19000", allow_headers=[
    "Content-Type", "Authorization", "Access-Control-Allow-Credentials", "Access-Control-Allow-Headers","Access-Control-Allow-Origin"],
    supports_credentials=True, intercept_exceptions=False)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.route('/laba_inf_tex/api/v1.0/get_DBs', methods=['GET'])
def get_DBs():
    return jsonify({'DB': list(dbs.keys())})

@app.route('/laba_inf_tex/api/v1.0/import_DB/<name>', methods=['GET'])
def import_DB(name):
    path = os.path.join('datasource/', name)
    exists = os.path.isfile(path)
    #return jsonify({path:exists})
    if exists:
        return jsonify(db.import_DB(name))
    abort(404)
'''{
	"names" : ["",""]
}
'''
@app.route('/laba_inf_tex/api/v1.0/<source>/diff_of_tables', methods=['POST'])
def diff_of_tables(source):
    if source not in dbs:
        abort(404)
    db = dbs[source]
    if not request.json or not 'names' in request.json:
        abort(400)
    names = request.json['names']
    if names[0] in db.tables and names[1] in db.tables:
        return jsonify({'records': db.diff_of_tables(names[0], names[1])})
    abort(404)

'''{
	"names" : ["",""]
}
'''
@app.route('/laba_inf_tex/api/v1.0/<source>/union_of_tables/<name_0>/<name_1>', methods=['POST'])
def union_of_tables(source,name_0,name_1):
    if source not in dbs:
        abort(404)
    db = dbs[source]
    if name_0 and name_1 in db.tables:
        return jsonify({'records': db.union_of_tables(name_0, name_1)})
    abort(404)

@app.route('/laba_inf_tex/api/v1.0/export_DB/<name>', methods=['GET'])
def export_DB(name):
    print(name)
    path = os.path.join('datasource/', name)
    exists = os.path.isfile(path)
    if exists:
        return (db.export_DB(name))
    abort(404)

@app.route('/laba_inf_tex/api/v1.0/create_DB/<name>', methods=['POST'])
def create_DB(name):
    #dbs[name] = DB_main.DB(name)
    db = dbs[name]
    return db
    #db.export_DB(name)
    #return jsonify({db})
    #return 201

'''{
	"table":"",
	"id":""
}'''

@app.route('/laba_inf_tex/api/v1.0/delete_DB/<name>', methods=['DELETE'])
def delete_BD(name):
    path = os.path.join('datasource/', name)
    exists = os.path.isfile(path)
    if exists:
        del dbs[name]
        os.remove(path)
        return jsonify({'result': True})
    abort(404)


@app.route('/laba_inf_tex/api/v1.0/delete_table/<source>/<name>', methods=['DELETE'])
def delete_table(source, name):
    if source not in dbs:
        abort(404)
    db = dbs[source]
    if name not in db.tables :
        abort(404)
    db.delete_table(name)
    export_DB(db.name)
    return jsonify({'result': list(db.tables.keys())})

@app.route('/laba_inf_tex/api/v1.0/<source>/get_table/<name>', methods=['GET'])
def get_table(source, name):
    if source not in dbs:
        abort(404)
    db = dbs[source]
    if name not in db.tables :
        abort(404)
    t = db.tables[name]
    return jsonify({'table': {'name': t.name,'columns':t.columns,'records': t.records}})



@app.route('/laba_inf_tex/api/v1.0/<source>/delete_record/<table>/<id>', methods=['DELETE'])
def delete_record(source,table,id):
    if source not in dbs:
        abort(404)
    db = dbs[source]
    # id = request.json['id']
    # table = request.json['table']
    if table not in db.tables :
        abort(404)
    t = db.tables[table]
    t.delete_record(int(id))
    export_DB(db.name)
    return jsonify({'result':t.records})
'''{
	"name":"",
	"columns":""
}
'''
@app.route('/laba_inf_tex/api/v1.0/<source>/create_table', methods=['POST'])
def create_table(source):
    print(source, [dbs.keys(), source in dbs])
    if source not in dbs:
        abort(404)
    db = dbs[source]
    name = request.json['name']
    columns = request.json['columns']
    temp = DB_main.Table(name,columns)
    db.add_table(temp)
    export_DB(db.name)
    return jsonify({'result': list(db.tables),"name":db.tables[name].name,"columns":list(db.tables[name].columns)})

'''{
	"table":"",
	"content":[]
}
'''
@app.route('/laba_inf_tex/api/v1.0/<source>/create_record', methods=['POST'])
def create_record(source):
    if source not in dbs:
        abort(404)
    db = dbs[source]
    content = request.json['content']
    table = request.json['table']
    if table not in db.tables:
        abort(404)
    t = db.tables[table]
    t.add_record(content)
    export_DB(db.name)
    return jsonify({'result':t.records})

'''{
	"table":"",
	"id":"",
	"content":[]
}
'''
app.route('/laba_inf_tex/api/v1.0/<source>/edit_record', methods=['POST'])
def edit_record(source):
    if source not in dbs:
        abort(404)
    db = dbs[source]
    content = request.json['content']
    table = request.json['table']
    id = request.json['id']
    if table not in db.tables:
        abort(404)
    t = db.tables[table]
    t.edit_record(int(id), content)
    export_DB(db.name)
    return jsonify({'result':t.records})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port ="80")