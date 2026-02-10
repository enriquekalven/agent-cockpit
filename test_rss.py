import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime

url = "https://blog.google/technology/ai/rss/"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'})

try:
    with urllib.request.urlopen(req, timeout=10) as response:
        content = response.read()
        print(f"Content length: {len(content)}")
        root = ET.fromstring(content)
        print(f"Root tag: {root.tag}")
        if root.tag == 'rss':
            channel = root.find('channel')
            print(f"Channel found: {channel is not None}")
            if channel is not None:
                latest_item = channel.find('item')
                print(f"Item found: {latest_item is not None}")
                if latest_item is not None:
                    title = latest_item.find('title').text
                    print(f"Title: {title}")
except Exception as e:
    print(f"Error: {e}")
