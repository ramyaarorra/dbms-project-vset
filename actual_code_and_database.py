from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for flash messages

DB_NAME = 'expenses.db'

def init_db():
    if not os.path.exists(DB_NAME):
        with sqlite3.connect(DB_NAME) as conn:
            c = conn.cursor()
            c.execute('''CREATE TABLE months (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                month TEXT NOT NULL,
                year INTEGER NOT NULL,
                budget REAL NOT NULL,
                spent REAL DEFAULT 0,
                left REAL GENERATED ALWAYS AS (budget - spent) STORED
            )''')
            c.execute('''CREATE TABLE items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                month_id INTEGER,
                item TEXT NOT NULL,
                cost REAL NOT NULL,
                FOREIGN KEY (month_id) REFERENCES months(id) ON DELETE CASCADE
            )''')

@app.route('/')
def index():
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute("SELECT id, month, year, budget, spent, left FROM months")
        months = c.fetchall()
    return render_template('index.html', months=months)

@app.route('/add_month', methods=['POST'])
def add_month():
    month = request.form['month']
    year = request.form['year']
    budget = float(request.form['budget'])
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute("INSERT INTO months (month, year, budget) VALUES (?, ?, ?)", (month, year, budget))
    return redirect(url_for('index'))

@app.route('/details/<int:month_id>')
def details(month_id):
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM months WHERE id = ?", (month_id,))
        month = c.fetchone()
        c.execute("SELECT id, item, cost FROM items WHERE month_id = ?", (month_id,))
        items = c.fetchall()

    # Flash warning if budget < 10%
    if month[5] < 0.1 * month[3]:
        flash("⚠️ Warning: You have less than 10% of your budget left!", "warning")

    return render_template('details.html', month=month, items=items)

@app.route('/add_item/<int:month_id>', methods=['POST'])
def add_item(month_id):
    item = request.form['item']
    cost = float(request.form['cost'])
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute("INSERT INTO items (month_id, item, cost) VALUES (?, ?, ?)", (month_id, item, cost))
        c.execute("UPDATE months SET spent = spent + ? WHERE id = ?", (cost, month_id))
    return redirect(url_for('details', month_id=month_id))

@app.route('/delete_item/<int:item_id>/<int:month_id>')
def delete_item(item_id, month_id):
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        # Get cost of the item before deleting
        c.execute("SELECT cost FROM items WHERE id = ?", (item_id,))
        cost = c.fetchone()[0]

        # Delete item
        c.execute("DELETE FROM items WHERE id = ?", (item_id,))

        # Subtract from spent
        c.execute("UPDATE months SET spent = spent - ? WHERE id = ?", (cost, month_id))

    return redirect(url_for('details', month_id=month_id))


@app.route('/edit_item/<int:item_id>/<int:month_id>', methods=['POST'])
def edit_item(item_id, month_id):
    new_item = request.form['item']
    new_cost = float(request.form['cost'])

    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        
        # Get old cost
        c.execute("SELECT cost FROM items WHERE id = ?", (item_id,))
        old_cost = c.fetchone()[0]

        # Update item
        c.execute("UPDATE items SET item = ?, cost = ? WHERE id = ?", (new_item, new_cost, item_id))

        # Adjust the spent value
        diff = new_cost - old_cost
        c.execute("UPDATE months SET spent = spent + ? WHERE id = ?", (diff, month_id))

    return redirect(url_for('details', month_id=month_id))


if __name__ == '__main__':
    init_db()
    app.run(debug=True)
