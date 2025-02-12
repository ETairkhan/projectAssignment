from datetime import datetime
from models.database import db
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
   amount = db.Column(db.Float, nullable=False)
   category = db.Column(db.String(50), nullable=False)
   date = db.Column(db.DateTime, default=datetime.utcnow)
   description = db.Column(db.String(200))
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