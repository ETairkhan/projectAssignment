from flask import Blueprint, render_template, request, redirect, url_for
from models.expense import Expense, ExpenseReport
from models.database import db
expense_bp = Blueprint("expense_bp", __name__)

@expense_bp.route("/")
def index():
   expenses = Expense.query.all()
   return render_template("index.html", expenses=expenses)

@expense_bp.route("/add", methods=["GET", "POST"])
def add_expense():
   if request.method == "POST":
      amount = float(request.form["amount"])
      category = request.form["category"]
      description = request.form["description"]
      new_expense = Expense(amount, category, description)
      new_expense.save()
      return redirect(url_for("expense_bp.index"))
   return render_template("add_expense.html")

@expense_bp.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_expense(id):
   expense = Expense.query.get_or_404(id)
   if request.method == "POST":
      expense.amount = float(request.form["amount"])
      expense.category = request.form["category"]
      expense.description = request.form["description"]
      db.session.commit()
      return redirect(url_for("expense_bp.index"))
   return render_template("edit_expense.html", expense=expense)

@expense_bp.route("/delete/<int:id>")
def delete_expense(id):
   expense = Expense.query.get_or_404(id)
   expense.delete()
   return redirect(url_for("expense_bp.index"))

@expense_bp.route("/report")
def report():
   expenses = Expense.query.all()
   report = ExpenseReport(expenses).generate_report()
   # Convert dict_keys to a list
   categories = list(report.keys())
   amounts = list(report.values())
   return render_template("report.html", categories=categories, amounts=amounts)