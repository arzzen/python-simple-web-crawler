# Requirements

```bash
python v2.7.x
pip install beautifulsoup4
```

# Crawler options

```python
Options:
  --version             show program's version number and exit
  -h, --help            show this help message and exit
  -q, --quiet           Enable quiet mode
  -l, --links           Get links for specified url only
  -d DEPTH_LIMIT, --depth=DEPTH_LIMIT
                        Maximum depth to traverse
  -c CONFINE, --confine=CONFINE
                        Confine crawl to specified prefix
  -x EXCLUDE, --exclude=EXCLUDE
                        Exclude URLs by prefix
  -L, --show-links      Output links found
  -u, --show-urls       Output URLs found
  -D, --dot             Output Graphviz dot file
  -p OUT_PATH, --path=OUT_PATH
                        Output path directory
Usage: crawler.py [options] <url>


```
# Usage

```python
python crawler.py -d 0 -u -p "/var/tmp/downloaded/" "https://github.com/"
```

