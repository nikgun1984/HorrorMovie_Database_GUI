from flask import Flask, render_template, url_for,redirect,session,request
from form import EntryForm, SubmissionForm, Form1, InsertForm
from collections import Counter
import pymysql

app = Flask(__name__)
db = pymysql.connect("localhost","project","13february","horror_movies" )

app.config['SECRET_KEY'] = '2d01cfb5a1d844e7072bd00fd2bd3691'

@app.route("/", methods=['GET', 'POST'])
@app.route("/index", methods=['GET', 'POST'])

def index():
    form = EntryForm()
    if form.query.data:
        return render_template('index.html', form=form)
    elif form.intQuery.data:
        return render_template('index.html', form=form)
    else:
        return render_template('index.html', form=form)

@app.route("/submit", methods=['GET', 'POST'])
def submit():
    form = SubmissionForm()
    #return render_template('submit.html', form=entry)
    if request.method == 'POST':
        if form.validate_on_submit():
            new_text = form.text.data
            return redirect(url_for('result', text=new_text))
    return render_template('submit.html', form=form)

@app.route("/insert", methods=['GET', 'POST'])
def insert():
    sql = """ SELECT actorName FROM Actors
              ORDER BY actorName; """
    cursor = db.cursor()
    rv = cursor.execute(sql)
    actors = cursor.fetchall()
    sql1 = """ SELECT dirName FROM Directors
               ORDER BY dirName; """
    rv = cursor.execute(sql1)
    directors = cursor.fetchall()
    form = InsertForm()
    form.actor.choices = [(actor[0],actor[0]) for actor in actors]
    form.director.choices = [(director[0],director[0]) for director in directors]

    #return render_template('submit.html', form=entry)
    if request.method == 'POST':
        if form.validate_on_submit():
            new_name = form.name.data
            new_year = form.year.data

            new_runtime = form.runtime.data
            new_actor = form.actor.data
            new_director = form.director.data

            sql3 = """SELECT dirID FROM Directors
                    WHERE dirName = '"""+new_director+"""';"""
            rv3 = cursor.execute(sql3)
            directorID = cursor.fetchall()
            sql4 = """INSERT INTO `horror_movies`.`HorrorMovies`(`name`,`year`,`runtime`,`dirID`)
                      VALUES('"""+new_name+"',"+new_year+","+new_runtime+ \
                      ","+str(directorID[0][0])+");"
            rv4 = cursor.execute(sql4)
            db.commit()
            sql5 = """SELECT idActors FROM actors
                      WHERE actorName = '"""+new_actor+"""';"""
            rv5 = cursor.execute(sql5)
            actorID = cursor.fetchall()
            sql6 = """SELECT idScaryMovies FROM HorrorMovies
                      WHERE name = '"""+new_name+"""';"""
            rv6 = cursor.execute(sql6)
            movieID = cursor.fetchall()
            sql7 = """INSERT INTO `horror_movies`.`HorrorMovies_Actors`(`idScaryMovies`,
                     `idActors`) VALUES("""+str(movieID[0][0])+","+str(actorID[0][0])+");"
            rv7 = cursor.execute(sql7)
            sql8 = """INSERT INTO `horror_movies`.`HorrorMovies_Country`(`idScaryMovies`,`idCountry`)
            VALUES("""+str(movieID[0][0])+","+str(2)+");"
            rv8 = cursor.execute(sql8)

            sql9 = """INSERT INTO `horror_movies`.`HorrorMovies_Company`(`idScaryMovies`,`idCompany`)
            VALUES("""+str(movieID[0][0])+","+str(7)+");"
            rv9 = cursor.execute(sql9)
            db.commit()
            return render_template('insertresult.html')
    return render_template('insert.html', form=form)

@app.route("/form1", methods=['GET', 'POST'])
def form1():
    form = Form1()
    #return render_template('submit.html', form=entry)
    if request.method == 'POST':
        if form.validate_on_submit():
            new_text = form.text.data
            search_by = form.select.data
            print(search_by)
            return redirect(url_for('output', select=search_by,text=new_text))
    return render_template('form1.html', form=form)

@app.route("/submit1", methods=['GET', 'POST'])
def submit1():
    return render_template('submit1.html')

@app.route("/submit2", methods=['GET', 'POST'])
def submit2():
    return render_template('submit2.html')

#3 tables joined
@app.route('/result1')
def result1():
    #return render_template('submit.html', form=entry)
    cursor = db.cursor()
    sql = """SELECT name,Directors.dirName, year, metascore,runtime, countryName
            FROM HorrorMovies,Directors,HorrorMovies_Country, Country
            WHERE HorrorMovies.dirID = Directors.dirID AND
            HorrorMovies.idScaryMovies = HorrorMovies_Country.idScaryMovies
            AND Country.idCountry = HorrorMovies_Country.idCountry
            AND year = year(CURRENT_DATE)
            AND metascore is not null
            ORDER BY name;"""
    rv = cursor.execute(sql)

    if rv > 0:
        movieDetails = cursor.fetchall()
        return render_template('result1.html',movieDetails=movieDetails)

