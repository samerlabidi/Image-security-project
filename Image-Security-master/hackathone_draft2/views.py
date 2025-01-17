"""
Routes and views for the flask application.


from datetime import datetime
from flask import render_template
from hackathone_draft2 import app
from flask import request
import random
import os
from flask import Flask, flash, request, redirect, url_for
from flask import send_from_directory
from flask import send_file
import base64  # for encoding/decoding (optional)
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC



def encrypt(file):
    fo = open(file, "rb")
    image=fo.read()
    fo.close()
    image=bytearray(image)
    # key=random.randint(0,256)
    # key=random.getrandbits(128)
    #key = bytearray(random.getrandbits(128) for _ in range(16))
    #key = secrets.token_bytes(16)
    key= os.urandom(16)
    for index , value in enumerate(image): image[index] = value^key[index % len(key)]
    fo=open("enc.jpg","wb")
    imageRes="enc.jpg"
    fo.write(image)
    fo.close()
    return (key,imageRes)

def decrypt(key,file):
    fo = open(file, "rb")
    image=fo.read()
    fo.close()
    image=bytearray(image)
    for index , value in enumerate(image): image[index] = value^key
    fo=open("dec.jpg","wb")
    imageRes="dec.jpg"
    fo.write(image)
    fo.close()
    return imageRes



@app.route('/')
@app.route('/home')
def home():
    """"Renders the home page."""""
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
    )

@app.route('/contact')
def contact():
    """"Renders the contact page.""""
    return render_template(
        'contact.html',
        title='Decrypt',
        year=datetime.now().year,
        message='Upload your encrypted image along with the key'
    )
@app.route('/team')
def team():
    """"Renders the team page."""""
    return render_template(
        'team.html',
        title='Team',
        year=datetime.now().year,
        message='.'
    )

@app.route('/about')
def about():
    """"Renders the about page."""""
    return render_template(
        'about.html',
        title='Encrypt',
        year=datetime.now().year,
        message='Upload the image here'
    )

@app.route('/contact1', methods = ['POST'])  
def contact1():  
    if request.method == 'POST':  
        global f
        f = request.files['file']  
        f.save(f.filename)  
        text = request.form['key']
        key=int(text)
        image=decrypt(key,f.filename)
        return render_template('contact1.html',
        title='Decrypted',
        year=datetime.now().year,
        message='This is your Decrypted image', name = f.filename) 

@app.route('/about1', methods = ['POST'])  
def about1():  
    if request.method == 'POST':  
        global f
        f = request.files['file']  
        f.save(f.filename)  
        key,image=encrypt(f.filename)
        return render_template('about1.html',
        title='Encrypted',
        year=datetime.now().year,
        message='This is your encrypted image', name = f.filename,keys=key,images=image)

@app.route('/return-file')
def return_file():
    return send_file("../enc.jpg",attachment_filename="enc.jpg")

@app.route('/return-file1')
def return_file1():
    return send_file("../dec.jpg",attachment_filename="dec.jpg")
    """
from datetime import datetime
from flask import render_template, request, send_file
from hackathone_draft2 import app
import random
import os
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

def encrypt(file, password):
    with open(file, "rb") as fo:
        image = bytearray(fo.read())

    # Derive a secure key from the password
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=b'kfxkdnlsf',  # Use a fixed salt for simplicity
        iterations=100000
    )
    key = kdf.derive(password.encode())

    for index, value in enumerate(image):
        image[index] = value ^ key[index % len(key)]

    encrypted_file = "enc.jpg"
    with open(encrypted_file, "wb") as fo:
        fo.write(image)

    return encrypted_file

def decrypt(password, file):
    with open(file, "rb") as fo:
        image = bytearray(fo.read())

    # Derive the key using the same fixed salt
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=b'kfxkdnlsf',  # Use the same fixed salt
        iterations=100000
    )
    key = kdf.derive(password.encode())

    for index, value in enumerate(image):
        image[index] = value ^ key[index % len(key)]

    decrypted_file = "dec.jpg"
    with open(decrypted_file, "wb") as fo:
        fo.write(image)

    return decrypted_file

@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
    )

@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Decrypt',
        year=datetime.now().year,
        message='Upload your Encrypted image along with the password'
    )
@app.route('/team')
def team():
    """Renders the team page."""
    return render_template(
        'team.html',
        title='Team',
        year=datetime.now().year,
        message='.'
    )
@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='Encrypt',
        year=datetime.now().year,
        message='Upload the image here along with the password'
    )

@app.route('/contact1', methods=['POST'])
def contact1():
    if request.method == 'POST':
        f = request.files['file']
        f.save(f.filename)
        password = request.form['password']
        decrypted_image = decrypt(password, f.filename)
        return render_template('contact1.html',
                               title='Decrypted',
                               year=datetime.now().year,
                               message='This is your Decrypted image', name=decrypted_image)

@app.route('/about1', methods=['POST'])
def about1():
    if request.method == 'POST':
        f = request.files['file']
        f.save(f.filename)
        password = request.form['password']
        encrypted_image = encrypt(f.filename, password)
        return render_template('about1.html',
                               title='Encrypted',
                               year=datetime.now().year,
                               message='This is your Encrypted image', name=encrypted_image)

@app.route('/return-file')
def return_file():
    return send_file("enc.jpg", attachment_filename="enc.jpg")

@app.route('/return-file1')
def return_file1():
    return send_file("dec.jpg", attachment_filename="dec.jpg")
