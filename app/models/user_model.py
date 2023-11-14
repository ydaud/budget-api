from werkzeug.security import check_password_hash, generate_password_hash

from app.services import db


class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)

    accounts = db.relationship("AccountModel", back_populates="user", lazy="dynamic")

    db.UniqueConstraint(email)

    def __init__(self, email: str, password: str):
        self.email = email
        self.password = self._generate_password_hash(password)

    def is_password_correct(self, password_plaintext: str):
        return check_password_hash(self.password, password_plaintext)

    def set_password(self, password_plaintext: str):
        self.password = self._generate_password_hash(password_plaintext)

    @staticmethod
    def _generate_password_hash(password_plaintext):
        return generate_password_hash(password_plaintext)

    def __repr__(self):
        return f"<User: {self.email}>"
