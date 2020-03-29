import os
import base64

from flask import Flask, render_template, request, redirect, url_for, session

from model import Donation, Donor

app = Flask(__name__)


@app.route('/')
def home():
    return redirect(url_for('all'))


@app.route('/donations/')
def all():
    donations = Donation.select()
    return render_template('donations.jinja2', donations=donations)


@app.route('/add', methods=['GET', 'POST'])
def add_donation():
    if request.method == 'POST':
        uname = request.form['name']
        donation_amount = request.form['amount']
        name = Donor.select().where(Donor.name == uname)
        if name:
            Donation.insert(value=donation_amount, donor=name.id).execute()
            return redirect(url_for('all'))
        else:
            return render_template('add.jinja2', error='Donor not found.')
    else:
        return render_template('add.jinja2')


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6738))
    app.run(host='0.0.0.0', port=port)

