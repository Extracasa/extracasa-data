#!/usr/bin/env python3
import argparse
import hashlib
import json
import math
import re
import urllib.request
import xml.etree.ElementTree as ET
from decimal import Decimal
from pathlib import Path

NS = {"k": "http://www.opengis.net/kml/2.2"}
R = 6371008.8


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def ensure_kml(slug, cfg, source_dir, download):
    path = source_dir / f"{slug}.kml"
    if download:
        url = f"https://www.google.com/maps/d/kml?mid={cfg['mid']}&forcekml=1"
        with urllib.request.urlopen(url) as response:
            path.write_bytes(response.read())
    if not path.exists():
        raise ValueError(f"KML mancante: {path}")
    if sha256(path) != cfg["kml_sha256"]:
        raise ValueError(f"SHA-256 KML inatteso per {slug}")
    if not path.read_bytes().startswith(b"<?xml"):
        raise ValueError(f"Risposta KML non XML per {slug}")
    return path


def parse_ring(node):
    raw = node.findtext(".//k:coordinates", namespaces=NS) or ""
    points = []
    for token in raw.split():
        parts = token.split(",")
        if len(parts) >= 2:
            points.append([round(float(parts[0]), 6), round(float(parts[1]), 6)])
    if points and points[0] != points[-1]:
        points.append(points[0][:])
    if len({tuple(point) for point in points[:-1]}) < 3:
        raise ValueError("Anello con meno di tre vertici distinti")
    for lng, lat in points:
        if not (8.5 <= lng <= 10.0 and 44.8 <= lat <= 46.0):
            raise ValueError(f"Coordinate fuori Lombardia: {[lng, lat]}")
    return points


def parse_kml(path):
    root = ET.parse(path).getroot()
    by_code = {}
    for placemark in root.findall(".//k:Placemark", NS):
        polygons = placemark.findall(".//k:Polygon", NS)
        if not polygons:
            continue
        name = placemark.findtext("k:name", default="", namespaces=NS)
        match = re.search(r"Zona OMI\s+([A-Z0-9]+)", name, re.IGNORECASE)
        if not match:
            raise ValueError(f"Placemark poligonale senza codice OMI: {name}")
        code = match.group(1).upper()
        target = by_code.setdefault(code, [])
        for polygon in polygons:
            outer = polygon.find("k:outerBoundaryIs/k:LinearRing", NS)
            if outer is None:
                raise ValueError(f"Poligono senza anello esterno: {name}")
            rings = [parse_ring(outer)]
            for inner in polygon.findall("k:innerBoundaryIs/k:LinearRing", NS):
                rings.append(parse_ring(inner))
            target.append(rings)
    return by_code


def ring_area(ring, lat0):
    projected = [
        (R * math.radians(lng) * math.cos(math.radians(lat0)), R * math.radians(lat))
        for lng, lat in ring
    ]
    return abs(sum(
        projected[i][0] * projected[i + 1][1] - projected[i + 1][0] * projected[i][1]
        for i in range(len(projected) - 1)
    )) / 2


def polygons_area(polygons, lat0):
    return sum(ring_area(rings[0], lat0) - sum(ring_area(ring, lat0) for ring in rings[1:]) for rings in polygons)


def point_in_ring(lat, lng, ring):
    inside = False
    j = len(ring) - 1
    for i in range(len(ring)):
        yi, xi = ring[i]
        yj, xj = ring[j]
        if (xi > lat) != (xj > lat) and lng < (yj - yi) * (lat - xi) / (xj - xi) + yi:
            inside = not inside
        j = i
    return inside


def point_in_polygons(lat, lng, polygons):
    return any(point_in_ring(lat, lng, rings[0]) and not any(point_in_ring(lat, lng, ring) for ring in rings[1:]) for rings in polygons)


def validate_canoni(canoni):
    for zone, bands in canoni.items():
        values = [Decimal(bands[band][edge]) for band, edge in (
            ("sf1", "min"), ("sf1", "max"), ("sf2", "min"),
            ("sf2", "max"), ("sf3", "min"), ("sf3", "max")
        )]
        if not (values[0] < values[1] <= values[2] < values[3] <= values[4] < values[5]):
            raise ValueError(f"Canoni non crescenti in zona {zone}: {values}")


