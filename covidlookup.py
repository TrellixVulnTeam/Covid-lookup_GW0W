# Imports..
from flask import Flask, render_template, send_from_directory, request, json
import os
import urllib.request
import json
import datetime
import random
import webbrowser
import threading

# Browser settings + open the browser with the Flaks url when the program is being runned..
port = 5000 # Change this if needed
url = "http://127.0.0.1:{0}".format(port)
threading.Timer(1.25, lambda: webbrowser.open(url) ).start()

# Generate secure key for the form session..
l33t = os.urandom(24)

# Set Flask config..
app = Flask(__name__)
app.config['SECRET_KEY'] = l33t

# /Search page..
@app.route('/search', methods=["GET", "POST"])
def search():
    if request.method == "POST":

        # Convert the PythonWTF ImmutableMultiDict to a normal dictionary..
        result = request.form.to_dict()

        # Make a query from the string we got from the POST form..
        query = result['Region']

        # API..
        covid_api = 'https://api.covid19api.com/summary'
        jso = urllib.request.urlopen(covid_api)
        data = json.load(jso)

        # Get date..
        date = datetime.datetime.utcnow()
        dataDate = date.strftime('%A %d %B %Y')

        # Overall general..
        totalInfected = data['Global']['TotalConfirmed']
        totalRecovered = data['Global']['TotalRecovered']
        totalDeceased = data['Global']['TotalDeaths']
        dailyInfected = data['Global']['NewConfirmed']
        dailyRecovered = data['Global']['NewRecovered']
        dailyDeceased = data['Global']['NewDeaths']

        # Create dictionaries for iteration..
        country_Names = {}
        country_TotalInfected = {}
        country_TotalDeceased = {}
        country_TotalRecovered = {}
        country_NewInfected = {}
        country_NewDeceased = {}
        country_NewRecovered = {}

        # Create scope for loop based on the number of countries..
        scope = data['Countries']

        # Iterate over data and put them into the dictionaries made earlier..
        for i in range(len(scope)):
            country_Names["country{0}|".format(i)] = data['Countries'][i]['Country']
            country_TotalInfected["TotalInfected{0}|".format(i)] = data['Countries'][i]['TotalConfirmed']
            country_TotalDeceased["TotalDeceased{0}|".format(i)] = data['Countries'][i]['TotalDeaths']
            country_TotalRecovered["TotalRecovered{0}|".format(i)] = data['Countries'][i]['TotalRecovered']
            country_NewInfected["NewInfected{0}|".format(i)] = data['Countries'][i]['NewConfirmed']
            country_NewDeceased["NewDeceased{0}|".format(i)] = data['Countries'][i]['NewDeaths']
            country_NewRecovered["NewRecovered{0}|".format(i)] = data['Countries'][i]['NewRecovered']

        # Create a placeholder list and choose one random from the list..
        placeholderList = ['Finland', 'Netherlands', 'Belgium', 'US', 'Germany', 'China']
        placeholder = random.choice(placeholderList)

        # If query is empty set country equal to the random chosen placeholder..
        if query == '':
            country = placeholder
        else:
            country = query

        # Iterate over the dictionaries and collect data..
        for x in range(len(country_Names)):
            if country in data['Countries'][x]['Country'] or country in data['Countries'][x]['Slug'] or country in data['Countries'][x]['CountryCode']:
                infectedTotal = data['Countries'][x]['TotalConfirmed']
                deceasedTotal = data['Countries'][x]['TotalDeaths']
                recoveredTotal = data['Countries'][x]['TotalRecovered']
                infectedNew = data['Countries'][x]['NewConfirmed']
                deceasedNew = data['Countries'][x]['NewDeaths']
                recoveredNew = data['Countries'][x]['NewRecovered']
                country = data['Countries'][x]['Country']
                break
        else:
            placeholder = 'Country not found'
            date = datetime.datetime.utcnow()
            date = date.strftime('%A %d %B %Y')
            return render_template('index.html',
                                   date=date,
                                   totalInfected=totalInfected,
                                   totalRecovered=totalRecovered,
                                   totalDeceased=totalDeceased,
                                   dailyInfected=dailyInfected,
                                   dailyRecovered=dailyRecovered,
                                   dailyDeceased=dailyDeceased,
                                   placeholder=placeholder)

        # Calculate the average confirmed infections by dividing the total confirmed globally by the country names..
        averageInfectedTotal = round(totalInfected / len(country_Names))
        averageInfectedToday = round(dailyInfected / len(country_Names))

        # Compare the total confirmed infections in a country to the average to make a country status..
        if infectedTotal < averageInfectedTotal:
            countryStatusTotal = 'Under average'
        elif infectedTotal > averageInfectedTotal and infectedTotal < 500000:
            countryStatusTotal = 'Average'
        elif infectedTotal > 500000:
            countryStatusTotal = 'Above average'

        # Compare the today's confirmed infections in a country to the average to make a country status..
        if infectedNew < averageInfectedToday:
            countryStatusToday = 'Under average'
        elif infectedNew > averageInfectedToday and infectedNew < 2500:
            countryStatusToday = 'Avarage'
        elif infectedNew > 2500:
            countryStatusToday = 'Above average'

        # Calculate a country percentage based on the total infected globally..
        countryTotalPercentage = "{:.2f}%".format(infectedTotal / totalInfected * 100)
        countryTodayPercentage = "{:.2f}%".format(infectedNew / dailyInfected * 100)

        # Format the integers by , (1000000 -> 1,000,000)..
        totalInfected = '{:,}'.format(data['Global']['TotalConfirmed'])
        infectedTotal = '{:,}'.format(data['Countries'][x]['TotalConfirmed'])
        dailyInfected = '{:,}'.format(data['Global']['NewConfirmed'])
        infectedNew = '{:,}'.format(data['Countries'][x]['NewConfirmed'])
        deceasedTotal = '{:,}'.format(data['Countries'][x]['TotalDeaths'])
        recoveredNew = '{:,}'.format(data['Countries'][x]['NewRecovered'])
        deceasedNew = '{:,}'.format(data['Countries'][x]['NewDeaths'])
        recoveredTotal = '{:,}'.format(data['Countries'][x]['TotalRecovered'])
        totalRecovered = '{:,}'.format(data['Global']['TotalRecovered'])
        totalDeceased = '{:,}'.format(data['Global']['TotalDeaths'])
        dailyRecovered = '{:,}'.format(data['Global']['NewRecovered'])
        dailyDeceased = '{:,}'.format(data['Global']['NewDeaths'])

        return render_template('search.html',
                               country=country,
                               result=result,
                               infectedTotal=infectedTotal,
                               deceasedTotal=deceasedTotal,
                               recoveredTotal=recoveredTotal,
                               infectedNew=infectedNew,
                               deceasedNew=deceasedNew,
                               recoveredNew=recoveredNew,
                               totalInfected=totalInfected,
                               totalDeceased=totalDeceased,
                               totalRecovered=totalRecovered,
                               dailyDeceased=dailyDeceased,
                               dailyInfected=dailyInfected,
                               dailyRecovered=dailyRecovered,
                               placeholder=placeholder,
                               date=dataDate,
                               countryStatusTotal=countryStatusTotal,
                               countryStatusToday=countryStatusToday,
                               countryTodayPercentage=countryTodayPercentage,
                               countryTotalPercentage=countryTotalPercentage)

    if request.method == "GET":
        # API..
        covid_api = 'https://api.covid19api.com/summary'
        jso = urllib.request.urlopen(covid_api)
        data = json.load(jso)

        # Get date..
        date = datetime.datetime.utcnow()
        date = date.strftime('%A %d %B %Y')

        # Create a placeholder list to display on the form..
        placeholderList = ['Finland', 'Netherlands', 'Belgium', 'US', 'Germany', 'China']
        placeholder = random.choice(placeholderList)

        # Overall general & Format the variables by , (1000000 -> 1,000,000)..
        totalInfected = '{:,}'.format(data['Global']['TotalConfirmed'])
        totalRecovered = '{:,}'.format(data['Global']['TotalRecovered'])
        totalDeceased = '{:,}'.format(data['Global']['TotalDeaths'])
        dailyInfected = '{:,}'.format(data['Global']['NewConfirmed'])
        dailyRecovered = '{:,}'.format(data['Global']['NewRecovered'])
        dailyDeceased = '{:,}'.format(data['Global']['NewDeaths'])

        return render_template('index.html',
                                   date=date,
                                   totalInfected=totalInfected,
                                   totalRecovered=totalRecovered,
                                   totalDeceased=totalDeceased,
                                   dailyInfected=dailyInfected,
                                   dailyRecovered=dailyRecovered,
                                   dailyDeceased=dailyDeceased,
                                   placeholder=placeholder)

