import json

from flask import abort
from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy.query import Query


class CustomBaseQuery(Query):
    def none_or_409(self, description: str | None = None):
        rv = self.first()

        if rv is not None:
            abort(409, description=description)

        return rv


db = SQLAlchemy(query_class=CustomBaseQuery)
