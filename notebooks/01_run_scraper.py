# Databricks notebook source
# MAGIC %md
# MAGIC # Run Wikipedia Scraper

# COMMAND ----------

# MAGIC %run ../src/utils/_databricks_setup

# COMMAND ----------
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.utils.logger import get_logger  # Updated import

from src.scrape_data.scraper import WikipediaScraper
# from src.scrape_data.topic_manager import TopicManager
# from src.utils.config_loader import load_config, get_storage_paths
# from src.utils.storage_manager import save_scraped_data

# Load configuration
config = load_config('../config/settings.yaml')
paths = get_storage_paths(config)

# Initialize components
scraper = WikipediaScraper()
topic_manager = TopicManager('../config/topics.yaml')

# Scrape data
topics = topic_manager.get_topics()
scraped_data = []

for topic_name, topic_url in topics.items():
    data = scraper.scrape_page(topic_url)
    if data:
        data['topic'] = topic_name
        scraped_data.append(data)

# Save to storage
if scraped_data:
    save_scraped_data(scraped_data, paths['raw_path'])
    print(f"Saved {len(scraped_data)} items to {paths['raw_path']}")