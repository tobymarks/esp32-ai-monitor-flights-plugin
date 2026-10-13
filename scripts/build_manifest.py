#!/usr/bin/env python3
"""Write plugin.json. The six scenes share one structure, so they are generated
here; edit this file, then run it and scripts/package.py."""
import json

DARK = dict(bg=1580575, primary=0xFFFFFF, secondary=11250603, divider=3717119, accent=0x6FC3FF)
LIGHT = dict(bg=0xF5F7FA, primary=0x17212F, secondary=0x45566A, divider=0xD4DDE7, accent=0x1558B0)

HAS = {"binding": "count", "notEquals": "0"}
NONE = {"binding": "count", "equals": "0"}

def text(x, y, w, h, color, font, value, align=None, when=None):
    node = {"type": "text", "x": x, "y": y, "w": w, "h": h, "color": color, "font": font, "text": value}
    if align: node["align"] = align
    if when: node["visibleWhen"] = when
    return node

def rect(x, y, w, h, color, when=None):
    node = {"type": "rect", "x": x, "y": y, "w": w, "h": h, "color": color}
    if when: node["visibleWhen"] = when
    return node

def scene(c, layout):
    p, s, d, a = c["primary"], c["secondary"], c["divider"], c["accent"]
    second = {"binding": "f2", "notEquals": ""}
    third = {"binding": "f3", "notEquals": ""}
    if layout == "portrait":      # 240 x 320
        return {"background": c["bg"], "nodes": [
            text(50, 30, 740, 60, s, 14, "FLIGHTS IN RANGE"),
            text(790, 30, 160, 60, s, 14, "{{count}}", "right"),
            rect(50, 100, 900, 4, d),
            text(50, 130, 900, 140, a, 36, "{{f1}}", when=HAS),
            text(50, 275, 900, 75, p, 16, "{{t1}}  {{r1}}", when=HAS),
            text(50, 370, 900, 75, p, 16, "{{alt1}}  {{spd1}}", when=HAS),
            text(50, 450, 900, 75, s, 16, "{{d1}}  heading {{trk1}}", when=HAS),
            text(50, 300, 900, 160, s, 16, "No flight in range", when=NONE),
            rect(50, 565, 900, 4, d, when=second),
            text(50, 610, 900, 75, p, 16, "{{f2}}  {{t2}}  {{d2}}", when=second),
            text(50, 705, 900, 75, p, 16, "{{f3}}  {{t3}}  {{d3}}", when=third),
            text(50, 915, 900, 55, s, 12, "Data: adsb.lol"),
        ]}
    if layout == "landscape":     # 320 x 240
        return {"background": c["bg"], "nodes": [
            text(40, 35, 740, 80, s, 14, "FLIGHTS IN RANGE"),
            text(800, 35, 160, 80, s, 14, "{{count}}", "right"),
            rect(40, 125, 920, 5, d),
            text(40, 160, 560, 190, a, 36, "{{f1}}", when=HAS),
            text(600, 185, 360, 100, p, 16, "{{t1}}", "right", when=HAS),
            text(600, 280, 360, 90, s, 14, "{{r1}}", "right", when=HAS),
            text(40, 380, 920, 95, p, 16, "{{alt1}}  {{spd1}}", when=HAS),
            text(40, 480, 920, 95, s, 16, "{{d1}}  heading {{trk1}}", when=HAS),
            text(40, 300, 920, 200, s, 16, "No flight in range", when=NONE),
            rect(40, 610, 920, 5, d, when=second),
            text(40, 650, 920, 85, p, 14, "{{f2}}  {{t2}}  {{d2}}", when=second),
            text(40, 745, 920, 85, p, 14, "{{f3}}  {{t3}}  {{d3}}", when=third),
            text(40, 900, 920, 75, s, 12, "Data: adsb.lol"),
        ]}
    return {"background": c["bg"], "nodes": [   # 480 x 480
        text(60, 45, 700, 70, s, 20, "FLIGHTS IN RANGE"),
        text(780, 45, 160, 70, s, 20, "{{count}}", "right"),
        rect(60, 130, 880, 3, d),
        text(60, 170, 620, 130, a, 48, "{{f1}}", when=HAS),
        text(640, 180, 300, 70, p, 24, "{{t1}}", "right", when=HAS),
        text(640, 250, 300, 60, s, 20, "{{r1}}", "right", when=HAS),
        text(60, 330, 880, 70, p, 24, "{{alt1}}  {{spd1}}", when=HAS),
        text(60, 410, 880, 70, s, 24, "{{d1}}  heading {{trk1}}", when=HAS),
        text(60, 280, 880, 150, s, 24, "No flight in range", when=NONE),
        rect(60, 530, 880, 3, d, when=second),
        text(60, 570, 880, 70, p, 24, "{{f2}}  {{t2}}  {{d2}}", when=second),
        text(60, 660, 880, 70, p, 24, "{{f3}}  {{t3}}  {{d3}}", when=third),
        text(60, 900, 880, 60, s, 16, "Data: adsb.lol"),
    ]}

