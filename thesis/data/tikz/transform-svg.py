#!/usr/bin/env python3

import re
import sys
import xml.etree.ElementTree as ET

ET.register_namespace("", "http://www.w3.org/2000/svg")
ET.register_namespace("xlink", "http://www.w3.org/1999/xlink")


# Switch these targets to installed desktop fonts as needed.
FONT_TARGETS = {
    "serif": "serif",
    "sans": "NewComputerModernSans10,NewComputerModernSans10_MSFontService,sans-serif",
    "mono": "monospace",
    "math": None,
}

# LaTeX font family prefixes to logical font buckets.
LATEX_FONT_FAMILIES = [
    ("cmss", "sans"),
    ("cmr", "serif"),
    ("cmtt", "mono"),
    ("cmsy", "math"),
]


def local_name(tag: str) -> str:
    if tag.startswith("{"):
        return tag.split("}", 1)[1]
    return tag


def font_bucket(value: str) -> str | None:
    family = value.strip()
    for prefix, bucket in LATEX_FONT_FAMILIES:
        if family.startswith(prefix):
            return bucket
    return None


def rewrite_font_family(value: str) -> str:
    family = value.strip()

    bucket = font_bucket(family)
    if bucket:
        target = FONT_TARGETS.get(bucket)
        return target if target else family

    return family


def font_weight(value: str) -> str | None:
    family = value.strip()
    if font_bucket(family) == "math":
        return None
    if "bx" in family:
        return "700"
    return "400"


def font_style(value: str) -> str | None:
    family = value.strip()
    if font_bucket(family) == "math":
        return None
    if "ssi" in family or "sl" in family or "ti" in family or "it" in family:
        return "oblique"
    return "normal"


def can_flatten_text(element: ET.Element) -> bool:
    for child in element:
        if local_name(child.tag) != "tspan":
            return False
        if set(child.attrib) - {"x"}:
            return False
        if list(child):
            return False
    return True


def parse_font_size(element: ET.Element) -> float | None:
    value = element.get("font-size")
    if value:
        return parse_size(value)

    style_value = style_value_for_class(element, "_style_sizes")
    if style_value:
        return parse_size(style_value)

    return None


def parse_x(element: ET.Element) -> float | None:
    value = element.get("x")
    if not value:
        return None
    first = value.replace(",", " ").split()[0]
    try:
        return float(first)
    except ValueError:
        return None


def parse_size(value: str) -> float | None:
    if value.endswith("px"):
        value = value[:-2]
    try:
        return float(value)
    except ValueError:
        return None


def extract_style_sizes(root: ET.Element) -> dict[str, str]:
    sizes: dict[str, str] = {}

    for element in root.iter():
        if local_name(element.tag) != "style":
            continue
        text = "".join(element.itertext())
        for match in re.finditer(r"text\.([^{\s]+)\s*\{[^}]*font-size:([^;}\s]+)", text):
            sizes[match.group(1)] = match.group(2)

    return sizes


def extract_style_families(root: ET.Element) -> dict[str, str]:
    families: dict[str, str] = {}

    for element in root.iter():
        if local_name(element.tag) != "style":
            continue
        text = "".join(element.itertext())
        for match in re.finditer(r"text\.([^{\s]+)\s*\{[^}]*font-family:([^;}\s]+)", text):
            families[match.group(1)] = match.group(2)

    return families


def style_value_for_class(element: ET.Element, attr_name: str) -> str | None:
    class_name = element.get("class")
    if not class_name:
        return None

    packed = element.attrib.get(attr_name)
    if not packed:
        return None

    for entry in packed.split(";"):
        if not entry:
            continue
        name, value = entry.split("=", 1)
        if name == class_name:
            return value

    return None


def is_zero(value: str | None) -> bool:
    if value is None:
        return False
    try:
        return float(value) == 0.0
    except ValueError:
        return False


def has_visible_fill(element: ET.Element) -> bool:
    fill = element.get("fill")
    if fill == "none":
        return False
    return not is_zero(element.get("fill-opacity"))


def has_visible_stroke(element: ET.Element) -> bool:
    stroke = element.get("stroke")
    if stroke is None or stroke == "none":
        return False
    return not is_zero(element.get("stroke-opacity"))


def is_invisible(element: ET.Element) -> bool:
    if is_zero(element.get("opacity")):
        return True

    tag = local_name(element.tag)
    if tag in {"tspan", "text"}:
        return not has_visible_fill(element)

    return not has_visible_fill(element) and not has_visible_stroke(element)


def remove_invisible_elements(root: ET.Element) -> None:
    parent_map = {child: parent for parent in root.iter() for child in parent}

    for element in list(root.iter()):
        if element is root:
            continue
        if not is_invisible(element):
            continue
        parent = parent_map.get(element)
        if parent is not None:
            parent.remove(element)


def remove_empty_text_nodes(root: ET.Element) -> None:
    parent_map = {child: parent for parent in root.iter() for child in parent}

    for element in list(root.iter()):
        if local_name(element.tag) != "text":
            continue
        if list(element):
            continue
        if (element.text or "").strip():
            continue
        parent = parent_map.get(element)
        if parent is not None:
            parent.remove(element)


def flatten_text(element: ET.Element) -> None:
    pieces: list[str] = []
    font_size = parse_font_size(element)
    prev_x = parse_x(element)
    prev_text = element.text or ""

    if prev_text:
        pieces.append(prev_text)

    for child in list(element):
        next_text = child.text or ""
        next_x = parse_x(child)

        if (
            pieces
            and next_text
            and prev_x is not None
            and next_x is not None
            and font_size is not None
            and next_x - prev_x > 1.6 * font_size
        ):
            pieces.append(" ")

        pieces.append(next_text)
        prev_x = next_x if next_x is not None else prev_x
        prev_text = next_text

        element.remove(child)

    element.text = "".join(pieces)


def main() -> int:
    if len(sys.argv) != 3:
        print(f"usage: {sys.argv[0]} INPUT.svg OUTPUT.svg", file=sys.stderr)
        return 1

    input_path, output_path = sys.argv[1], sys.argv[2]

    tree = ET.parse(input_path)
    root = tree.getroot()
    style_sizes = extract_style_sizes(root)
    style_families = extract_style_families(root)
    style_sizes_attr = ";".join(f"{name}={size}" for name, size in style_sizes.items())
    style_families_attr = ";".join(f"{name}={family}" for name, family in style_families.items())

    for element in root.iter():
        if local_name(element.tag) != "text":
            continue

        if style_sizes_attr:
            element.set("_style_sizes", style_sizes_attr)
        if style_families_attr:
            element.set("_style_families", style_families_attr)

        font_family = element.get("font-family")
        if not font_family:
            font_family = style_value_for_class(element, "_style_families")
        if font_family:
            element.set("font-family", rewrite_font_family(font_family))
            weight = font_weight(font_family)
            style = font_style(font_family)
            if weight:
                element.set("font-weight", weight)
            if style:
                element.set("font-style", style)

        if can_flatten_text(element):
            flatten_text(element)

        if style_sizes_attr:
            element.attrib.pop("_style_sizes", None)
        if style_families_attr:
            element.attrib.pop("_style_families", None)

    remove_invisible_elements(root)
    remove_empty_text_nodes(root)

    tree.write(output_path, encoding="utf-8", xml_declaration=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
