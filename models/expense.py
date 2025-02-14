# filepath: /d:/oldversion/models/expense.py
from datetime import datetime
from models.database import db
from flask_login import current_user

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    description = db.Column(db.String(200))
    user_id = db.Column(db.Integer, db.ForeignKey('user_profile.id'), nullable=False)
    username = db.Column(db.String(150), nullable=False)

    def __init__(self, amount, category, description):
        self.amount = amount
        self.category = category
        self.description = description
        self.user_id = current_user.id
        self.username = current_user.username

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class ExpenseReport:
    def __init__(self, expenses):
        self.expenses = expenses

    def generate_report(self):
        category_totals = {}
        for expense in self.expenses:
            category_totals[expense.category] = category_totals.get(expense.category, 0) + expense.amount
        return category_totals