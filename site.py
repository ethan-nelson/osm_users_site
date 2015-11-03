from flask import (
    Flask,
    abort,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
#import logging, sys
import psycopg2
import psycopg2.extensions

psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)

#logging.basicConfig(stream=sys.stderr)
app = Flask(__name__)
app.config['SECRET_KEY'] = 'applesauce';

#connection = psycopg2.connect("dbname='osm_users' host='localhost' user='osm_users_view' password='osm'")


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/error')
def flash_home():
    return render_template('indexflash.html')


@app.route('/search', methods=['POST','GET'])
def search():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('results'))
    else:
        flash('You did not POST to the search. Please try searching from here.')
        return redirect(url_for('flash_home'))


@app.route('/results')
def results():
    if 'username' not in session:
        flash('You did not submit anything. Please try again.')
        return redirect(url_for('flash_home'))

    converted_username = session['username'].replace('*','%%')

    try:
        connection = psycopg2.connect("dbname='osm_users' host='localhost' user='osm_users_view' password='osm'")
        cursor = connection.cursor()
        cursor.execute("""SELECT * FROM users WHERE username ILIKE %s ORDER BY end_date DESC;""", (converted_username,))
        results = cursor.fetchmany(100)
    except:
        flash('I am very sorry. It seems we are having database issues. Please retry your query or come back again later.')
        return redirect(url_for('flash_home'))

    if len(results) == 0:
        flash('No results found for %s. Please try again.' % (session['username'],))
        return redirect(url_for('flash_home'))

    if len(results) == 100:
        msg = '(Search limited to 100 most recently active users)'
    else:
        msg = ''

    return render_template('results.html', query=session['username'], message=msg, results=results)


@app.route('/newest')
def newest():
    try:
        connection = psycopg2.connect("dbname='osm_users' host='localhost' user='osm_users_view' password='osm'")
        cursor = connection.cursor()
        cursor.execute("""SELECT * FROM users ORDER BY start_date DESC;""")
        results = cursor.fetchmany(250)
    except:
        flash('I am very sorry. It seems we are having database issues. Please retry your query or come back again later.')
        return redirect(url_for('flash_home'))

    qry = 'the newest editors'
    msg = '(Search limited to the 250 newest users)'

    return render_template('results.html', query=qry, message=msg, results=results)


@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == '__main__':
    app.run()