#2 tables joined
@app.route('/result2')
def result2():
    #return render_template('submit.html', form=entry)
    cursor = db.cursor()
    sql = """SELECT name, dirName, imdbRatings, year
             FROM HorrorMovies,Directors
             WHERE HorrorMovies.dirID = Directors.dirID
             ORDER BY imdbRatings DESC, year
             LIMIT 10;"""
    rv = cursor.execute(sql)

    if rv > 0:
        movieDetails = cursor.fetchall()
        return render_template('result2.html',movieDetails=movieDetails)
#1 table
@app.route('/result3')
def result3():
    #return render_template('submit.html', form=entry)
    cursor = db.cursor()
    sql = """WITH maxRate AS(SELECT year, MAX(imdbRatings) AS maxRate
             FROM HorrorMovies
             GROUP BY year)

             SELECT HorrorMovies.year,name, HorrorMovies.imdbRatings
             FROM HorrorMovies, maxRate
             WHERE HorrorMovies.imdbRatings = maxRate.maxRate AND
             HorrorMovies.year = maxRate.year
             ORDER BY year DESC;"""
    rv = cursor.execute(sql)

    if rv > 0:
        movieDetails = cursor.fetchall()
        return render_template('result3.html',movieDetails=movieDetails)
#3tables joined
@app.route('/result4')
def result4():
    #return render_template('submit.html', form=entry)
    cursor = db.cursor()
    sql = """SELECT name, year, imdbRatings, dirName, countryName, concat('$ ', format(gross, 2)) AS Revenue
             FROM HorrorMovies, Country, HorrorMovies_Country, Directors
             WHERE HorrorMovies.idScaryMovies = HorrorMovies_Country.idScaryMovies
             AND Country.idCountry = HorrorMovies_Country.idCountry
             AND Directors.dirID = HorrorMovies.dirID
             ORDER BY gross DESC
             LIMIT 10;"""
    rv = cursor.execute(sql)

    if rv > 0:
        movieDetails = cursor.fetchall()
        return render_template('result4.html',movieDetails=movieDetails)
#2 tables joined
@app.route('/result5')
def result5():
    #return render_template('submit.html', form=entry)
    cursor = db.cursor()
    sql = """SELECT dirName AS Director, COUNT(name) AS 'Movie Count'
             FROM HorrorMovies, Directors
             WHERE HorrorMovies.dirID = Directors.dirID
             GROUP BY dirName
             ORDER BY COUNT(name) DESC;"""
    rv = cursor.execute(sql)

    if rv > 0:
        movieDetails = cursor.fetchall()
        return render_template('result5.html',movieDetails=movieDetails)

@app.route('/result/<text>')
def result(text):
    cursor = db.cursor()
    rv = cursor.execute(text)

    if rv > 0:
        movieDetails = cursor.fetchall()
        return render_template('result.html',movieDetails=movieDetails)

#Form Query has 4 tables joined
@app.route('/output/<select>/<text>')
def output(select,text):
    sql = """WITH minCompany AS (SELECT MIN(idCompany) AS idCompany, idScaryMovies
            FROM HorrorMovies_Company
            GROUP BY idScaryMovies)

            SELECT DISTINCT name, year, imdbRatings, dirName, compName, countryName
            FROM HorrorMovies, Country, HorrorMovies_Country, Directors, Company, HorrorMovies_Company, minCompany
            WHERE HorrorMovies.idScaryMovies = HorrorMovies_Country.idScaryMovies
            AND Country.idCountry = HorrorMovies_Country.idCountry
            AND Directors.dirID = HorrorMovies.dirID
            AND HorrorMovies.idScaryMovies = minCompany.idScaryMovies
            AND Company.idCompany = minCompany.idCompany
            AND name LIKE '%"""+text+"""%'
            ORDER BY name;"""
    sql2 = """SELECT dirName, name, year, imdbRatings
            FROM HorrorMovies, Directors
            WHERE Directors.dirID = HorrorMovies.dirID
            AND dirName LIKE '%"""+text+"""%'
            ORDER BY name; """
    sql3 = """SELECT actorName, name, year, imdbRatings
            FROM HorrorMovies, Actors, HorrorMovies_Actors
            WHERE Actors.idActors = HorrorMovies_Actors.idActors
            AND HorrorMovies.idScaryMovies = HorrorMovies_Actors.idScaryMovies
            AND actorName LIKE '%"""+text+"""%'
            ORDER BY name; """
    cursor = db.cursor()
    rv = 0
    if select == 'Name':
        rv = cursor.execute(sql)
        if rv > 0:
            movieDetails = cursor.fetchall()
            return render_template('output.html',movieDetails=movieDetails)
        else:
            return render_template('error.html', c='500'), 500
    elif select == 'Actor':
        rv = cursor.execute(sql3)
        if rv > 0:
            movieDetails = cursor.fetchall()
            return render_template('output1.html',movieDetails=movieDetails)
        else:
            return render_template('error.html', c='500'), 500
    elif select == 'Director':
        rv = cursor.execute(sql2)
        if rv > 0:
            movieDetails = cursor.fetchall()
            return render_template('output2.html',movieDetails=movieDetails)
        else:
            return render_template('error.html', c='500'), 500

@app.errorhandler(404)
def page_not_found1(e):
    return render_template('error.html', c='404'), 404

@app.errorhandler(403)
def page_not_found2(e):
    return render_template('error.html', c='403'), 403

@app.errorhandler(500)
def page_not_found3(e):
    return render_template('error.html', c='500'), 500

if __name__ == '__main__':
    app.run(debug=True)
