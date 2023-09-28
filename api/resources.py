from flask_restx import Resource, Namespace, fields
from flask import request
from api.models import Sample, db, seed_database

api = Namespace("sample", description="Sample operations")

# Define a model for the Sample resource
sample_model = api.model('Sample', {
    'sampleID': fields.String(required=True, description='The unique sample identifier'),
    'labware': fields.String(required=True, description='The labware identifier'),
    'volume': fields.Float(required=True, description='The volume value'),
    'conc': fields.Float(required=True, description='The concentration value')
})

@api.route('/<string:sampleID>')
class SampleResource(Resource):
    @api.doc(params={'sampleID': 'The unique sample identifier'})
    @api.marshal_with(sample_model)
    def get(self, sampleID):
        sample = Sample.query.filter_by(sampleID=sampleID).first()
        if sample:
            return sample
        else:
            api.abort(404, "Sample not found")

    @api.doc(params={'sampleID': 'The unique sample identifier'})
    @api.expect(sample_model)
    def post(self, sampleID):
        data = request.json
        new_volume = data.get('volume')
        new_conc = data.get('conc')

        sample = Sample.query.filter_by(sampleID=sampleID).first()
        if sample:
            sample.volume = new_volume
            sample.conc = new_conc
            db.session.commit()
            return {"message": f"Sample {sampleID} updated successfully"}
        else:
            api.abort(404, "Sample not found")

@api.route('/')
class SampleListResource(Resource):
    @api.marshal_with(sample_model, as_list=True)
    def get(self):
        samples = Sample.query.all()
        return samples

@api.route('/seed')
class SeedDatabaseResource(Resource):
    @api.doc(description='Seed the database with sample data')
    def post(self):
        seed_database()
        return {"message": "Database seeded with sample data"}

