from django.core.serializers import json, serialize
from .models import Listings
import json

def backup():
    # Fetch all listings
    listings = Listings.objects.all()

    # Option 1: Save as JSON
    data = json.dumps(serialize("json", listings), indent=4)
    with open("listings_backup.json", "w") as outfile:
        outfile.write(data)

def refill():
    with open("listings_backup.json", "r") as infile:
        data = json.load(infile)

    # Each element in 'data' is a serialized representation of a listing
    # print(data)
    for listing_data in data:
        
        title = listing_data["fields"]["title"]
        description = listing_data["fields"]["description"]
        img_url = listing_data["fields"].get("img_url", None)  # Handle optional field
        owner_id = listing_data["fields"]["owner"]  # Assuming owner is stored as ID
        category = listing_data["fields"]["category"]
        active = listing_data["fields"]["active"]

# Create a new Listings object with the extracted data
        listing = Listings.objects.create(
            title=title,
            description=description,
            img_url=img_url,
            owner=owner_id,
            category=category,
            active=active,
        )
        # Save the listing to the database
        listing.save()
