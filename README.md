# Global-News-Analytics-wikipedia
Build a Wikipedia Knowledge Trends Tracker to analyze trending topics, entities, and their relationships over time for media monitoring and content recommendations.




wikipedia-scraper/
├── dags/                           # Airflow DAGs directory
│   └── wikipedia_pipeline.py       # Main DAG with scraping and processing
├── plugins/
│   └── wikipedia_scraper/
│       ├── __in# Create directories
mkdir -p wikipedia-scraper/dags
mkdir -p wikipedia-scraper/plugins/wikipedia_scraper
mkdir -p wikipedia-scraper/config
mkdir -p wikipedia-scraper/data/raw/{topic_name}/year=2024/month=01/day=01
mkdir -p wikipedia-scraper/data/raw/{topic_name}/year=2024/month=01/day=02
mkdir -p wikipedia-scraper/data/processed/{topic_name}/year=2024/month=01/day=01
mkdir -p wikipedia-scraper/data/processed/{topic_name}/year=2024/month=01/day=02
mkdir -p wikipedia-scraper/data/state
mkdir -p wikipedia-scraper/scripts
mkdir -p wikipedia-scraper/logs

# Create files
touch wikipedia-scraper/dags/wikipedia_pipeline.py
touch wikipedia-scraper/plugins/wikipedia_scraper/__init__.py
touch wikipedia-scraper/plugins/wikipedia_scraper/scraper.py
touch wikipedia-scraper/plugins/wikipedia_scraper/topic_manager.py
touch wikipedia-scraper/plugins/wikipedia_scraper/data_handler.py
touch wikipedia-scraper/plugins/wikipedia_scraper/utils.py
touch wikipedia-scraper/config/__init__.py
touch wikipedia-scraper/config/settings.py
touch wikipedia-scraper/config/topics.yaml
touch wikipedia-scraper/data/raw/{topic_name}/year=2024/month=01/day=01/data.json
touch wikipedia-scraper/data/raw/{topic_name}/year=2024/month=01/day=02/data.json
touch wikipedia-scraper/data/processed/{topic_name}/year=2024/month=01/day=01/
touch wikipedia-scraper/data/processed/{topic_name}/year=2024/month=01/day=02/
touch wikipedia-scraper/data/state/last_scraped.json
touch wikipedia-scraper/scripts/pyspark_processor.py
touch wikipedia-scraper/scripts/topic_updater.py
touch wikipedia-scraper/logs/scraper.log
touch wikipedia-scraper/requirements.txt
touch wikipedia-scraper/README.mdit__.py
│       ├── scraper.py             # Main scraping logic
│       ├── topic_manager.py       # Topic management and tracking
│       ├── data_handler.py        # Data storage and retrieval
│       └── utils.py               # Utility functions
├── config/
│   ├── __init__.py
│   ├── settings.py                # Configuration settings
│   └── topics.yaml                # Topic definitions and URLs
├── data/
│   ├── raw/                       # Raw scraped data (for PySpark)
│   │   └── {topic_name}/          # Separate directory per topic
│   │       ├── year=2024/
│   │       │   ├── month=01/
│   │       │   │   ├── day=01/
│   │       │   │   │   └── data.json
│   │       │   │   └── day=02/
│   │       │   │       └── data.json
│   ├── processed/                 # Processed data by PySpark
│   │   └── {topic_name}/
│   │       ├── year=2024/
│   │       │   ├── month=01/
│   │       │   │   ├── day=01/
│   │       │   │   └── day=02/
│   └── state/                     # State tracking files
│       └── last_scraped.json      # Track last scrape time per topic
├── scripts/
│   ├── pyspark_processor.py       # PySpark data processing
│   └── topic_updater.py           # Script to add new topics
├── logs/
│   └── scraper.log
├── requirements.txt
└── README.md

# Create directories
mkdir -p wikipedia-scraper/dags
mkdir -p wikipedia-scraper/plugins/wikipedia_scraper
mkdir -p wikipedia-scraper/config
mkdir -p wikipedia-scraper/data/raw/{topic_name}/year=2024/month=01/day=01
mkdir -p wikipedia-scraper/data/raw/{topic_name}/year=2024/month=01/day=02
mkdir -p wikipedia-scraper/data/processed/{topic_name}/year=2024/month=01/day=01
mkdir -p wikipedia-scraper/data/processed/{topic_name}/year=2024/month=01/day=02
mkdir -p wikipedia-scraper/data/state
mkdir -p wikipedia-scraper/scripts
mkdir -p wikipedia-scraper/logs

# Create files
touch wikipedia-scraper/dags/wikipedia_pipeline.py
touch wikipedia-scraper/plugins/wikipedia_scraper/__init__.py
touch wikipedia-scraper/plugins/wikipedia_scraper/scraper.py
touch wikipedia-scraper/plugins/wikipedia_scraper/topic_manager.py
touch wikipedia-scraper/plugins/wikipedia_scraper/data_handler.py
touch wikipedia-scraper/plugins/wikipedia_scraper/utils.py
touch wikipedia-scraper/config/__init__.py
touch wikipedia-scraper/config/settings.py
touch wikipedia-scraper/config/topics.yaml
touch wikipedia-scraper/data/raw/{topic_name}/year=2024/month=01/day=01/data.json
touch wikipedia-scraper/data/raw/{topic_name}/year=2024/month=01/day=02/data.json
touch wikipedia-scraper/data/processed/{topic_name}/year=2024/month=01/day=01/
touch wikipedia-scraper/data/processed/{topic_name}/year=2024/month=01/day=02/
touch wikipedia-scraper/data/state/last_scraped.json
touch wikipedia-scraper/scripts/pyspark_processor.py
touch wikipedia-scraper/scripts/topic_updater.py
touch wikipedia-scraper/logs/scraper.log
touch wikipedia-scraper/requirements.txt
touch wikipedia-scraper/README.md