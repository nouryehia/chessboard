import os
import src.models.queue as q
from app import db

test_q = q.Queue(status=q.Status.CLOSED)
db.session.add(test_q)
db.session.commit()
print(q.Queue.query.all())