def item(i, field): return f"lists.flights.items.{i}.{field}"
def b(name, path, fmt, fallback, **extra):
    return {"name": name, "path": path, "format": fmt, "suffix": extra.pop("suffix", ""), "map": {}, "fallback": fallback, **extra}

bindings = [b("count", "lists.flights.count", "integer", "0")]
for n in (1, 2, 3):
    i = n - 1
    bindings += [
        b(f"f{n}", item(i, "flight"), "text", "", trim=True),
        b(f"t{n}", item(i, "t"), "text", "-", trim=True),
        b(f"d{n}", item(i, "dst"), "decimal1", "", scale=1.852, suffix=" km"),
    ]
bindings += [
    b("r1", item(0, "r"), "text", "", trim=True),
    b("alt1", item(0, "alt_baro"), "integer", "", scale=0.3048, suffix=" m"),
    b("spd1", item(0, "gs"), "integer", "", scale=1.852, suffix=" km/h"),
    b("trk1", item(0, "track"), "integer", "-"),
]

manifest = {
    "formatVersion": 3,
    "id": "org.aimonitor.flights",
    "name": "Flights",
    "version": "1.0.0",
    "author": "AI Monitor contributors",
    "description": "Aircraft currently flying near the display's location, nearest first.",
    "viewLabel": "Flights",
    "attribution": "Flight data by adsb.lol contributors (ODbL 1.0)",
    "minSceneProtocol": 1,
    "source": {
        "url": "https://api.adsb.lol/v2/point/{location.latitude}/{location.longitude}/{radius}",
        "intervalSeconds": 20,
    },
    "requires": ["location"],
    "lists": [{
        "name": "flights", "path": "ac", "sortBy": "dst", "limit": 3,
        "where": [
            {"path": "flight", "operator": "exists"},
            {"path": "alt_baro", "operator": "notEquals", "value": "ground"},
            {"path": "gs", "operator": "atLeast", "value": 40},
        ],
    }],
    "attentionRules": [
        {"id": "flight-in-range", "path": "lists.flights.count", "operator": "atLeast", "value": 1},
    ],
    "settings": [
        {"key": "radius", "label": "Radius (nautical miles)", "kind": "number", "default": 15, "min": 1, "max": 40},
    ],
    "bindings": bindings,
    "localizations": {"de": {
        "Flights": "Fluege",
        "Aircraft currently flying near the display's location, nearest first.":
            "Flugzeuge in der Naehe des Display-Standorts, das naechste zuerst.",
        "Flight data by adsb.lol contributors (ODbL 1.0)": "Flugdaten von adsb.lol und Mitwirkenden (ODbL 1.0)",
        "Radius (nautical miles)": "Radius (Seemeilen)",
        "FLIGHTS IN RANGE": "FLUEGE IM UMKREIS",
        "{{d1}}  heading {{trk1}}": "{{d1}}  Kurs {{trk1}}",
        "No flight in range": "Kein Flug in Reichweite",
        "Data: adsb.lol": "Daten: adsb.lol",
    }},
    "scenes": {k: scene(DARK, k) for k in ("portrait", "landscape", "square")},
    "lightScenes": {k: scene(LIGHT, k) for k in ("portrait", "landscape", "square")},
}

def dump(value, indent=0):
    """Keep nodes, bindings and filters on one line each for readable diffs."""
    pad = "  " * indent
    if isinstance(value, dict) and (indent >= 2 and all(not isinstance(v, (dict, list)) or k in ("visibleWhen", "map") for k, v in value.items())):
        return json.dumps(value, ensure_ascii=True)
    if isinstance(value, dict):
        rows = [f'{pad}  {json.dumps(k)}: {dump(v, indent + 1)}' for k, v in value.items()]
        return "{\n" + ",\n".join(rows) + f"\n{pad}}}"
    if isinstance(value, list) and value and all(isinstance(v, (dict, list)) for v in value):
        return "[\n" + ",\n".join(f"{pad}  {dump(v, indent + 1)}" for v in value) + f"\n{pad}]"
    return json.dumps(value, ensure_ascii=True)

from pathlib import Path
Path(__file__).resolve().parents[1].joinpath("plugin.json").write_text(dump(manifest) + "\n")
