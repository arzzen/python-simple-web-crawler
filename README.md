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

```bash
python crawler.py -d 0 -u -p "/var/tmp/downloaded/" "https://github.com/"

Crawling https://github.com/ (Max Depth: 0)
Stats:    (2/s after 19.02s)
```

```bash
python crawler.py -d 0 -l "https://github.com/"

0. https://github.com/#start-of-content
1. https://github.com/
2. https://github.com/join
3. https://github.com/login
4. https://github.com/explore
5. https://github.com/features
6. https://enterprise.github.com/
7. https://github.com/blog
8. https://help.github.com/terms
9. https://help.github.com/privacy
10. https://github.com/plans
11. https://enterprise.github.com
12. https://github.com/integrations
13. https://central.github.com/mac/latest
14. https://mac.github.com
15. https://windows.github.com/
16. https://github-windows.s3.amazonaws.com/GitHubSetup.exe
17. https://windows.github.com
18. https://mac.github.com/
19. https://status.github.com/
20. https://developer.github.com
21. https://training.github.com
22. https://shop.github.com
23. https://github.com/about
24. https://help.github.com
25. https://github.com
26. https://github.com/site/terms
27. https://github.com/site/privacy
28. https://github.com/security
29. https://github.com/contact
```



