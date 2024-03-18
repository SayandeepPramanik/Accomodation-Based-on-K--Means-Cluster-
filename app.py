# pip install Flask
# pip install mysql-connector-python

from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

# Configure MySQL connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="ritvik@6",
    database="db2"
)


@app.route('/home')
def home():
    query = '''SELECT * from feature'''

    cursor = db.cursor(dictionary=True)
    cursor.execute(query)
    result = cursor.fetchall()

    #return render_template('search_results.html', results=result)
    return render_template('home.html', results=result, count=len(result))

@app.route('/')
def index():
    query = '''SELECT * from feature'''

    cursor = db.cursor(dictionary=True)
    cursor.execute(query)
    result = cursor.fetchall()

    #return render_template('search_results.html', results=result)
    return render_template('index.html', results=result, count=len(result))

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/properties')
def properties():
    return render_template('properties.html')

@app.route('/property-single')
def property_single():
    return render_template('property-single.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/services')
def services():
    return render_template('services.html')


@app.route('/search_results')
def search_results():
    return render_template('search_results.html')

@app.route('/search', methods=['POST'])
def search():
    # Retrieve user-selected features from the form
    selected_features = request.form.getlist('feature')

    # Execute the SQL query based on user-selected features


    # query = '''
    #     SELECT Flat.*
    #     FROM Flat
    #     JOIN FlatFeature ON Flat.FlatID = FlatFeature.FlatID
    #     JOIN FeatureType ON FlatFeature.FeatureTypeID = FeatureType.FeatureTypeID
    #     JOIN Feature ON FeatureType.FeatureID = Feature.FeatureID
    #     JOIN Location ON Feature.LocationID = Location.LocationID
    #     WHERE FeatureName IN ({})
    #     AND FeatureTypeName = 'Distance'
    #     ;
    # '''.format(', '.join(["'{}'".format(feature) for feature in selected_features]))
    
    try:
        query = '''SELECT f.*, loc.*
            FROM flat AS f
            JOIN flatfeature AS ff ON f.FlatID = ff.FlatID
            JOIN feature AS ft ON ff.FeaturetypeID = ft.FeatureID
            JOIN location as loc on loc.locationid=f.locationid
            WHERE ft.FeatureName IN ({})
            GROUP BY f.FlatID
            HAVING COUNT(DISTINCT ft.FeatureID) = {}'''.format(', '.join(["'{}'".format(feature) for feature in selected_features]), len(selected_features))
        print(query)
        cursor = db.cursor(dictionary=True)
        cursor.execute(query)
        result = cursor.fetchall()
    except Exception as exp:
        print()

    return render_template('search_results.html', results=result)

if __name__ == '__main__':
    app.run(debug=True)
