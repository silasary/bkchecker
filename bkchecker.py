# /// script
# dependencies = [
#   "requests",
#   "beautifulsoup4",
#   "python-dotenv",
# ]
# ///

# A very barebones script by Silasary.
# To configure, point it at the Spoiler file (Including Playthrough!), and the web tracker
# It'll tell you what the lowest incomplete sphere is, and which checks in that sphere have not been done.
# It does not tell you what items are there.
# This is designed with the intention of untangling BK'd multiworlds without anyone (even the host) having to read the spoiler log directly.
# If it doesn't work, let me know, this was thrown together in an afternoon and tested on exactly one multiworld.

import os
import re
import sys
import requests
from bs4 import BeautifulSoup, Tag
import dotenv

dotenv.load_dotenv()

TRACKER_URL = os.getenv("TRACKER_URL", None)
SPOILER_PATH = os.getenv("SPOILER_PATH", None)

if not TRACKER_URL:
    print("Please enter the url of the multiworld tracker (Looks like https://archipelago.gg/tracker/AAAAAAA):")
    TRACKER_URL = input().strip()
    dotenv.set_key('.env', 'TRACKER_URL', TRACKER_URL)

if not SPOILER_PATH:
    print("Please enter the path to the spoiler log (Including playthrough)")
    print("(Looks like C:\\ProgramData\\Archipelago\\output\\AP_03331224368454627526\\AP_03331224368454627526_Spoiler.txt or https://archipelago.gg/dl_spoiler/AAAAAAA):")
    SPOILER_PATH = input().strip()
    dotenv.set_key('.env', 'SPOILER_PATH', SPOILER_PATH)

def process_table(table: Tag) -> list[dict]:
    headers = [i.string for i in table.find_all("th")]
    rows = [[try_int(i) for i in r.find_all("td")] for r in table.find_all("tr")[1:]]
    return [dict(zip(headers, r)) for r in rows]


def try_int(text: Tag | str) -> str | int:
    if isinstance(text, Tag):
        if text.string:
            text = text.string
        else:
            text = text.get_text()
    text = text.strip()
    try:
        return int(text)
    except ValueError:
        return text

def process_locations(table: Tag) -> dict[str, bool]:
    checks = {}
    if table is None:
        return checks
    rows = process_table(table)
    for r in rows:
        checks[r["Location"]] = bool(r["Checked"])
    return checks

def fetch_tracker(room: str, slot: int) -> dict[str, bool]:
    url = f'{room}/0/{slot}'
    req = requests.get(url)
    if req.status_code == 200:
        soup = BeautifulSoup(req.text, 'html.parser')
        table = soup.find(id="locations-table")
        return process_locations(table)
    return {}



lineRegex = r'^\s*(.*) \((.{1,16}?)\):\s+(.*)\((.{1,16}?)\)$'

if os.path.exists(SPOILER_PATH):
    with open(SPOILER_PATH, 'r') as f:
        lines = f.readlines()
elif re.match(r'^https?://', SPOILER_PATH):
    req = requests.get(SPOILER_PATH)
    if req.status_code == 200:
        lines = req.text.splitlines()
    else:
        print("Failed to fetch spoiler log from url")
        sys.exit(1)
else:
    print("Invalid spoiler path")
    sys.exit(1)

player_checks: dict[str, dict] = {}
inPlaythrough = False
checks = []
sphere = None
for line in lines:
    line = line.strip()
    if not inPlaythrough:
        if m := re.match(r'Player (\d+): (.{1,16})', line):
            player_checks[m.group(2)] = fetch_tracker(TRACKER_URL, m.group(1))
        if line == "Playthrough:":
            inPlaythrough = True
        continue
    if re.match(r'^\d+: \{$', line):
        checks = []
        sphere = int(line.split(':')[0].strip())
    elif m := re.match(lineRegex, line):
        checks.append((m.group(1), m.group(2)))
    elif line == '}':
        abort = False
        # Check the contents of checks against tracker
        for check in checks:
            location_name, slotname = check
            if player_checks[slotname].get(location_name, True) == False:
                print(f"Missing: {location_name} ({slotname}) in sphere {sphere}")
                abort = True
        if abort:
            sys.exit(1)
        pass
    elif not line.strip():
        pass  # Blank line
    elif sphere == 0:
        pass # Starting items don't meet the regex
    else:
        inPlaythrough = False
        print("Unexpected:" + line)

