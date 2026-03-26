from flask import (Flask, render_template, redirect, 
                   url_for)
from form import ContactForm
from flask_ckeditor import CKEditor
import sqlite3

app = Flask(__name__)

app.config['SECRET_KEY'] = 'mysecretkey'
app.config['CKEDITOR_PKG_TYPE'] = 'full-all'

ckeditor = CKEditor(app)

################# Route ##################
@app.route('/')
def index():
    form = ContactForm()
    return render_template('contact.html', form=form)

@app.route('/message', methods=['GET','POST'])
def submit():
    form = ContactForm()
    
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        subscribe = form.subscribe.data
        message = form.message.data
        
        conn = sqlite3.connect(app.config.get('DATABASE', 'flask_ckeditor/message.db'))
        # conn = sqlite3.connect("flask_ckeditor/message.db")
        c = conn.cursor()
        try:
            query = ("""INSERT INTO message
                        VALUES (:id, :name, :email, :subscribe, :message)""")

            my_data = {
                'id' : None,
                'name': name,
                'email': email,
                'subscribe': subscribe,
                'message': message
                }
         
            content = c.execute(query, my_data)
            conn.commit()

            print(f"Data Added ID: " + str(content.lastrowid))

        except sqlite3.Error as e:
            print(e)
       
        return redirect(url_for('thankyou'))
    
    return render_template('contact.html', form=form)

@app.route('/thankyou')
def thankyou():
    return render_template('thankyou.html')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
