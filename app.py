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
    name = db.Column(db.String(100), nullable=False)
    template = db.Column(db.Text, nullable=False)

    def __init__(self, name, template):
        self.name = name
        self.template = template


# schema
class TemplateSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'template')


one_template_schema = TemplateSchema()
multi_template_schema = TemplateSchema(many=True)

# POST endpoint for a template
@app.route('/template/add', methods=['POST'])
def add_template():
    if request.content_type != 'application/json':
        return jsonify('Error: Data must be sent as JSON')

    data = request.get_json()
    name = data.get("name")
    template = data.get("template")

    if name == None:
        return jsonify("Must include a name key")
    if template == None:
        return jsonify("Must include a template key")
    
    new_template = Template(name, template)
    db.session.add(new_template)
    db.session.commit()

    return jsonify(one_template_schema.dump(new_template))


# GET endpoint for a single template
@app.route("/template/get/<id>", methods=['GET'])
def get_template_by_id(id):
    return jsonify(one_template_schema.dump(Template.query.get(id)))


# GET endpoint for all templates
@app.route("/template/get/all", methods=['GET'])
def get_all_templates():
    return jsonify(multi_template_schema.dump(Template.query.all()))




if __name__ == "__main__":
    app.run(debug=True)
