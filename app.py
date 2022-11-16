from flask import Flask, jsonify, request
from peewee import *
from playhouse.shortcuts import model_to_dict, dict_to_model

db = PostgresqlDatabase('supermario', user='caprice', password='password', host='localhost', port=5432)

class BaseModel(Model):
  class Meta:
    database = db

class Character(BaseModel):
  name = CharField()
  occupation = CharField()

db.connect()
db.drop_tables([Character])
db.create_tables([Character])

Character(name='Mario', occupation='Plumber').save()
Character(name='Peach', occupation='Princess').save()

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return 'Hello'
@app.route('/characters/', methods=['GET', 'POST'])
@app.route('/characters/<id>', methods=['GET', 'PUT', 'DELETE'])
def endpoint(id=None):
  if request.method == 'GET':
    if id:
        return jsonify(model_to_dict(Character.get(Character.id == id)))
    else:
        character_list = []
        for character in Character.select():
            character_list.append(model_to_dict(character))
        return jsonify(character_list)

  if request.method =='PUT':
    body = request.get_json()
    Character.update(body).where(Character.id == id).execute()
    return "Character " + str(id) + " has been updated."

  if request.method == 'POST':
    new_character = dict_to_model(Character, request.get_json())
    new_character.save()
    return jsonify({"success": True})

  if request.method == 'DELETE':
    Character.delete().where(Character.id == id).execute()
    return "Character " + str(id) + " deleted."

app.run(debug=True, port=9000)
