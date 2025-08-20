from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# temporary in-memory storage (for demo only)
users = {}

# Luhn's Algorithm to check credit card validity
def luhn_algorithm(card_number):
    card_number = card_number.replace(" ", "")
    if not card_number.isdigit():
        return False
    total = 0
    reverse_digits = card_number[::-1]
    for i, digit in enumerate(reverse_digits):
        n = int(digit)
        if i % 2 == 1:  # double every 2nd digit
            n *= 2
            if n > 9:
                n -= 9
        total += n
    return total % 10 == 0

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']

    if email in users and users[email]['password'] == password:
        return render_template('welcome.html', name=users[email]['first_name'])
    else:
        return redirect(url_for('register'))

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def register_post():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    email = request.form['email']
    password = request.form['password']
    address = request.form['address']
    aadhar = request.form['aadhar']
    credit_card = request.form['credit_card']

    if not luhn_algorithm(credit_card):
        return "Credit Card Number is NOT valid!"

    # save user
    users[email] = {
        'first_name': first_name,
        'last_name': last_name,
        'password': password,
        'address': address,
        'aadhar': aadhar,
        'credit_card': credit_card
    }

    return render_template('welcome.html', name=first_name)

if __name__ == '__main__':
    app.run(debug=True)
