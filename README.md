# 2006-Portfolio
Portfolio tasks


C15
# Threat Intelligence Module Demo

This Python module fetches threat intelligence indicators and contextual threat data from the AlienVault OTX API and processes them into a local cache. It demonstrates:

- Querying public OTX pulses for IPs, domains, or URLs
- Extracting relevant indicators (malware families, YARA rules)
- Caching responses in SQLite for offline lookup
- Simple summary reports of threat reputations
