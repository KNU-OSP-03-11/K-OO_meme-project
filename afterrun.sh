#!/bin/bash
# run program
python crawl_test.py
python crawl_links.py
echo "data crawling complete"
python app.py
