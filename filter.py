import requests
import pathlib
import datetime

URL = "https://iptv-org.github.io/iptv/countries/tr.m3u"
CHANNEL_LIST_FILE = "selected_channels.txt"
OUTPUT_FILE = "tr_custom.m3u"

def get_selected():
    return [line.strip().lower() for line in open(CHANNEL_LIST_FILE, encoding="utf-8")
            if line.strip() and not line.lstrip().startswith("#")]

def download_playlist():
    r = requests.get(URL, timeout=30)
    r.raise_for_status()
    return r.text.splitlines()

def filter_playlist(lines, wanted):
    out = ["#EXTM3U"]
    current_entry = []
    
    for line in lines:
        if line.startswith("#EXTINF"):
            # Extrahiere Kanalname aus dem letzten Komma-separierten Teil
            parts = line.split(',')
            name = parts[-1].split('(')[0].strip().lower()
            current_entry = [line] if name in wanted else []
            
        elif line.strip() and current_entry:
            # Füge Stream-URL hinzu wenn Kanal gewählt
            current_entry.append(line)
            out.extend(current_entry)
            current_entry = []

    out.insert(1, f"# Generated {datetime.datetime.utcnow().isoformat()}Z from {URL}")
    return "\n".join(out) + "\n"

def main():
    wanted = get_selected()
    lines = download_playlist()
    result = filter_playlist(lines, wanted)
    pathlib.Path(OUTPUT_FILE).write_text(result, encoding="utf-8")

if __name__ == "__main__":
    main()
