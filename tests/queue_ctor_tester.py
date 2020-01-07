import os
import queue as q
from app import db

test_q = Queue(status=Status.CLOSED)
db.session.add(test_q)
db.session.commit()
print(Queue.query.all())
