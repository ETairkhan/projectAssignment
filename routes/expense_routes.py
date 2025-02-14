from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from models.expense import Expense, ExpenseReport
from models.database import db

expense_bp = Blueprint("expense_bp", __name__)

@expense_bp.route("/")
@login_required
def index():
    print(f"User authenticated: {current_user.is_authenticated}")
    expenses = Expense.query.filter_by(username=current_user.username).all()
    return render_template("index.html", expenses=expenses)


@expense_bp.route("/add", methods=["GET", "POST"])
@login_required
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
@login_required
def edit_expense(id):
    expense = Expense.query.get_or_404(id)
    if expense.user_id != current_user.id:
        return redirect(url_for("expense_bp.index"))
    if request.method == "POST":
        expense.amount = float(request.form["amount"])
        expense.category = request.form["category"]
        expense.description = request.form["description"]
        db.session.commit()
        return redirect(url_for("expense_bp.index"))
    return render_template("edit_expense.html", expense=expense)

@expense_bp.route("/delete/<int:id>")
@login_required
def delete_expense(id):
    expense = Expense.query.get_or_404(id)
    if expense.user_id != current_user.id:
        return redirect(url_for("expense_bp.index"))
    expense.delete()
    return redirect(url_for("expense_bp.index"))

@expense_bp.route("/report")
@login_required
def report():
    expenses = Expense.query.filter_by(username=current_user.username).all()
    report = ExpenseReport(expenses).generate_report()
    categories = list(report.keys())
    amounts = list(report.values())
    return render_template("report.html", categories=categories, amounts=amounts)