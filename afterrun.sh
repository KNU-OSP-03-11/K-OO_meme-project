#!/bin/bash
# run program
source pyvenv/bin/activate
echo "data crawling start"
python crawl_test.py
python crawl_links.py
echo "data crawling complete"
echo "flask web service start"
python app.py
