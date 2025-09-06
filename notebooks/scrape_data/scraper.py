"""
Main scraping module - pure Python, no Databricks dependencies
"""
import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import time
from typing import Dict, List, Optional
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from src.utils.logger import get_logger  # Updated import

logger = get_logger(__name__)

class WikipediaScraper:
    def __init__(self, rate_limit_delay: float = 1.0):
        self.session = requests.Session()
        self.rate_limit_delay = rate_limit_delay
        self.session.headers.update({
            'User-Agent': 'WikipediaScraper/1.0'
        })
    
    def scrape_page(self, url: str) -> Optional[Dict]:
        """Scrape a single Wikipedia page"""
        try:
            time.sleep(self.rate_limit_delay)
            
            response = self.session.get(url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract data
            title = self._extract_title(soup)
            content = self._extract_content(soup)
            categories = self._extract_categories(soup)
            links = self._extract_links(soup)
            
            return {
                'title': title,
                'content': content,
                'categories': categories,
                'links': links,
                'url': url,
                'scrape_timestamp': datetime.utcnow().isoformat(),
                'content_length': len(content),
                'success': True
            }
            
        except Exception as e:
            logger.error(f"Error scraping {url}: {e}")
            return None
    
    def _extract_title(self, soup) -> str:
        """Extract page title"""
        title = soup.find('h1', {'id': 'firstHeading'})
        return title.text if title else 'Unknown'
    
    def _extract_content(self, soup) -> str:
        """Extract main content"""
        content_div = soup.find('div', {'id': 'mw-content-text'})
        if content_div:
            # Remove unwanted elements
            for element in content_div.find_all(['sup', 'span.edit-section', 'table.infobox']):
                element.decompose()
            return content_div.get_text(separator='\n', strip=True)
        return ''
    
    def _extract_categories(self, soup) -> List[str]:
        """Extract categories"""
        categories = []
        cat_div = soup.find('div', {'id': 'mw-normal-catlinks'})
        if cat_div:
            categories = [a.text for a in cat_div.find_all('a')]
        return categories
    
    def _extract_links(self, soup) -> List[str]:
        """Extract internal links"""
        links = []
        for a in soup.find_all('a', href=True):
            href = a['href']
            if href.startswith('/wiki/') and ':' not in href:
                links.append(f"https://en.wikipedia.org{href}")
        return links