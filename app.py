from flask import Flask, redirect, render_template, request, flash
from db import load_inventory, load_account, save_account, save_inventory,save_history, load_history


app = Flask(__name__)
app.config["SECRET_KEY"] = "1234abcd"

#http://127.0.0.1:5000
@app.route("/")
def mainpage():
    inventory = load_inventory()
    account = load_account()
    return render_template("index.html", stocks=inventory,transactions=account)

#http://127.0.0.1:5000/add-product
@app.route("/add-product", methods=["GET", "POST"])
def add_product():
    if request.method == "POST":
        name = request.form.get("Product Name")
        size = request.form.get("Size")
        quantity = int(request.form.get("Quantity"))
        unit_price = float(request.form.get("Unit Price"))
        purchase = quantity*unit_price
        inventory = load_inventory()
        account = load_account()
        history = load_history()
        
        if account >purchase:
            account -= purchase
            history.append(f"This deal - {name} cost you {purchase} euros.")
            if name not in inventory:
                inventory[name] = {
                "Size": int(size),
                "Quantity": quantity,
                "Unit_Price":int(unit_price), 
            }
                history.append(f"New product added on inventory - Product{name}: Size {size}/QTY{quantity}/Price{unit_price}. Cost you {purchase} euros.")
            else:
                inventory[name]['Quantity'] += quantity
                account -= purchase
                history.append(f"Stock added for product {name} - : {quantity}, cost {purchase} euros.")
            
            save_inventory(inventory)
            save_account(account)
            save_history(history)

        else:
            flash("No enough balance to purchase these products!")

        return redirect("/")
    return render_template("add_product.html")

#http://127.0.0.1:5000/sell-product
@app.route("/sell-product", methods=["GET", "POST"])
def sell_inventory():
    if request.method == "POST":
        name = request.form.get("Product Name")
        quantity = int(request.form.get("Quantity"))
        #stock_quantity= int()
        unit_price = float(request.form.get("Unit_Price"))
        sale = quantity*unit_price
        inventory = load_inventory()
        account = load_account()
        history = load_history()
        
        if name in inventory:
            stock_quantity = int(inventory[name]["Quantity"])
        else:
            stock_quantity = 0
            flash("This product is not in the stock. Please enter a valid product type.")

        if stock_quantity > quantity:
            inventory[name]['Quantity'] -= quantity
            account += sale
            history.append(f"This deal - {name} brought you {sale} euros sales.")
            history.append(f"Stock reduced for product {name}  : {quantity} units")

            save_inventory(inventory)
            save_account(account)
            save_history(history)
        else:
            flash('No enough stock to sell!')
         
        return redirect("/")
    return render_template("sell_product.html")

#http://127.0.0.1:5000/balance
@app.route("/balance", methods=["GET", "POST"])
def balance():
    if request.method == "POST":
        account = load_account()
        transaction= float(request.form.get("Amount"))
        account += transaction
        history.append(f"Account updated: {transaction}.")
        save_account(account)
        save_history(history)
        
        return redirect("/")
    return render_template("balance.html")

#http://127.0.0.1:5000/history
@app.route("/history", methods=["GET", "POST"])
def history():
    history = load_history()
    return render_template("history.html", history=history)



if __name__ == '__main__':
    app.run(debug=True, port=8088)