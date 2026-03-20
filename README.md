# Real Estate MLS Scraper

Scrape real estate listings from Zillow, Redfin, Trulia, and MLS databases. Extract property data, pricing, images, market trends.

## Features

- **Multi-site scraping** — Zillow, Redfin, Trulia, Realtor.com
- **MLS integration** — Direct MLS API where available
- **Property extraction** — address, price, beds, baths, sqft, year built, listing agent
- **Image scraping** — download all property photos automatically
- **Market analysis** — track price trends by neighborhood/zip code
- **Lead generation** — export fresh listings for outreach
- **Historical data** — track price changes over weeks/months
- **Proxy rotation** — handle anti-bot protection on major sites

## Use Cases

- **Real estate investing** — find undervalued properties
- **Market analysis** — analyze neighborhood trends
- **Lead generation** — automated realtor/buyer leads
- **Competitive intelligence** — monitor competitor listings
- **Data research** — historical pricing datasets

## Installation

```bash
pip install mls-scraper
```

## Quick Start

```python
from mls_scraper import MLSScraper

scraper = MLSScraper()

# Scrape Zillow listings
listings = scraper.scrape_zillow(
    location='Los Angeles, CA',
    min_price=300000,
    max_price=1000000,
    limit=100
)

for listing in listings:
    print(f"{listing['address']} - ${listing['price']}")
    print(f"  {listing['beds']} bed / {listing['baths']} bath / {listing['sqft']} sqft")

# Export to CSV
scraper.export_csv('la_properties.csv', listings)
```

## Advanced Usage

```python
# Multi-site scrape
listings = scraper.scrape_multiple(
    sites=['zillow', 'redfin', 'realtor'],
    location='San Francisco, CA',
    property_type='single_family',
    min_beds=3,
    max_price=2000000
)

# Download all images
scraper.download_images(listings, output_dir='property_photos/')

# Get market trends
market_data = scraper.get_market_trends(
    location='94102',  # San Francisco zip
    days=90
)

print(f"Average price: ${market_data['avg_price']}")
print(f"Price trend: {market_data['trend']}")  # up/down/stable
```

## Data Structure

```json
{
  "mls_id": "12345678",
  "source": "zillow",
  "address": "123 Main St, San Francisco, CA 94102",
  "price": 2500000,
  "beds": 3,
  "baths": 2,
  "sqft": 2100,
  "lot_size": 5000,
  "year_built": 1995,
  "property_type": "single_family",
  "listing_agent": "John Smith",
  "listing_agent_phone": "(555) 123-4567",
  "listing_date": "2026-03-19",
  "days_on_market": 12,
  "price_history": [
    {"price": 2600000, "date": "2026-03-19"},
    {"price": 2550000, "date": "2026-03-12"}
  ],
  "images": [
    "https://...photo1.jpg",
    "https://...photo2.jpg"
  ],
  "description": "Beautiful home in prime location...",
  "scraped_at": "2026-03-19T23:57:00Z"
}
```

## Performance

- Scrapes 50-200 listings per minute
- Image downloading: 20-50 photos per minute
- Handles pagination automatically
- Rate limiting to avoid IP bans

## Data Quality

- Address validation: 99%+ accuracy
- Price accuracy: verified against source
- Image completeness: captures all available photos
- Deduplication: removes duplicate listings across sites

## License

MIT
