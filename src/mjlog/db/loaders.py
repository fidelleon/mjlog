"""Data loaders for importing external data into database."""
import csv
import datetime
import enum
import io
import re
import zipfile

import feedparser
import requests
from bs4 import BeautifulSoup

from mjlog.db.models import DXCCEntity, InternetImportation
from mjlog.db.session import get_session

NS = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"


def col_letter_to_num(col_letter):
    """Convert Excel column letter to 0-based position.

    A=0, B=1, ..., Z=25, AA=26.
    """
    result = 0
    for char in col_letter:
        result = result * 26 + (ord(char) - ord('A') + 1)
    return result - 1


def get_big_cty():
    """Fetch the latest Big CTY data and update database prefixes."""
    # Use country-files feed to find the latest Big CTY URL
    date_matcher = re.compile(r'^.*?\s(\d\d)\s.*?(\w+)\s(\d+)')
    url: str = "https://www.country-files.com/feed/"
    feed = feedparser.parse(url)
    if feed.status != 200:
        raise Exception(f"Failed to fetch feed: HTTP {feed.status}")

    bigcty_data: dict | None = next(
        (entry for entry in feed.entries if entry.title.startswith('Big CTY')),
        None,
    )
    if bigcty_data is None:
        raise Exception("Big CTY entry not found in feed")

    title = bigcty_data['title']
    # This is not a regular dash, but an en dash (U+2013).
    filename = title.split(' – ')[0]

    matcher = date_matcher.match(title)
    if not matcher:
        raise Exception(f"Failed to parse date from title: {title}")

    groups = matcher.groups()

    # Format is "Big CTY – 22 October 2024".
    file_date: datetime.date = datetime.date(
        int(groups[2]),
        datetime.datetime.strptime(groups[1], '%B').month,
        int(groups[0]),
    )
    bigcty_url: str = bigcty_data['link']

    # Now, request the Big CTY page to find the actual download link
    response = requests.get(bigcty_url)
    response.raise_for_status()  # Ensure we got a successful response
    soup = BeautifulSoup(response.content, "html.parser")
    tag = soup.find('a', text='[download]')
    if tag is None:
        raise Exception("Download link not found in Big CTY page")

    # Now we have the download link, let's fetch the zip file
    bigcty_response = requests.get(tag['href'])
    bigcty_response.raise_for_status()
    buffer = io.BytesIO(bigcty_response.content)

    with zipfile.ZipFile(buffer, 'r') as zf:
        csv_data = zf.read("cty.csv")

    csv_file = csv.reader(io.StringIO(csv_data.decode('utf-8')))
    session = get_session()

    rows = [line for line in csv_file if len(line) > CtyLine.prefixes.value]
    cty_names = {line[CtyLine.name.value] for line in rows}
    entities_by_name = {}
    if cty_names:
        entities_by_name = {
            entity.name: entity
            for entity in session.query(DXCCEntity)
            .filter(DXCCEntity.name.in_(cty_names))
            .all()
        }

    for line in rows:
        cty_name = line[CtyLine.name.value]
        entity = entities_by_name.get(cty_name)
        if entity:
            entity.prefixes = line[CtyLine.prefixes.value].rstrip(';')
        else:
            print(f"Warning: No matching DXCCEntity found for {cty_name}")

    today = datetime.date.today()
    version = file_date.isoformat()
    updated = (
        session.query(InternetImportation)
        .filter(InternetImportation.filename == filename)
        .update(
            {
                InternetImportation.import_date: today,
                InternetImportation.import_version: version,
            },
            synchronize_session=False,
        )
    )

    if not updated:
        importation = InternetImportation(
            filename=filename,
            import_date=today,
            import_version=version
        )
        session.add(importation)
    session.commit()


class CtyLine(enum.Enum):
    """Enum for column indices in cty.csv from Big CTY."""
    # Example row:
    # ['XX9', 'Macao', '152', 'AS', '24', '44',
    #  '22.10', '-113.50', '-8.0', 'XX9;']
    prefix = 0
    name = 1
    entity_code = 2
    continent = 3
    cq_zone_id = 4
    itu_zone = 5
    latitude = 6
    longitude = 7
    utc_offset = 8
    prefixes = 9
