from app import db
from checkoff_suite import CheckoffSuite


class Checkoff(db.Model):
    """
    Represents a checkoff in the DB with relevant description and points.\n
    Fields:
    id --> Checkoff ID. Unique, primary key\n
    description --> Description of checkoff\n
    name --> Corresponding assignment\n
    suite_id --> ID of assignment checkoff is for\n
    points --> Number of points checkoff is worth\n
    @author sravyabalasa
    """
    __tablename__ = 'Checkoff'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    description = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    suite_id = db.Column(db.Integer(11), nullable=False)
    points = db.Column(db.Integer, db.ForeignKey(CheckoffSuite.id),
                       nullable=False, default=1)
