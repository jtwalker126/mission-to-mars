from flask import Flask, render_template
from flask_pymongo import PyMongo
import scraping

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

@app.route("/")
def index():
   mars = mongo.db.mars.find_one()
   hemisphere = mongo.db.hemisphere
   hemispheres = [elm for elm in hemisphere.find({})]
   print(hemispheres)
   return render_template("index.html", mars=mars, hemispheres=hemispheres)

@app.route("/scrape")
def scrape():
   mars = mongo.db.mars
   hemisphere = mongo.db.hemisphere
   hemisphere.delete_many({})
   mars_data = scraping.scrape_all()
   mars.update({}, mars_data, upsert=True)
   hemisphere_data = scraping.hemisphere_images()
   #print(hemisphere_data)
   hemisphere.insert_many(hemisphere_data)
   return "Scraping successful!"

if __name__ == "__main__":
    app.run()
   