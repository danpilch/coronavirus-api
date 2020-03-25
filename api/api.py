import os
from flask import Flask
from flask_table import Table, Col
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from flask_restful import Resource, Api
from flask_marshmallow import Marshmallow
from marshmallow import fields

app = Flask(__name__)

# DB vars
db_host = os.getenv('MYSQL_HOST', '127.0.0.1') 
db_user = os.getenv('MYSQL_USER', 'api')
db_pass = os.getenv('MYSQL_PASS', 'api')
db_name = os.getenv('MYSQL_NAME', 'cv')
db_table = os.getenv('MYSQL_TABLE_NAME', 'county_data')

# DB connection config
app.config['SQLALCHEMY_POOL_RECYCLE'] = 299
app.config['SQLALCHEMY_POOL_TIMEOUT'] = 20
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{db_user}:{db_pass}@{db_host}/{db_name}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Define application objects
db = SQLAlchemy(app)
ma = Marshmallow(app)
api = Api(app)

version = os.getenv('VERSION', None)
app_debug = os.getenv('APP_DEBUG', False)
app_port = os.getenv('APP_PORT', 5000)

class ItemTable(Table):
    classes = ['table', 'table-striped', 'table-bordered', 'table-condensed']
    GSS_NM = Col('GSS_NM')
    TotalCases = Col('TotalCases')

class County(db.Model):
    __tablename__ = db_table
    id = db.Column(db.BigInteger, primary_key=True)
    GSS_NM = db.Column(db.Text, unique=True, nullable=False)
    TotalCases = db.Column(db.BigInteger, unique=True, nullable=False)

class CountySchema(ma.ModelSchema):
    class Meta:
        fields = ["GSS_NM", "TotalCases"]

county_schema = CountySchema()
countys_schema = CountySchema(many=True)

class CountyListResource(Resource):
    def get(self):
        items = County.query.order_by(County.TotalCases.desc()).all()
        return countys_schema.dump(items)

# To display a table we have to use a basic flask route
@app.route("/table/county/all")
def get():
    items = County.query.order_by(County.TotalCases.desc()).all()
    print(items)
    table = ItemTable(items)
    return table.__html__()

class CountySearchResource(Resource):
    def get(self, query):
        search = County.query.filter(County.GSS_NM.like(f"%{query}%")).all()
        return countys_schema.dump(search)

class CountyTotalResource(Resource):
    def get(self):
        total = County.query.with_entities(func.sum(County.TotalCases).label('total')).scalar()
        return {'total': int(total)}

class Version(Resource):
    def get(self):
        return version

class Health(Resource):
    def get(self):
        return "OK"


api.add_resource(Version, '/api/version')
api.add_resource(Health, '/api/health')
api.add_resource(CountyListResource, '/api/county/all')
api.add_resource(CountyTotalResource, '/api/county/total')
api.add_resource(CountySearchResource, '/api/county/search/<string:query>')

if __name__ == '__main__':
    app.run('0.0.0.0', port=app_port, debug=app_debug)
