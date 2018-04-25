
from firebase import firebase
from flask import Flask,render_template, flash,request , abort , redirect , Response ,url_for, session
from flask_login import LoginManager , login_required , UserMixin , login_user
from flask_googlemaps import GoogleMaps
from datetime import datetime
import logist
import recommend
import download_data
import requests
import random
import json

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'secret_key'
app.config['GOOGLEMAPS_KEY'] = "AIzaSyB0_0YF6CqoeTD5EpRBYBLPoeMYRXvjfk8"
GoogleMaps(app)
recom = recommend.Recommender()
logist = logist.Logistc()
down = download_data.download()


# firebase = firebase.FirebaseApplication('https://foodie-yelp.firebaseio.com', None)
firebase_ = down.firebase1

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = firebase_.get('/users', None)
        if(username in users and password==''.join(users[username]['password'].values())):
            session['logged_in'] = True
            session['username'] = username
            global user
            user = username
            flash('Logged in!')
            return render_template('index.html',)
        else:
            flash('Wrong username or password')
    return render_template('login.html')

@app.route('/register' , methods = ['GET' , 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        password2 = request.form['password2']
        users = firebase_.get('/users', None)
        # firebase_.post('/users', username)
        if(username in users):
            users = firebase_.get('/users', None)
        # firebase_.post('/users', username)
            users = firebase_.get('/users', None)
        # firebase_.post('/users', username)
        if(username in users or password != password2):
            flash('username exits!')
            return render_template('register.html')
        else:
            firebase_.post('/users/'+username+'/password', password)
            flash('Register Sucessfully!')
            return render_template('login.html')
    else:
        flash('Try Again!')
        return render_template('register.html')


@app.route("/logout")
def logout():
    """Logout Form"""
    session['logged_in'] = False
    flash('Logged Out')
    return render_template('index.html')

@app.route('/', methods = ['GET' , 'POST'])
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/review', methods=['GET', 'POST'])
def review():
    if request.method == 'GET':
        return render_template('review.html')
    else:
        review = request.form.get('review_submit')
        return render_template('review.html', rev=review,feedback=logist.predict_rating_direction([review.encode('utf-8')]))

@app.route('/recommendation',methods=['GET', 'POST'])
def recommendation():
    if request.method == 'GET':
        return render_template('recommendation.html')
    else:
        user_id_temp = request.form.get('user_id_submit')
        return render_template('recommendation.html', res_id=recom.pre_rate_recommend(user_id_temp), data=down.data)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/show_results', methods = ['POST'])
def show_results():

    search = request.form['search']
    user_id = session['username']

    search = request.form['search'] 
    user_id = session['username']

    if request.method == 'POST':
        data = down.data
        check = request.form.getlist("check")
        global search_history
        search_history=[]
        search_history.append(search)
        search_history.append(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))


    return render_template('show_results.html',search= search, check= check,res_id=recom.pre_rate_recommend(user_id), data=down.data)

@app.route('/show_history', methods = ['get','POST'])
def show_history():
    if session['logged_in'] == True:
        firebase_.post('/users/'+user+'/history', search_history)
        users = firebase_.get('/users', None)
        history = users[user]['history'].values()

        # time_stamp =users[user]['history'].values()

    return render_template('/show_history.html', user=user, history=history)

@app.route('/restaurant/<business_id>/<name>/<address>/<city>/<state>/<postal_code>/<lat>/<longi>/<categories>/<ratings>/<hours>/<attributes>', methods=['GET', 'POST'])
def restaurant(business_id, name, address, city, state, postal_code, lat,longi, categories, ratings, hours, attributes):
    pos_words = logist.top_words
    if request.method == 'GET':
        cate = categories.replace('\'', '').replace('[','').replace(']','')
        hours = hours.replace('\'', '').replace('{','').replace('}','').replace('u','').split(',')
        attributes = attributes.replace('\'', '').replace('{','').replace('}','').replace('u','').split(',')
        return render_template('restaurant.html',pos_words=pos_words,business_id= business_id, name= name, address=address, city=city,
                               state=state,postal_code=postal_code, lat=lat,longi=longi, categories=cate, ratings=ratings,
                               hours=hours, attributes=attributes)
    else:
        cate = categories.replace('\'', '').replace('[', '').replace(']', '')
        hours = hours.replace('\'', '').replace('{', '').replace('}', '').replace('u', '').split(',')
        attributes = attributes.replace('\'', '').replace('{', '').replace('}', '').replace('u', '').split(',')

        b_id = business_id
        user_id = session['username']
        
        review_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        stars_review = request.form.get('rating')
        text = request.form.get('sss')
        review_input ='{'+'"business_id":"' + b_id + '",' + '"stars_review":' + str(stars_review) + ',' + '"text":"' + text + '",' + '"user_id":"' + user_id + '",' + '"date":"' + review_date + '"}'
        review_input = '{"'+ str(random.randint(0,10000))+'":'+review_input+'}'
        url = 'https://inf552-69068.firebaseio.com/reviews.json'
        requests.patch(url,review_input)
        return render_template('restaurant.html',pos_words=pos_words,business_id= business_id, name= name, address=address, city=city,
                               state=state,postal_code=postal_code, lat=lat,longi=longi, categories=cate, ratings=ratings,
                               hours=hours, attributes=attributes,text=text,feedback_emoji=logist.predict_rating_direction([text.encode('utf-8')]))

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html')

@app.route('/redirect_to_index')
def redirect_to_index():
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run('0.0.0.0')
