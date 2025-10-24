#!/usr/bin/env python3
"""Generează fișierul PDF pentru cursul de C++ folosind un generator minimalist."""

from __future__ import annotations

import os
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "docs" / "curs_cpp.md"
OUTPUT = ROOT / "docs" / "curs_cpp.pdf"

LINE_WIDTH = 90
LINE_HEIGHT = 14
TOP_MARGIN = 770
LEFT_MARGIN = 72
BOTTOM_MARGIN = 72
PAGE_HEIGHT = 792


def read_source() -> str:
    if not SOURCE.exists():
        raise FileNotFoundError(f"Nu am găsit fișierul sursă: {SOURCE}")
    return SOURCE.read_text(encoding="utf-8")


def markdown_to_lines(markdown: str) -> list[str]:
    lines: list[str] = []
    in_code_block = False
    buffer: list[str] = []

    for raw_line in markdown.splitlines():
        line = raw_line.rstrip()
        if line.startswith("```"):
            if in_code_block:
                lines.extend(buffer)
                buffer.clear()
            in_code_block = not in_code_block
            continue

        if in_code_block:
            buffer.append(f"    {line}")
            continue

        if line.startswith("#"):
            level = len(line) - len(line.lstrip("#"))
            text = line[level:].strip()
            if not text:
                continue
            formatted = text.upper() if level == 1 else text
            if lines and lines[-1] != "":
                lines.append("")
            lines.append(formatted)
            lines.append("" )
            continue

        if line.startswith(('- ', '* ')):
            lines.append(f"  • {line[2:].strip()}")
            continue

        if not line:
            if lines and lines[-1] == "":
                continue
            lines.append("")
            continue

        wrapped = textwrap.wrap(line, width=LINE_WIDTH)
        if not wrapped:
            lines.append("")
            continue
        lines.extend(wrapped)

    if buffer:
        lines.extend(buffer)

    # Normalize consecutive blanks to maximum two
    normalized: list[str] = []
    blank_count = 0
    for line in lines:
        if line == "":
            blank_count += 1
            if blank_count <= 2:
                normalized.append(line)
        else:
            blank_count = 0
            normalized.append(line)
    return normalized


def chunk_lines(lines: list[str]) -> list[list[str]]:
    usable_height = TOP_MARGIN - BOTTOM_MARGIN
    lines_per_page = max(1, usable_height // LINE_HEIGHT)
    pages: list[list[str]] = []
    current: list[str] = []

    for line in lines:
        if len(current) >= lines_per_page:
            pages.append(current)
            current = []
        current.append(line if line else " ")
    if current:
        pages.append(current)
    return pages


def escape_pdf_text(text: str) -> str:
    return (
        text.replace("\\", r"\\\\")
        .replace("(", r"\\(")
        .replace(")", r"\\)")
    )


def build_content_stream(page_lines: list[str]) -> bytes:
    commands = ["BT", "/F1 12 Tf", f"1 0 0 1 {LEFT_MARGIN} {TOP_MARGIN} Tm", f"{LINE_HEIGHT} TL"]
    first = True
    for line in page_lines:
        escaped = escape_pdf_text(line)
        if first:
            commands.append(f"({escaped}) Tj")
            first = False
        else:
            commands.append("T*")
            commands.append(f"({escaped}) Tj")
    commands.append("ET")
    return "\n".join(commands).encode("utf-8")


def build_pdf_objects(pages: list[list[str]]) -> tuple[list[bytes], int]:
    objects: list[bytes] = []

    # Placeholder for catalog and pages
    num_pages = len(pages)
    catalog_obj = b"<< /Type /Catalog /Pages 2 0 R >>"
    objects.append(catalog_obj)

    kids = " ".join(f"{3 + i} 0 R" for i in range(num_pages))
    pages_obj = f"<< /Type /Pages /Kids [{kids}] /Count {num_pages} >>".encode("utf-8")
    objects.append(pages_obj)

    content_streams: list[bytes] = []
    for page_lines in pages:
        stream = build_content_stream(page_lines)
        content_streams.append(stream)

    font_obj_num = 3 + 2 * num_pages

    # Page objects
    for index in range(num_pages):
        content_num = 3 + num_pages + index
        page_obj = (
            f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] "
            f"/Resources << /Font << /F1 {font_obj_num} 0 R >> >> "
            f"/Contents {content_num} 0 R >>"
        ).encode("utf-8")
        objects.append(page_obj)

    # Content objects
    for stream in content_streams:
        content_obj = (
            f"<< /Length {len(stream)} >>\nstream\n".encode("utf-8")
            + stream
            + b"\nendstream"
        )
        objects.append(content_obj)

    font_obj = b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>"
    objects.append(font_obj)

    return objects, font_obj_num


def write_pdf(objects: list[bytes]) -> bytes:
    output = bytearray()
    output.extend(b"%PDF-1.4\n")
    offsets = [0]

    for obj_number, obj in enumerate(objects, start=1):
        offsets.append(len(output))
        output.extend(f"{obj_number} 0 obj\n".encode("utf-8"))
        output.extend(obj)
        output.extend(b"\nendobj\n")

    xref_position = len(output)
    count = len(objects) + 1
    output.extend(b"xref\n")
    output.extend(f"0 {count}\n".encode("utf-8"))
    output.extend(b"0000000000 65535 f \n")
    for offset in offsets[1:]:
        output.extend(f"{offset:010d} 00000 n \n".encode("utf-8"))

    output.extend(b"trailer\n")
    output.extend(
        f"<< /Size {count} /Root 1 0 R >>\n".encode("utf-8")
    )
    output.extend(b"startxref\n")
    output.extend(f"{xref_position}\n".encode("utf-8"))
    output.extend(b"%%EOF\n")
    return bytes(output)


def main() -> None:
    markdown = read_source()
    lines = markdown_to_lines(markdown)
    pages = chunk_lines(lines)
    objects, _ = build_pdf_objects(pages)
    pdf_bytes = write_pdf(objects)
    os.makedirs(OUTPUT.parent, exist_ok=True)
    OUTPUT.write_bytes(pdf_bytes)
    print(f"PDF generat: {OUTPUT} (pagini: {len(pages)})")


if __name__ == "__main__":
    main()
