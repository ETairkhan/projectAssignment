from datetime import datetime
from . import db

# Parent class
class BaseExpense:
    def __init__(self, amount, category, description):
        self.amount = amount
        self.category = category
        self.description = description

    def get_details(self):
        return f"{self.category}: ${self.amount} - {self.description}"

# Child class inheriting BaseExpense
class Expense(BaseExpense, db.Model):
    __tablename__ = "expenses"

    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(255), nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    description = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self, amount, category, description):
        super().__init__(amount, category, description)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

# Association - ExpenseReport contains multiple Expense objects
class ExpenseReport:
    def __init__(self, expenses):
        self.expenses = expenses

    def generate_report(self):
        category_totals = {}
        for expense in self.expenses:
            category_totals[expense.category] = category_totals.get(expense.category, 0) + expense.amount
        return category_totals
