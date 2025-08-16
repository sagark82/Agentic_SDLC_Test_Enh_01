# app.py (Backend)
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__, template_folder='.',static_folder='.')
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/products')
def products():
    return render_template('products.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/api/contact', methods=['POST'])
def handle_contact_form():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    message = data.get('message')
    
    # In a real app, you would use a library like smtplib to send an email
    print("--- NEW INQUIRY ---")
    print(f"Recipient: contact@pharma-inc.com")
    print(f"From: {name} <{email}>")
    print(f"Message: {message}")
    print("-------------------")
    
    return jsonify({"message": "Your inquiry has been sent!"})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
