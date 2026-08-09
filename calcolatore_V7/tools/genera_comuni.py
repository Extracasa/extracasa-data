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
    if not path.read_bytes().startswith(b"<?xml"):
        raise ValueError(f"Risposta KML non XML per {slug}")
    return path


def ensure_pdf(slug, cfg, source_dir, download):
    path = source_dir / f"pdf-{cfg['pdf_file_id']}.pdf"
    if download:
        url = f"https://drive.google.com/uc?export=download&id={cfg['pdf_file_id']}"
        with urllib.request.urlopen(url) as response:
            payload = response.read()
        if not payload.startswith(b"%PDF"):
            raise ValueError(f"Risposta PDF non valida per {slug}")
        if hashlib.sha256(payload).hexdigest() != cfg["pdf_sha256"]:
            raise ValueError(f"SHA-256 PDF inatteso per {slug}")
        path.write_bytes(payload)
    if not path.exists():
        raise ValueError(f"PDF mancante: {path}")
    if not path.read_bytes().startswith(b"%PDF"):
        raise ValueError(f"Risposta PDF non valida per {slug}")
    if sha256(path) != cfg["pdf_sha256"]:
        raise ValueError(f"SHA-256 PDF inatteso per {slug}")
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


def parse_kml(path, placemark_mode="omi"):
    root = ET.parse(path).getroot()
    by_code = {}
    for placemark in root.findall(".//k:Placemark", NS):
        polygons = placemark.findall(".//k:Polygon", NS)
        if not polygons:
            continue
        name = placemark.findtext("k:name", default="", namespaces=NS)
        if placemark_mode == "omi":
            match = re.search(r"Zona OMI\s+([A-Z0-9]+)", name, re.IGNORECASE)
            code = match.group(1).upper() if match else None
        elif placemark_mode == "agreement_zone":
            match = re.search(r"\bZONA\s*([0-9]+)\b", name, re.IGNORECASE)
            code = f"Z{int(match.group(1))}" if match else None
            if not match:
                match = re.search(r"\bZONA\s+UNICA\b", name, re.IGNORECASE)
                code = "Z1" if match else None
        else:
            raise ValueError(f"Modalità placemark non supportata: {placemark_mode}")
        if not match:
            raise ValueError(f"Placemark poligonale non riconosciuto ({placemark_mode}): {name}")
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


