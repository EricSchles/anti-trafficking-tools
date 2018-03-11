from app import db

class BackpageAdInfo(db.Model):
    """
    This model gives us a set of specific information from each add scraped from backpage.

    parameters:
    @ad_title - used primarily to uniquely identify backpage ads - since titles are unique
    @phone_number - the phone number used in the ad, can be empty.  This number is stored as a string
    since it should be thought of as immutable.
    @city - the city the ad is from
    @state - the state the ad is from
    @location - the location mentioned in the advertisement
    @latitude - latitude derived from the location mentioned in the advertisement
    @longitude - longitude derived from the location mentioned in the advertisement
    @ad_body - the long form text in the ad
    @photos - a filepath link to the set of pictures downloaded for the ad
    @post_id - an id for each backpage post from backpage
    @timestamp - when the ad was scraped
    @url - the url of the scraped ad
    """
    __tablename__ = 'ad_info'
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String)
    ad_title = db.Column(db.String)
    phone_number = db.Column(db.String)
    location = db.Column(db.String)
    latitude = db.Column(db.String)
    longitude = db.Column(db.String)
    ad_body = db.Column(db.String)
    photos = db.Column(db.String)
    post_id = db.Column(db.String)
    timestamp = db.Column(db.DateTime)
    city = db.Column(db.String)
    state = db.Column(db.String)

    def __init__(self,url, ad_title, phone_number, ad_body, location, latitude, longitude, photos, post_id,timestamp, city, state):
        self.url = url
        self.ad_title = ad_title
        self.phone_number = phone_number
        self.location = location
        self.latitude = latitude
        self.longitude = longitude
        self.ad_body = ad_body
        self.photos = photos
        self.post_id = post_id
        self.timestamp = timestamp
        self.city = city
        self.state = state
