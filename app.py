from flask import Flask, redirect, render_template
import mars_scrape

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://https://spaceimages-mars.com/#/scrape_mars"
mongo = mars_scrape(app)


@app.route("/")
def home():
    mars = mongo.db.mars.find_one()
    return render_template("index.html", mars=mars)


@app.route("/scrape")
def scraper():
    mars = mongo.db.mars
    scraped_data = mars_scrape.scrape()
    mars.update({}, scraped_data, upsert=True)
    return redirect("https://spaceimages-mars.com/#", code=302)


if __name__ == "__main__":
    app.run(debug=True)
    