def canonical_kml_sha256(by_code):
    payload = json.dumps(by_code, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


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


def point_on_segment(point, start, end):
    dx, dy = end[0] - start[0], end[1] - start[1]
    length = math.hypot(dx, dy)
    if not length:
        return point == start
    cross = (point[1] - start[1]) * dx - (point[0] - start[0]) * dy
    coordinate_tolerance = max(length * 1e-9, 1e-12)
    if abs(cross) / length > coordinate_tolerance:
        return False
    return (min(start[0], end[0]) - coordinate_tolerance <= point[0] <= max(start[0], end[0]) + coordinate_tolerance
            and min(start[1], end[1]) - coordinate_tolerance <= point[1] <= max(start[1], end[1]) + coordinate_tolerance)


def point_location_ring(point, ring):
    if any(point_on_segment(point, ring[i], ring[i + 1]) for i in range(len(ring) - 1)):
        return 0
    return 1 if point_in_ring(point[1], point[0], ring) else -1


def point_location_polygon(point, rings):
    outer = point_location_ring(point, rings[0])
    if outer != 1:
        return outer
    for hole in rings[1:]:
        location = point_location_ring(point, hole)
        if location == 0:
            return 0
        if location == 1:
            return -1
    return 1


def orientation_sign(p, q, r):
    first_x, first_y = q[0] - p[0], q[1] - p[1]
    second_x, second_y = r[0] - p[0], r[1] - p[1]
    value = first_x * second_y - first_y * second_x
    scale = abs(first_x * second_y) + abs(first_y * second_x)
    tolerance = max(scale * 1e-12, 1e-30)
    return 1 if value > tolerance else (-1 if value < -tolerance else 0)


def proper_segment_intersection(a, b, c, d):
    if orientation_sign(a, b, c) * orientation_sign(a, b, d) != -1:
        return None
    if orientation_sign(c, d, a) * orientation_sign(c, d, b) != -1:
        return None
    denominator = (a[0] - b[0]) * (c[1] - d[1]) - (a[1] - b[1]) * (c[0] - d[0])
    determinant_ab = a[0] * b[1] - a[1] * b[0]
    determinant_cd = c[0] * d[1] - c[1] * d[0]
    return [
        (determinant_ab * (c[0] - d[0]) - (a[0] - b[0]) * determinant_cd) / denominator,
        (determinant_ab * (c[1] - d[1]) - (a[1] - b[1]) * determinant_cd) / denominator,
    ]


def polygon_bbox(rings):
    points = rings[0]
    return min(p[0] for p in points), min(p[1] for p in points), max(p[0] for p in points), max(p[1] for p in points)


def bboxes_overlap(first, second):
    return first[0] < second[2] and second[0] < first[2] and first[1] < second[3] and second[1] < first[3]


def interior_edge_samples(rings):
    outer = rings[0]
    span = max(polygon_bbox(rings)[2] - polygon_bbox(rings)[0], polygon_bbox(rings)[3] - polygon_bbox(rings)[1])
    offset = max(span * 1e-6, 1e-9)
    for start, end in zip(outer, outer[1:]):
        dx, dy = end[0] - start[0], end[1] - start[1]
        length = math.hypot(dx, dy)
        if not length:
            continue
        midpoint = [(start[0] + end[0]) / 2, (start[1] + end[1]) / 2]
        for sign in (-1, 1):
            candidate = [midpoint[0] - sign * dy / length * offset, midpoint[1] + sign * dx / length * offset]
            if point_location_polygon(candidate, rings) == 1:
                yield candidate
                break


def polygon_overlap_witness(first, second):
    if not bboxes_overlap(polygon_bbox(first), polygon_bbox(second)):
        return None
    for point in first[0][:-1]:
        if point_location_polygon(point, second) == 1:
            return point
    for point in second[0][:-1]:
        if point_location_polygon(point, first) == 1:
            return point
    for ring_a in first:
        for ring_b in second:
            for a, b in zip(ring_a, ring_a[1:]):
                for c, d in zip(ring_b, ring_b[1:]):
                    witness = proper_segment_intersection(a, b, c, d)
                    if witness:
                        return witness
    for candidate in interior_edge_samples(first):
        if point_location_polygon(candidate, second) == 1:
            return candidate
    for candidate in interior_edge_samples(second):
        if point_location_polygon(candidate, first) == 1:
            return candidate
    return None


def polygons_overlap_witness(first, second):
    for polygon_a in first:
        for polygon_b in second:
            witness = polygon_overlap_witness(polygon_a, polygon_b)
            if witness:
                return witness
    return None


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


def semantic_zone(item):
    return ("canoni", item["z"]) if "z" in item else ("senza_canoni", item["o"])


def validate_overlap(slug, cfg, overlap_policy, hits, lat, lng):
    codes = sorted(f'{item["o"]}->{item.get("z", "senza_canoni")}' for item in hits)
    if not overlap_policy:
        raise ValueError(f"Sovrapposizione senza regola ufficiale per {slug} a {lat:.6f},{lng:.6f}: {codes}")
    if not (overlap_policy.get("source") or overlap_policy.get("source_page")):
        raise ValueError(f"Fonte della regola di sovrapposizione mancante per {slug}")
    if overlap_policy["type"] == "higher_value_first":
        if any("z" not in item for item in hits):
            raise ValueError(f"La priorità per maggior valore incontra una zona senza canoni per {slug}")
        if any(not dominates_canoni(cfg["canoni"], hits[0]["z"], item["z"]) for item in hits[1:]):
            raise ValueError(f"La priorità per maggior valore non risolve {slug} a {lat:.6f},{lng:.6f}")
    elif overlap_policy["type"] == "rural_first":
        unpriced = [item for item in hits if "z" not in item]
        if unpriced and "z" in hits[0]:
            raise ValueError(f"La zona rurale non precede le zone calcolabili per {slug}")
        priced = [item for item in hits if "z" in item]
        if len(priced) > 1 and any(
            not dominates_canoni(cfg["canoni"], priced[0]["z"], item["z"])
            for item in priced[1:]
        ):
            raise ValueError(f"La priorità per maggior valore non risolve {slug} a {lat:.6f},{lng:.6f}")
    elif overlap_policy["type"] == "agreement_zone_order":
        if any("z" not in item for item in hits) or hits[0]["z"] != min(item["z"] for item in hits):
            raise ValueError(f"L'ordine delle zone contrattuali non risolve {slug} a {lat:.6f},{lng:.6f}")
        if cfg.get("canoni_confirmed", True) and any(
            not dominates_canoni(cfg["canoni"], hits[0]["z"], item["z"])
            for item in hits[1:]
        ):
            raise ValueError(f"L'ordine contrattuale non segue i canoni per {slug} a {lat:.6f},{lng:.6f}")
    else:
        raise ValueError(f"Regola di sovrapposizione non supportata per {slug}")
    return codes


def render_canoni(canoni):
    if not canoni:
        return "{}"
    rows = []
    for zone in sorted(canoni, key=int):
        bands = canoni[zone]
        rendered = ", ".join(
            f'"{band}": {{"min": {bands[band]["min"]}, "max": {bands[band]["max"]}}}'
            for band in ("sf1", "sf2", "sf3")
        )
        rows.append(f'    "{zone}": {{{rendered}}}')
    return "{\n" + ",\n".join(rows) + "\n  }"


def render_data(canoni, zones, unpriced, center, zoom, bounds, overlap_policy, mostra_omi):
    lines = ["{", f'  "canoni": {render_canoni(canoni)},', f'  "omi_zones": {json.dumps(zones, separators=(",", ":"))},']
    if not mostra_omi:
        lines.append('  "mostra_omi": false,')
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
    by_code = parse_kml(kml_path, cfg.get("placemark_mode", "omi"))
    if canonical_kml_sha256(by_code) != cfg["kml_canonical_sha256"]:
        raise ValueError(f"SHA-256 canonico KML inatteso per {slug}")
    expected = set(cfg["zone_map"]) | set(cfg["zone_senza_canoni"])
    if set(by_code) != expected:
        raise ValueError(f"Codici KML inattesi per {slug}: {sorted(by_code)} != {sorted(expected)}")
    canoni_confirmed = cfg.get("canoni_confirmed", True)
    if canoni_confirmed:
        validate_canoni(cfg["canoni"])
    elif cfg["canoni"]:
        raise ValueError(f"Canoni presenti ma non confermati per {slug}")
    mapped_zones = {int(zone) for zone in cfg["zone_map"].values()}
    if canoni_confirmed and mapped_zones != {int(zone) for zone in cfg["canoni"]}:
        raise ValueError(f"Zone/canoni non allineati per {slug}")
    overlap_policy = cfg.get("overlap_policy")
    if overlap_policy and overlap_policy.get("type") not in ("higher_value_first", "rural_first", "agreement_zone_order"):
        raise ValueError(f"Regola di sovrapposizione non supportata per {slug}")
    oracle = cfg.get("rent_oracle")
    if oracle:
        if oracle.get("scope") != "rent_only":
            raise ValueError(f"Portata dell'oracolo canone non valida per {slug}")
        if cfg["zone_map"].get(oracle["expected_omi"]) != oracle["expected_zone"]:
            raise ValueError(f"Oracolo canone non allineato alla mappa zone per {slug}")
        matching_zones = [
            int(zone) for zone, bands in cfg["canoni"].items()
            if Decimal(str(oracle["surface_mq"])) * Decimal(bands["sf1"]["min"])
            == Decimal(str(oracle["monthly_min"]))
        ]
        if matching_zones != [oracle["expected_zone"]]:
            raise ValueError(f"L'oracolo esterno non discrimina il canone per {slug}")
        competing_zone = cfg["zone_map"].get(oracle["competing_omi"])
        competing_min = (Decimal(str(oracle["surface_mq"]))
                         * Decimal(cfg["canoni"][str(competing_zone)]["sf1"]["min"]))
        if (competing_min != Decimal(str(oracle["competing_monthly_min"]))
                or competing_zone == oracle["expected_zone"]):
            raise ValueError(f"L'oracolo esterno non discrimina il canone concorrente per {slug}")
    zones = [{"o": code, "z": cfg["zone_map"][code], "p": by_code[code]} for code in cfg["zone_map"]]
    if overlap_policy and overlap_policy["type"] == "higher_value_first":
        zones.sort(key=lambda item: (canone_vector(cfg["canoni"], item["z"]), item["o"]), reverse=True)
    else:
        zones.sort(key=lambda item: (item["z"], item["o"]))
    unpriced = [{"o": code, "p": by_code[code]} for code in cfg["zone_senza_canoni"]]
    if overlap_policy and overlap_policy["type"] == "rural_first":
        unpriced.sort(key=lambda item: item["o"])
        all_items = unpriced + zones
    else:
        unpriced.sort(key=lambda item: item["o"])
        all_items = zones + unpriced
    all_points = [point for item in all_items for polygon in item["p"] for ring in polygon for point in ring]
    lngs, lats = [p[0] for p in all_points], [p[1] for p in all_points]
    bounds = {"sw": [round(min(lats), 6), round(min(lngs), 6)], "ne": [round(max(lats), 6), round(max(lngs), 6)]}
    center = {"lat": round((bounds["sw"][0] + bounds["ne"][0]) / 2, 6), "lng": round((bounds["sw"][1] + bounds["ne"][1]) / 2, 6)}
    area = sum(polygons_area(item["p"], center["lat"]) for item in all_items) / 1_000_000
    delta = (area / cfg["official_area_km2"] - 1) * 100
    area_tolerance_pct = cfg.get("area_tolerance_pct", 2.0)
    if not 0 < area_tolerance_pct <= 10:
        raise ValueError(f"Tolleranza superficie non valida per {slug}: {area_tolerance_pct}")
    if abs(delta) > area_tolerance_pct:
        raise ValueError(f"Superficie fuori tolleranza per {slug}: {area:.3f} km2 ({delta:+.1f}%)")
    exact_overlaps = []
    for index, first in enumerate(all_items):
        for second in all_items[index + 1:]:
            if semantic_zone(first) == semantic_zone(second):
                continue
            witness = polygons_overlap_witness(first["p"], second["p"])
            if not witness:
                continue
            codes = validate_overlap(slug, cfg, overlap_policy, [first, second], witness[1], witness[0])
            exact_overlaps.append({"lat": round(witness[1], 6), "lng": round(witness[0], 6), "zone": codes})
    overlaps = []
    same_zone_overlaps = 0
    for row in range(1, 60):
        lat = bounds["sw"][0] + (bounds["ne"][0] - bounds["sw"][0]) * row / 60
        for col in range(1, 60):
            lng = bounds["sw"][1] + (bounds["ne"][1] - bounds["sw"][1]) * col / 60
            hits = [item for item in all_items if point_in_polygons(lat, lng, item["p"])]
            semantic_zones = {semantic_zone(item) for item in hits}
            if len(semantic_zones) > 1:
                codes = validate_overlap(slug, cfg, overlap_policy, hits, lat, lng)
                overlaps.append({
                    "lat": round(lat, 6),
                    "lng": round(lng, 6),
                    "zone": sorted(f'{item["o"]}->{item.get("z", "senza_canoni")}' for item in hits)
                })
            elif len(hits) > 1:
                same_zone_overlaps += 1
    stats = {"comune": cfg["label"], "area_km2": round(area, 3), "delta_pct": round(delta, 1), "poligoni": sum(len(item["p"]) for item in all_items), "vertici": len(all_points), "sovrapposizioni_esatte": len(exact_overlaps), "campioni_stessa_zona": same_zone_overlaps, "campioni_multi_zona": len(overlaps)}
    return render_data(cfg["canoni"], zones, unpriced, center, cfg["zoom"], bounds, overlap_policy, cfg.get("mostra_omi", True)), stats


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
    if manifest.get("agreement"):
        ensure_pdf("accordo", manifest["agreement"], args.source_dir, args.download)
    for slug, cfg in manifest["comuni"].items():
        kml = ensure_kml(slug, cfg, args.source_dir, args.download)
        if cfg.get("pdf_file_id"):
            ensure_pdf(slug, cfg, args.source_dir, args.download)
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
