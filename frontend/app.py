from flask import request, redirect, render_template, Flask
import pandas as pd
import numpy as np

import tensorflow as tf

model = tf.keras.models.load_model('LModel.h5')

def get_score(X):
    return 1-model.predict(X.reshape(1,119))[0][0]

app = Flask(__name__)
persons = [[200, 'CA', 'Education', 20000],  [3500, 'TX', 'Wedding', 95000], [1300, 'WA', 'House', 35000],
 [8900, 'CA',  'Education', 85000], [200, 'IL',  'Business', 45000], [1100, 'DC', 'Education', 15000], [600, 'CA', 'Education', 35000],
 [1000, 'CA', 'Education', 135000], [300, 'DC', 'Education', 45000], [55000, 'MI', 'DebtConsolidation', 350000]]
info = np.load('10ppl.npy')
bank = pd.read_pickle('funds.pickle')
borrowers = pd.read_pickle('borrowers.pickle')

@app.route('/', methods = ['GET'])
def home():
    return render_template('index.html')

@app.route('/request', methods = ['GET'])
def requestq():
    return render_template('request.html')

@app.route('/requested', methods = ['GET'])
def requested():
    person = int(request.args.get('person'))
    data = persons[person]
    print(info[person, :])
    score = get_score(np.array(info[person, :]))
    if score < 0.4:
        msg = "Unfortunately, your credit rating is too poor to be matched with a lender."
    else:
        msg = "You have been added to the borrowers queue."
    print(msg)
    #update_requests()

    return render_template('requested.html', message=msg)

@app.route('/donated', methods = ['GET'])
def donated():
    amount = float(request.args.get('amount'))
    location = request.args.get('location')
    purpose = request.args.get('purpose')
    income = int(request.args.get('income'))

    update_funds(amount, location, purpose, income)
    #identify_recipients(amount, location, purpose, income)

    return render_template('donated.html')

@app.route('/donate', methods = ['GET'])
def donate():
    return render_template('donate.html')

@app.route('/landing', methods = ['GET'])
def landing():
    return render_template('donated.html')


def identify_recipients(funds, location, purpose, income):
    global borrowers
    m1 = borrowers[borrowers['location'] == location]
    m2 = m1[m1['income'] == income]
    m3 = m2[m2['purpose'] == purpose]
    #and bank['purpose'] == purpose and bank['income'] == income
    if len(m3) == 0:
        bank = pd.concat([pd.DataFrame([[funds, location, purpose, income]], columns=['score', 'amount', 'location', 'purpose', 'income']), borrowers], ignore_index=True)
    else:
        bank.at[m2.index[m2['purpose'] == purpose].tolist()[0], 'amount'] += funds
    bank.to_pickle('funds.pickle')
    print(bank)

def update_funds(funds, location, purpose, income):
    global bank
    m1 = bank[bank['location'] == location]
    m2 = m1[m1['income'] == income]
    m3 = m2[m2['purpose'] == purpose]
    #and bank['purpose'] == purpose and bank['income'] == income
    if len(m3) == 0:
        bank = pd.concat([pd.DataFrame([[funds, location, purpose, income]], columns=['amount', 'location', 'purpose', 'income']), bank], ignore_index=True)
    else:
        bank.at[m2.index[m2['purpose'] == purpose].tolist()[0], 'amount'] += funds
    bank.to_pickle('funds.pickle')
    print(bank)

def update_requests(funds, location, purpose, income):
    global borrowers
    m1 = bank[bank['location'] == location]
    m2 = m1[m1['income'] == income]
    m3 = m2[m2['purpose'] == purpose]
    #and bank['purpose'] == purpose and bank['income'] == income
    if len(m3) == 0:
        bank = pd.concat([pd.DataFrame([[funds, location, purpose, income]], columns=['amount', 'location', 'purpose', 'income']), bank], ignore_index=True)
    else:
        bank.at[m2.index[m2['purpose'] == purpose].tolist()[0], 'amount'] += funds
    bank.to_pickle('funds.pickle')
    print(bank)

app.run()
