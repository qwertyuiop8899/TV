import gzip
import io
import os
import xml.etree.ElementTree as ET

import requests

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


def resolve_output_dir() -> str:
    """Return repo root when detectable, otherwise fallback to script directory."""
    if os.path.isdir(os.path.join(SCRIPT_DIR, ".git")):
        return SCRIPT_DIR

    parent_dir = os.path.dirname(SCRIPT_DIR)
    if os.path.isdir(os.path.join(parent_dir, ".git")):
        return parent_dir

    if os.path.basename(SCRIPT_DIR).lower() == "src":
        return parent_dir

    return SCRIPT_DIR


OUTPUT_DIR = resolve_output_dir()

SOURCE_URLS = [
    "https://www.open-epg.com/files/italy1.xml",
    "https://www.open-epg.com/files/italy2.xml",
    "https://www.open-epg.com/files/italy3.xml",
    "https://www.open-epg.com/files/italy4.xml",
    "https://epgshare01.online/epgshare01/epg_ripper_IT1.xml.gz",
    "https://raw.githubusercontent.com/matthuisman/i.mjh.nz/master/PlutoTV/it.xml",
]


def download_and_parse_xml(url: str, timeout: int = 30) -> ET.ElementTree | None:
    """Download an XML or GZIP-compressed XML and parse it as ElementTree."""
    try:
        response = requests.get(url, timeout=timeout, verify=False)
        response.raise_for_status()

        try:
            with gzip.open(io.BytesIO(response.content), "rb") as gz_file:
                xml_content = gz_file.read()
        except (gzip.BadGzipFile, OSError):
            xml_content = response.content

        return ET.ElementTree(ET.fromstring(xml_content))
    except requests.RequestException as exc:
        print(f"[ERROR] Download failed for {url}: {exc}")
    except ET.ParseError as exc:
        print(f"[ERROR] XML parse failed for {url}: {exc}")
    return None


def clean_attribute(element: ET.Element, attr_name: str) -> None:
    value = element.attrib.get(attr_name)
    if value is not None:
        element.attrib[attr_name] = value.replace(" ", "").lower()


def append_all_children(target_root: ET.Element, source_tree: ET.ElementTree) -> None:
    source_root = source_tree.getroot()
    for element in source_root:
        target_root.append(element)


def merge_epg() -> ET.ElementTree:
    requests.packages.urllib3.disable_warnings(
        requests.packages.urllib3.exceptions.InsecureRequestWarning
    )

    final_root = ET.Element("tv")
    final_tree = ET.ElementTree(final_root)

    for url in SOURCE_URLS:
        tree = download_and_parse_xml(url)
        if tree is not None:
            append_all_children(final_root, tree)

    for channel in final_root.findall(".//channel"):
        clean_attribute(channel, "id")

    for programme in final_root.findall(".//programme"):
        clean_attribute(programme, "channel")

    return final_tree


def write_outputs(tree: ET.ElementTree) -> None:
    output_xml = os.path.join(OUTPUT_DIR, "epg.xml")
    output_gz = os.path.join(OUTPUT_DIR, "epg.xml.gz")

    with open(output_xml, "wb") as xml_file:
        tree.write(xml_file, encoding="utf-8", xml_declaration=True)
    print(f"[OK] Wrote XML: {output_xml}")

    with gzip.open(output_gz, "wb") as gz_file:
        tree.write(gz_file, encoding="utf-8", xml_declaration=True)
    print(f"[OK] Wrote GZ: {output_gz}")


def main() -> None:
    tree = merge_epg()
    write_outputs(tree)


if __name__ == "__main__":
    main()