def canone_vector(canoni, zone):
    bands = canoni[str(zone)]
    return tuple(Decimal(bands[band][edge]) for band in ("sf1", "sf2", "sf3") for edge in ("min", "max"))


def dominates_canoni(canoni, higher, lower):
    high = canone_vector(canoni, higher)
    low = canone_vector(canoni, lower)
    return all(a >= b for a, b in zip(high, low)) and high != low


def render_canoni(canoni):
    rows = []
    for zone in sorted(canoni, key=int):
        bands = canoni[zone]
        rendered = ", ".join(
            f'"{band}": {{"min": {bands[band]["min"]}, "max": {bands[band]["max"]}}}'
            for band in ("sf1", "sf2", "sf3")
        )
        rows.append(f'    "{zone}": {{{rendered}}}')
    return "{\n" + ",\n".join(rows) + "\n  }"


def render_data(canoni, zones, unpriced, center, zoom, bounds, overlap_policy):
    lines = ["{", f'  "canoni": {render_canoni(canoni)},', f'  "omi_zones": {json.dumps(zones, separators=(",", ":"))},']
    if overlap_policy:
        lines.append(f'  "zone_overlap_policy": "{overlap_policy["type"]}",')
    if unpriced:
        lines.append(f'  "zone_senza_canoni": {json.dumps(unpriced, separators=(",", ":"))},')
    lines.extend([
        f'  "center": {json.dumps(center, separators=(",", ":"))},',
        f'  "zoom": {zoom},',
        f'  "bounds": {json.dumps(bounds, separators=(",", ":"))}',
        "}"
    ])
    return "\n".join(lines) + "\n"


