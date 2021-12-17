from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import random

import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.sqlite')

db = SQLAlchemy(app)
ma = Marshmallow(app)

# models
class Template(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.String(200), nullable=False)
    template = db.Column(db.Text, nullable=False)

    def __init__(self, title, template):
        self.title = title
        self.template = template


class Word(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    word = db.Column(db.String(100), nullable=False)
    part_of_speech = db.Column(db.String(50), nullable=False)

    def __init__(self, word, part_of_speech):
        self.word = word
        self.part_of_speech = part_of_speech

class CreatedLibs(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    user_created_libs = db.Column(db.Text)
    
    def __init__(self, user_created_libs ):
        self.user_created_libs = user_created_libs
    

# schema
class TemplateSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'template')

one_template_schema = TemplateSchema()
multi_template_schema = TemplateSchema(many=True)

class WordSchema(ma.Schema):
    class Meta:
        fields = ('id', 'word', 'part_of_speech')

one_word_schema = WordSchema()
multi_word_schema = WordSchema(many=True)

class CreatedLibsSchema(ma.Schema):
    
    class Meta:
        fields = ('id', 'user_created_libs')
        
one_user_created_libs = CreatedLibsSchema()
multi_word_schema = CreatedLibsSchema(many=True)
        

# POST endpoint for a single template
@app.route('/template/add', methods=['POST'])
def add_template():
    if request.content_type != 'application/json':
        return jsonify('Error: Data must be sent as JSON')

    data = request.get_json()

    return jsonify(one_template_schema.dump(process_template(data)))


# POST endpoint for multiple templates
@app.route('/template/add/many', methods=['POST'])
def add_many_templates():
    if request.content_type != 'application/json':
        return jsonify('Error: Data must be sent as JSON')
    
    data = request.get_json()
    template_list = []
    for template in data:
        template_list.append(process_template(template))
    return jsonify(multi_template_schema.dump(template_list))


# function to actually deal with the templates
def process_template(data):
    name = data.get("title")
    template = data.get("template")

    if name == None:
        return jsonify("Must include a title key")
    if template == None:
        return jsonify("Must include a template key")
    
    new_template = Template(name, template)
    db.session.add(new_template)
    db.session.commit()

    return new_template


# post endpoint for single word
@app.route("/word/add", methods=['POST'])
def add_word():
    if request.content_type != 'application/json':
        return jsonify('Error: Data must be sent as JSON')
    data = request.get_json()
    return jsonify(one_word_schema.dump(process_word(data)))


# post endpoint for multiple words
@app.route("/word/add/many", methods=['POST'])
def add_multi_words():
    if request.content_type != 'application/json':
        return jsonify('Error: Data must be sent as JSON')
    data = request.get_json()
    word_list = []
    for word in data:
        word_list.append(process_word(word))
    return jsonify(multi_word_schema.dump(word_list))


# function for processing words
def process_word(data):
    word = data.get("word")
    part_of_speech = data.get("part_of_speech")

    if word == None:
        return jsonify("Must include a word")
    if part_of_speech == None:
        return jsonify("Must include a part of speech")
    
    new_word = Word(word, part_of_speech)
    db.session.add(new_word)
    db.session.commit()

    return new_word


#  PUT endpoint to update a record
@app.route('/template/update/<id>', methods=["PUT"])
def update_template_by_id(id):
    if request.content_type != 'application/json':
        return jsonify('Error: Data must be sent as JSON')

    put_data = request.get_json()
    title = put_data.get('title')
    template = put_data.get('template')

    madlib_to_update = db.session.query(Template).filter(Template.id == id).first()

    if title != None:
        madlib_to_update.title = title
    if template != None:
        madlib_to_update.template = template

    db.session.commit()

    return jsonify(one_template_schema.dump(madlib_to_update))


#  DELETE endpoint to delete a record
@app.route('/template/delete/<id>', methods=["DELETE"])
def delete_madlib_by_id(id):
    madlib_to_delete = db.session.query(Template).filter(Template.id == id).first()
    db.session.delete(madlib_to_delete)
    db.session.commit()

    return jsonify("Madlib successfully deleted")

# GET endpoint for a single template
@app.route("/template/get_id/<id>", methods=['GET'])
def get_template_by_id(id):
    return jsonify(one_template_schema.dump(Template.query.get(id)))


# GET endpoint for all templates
@app.route("/template/get/all", methods=['GET'])
def get_all_templates():
    return jsonify(multi_template_schema.dump(Template.query.all()))


# GET endpoint for template by title
@app.route("/template/get_title/<title>", methods=['GET'])
def get_template_by_title(title):
    return jsonify(one_template_schema.dump(Template.query.filter_by(title=title).first()))


# GET endpoint for a random word by part of speech
@app.route("/word/get/random", methods=['GET'])
def get_random_word(part_of_speech):
    word_list = Word.query.filter_by(part_of_speech=part_of_speech).all()
    if len(word_list) == 0:
        return jsonify(f"No words found for part of speech {part_of_speech}")
    return jsonify(one_word_schema.dump(random.choice(word_list)))

# GET endpoint for all words
@app.route("/word/get/all", methods=['GET'])
def get_all_words():
    return jsonify(multi_word_schema.dump(Word.query.all()))


# GET endpoint for word by word
@app.route("/word/get/<word>", methods=['GET'])
def get_word_by_word(word):
    return jsonify(one_word_schema.dump(Word.query.filter_by(word=word).first()))

if __name__ == "__main__":
    app.run(debug=True)