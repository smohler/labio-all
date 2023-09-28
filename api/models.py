import random
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Sample(db.Model):
    __tablename__ = 'samples'

    sampleID = db.Column(db.String(80), primary_key=True)
    labware = db.Column(db.String(80), nullable=False)
    volume = db.Column(db.Float, nullable=False)
    conc = db.Column(db.Float, nullable=False)
    created = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __init__(self, sampleID, labware, volume, conc):
        self.sampleID = sampleID
        self.labware = labware
        self.volume = volume
        self.conc = conc

    def json(self):
        return {
            "sampleID": self.sampleID,
            "labware": self.labware,
            "volume": {
                "value": self.volume,
                "unit": "uL"
            },
            "conc": {
                "value": self.conc,
                "unit": "mg/ml"
            },
            "created": self.created
        }

# Database seeding function
def seed_database():
    with app.app_context():
        db.drop_all()
        db.create_all()

        for _ in range(1000):
            sampleID = f"ID{random.randint(10000, 99999)}"
            labware = f"Labware{random.randint(1, 10)}"
            volume_value = random.uniform(500, 1500)
            conc_value = random.uniform(0.5, 5)

            new_sample = Sample(
                sampleID=sampleID,
                labware=labware,
                volume_value=volume_value,
                conc_value=conc_value
            )
            db.session.add(new_sample)
        db.session.commit()
