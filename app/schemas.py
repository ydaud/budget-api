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


class PlainCategorySchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)


class PlainBudgetSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    available = fields.Float(dump_only=True)


class PlainMonthSchema(Schema):
    id = fields.Int(dump_only=True)
    month = fields.Date(required=True, format="%Y-%m")


class PlainEntrySchema(Schema):
    id = fields.Int(dump_only=True)
    assigned = fields.Float(required=True)
    activity = fields.Float(dump_only=True)
    available = fields.Float(required=True)
    category_id = fields.Int(required=True, load_only=True)


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
    category_id = fields.Int(required=True, load_only=True)
    category = fields.Nested(PlainCategorySchema(), dump_only=True)


class CategoryGroupSchema(PlainCategoryGroupSchema):
    user = fields.Nested(PlainUserSchema(), dump_only=True)
    categories = fields.List(fields.Nested(PlainCategorySchema()), dump_only=True)


class CategorySchema(PlainCategorySchema):
    category_group_id = fields.Int(required=True, load_only=True)
    category_group = fields.Nested(PlainCategoryGroupSchema(), dump_only=True)
    transactons = fields.List(fields.Nested(PlainTransactionSchema()), dump_only=True)


class BudgetSchema(PlainBudgetSchema):
    user = fields.Nested(PlainUserSchema(), dump_only=True)
    months = fields.List(fields.Nested(PlainMonthSchema()), dump_only=True)


class MonthSchema(PlainMonthSchema):
    budget = fields.Nested(PlainBudgetSchema(), dump_only=True)
    entries = fields.List(fields.Nested(PlainEntrySchema()), dump_only=True)


class EntrySchema(PlainEntrySchema):
    month_id = fields.Int(required=True, load_only=True)
    month = fields.Nested(PlainMonthSchema(), dump_only=True)
    category = fields.Nested(PlainCategorySchema(), dump_only=True)


class EntryUpdateSchema(Schema):
    id = fields.Int(required=True)
    assigned = fields.Float(required=True)
