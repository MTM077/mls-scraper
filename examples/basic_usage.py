from mls_scraper import MLSScraper

# Initialize scraper
scraper = MLSScraper(headless=True)

# Scrape Zillow listings
print("Scraping Zillow for properties in San Francisco...")
listings = scraper.scrape_zillow(
    location='San Francisco, CA',
    min_price=500000,
    max_price=2000000,
    limit=50
)

print(f"Found {len(listings)} listings\n")

# Display results
for listing in listings[:5]:
    print(f"📍 {listing['address']}")
    print(f"   Price: ${listing['price']:,}")
    print(f"   Beds: {listing['beds']} | Baths: {listing['baths']} | SqFt: {listing['sqft']:,}")
    print()

# Export to CSV
scraper.export_csv('sf_properties.csv', listings)
print("✓ Exported to sf_properties.csv")
