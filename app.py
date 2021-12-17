from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.sqlite')

db = SQLAlchemy(app)
ma = Marshmallow(app)

# models
class Template(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(200), nullable=False)
    template = db.Column(db.Text, nullable=False)

    def __init__(self, name, template):
        self.name = name
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
    userCreatedLibs = db.Column(db.String())
    
    def __init__(self, id, userCreatedLibs ):
        self.userCreatedLibs = userCreatedLibs
    

# schema
class TemplateSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'template')

one_template_schema = TemplateSchema()
multi_template_schema = TemplateSchema(many=True)

class WordSchema(ma.Schema):
    class Meta:
        fields = ('id', 'word', 'part_of_speech')

one_word_schema = WordSchema()
multi_word_schema = WordSchema(many=True)

class CreatedLibsSchema(ma.Schema):
    
    class Meta:
        fields = ('id', 'userCreatedLibs')
        
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
    name = data.get("name")
    template = data.get("template")

    if name == None:
        return jsonify("Must include a name key")
    if template == None:
        return jsonify("Must include a template key")
    
    new_template = Template(name, template)
    db.session.add(new_template)
    db.session.commit()

    return new_template
      

#  PUT endpoint to update a record
@app.route('/template/update/<id>', methods=["PUT"])
def update_template_by_id(id):
    if request.content_type != 'application/json':
        return jsonify('Error: Data must be sent as JSON')

    put_data = request.get_json()
    name = put_data.get('name')
    template = put_data.get('template')

    madlib_to_update = db.session.query(Template).filter(Template.id == id).first()

    if name != None:
        madlib_to_update.name = name
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