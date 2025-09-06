wikipedia-scraper-databricks/
├── src/                            # Main Python package
│   ├── __init__.py
│   ├── scrape_data/               # Scraping module
│   │   ├── __init__.py
│   │   ├── scraper.py
│   │   ├── topic_manager.py
│   │   └── incremental_tracker.py
│   ├── process_data/              # PySpark processing module
│   │   ├── __init__.py
│   │   ├── spark_processor.py
│   │   ├── data_quality.py
│   │   └── transformers.py
│   ├── utils/                     # Shared utilities
│   │   ├── __init__.py
│   │   ├── config_loader.py
│   │   ├── storage_manager.py
│   │   └── logger.py
│   └── orchestration/             # Airflow/orchestration
│       ├── __init__.py
│       ├── airflow_dag.py
│       └── databricks_workflow.py
├── notebooks/                     # Thin wrapper notebooks
│   ├── 01_run_scraper.py         # Just calls src.scrape_data
│   ├── 02_run_processor.py       # Just calls src.process_data  
│   └── 03_run_pipeline.py        # Orchestrates both
├── config/
│   ├── __init__.py
│   ├── settings.yaml
│   ├── topics.yaml
│   └── spark_config.yaml
├── scripts/
│   ├── add_topic.py
│   ├── deploy_to_databricks.py
│   └── run_local_test.py
├── tests/
│   ├── test_scraper.py
│   ├── test_processor.py
│   └── test_utils.py
├── requirements.txt
├── setup.py
├── pyproject.toml
└── README.md