@app.route('/')
def index():
    # API..
    covid_api = 'https://api.covid19api.com/summary'
    jso = urllib.request.urlopen(covid_api)
    data = json.load(jso)

    # Get date..
    date = datetime.datetime.utcnow()
    date = date.strftime('%A %d %B %Y')

    # Create a placeholder list to display on the form..
    placeholderList = ['Finland', 'Netherlands', 'Belgium', 'US', 'Germany', 'China']
    placeholder = random.choice(placeholderList)

    # Overall general & Format the variables by , (1000000 -> 1,000,000)..
    totalInfected = '{:,}'.format(data['Global']['TotalConfirmed'])
    totalRecovered = '{:,}'.format(data['Global']['TotalRecovered'])
    totalDeceased = '{:,}'.format(data['Global']['TotalDeaths'])
    dailyInfected = '{:,}'.format(data['Global']['NewConfirmed'])
    dailyRecovered = '{:,}'.format(data['Global']['NewRecovered'])
    dailyDeceased = '{:,}'.format(data['Global']['NewDeaths'])

    return render_template('index.html',
                           date=date,
                           totalInfected=totalInfected,
                           totalRecovered=totalRecovered,
                           totalDeceased=totalDeceased,
                           dailyInfected=dailyInfected,
                           dailyRecovered=dailyRecovered,
                           dailyDeceased=dailyDeceased,
                           placeholder=placeholder)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

if __name__ == "__main__":
    app.run(port=port)