def build(slug, cfg, kml_path):
    by_code = parse_kml(kml_path)
    expected = set(cfg["zone_map"]) | set(cfg["zone_senza_canoni"])
    if set(by_code) != expected:
        raise ValueError(f"Codici KML inattesi per {slug}: {sorted(by_code)} != {sorted(expected)}")
    validate_canoni(cfg["canoni"])
    mapped_zones = {int(zone) for zone in cfg["zone_map"].values()}
    if mapped_zones != {int(zone) for zone in cfg["canoni"]}:
        raise ValueError(f"Zone/canoni non allineati per {slug}")
    overlap_policy = cfg.get("overlap_policy")
    if overlap_policy and overlap_policy.get("type") not in ("higher_value_first", "kml_last_wins"):
        raise ValueError(f"Regola di sovrapposizione non supportata per {slug}")
    if overlap_policy and overlap_policy["type"] == "kml_last_wins":
        if list(by_code) != overlap_policy["expected_kml_order"]:
            raise ValueError(f"Ordine KML variato per {slug}: {list(by_code)}")
        oracle = overlap_policy["oracle"]
        if cfg["zone_map"].get(oracle["expected_omi"]) != oracle["expected_zone"]:
            raise ValueError(f"Oracolo non allineato alla mappa zone per {slug}")
        matching_zones = [
            int(zone) for zone, bands in cfg["canoni"].items()
            if Decimal(str(oracle["surface_mq"])) * Decimal(bands["sf1"]["min"])
            == Decimal(str(oracle["monthly_min"]))
        ]
        if matching_zones != [oracle["expected_zone"]] or list(by_code)[-1] != oracle["expected_omi"]:
            raise ValueError(f"L'oracolo esterno non discrimina l'ultimo poligono KML per {slug}")
    zones = [{"o": code, "z": cfg["zone_map"][code], "p": by_code[code]} for code in cfg["zone_map"]]
    if overlap_policy and overlap_policy["type"] == "higher_value_first":
        zones.sort(key=lambda item: (canone_vector(cfg["canoni"], item["z"]), item["o"]), reverse=True)
    elif overlap_policy and overlap_policy["type"] == "kml_last_wins":
        zones.sort(key=lambda item: list(by_code).index(item["o"]), reverse=True)
    else:
        zones.sort(key=lambda item: (item["z"], item["o"]))
    unpriced = [{"o": code, "p": by_code[code]} for code in cfg["zone_senza_canoni"]]
    if overlap_policy and overlap_policy["type"] == "kml_last_wins":
        unpriced.sort(key=lambda item: list(by_code).index(item["o"]), reverse=True)
        all_items = sorted(zones + unpriced, key=lambda item: list(by_code).index(item["o"]), reverse=True)
    else:
        unpriced.sort(key=lambda item: item["o"])
        all_items = zones + unpriced
    all_points = [point for item in all_items for polygon in item["p"] for ring in polygon for point in ring]
    lngs, lats = [p[0] for p in all_points], [p[1] for p in all_points]
    bounds = {"sw": [round(min(lats), 6), round(min(lngs), 6)], "ne": [round(max(lats), 6), round(max(lngs), 6)]}
    center = {"lat": round((bounds["sw"][0] + bounds["ne"][0]) / 2, 6), "lng": round((bounds["sw"][1] + bounds["ne"][1]) / 2, 6)}
    area = sum(polygons_area(item["p"], center["lat"]) for item in all_items) / 1_000_000
    delta = (area / cfg["official_area_km2"] - 1) * 100
    if abs(delta) > 10:
        raise ValueError(f"Superficie fuori tolleranza per {slug}: {area:.3f} km2 ({delta:+.1f}%)")
    overlaps = []
    same_zone_overlaps = 0
    for row in range(1, 60):
        lat = bounds["sw"][0] + (bounds["ne"][0] - bounds["sw"][0]) * row / 60
        for col in range(1, 60):
            lng = bounds["sw"][1] + (bounds["ne"][1] - bounds["sw"][1]) * col / 60
            hits = [item for item in all_items if point_in_polygons(lat, lng, item["p"])]
            semantic_zones = {
                ("canoni", item["z"]) if "z" in item else ("senza_canoni", item["o"])
                for item in hits
            }
            if len(semantic_zones) > 1:
                if not overlap_policy:
                    codes = sorted(f'{item["o"]}->{item.get("z", "senza_canoni")}' for item in hits)
                    raise ValueError(f"Sovrapposizione senza regola ufficiale per {slug} a {lat:.6f},{lng:.6f}: {codes}")
                if overlap_policy["type"] == "higher_value_first":
                    if any("z" not in item for item in hits):
                        raise ValueError(f"La priorità per maggior valore incontra una zona senza canoni per {slug}")
                    winner = hits[0]
                    if any(not dominates_canoni(cfg["canoni"], winner["z"], item["z"]) for item in hits[1:]):
                        raise ValueError(f"La priorità per maggior valore non risolve {slug} a {lat:.6f},{lng:.6f}")
                overlaps.append({
                    "lat": round(lat, 6),
                    "lng": round(lng, 6),
                    "zone": sorted(f'{item["o"]}->{item.get("z", "senza_canoni")}' for item in hits)
                })
            elif len(hits) > 1:
                same_zone_overlaps += 1
    stats = {"comune": cfg["label"], "area_km2": round(area, 3), "delta_pct": round(delta, 1), "poligoni": sum(len(item["p"]) for item in all_items), "vertici": len(all_points), "campioni_stessa_zona": same_zone_overlaps, "campioni_multi_zona": len(overlaps)}
    return render_data(cfg["canoni"], zones, unpriced, center, cfg["zoom"], bounds, overlap_policy), stats


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, default=Path(__file__).with_name("comuni_obiettivo1.json"))
    parser.add_argument("--source-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, default=Path(__file__).parents[1])
    parser.add_argument("--download", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    args.source_dir.mkdir(parents=True, exist_ok=True)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    for slug, cfg in manifest["comuni"].items():
        kml = ensure_kml(slug, cfg, args.source_dir, args.download)
        rendered, stats = build(slug, cfg, kml)
        output = args.output_dir / f"data_{slug.replace('-', '_')}.json"
        if args.check:
            if not output.exists() or output.read_text(encoding="utf-8") != rendered:
                raise ValueError(f"File non rigenerabile o non aggiornato: {output}")
        else:
            output.write_text(rendered, encoding="utf-8", newline="\n")
        print(json.dumps(stats, ensure_ascii=False))


if __name__ == "__main__":
    main()
