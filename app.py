# import dependencies
# Use Flask to render a template, redirecting to another url and creating a url
from flask import Flask, render_template, redirect, url_for
# use PyMongo to interact with mongo database
from flask_pymongo import PyMongo

# use the scraping code we will convert from Jypyter notebook to python
import scraping

# Set up flask
app=Flask(__name__)

# Create connect to Mongo using PyMongo
# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# Set up the route to our page
@app.route("/")
def index():
    mars = mongo.db.mars.find_one()
    return render_template("index.html", mars=mars)

# Set up 'scraping' route
@app.route("/scrape")
def scrape():
    mars = mongo.db.mars 
    mars_data = scraping.scrape_all()
    mars.update({}, mars_data, upsert=True)
    return redirect('/', code=302)

# Tell Flask to run
if __name__ == "__main__":
   app.run()