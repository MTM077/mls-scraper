import asyncio
import pandas as pd
from datetime import datetime
from typing import List, Dict, Optional
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import json
import logging
import os
import aiohttp

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MLSScraper:
    def __init__(self, headless=True, timeout=30, use_proxy=False):
        self.headless = headless
        self.timeout = timeout * 1000
        self.use_proxy = use_proxy
        self.listings = []

    async def scrape_zillow(self, location: str, min_price: int = 0, 
                           max_price: int = 10000000, limit: int = 100) -> List[Dict]:
        """Scrape Zillow listings"""
        listings = []
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=self.headless)
                page = await browser.new_page()
                
                # Zillow search URL
                url = f"https://www.zillow.com/homes/for_sale/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22usersSearchTerm%22%3A%22{location}%22%2C%22mapBounds%22%3Anull%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A%221%22%2C%22regionType%22%3A%22state%22%7D%5D%7D"
                
                await page.goto(url, wait_until='networkidle', timeout=self.timeout)
                
                # Scroll to load listings
                for _ in range(5):
                    await page.evaluate('window.scrollBy(0, 500)')
                    await page.wait_for_timeout(1000)
                
                content = await page.content()
                soup = BeautifulSoup(content, 'html.parser')
                
                # Parse listing cards
                listing_cards = soup.select('[data-test="property-card"]')
                
                for card in listing_cards[:limit]:
                    try:
                        address_elem = card.select_one('[data-test="property-address"]')
                        price_elem = card.select_one('[data-test="property-card-price"]')
                        beds_elem = card.select_one('[data-test="property-card-beds"]')
                        baths_elem = card.select_one('[data-test="property-card-baths"]')
                        sqft_elem = card.select_one('[data-test="property-card-sqft"]')
                        
                        listing = {
                            'source': 'zillow',
                            'address': address_elem.text.strip() if address_elem else 'Unknown',
                            'price': int(price_elem.text.replace('$', '').replace(',', '')) if price_elem else 0,
                            'beds': int(beds_elem.text.split()[0]) if beds_elem else 0,
                            'baths': int(baths_elem.text.split()[0]) if baths_elem else 0,
                            'sqft': int(sqft_elem.text.replace(',', '').split()[0]) if sqft_elem else 0,
                            'url': card.get('href', ''),
                            'scraped_at': datetime.now().isoformat()
                        }
                        
                        if min_price <= listing['price'] <= max_price:
                            listings.append(listing)
                    
                    except Exception as e:
                        logger.debug(f"Error parsing Zillow listing: {e}")
                
                await browser.close()
        
        except Exception as e:
            logger.error(f"Error scraping Zillow: {e}")
        
        return listings

    async def scrape_redfin(self, location: str, limit: int = 100) -> List[Dict]:
        """Scrape Redfin listings"""
        listings = []
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=self.headless)
                page = await browser.new_page()
                
                url = f"https://www.redfin.com/homes-for-sale/{location.replace(' ', '-')}"
                
                await page.goto(url, wait_until='networkidle', timeout=self.timeout)
                
                for _ in range(5):
                    await page.evaluate('window.scrollBy(0, 500)')
                    await page.wait_for_timeout(1000)
                
                content = await page.content()
                soup = BeautifulSoup(content, 'html.parser')
                
                listing_cards = soup.select('[data-testid="property-card"]')
                
                for card in listing_cards[:limit]:
                    try:
                        address_elem = card.select_one('.bp-Homecard__Address')
                        price_elem = card.select_one('[data-testid="property-card-price"]')
                        beds_elem = card.select_one('.bp-Homecard__bed')
                        baths_elem = card.select_one('.bp-Homecard__bath')
                        
                        listing = {
                            'source': 'redfin',
                            'address': address_elem.text.strip() if address_elem else 'Unknown',
                            'price': int(price_elem.text.replace('$', '').replace(',', '')) if price_elem else 0,
                            'beds': int(beds_elem.text.split()[0]) if beds_elem else 0,
                            'baths': int(baths_elem.text.split()[0]) if baths_elem else 0,
                            'url': card.get('href', ''),
                            'scraped_at': datetime.now().isoformat()
                        }
                        listings.append(listing)
                    
                    except Exception as e:
                        logger.debug(f"Error parsing Redfin listing: {e}")
                
                await browser.close()
        
        except Exception as e:
            logger.error(f"Error scraping Redfin: {e}")
        
        return listings

    async def scrape_multiple(self, sites: List[str], location: str, limit: int = 100) -> List[Dict]:
        """Scrape multiple real estate sites"""
        all_listings = []
        
        if 'zillow' in sites:
            zillow_listings = await self.scrape_zillow(location, limit=limit)
            all_listings.extend(zillow_listings)
        
        if 'redfin' in sites:
            redfin_listings = await self.scrape_redfin(location, limit=limit)
            all_listings.extend(redfin_listings)
        
        return all_listings

    async def download_images(self, listings: List[Dict], output_dir: str = 'property_photos/'):
        """Download all property images"""
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        async with aiohttp.ClientSession() as session:
            for listing in listings:
                images = listing.get('images', [])
                property_dir = os.path.join(output_dir, listing['address'].replace(' ', '_')[:50])
                
                if not os.path.exists(property_dir):
                    os.makedirs(property_dir)
                
                for i, image_url in enumerate(images):
                    try:
                        async with session.get(image_url) as resp:
                            filename = os.path.join(property_dir, f'photo_{i}.jpg')
                            with open(filename, 'wb') as f:
                                f.write(await resp.read())
                            logger.info(f"Downloaded {filename}")
                    except Exception as e:
                        logger.error(f"Error downloading {image_url}: {e}")

    def export_csv(self, filename: str, listings: List[Dict]):
        """Export listings to CSV"""
        df = pd.DataFrame(listings)
        df.to_csv(filename, index=False)
        logger.info(f"Exported {len(listings)} listings to {filename}")

    def export_json(self, filename: str, listings: List[Dict]):
        """Export listings to JSON"""
        with open(filename, 'w') as f:
            json.dump(listings, f, indent=2)
        logger.info(f"Exported {len(listings)} listings to {filename}")

    def scrape(self, site: str, location: str, limit: int = 100) -> List[Dict]:
        """Synchronous scrape"""
        if site == 'zillow':
            return asyncio.run(self.scrape_zillow(location, limit=limit))
        elif site == 'redfin':
            return asyncio.run(self.scrape_redfin(location, limit=limit))
        else:
            raise ValueError(f"Site '{site}' not supported")
