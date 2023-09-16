import json

def load_inventory():
    with open("stocks.json", "rb") as f:
        inventory = json.load(f)
    return inventory

def load_account():
    with open("transactions.json", "rb") as f:
        account = json.load(f)
    return account

def load_history():
    with open("history.json", "rb") as f:
        history = json.load(f)
    return history

def save_inventory(data):
    with open("stocks.json", "w") as f:
        json.dump(data, f)

def save_account(account):
    with open("transactions.json", "w") as f:
        json.dump(account, f)

def save_history(history):
    with open("history.json", "w") as f:
        json.dump(history, f)
