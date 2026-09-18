import re 
import xml.etree.ElementTree as ET

def clean(text):
    return re.sub(r"\s+", " ", text).strip()


def node_text(node):
    return clean("".join(node.itertext())) if node is not None else ""


def update_dict(full_texts, title_name, chapter_name_list, data):
        if len(full_texts) > 0:
            data.append({
                "title": title_name,
                "chapter": " - ".join(chapter_name_list) or title_name,
                "text": "\n\n".join(full_texts),
            })
            full_texts = []


def visit(child, chapter_name_list, title_name, full_texts, data):
    tag = child.tag.rsplit("}", 1)[-1]
    if tag == "section":
        update_dict(full_texts, title_name, chapter_name_list, data)
        collect_text(child, chapter_name_list, title_name, data)
    elif tag in {"title", "binary", "image", "empty-line"}:
        return
    elif tag in {"p", "v", "subtitle", "text-author", "date"}:
        text = node_text(child)
        if text:
            full_texts.append(text)
    else:
        for child2 in child:
            visit(child2, chapter_name_list, title_name, full_texts, data)


def collect_text(section, chapter_name_list, title_name, data):
    xml_str = "{http://www.gribuser.ru/xml/fictionbook/2.0}"
    chapter_name = node_text(section.find(f"{xml_str}title"))
    chapter_name_list = chapter_name_list + ([chapter_name] if chapter_name else [])
    full_texts = []

    for child in section:
        visit(child, chapter_name_list, title_name, full_texts, data)
    update_dict(full_texts, title_name, chapter_name_list, data)


def parse_fb2(path):
    xml_str = "{http://www.gribuser.ru/xml/fictionbook/2.0}"
    
    root = ET.parse(path).getroot()
    title = node_text(root.find(f"{xml_str}description/{xml_str}title-info/{xml_str}book-title"))
    data = []

    for body in root.findall(f"{xml_str}body"):
        if body.get("name", "").casefold() in {"notes", "comments"}:
            continue
        sections = body.findall(f"{xml_str}section")
        if sections:
            for section in sections:
                title_name = node_text(section.find(f"{xml_str}title")) or title
                collect_text(section, [], title_name, data)
        else:
            collect_text(body, [], title, data)
    return data