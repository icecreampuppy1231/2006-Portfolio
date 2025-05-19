import os
import requests
import sqlite3
from datetime import datetime

# Configuration
OTX_API_KEY = os.getenv('OTX_API_KEY')  # set this in your env
BASE_URL = 'https://otx.alienvault.com/api/v1'
DB_PATH = 'threat_intel.db'

# Initialize SQLite cache
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS pulses (
    id TEXT PRIMARY KEY,
    indicator TEXT,
    type TEXT,
    created_at TEXT,
    description TEXT,
    raw_json TEXT
)''')
conn.commit()


def fetch_pulses(indicator, itype='hostname'):
    """
    Fetch OTX pulses for a given indicator (IP, hostname, URL).
    Caches results in SQLite and returns parsed pulses.
    """
    url = f"{BASE_URL}/indicators/{itype}/{indicator}/general"
    headers = {'X-OTX-API-KEY': OTX_API_KEY}
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    data = resp.json().get('pulse_info', [])

    results = []
    for pulse in data:
        pid = pulse['id']
        # Upsert into cache
        cursor.execute('''
            INSERT OR REPLACE INTO pulses
            (id, indicator, type, created_at, description, raw_json)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            pid,
            indicator,
            itype,
            pulse.get('created'),
            pulse.get('name'),
            str(pulse)
        ))
        results.append({
            'id': pid,
            'name': pulse.get('name'),
            'created': pulse.get('created'),
            'description': pulse.get('description', '')
        })
    conn.commit()
    return results


def get_cached_pulses(indicator):
    """
    Return cached pulses for an indicator from SQLite.
    """
    cursor.execute('SELECT id, description, created_at FROM pulses WHERE indicator=?', (indicator,))
    rows = cursor.fetchall()
    return [{'id': r[0], 'description': r[1], 'created': r[2]} for r in rows]


if __name__ == '__main__':
    # Demo usage
    test_indicator = 'example.com'
    print(f"Fetching pulses for {test_indicator}...")
    pulses = fetch_pulses(test_indicator, 'hostname')
    print(f"Found {len(pulses)} pulses.\nLatest:\")
    if pulses:
        latest = sorted(pulses, key=lambda p: p['created'], reverse=True)[0]
        print(latest)
    print("\nCached entries now:")
    print(get_cached_pulses(test_indicator))
