"""Ergänzt oder ersetzt einen Tageseintrag in einer Preisalarm-Datendatei.

Aufruf:  python tools/add_entry.py data/mallorca.json date=2026-10-21 total=936.69 bInfo="Vueling 17:55 hin"
Zahlen werden als Zahl gespeichert, "null" als null, alles andere als Text.
"""
import json
import re
import sys


def parse(value):
    if value == "null":
        return None
    if re.fullmatch(r"-?\d+(\.\d+)?", value):
        return float(value) if "." in value else int(value)
    return value


def main():
    if len(sys.argv) < 3:
        sys.exit("Aufruf: add_entry.py DATEI key=wert ...")
    path = sys.argv[1]
    entry = {}
    for arg in sys.argv[2:]:
        key, sep, value = arg.partition("=")
        if not sep:
            sys.exit(f"Ungültiges Argument: {arg}")
        entry[key] = parse(value)
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(entry.get("date", ""))):
        sys.exit("date=JJJJ-MM-TT fehlt oder ist ungültig")

    with open(path, encoding="utf-8-sig") as f:
        data = json.load(f)
    data = [e for e in data if e.get("date") != entry["date"]] + [entry]
    data.sort(key=lambda e: e["date"])

    text = "[\n" + ",\n".join(json.dumps(e, ensure_ascii=False) for e in data) + "\n]\n"
    json.loads(text)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    print(f"OK: {path} hat {len(data)} Einträge, zuletzt {data[-1]['date']}")


if __name__ == "__main__":
    main()
