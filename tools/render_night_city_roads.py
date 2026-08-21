#!/usr/bin/env python3
"""Render Night City 2045 road-edge GeoJSON as a clean SVG road layer.

The renderer deliberately does not alter route angles or topology. It uses the
canonical graph geometry as supplied and applies only display styling.

Expected input: data/night-city-2045/roads/night_city_2045_road_graph_v12.geojson
Expected edge properties: kind='road_edge', road_class='local'|'major'
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from xml.sax.saxutils import escape

DEFAULT_CONFIG = Path("config/night-city-2045-roads.json")


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def fmt(value: float) -> str:
    text = f"{float(value):.3f}"
    return text.rstrip("0").rstrip(".")


def path_d(coords) -> str:
    if len(coords) < 2:
        return ""
    return "M " + " L ".join(f"{fmt(x)} {fmt(y)}" for x, y in coords)


def road_edges(graph):
    for feature in graph.get("features", []):
        props = feature.get("properties") or {}
        geom = feature.get("geometry") or {}
        if props.get("kind") != "road_edge":
            continue
        if geom.get("type") != "LineString":
            continue
        coords = geom.get("coordinates") or []
        if len(coords) < 2:
            continue
        yield feature


def build_svg(graph, config) -> str:
    space = config["coordinate_space"]
    display = config["display"]
    classes = display["classes"]
    width = space["width_px"]
    height = space["height_px"]

    grouped = {name: [] for name in classes}
    node_positions = {}

    for feature in graph.get("features", []):
        props = feature.get("properties") or {}
        geom = feature.get("geometry") or {}
        if props.get("kind") == "road_node" and geom.get("type") == "Point":
            node_id = props.get("id")
            coords = geom.get("coordinates") or []
            if node_id is not None and len(coords) >= 2:
                node_positions[node_id] = (coords[0], coords[1])

    edge_nodes = {name: set() for name in classes}

    for feature in road_edges(graph):
        props = feature["properties"]
        road_class = props.get("road_class")
        if road_class not in grouped:
            continue
        grouped[road_class].append(feature)
        for key in ("a", "b"):
            node_id = props.get(key)
            if node_id is not None:
                edge_nodes[road_class].add(node_id)

    lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
        f'width="{width}" height="{height}">'
    ]

    # Local roads first; major roads on top, matching the source hierarchy.
    order = [name for name in ("local", "major") if name in classes]
    order += [name for name in classes if name not in order]

    for road_class in order:
        style = classes[road_class]
        stroke = escape(style["stroke"])
        stroke_width = float(style["width_px"])
        lines.append(
            f'<g id="{escape(road_class)}-segments" fill="none" stroke="{stroke}" '
            f'stroke-width="{fmt(stroke_width)}" stroke-linecap="butt" '
            f'stroke-linejoin="round">'
        )
        for feature in grouped[road_class]:
            d = path_d(feature["geometry"]["coordinates"])
            if d:
                lines.append(f'<path d="{d}"/>')
        lines.append("</g>")

        # One node disc per used graph node avoids stacked round caps and makes
        # intersections visually clean while preserving the canonical node position.
        lines.append(f'<g id="{escape(road_class)}-nodes" fill="{stroke}">')
        radius = stroke_width / 2.0
        for node_id in sorted(edge_nodes[road_class]):
            xy = node_positions.get(node_id)
            if xy is None:
                continue
            x, y = xy
            lines.append(
                f'<circle cx="{fmt(x)}" cy="{fmt(y)}" r="{fmt(radius)}"/>'
            )
        lines.append("</g>")

    lines.append("</svg>")
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "graph",
        type=Path,
        nargs="?",
        default=Path("data/night-city-2045/roads/night_city_2045_road_graph_v12.geojson"),
    )
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("build/night-city-2045/roads.svg"),
    )
    args = parser.parse_args()

    graph = load_json(args.graph)
    config = load_json(args.config)
    svg = build_svg(graph, config)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(svg, encoding="utf-8")
    print(args.output)


if __name__ == "__main__":
    main()
