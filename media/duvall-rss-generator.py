import datetime
import os
import requests

# Config
base_url = "https://www.dukeduvall.com/MOTD/"
feed_title = "Duke DuVall Message of the Day"
feed_link = "https://wesleymartin.net/dukeduvall.xml"
feed_description = "Daily messages from Duke DuVall"
output_path = "lotw.xml"
days_back = 365  # One full year!

headers = {"User-Agent": "RSS-Bot/1.0"}

def file_exists(url):
    try:
        response = requests.head(url, headers=headers, timeout=5)
        return response.status_code == 200
    except requests.RequestException:
        return False

rss_items = []
today = datetime.date.today()
start_date = today - datetime.timedelta(days=days_back)

current_date = start_date
while current_date <= today:
    y, m, d = current_date.strftime("%Y"), current_date.strftime("%m"), current_date.strftime("%d")
    file_name = f"{y}-{m}-{d}.mp3"
    file_url = f"{base_url}{y}/{m}/{file_name}"

    if file_exists(file_url):
        pub_date = current_date.strftime("%a, %d %b %Y 00:00:00 +0000")
        item = f"""  <item>
    <title>Message of the Day - {current_date.strftime("%B %d")}</title>
    <enclosure url="{file_url}" type="audio/mpeg"/>
    <pubDate>{pub_date}</pubDate>
    <guid>{file_url}</guid>
    <link>{file_url}</link>
    <description>Daily message from Duke DuVall</description>
  </item>"""
        rss_items.append(item)
    current_date += datetime.timedelta(days=1)

rss_feed = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
<channel>
  <title>{feed_title}</title>
  <link>{feed_link}</link>
  <description>{feed_description}</description>
  <language>en-us</language>
{os.linesep.join(rss_items)}
</channel>
</rss>"""

with open(output_path, "w", encoding="utf-8") as f:
    f.write(rss_feed)

print(f"✅ RSS feed with {len(rss_items)} valid audio items saved to {output_path}")
