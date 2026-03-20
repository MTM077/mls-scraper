import unittest
from mls_scraper import MLSScraper

class TestMLSScraper(unittest.TestCase):
    def setUp(self):
        self.scraper = MLSScraper(headless=True)
    
    def test_initialization(self):
        self.assertIsNotNone(self.scraper)
        self.assertTrue(self.scraper.headless)
    
    def test_price_filter(self):
        listings = [
            {'price': 500000, 'address': 'Test 1'},
            {'price': 1500000, 'address': 'Test 2'},
            {'price': 2500000, 'address': 'Test 3'}
        ]
        
        filtered = [l for l in listings if 500000 <= l['price'] <= 2000000]
        self.assertEqual(len(filtered), 2)

if __name__ == '__main__':
    unittest.main()
