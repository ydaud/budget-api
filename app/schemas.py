from marshmallow import Schema, fields, validate


class PlainUserSchema(Schema):
    id = fields.Int(dump_only=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True)


class PlainAccountSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    balance = fields.Float(required=True)
    type = fields.Str(required=True, validate=validate.OneOf(["checking", "saving"]))


class AccountUpdateSchema(Schema):
    id = fields.Int(required=True)
    name = fields.Str()
    type = fields.Str(validate=validate.OneOf(["checking", "saving"]))


class PlainTransactionSchema(Schema):
    id = fields.Int(dump_only=True)
    date = fields.Date(required=True)
    payee = fields.Str(required=True)
    inflow = fields.Bool(required=True)
    amount = fields.Float(required=True)
    account_id = fields.Int(required=True)


class PlainCategoryGroupSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    assigned = fields.Float(required=True)
    activity = fields.Float(required=True)


class UserSchema(PlainUserSchema):
    accounts = fields.List(fields.Nested(PlainAccountSchema()), dump_only=True)
    category_groups = fields.List(
        fields.Nested(PlainCategoryGroupSchema()), dump_only=True
    )


class AccountSchema(PlainAccountSchema):
    user = fields.Nested(PlainUserSchema(), dump_only=True)
    transactions = fields.List(fields.Nested(PlainTransactionSchema()), dump_only=True)


class TransactionSchema(PlainTransactionSchema):
    account_id = fields.Int(required=True, load_only=True)
    account = fields.Nested(PlainAccountSchema(), dump_only=True)


class CategoryGroupSchema(PlainCategoryGroupSchema):
    user = fields.Nested(PlainUserSchema(), dump_only=True)
