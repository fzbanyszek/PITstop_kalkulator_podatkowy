from datetime import datetime
import unicodedata

import pandas as pd


PAGE_WIDTH = 842
PAGE_HEIGHT = 595
MARGIN_X = 34
MARGIN_TOP = 34
MARGIN_BOTTOM = 34
TABLE_TOP = 128
ROW_HEIGHT = 16
HEADER_ROW_HEIGHT = 18
FONT_NAME_OBJECT_ID = 3

POLISH_TRANSLATION = str.maketrans({
    "ą": "a",
    "ć": "c",
    "ę": "e",
    "ł": "l",
    "ń": "n",
    "ó": "o",
    "ś": "s",
    "ź": "z",
    "ż": "z",
    "Ą": "A",
    "Ć": "C",
    "Ę": "E",
    "Ł": "L",
    "Ń": "N",
    "Ó": "O",
    "Ś": "S",
    "Ź": "Z",
    "Ż": "Z",
})


def generate_trade_history_pdf(
    trades_df: pd.DataFrame,
    selected_year: int,
    total_profit: float,
    title: str,
    table_title: str,
    total_profit_label: str,
) -> bytes:
    rows = _format_rows(trades_df)
    streams = []
    page_rows = []
    current_y = PAGE_HEIGHT - TABLE_TOP - HEADER_ROW_HEIGHT

    for row in rows:
        if current_y < MARGIN_BOTTOM + ROW_HEIGHT:
            streams.append(_build_page_stream(
                page_rows,
                selected_year,
                total_profit,
                title,
                table_title,
                total_profit_label,
                len(streams) + 1,
            ))
            page_rows = []
            current_y = PAGE_HEIGHT - TABLE_TOP - HEADER_ROW_HEIGHT

        page_rows.append(row)
        current_y -= ROW_HEIGHT

    streams.append(_build_page_stream(
        page_rows,
        selected_year,
        total_profit,
        title,
        table_title,
        total_profit_label,
        len(streams) + 1,
    ))

    return _build_pdf(streams)


def _format_rows(trades_df: pd.DataFrame) -> list[list[str]]:
    report_columns = [
        "Date/Time",
        "Settlement Date",
        "Asset Category",
        "Symbol",
        "Currency",
        "Quantity",
        "Proceeds",
        "Comm/Fee",
        "Rate",
        "Proceeds in PLN",
        "Comm in PLN",
    ]
    available_columns = [column for column in report_columns if column in trades_df.columns]

    rows = [available_columns]
    for _, row in trades_df[available_columns].iterrows():
        rows.append([
            _format_cell(column, row[column])
            for column in available_columns
        ])

    return rows


def _format_cell(column: str, value) -> str:
    if pd.isna(value):
        return ""

    if column == "Date/Time":
        return pd.to_datetime(value).strftime("%Y-%m-%d %H:%M:%S")

    if column == "Settlement Date":
        return pd.to_datetime(value).strftime("%Y-%m-%d")

    if column in {"Quantity", "Proceeds", "Comm/Fee", "Proceeds in PLN", "Comm in PLN"}:
        return f"{float(value):,.2f}"

    if column == "Rate":
        return f"{float(value):.4f}" if isinstance(value, (int, float)) else str(value)

    return str(value)


def _build_page_stream(
    page_rows: list[list[str]],
    selected_year: int,
    total_profit: float,
    title: str,
    table_title: str,
    total_profit_label: str,
    page_number: int,
) -> str:
    commands = []
    generated_at = datetime.now().strftime("%Y-%m-%d %H:%M")

    commands.append(_text(MARGIN_X, PAGE_HEIGHT - 44, title, 18))
    commands.append(_text(MARGIN_X, PAGE_HEIGHT - 68, f"Tax year: {selected_year}", 10))
    commands.append(_text(
        MARGIN_X,
        PAGE_HEIGHT - 84,
        f"{total_profit_label}: {total_profit:,.2f} PLN",
        10,
    ))
    commands.append(_text(MARGIN_X, PAGE_HEIGHT - 100, f"Generated: {generated_at}", 8))
    commands.append(_text(MARGIN_X, PAGE_HEIGHT - 118, table_title, 12))

    y = PAGE_HEIGHT - TABLE_TOP
    if page_rows:
        commands.extend(_draw_table_header(page_rows[0], y))
        y -= HEADER_ROW_HEIGHT

    for row in page_rows[1:]:
        commands.extend(_draw_table_row(row, y))
        y -= ROW_HEIGHT

    commands.append(_text(PAGE_WIDTH - 92, 20, f"Page {page_number}", 8))
    return "\n".join(commands)


def _draw_table_header(columns: list[str], y: float) -> list[str]:
    commands = [_rectangle(MARGIN_X, y - HEADER_ROW_HEIGHT + 3, _table_width(), HEADER_ROW_HEIGHT, 0.9)]
    x = MARGIN_X + 4

    for column, width in zip(columns, _column_widths(columns)):
        commands.append(_text(x, y - 10, _truncate(column, width, 6), 6, bold=False))
        x += width

    return commands


def _draw_table_row(row: list[str], y: float) -> list[str]:
    commands = []
    x = MARGIN_X + 4

    for value, width in zip(row, _column_widths(row)):
        commands.append(_text(x, y - 10, _truncate(value, width, 6), 6))
        x += width

    return commands


def _column_widths(columns_or_row: list[str]) -> list[int]:
    width_map = {
        0: 86,
        1: 66,
        2: 94,
        3: 95,
        4: 42,
        5: 52,
        6: 58,
        7: 52,
        8: 44,
        9: 68,
        10: 62,
    }
    return [width_map.get(index, 55) for index in range(len(columns_or_row))]


def _table_width() -> int:
    return sum(_column_widths([""] * 11))


def _truncate(text: str, width: int, font_size: int) -> str:
    text = _sanitize_text(text)
    max_chars = max(int(width / (font_size * 0.52)), 4)

    if len(text) <= max_chars:
        return text

    return f"{text[:max_chars - 3]}..."


def _text(x: float, y: float, text: str, size: int, bold: bool = False) -> str:
    escaped = _escape_pdf_text(text)
    return f"BT /F1 {size} Tf {x:.2f} {y:.2f} Td ({escaped}) Tj ET"


def _rectangle(x: float, y: float, width: float, height: float, gray: float) -> str:
    return f"q {gray:.2f} g {x:.2f} {y:.2f} {width:.2f} {height:.2f} re f Q"


def _escape_pdf_text(text: str) -> str:
    return _sanitize_text(text).replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def _sanitize_text(text: str) -> str:
    text = str(text).translate(POLISH_TRANSLATION).replace("\n", " ")
    return unicodedata.normalize("NFKD", text).encode("latin-1", "ignore").decode("latin-1")


def _build_pdf(streams: list[str]) -> bytes:
    objects: list[bytes | None] = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        None,
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
    ]
    page_ids = []

    for stream in streams:
        stream_bytes = stream.encode("latin-1", errors="ignore")
        content_id = len(objects) + 1
        objects.append(
            b"<< /Length " + str(len(stream_bytes)).encode("ascii") + b" >>\n"
            b"stream\n" + stream_bytes + b"\nendstream"
        )

        page_id = len(objects) + 1
        page_ids.append(page_id)
        objects.append(
            f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 {PAGE_WIDTH} {PAGE_HEIGHT}] "
            f"/Resources << /Font << /F1 {FONT_NAME_OBJECT_ID} 0 R >> >> "
            f"/Contents {content_id} 0 R >>"
            .encode("ascii")
        )

    kids = " ".join(f"{page_id} 0 R" for page_id in page_ids)
    objects[1] = f"<< /Type /Pages /Kids [{kids}] /Count {len(page_ids)} >>".encode("ascii")

    pdf = bytearray(b"%PDF-1.4\n")
    offsets = [0]

    for object_id, obj in enumerate(objects, start=1):
        offsets.append(len(pdf))
        pdf.extend(f"{object_id} 0 obj\n".encode("ascii"))
        pdf.extend(obj or b"")
        pdf.extend(b"\nendobj\n")

    xref_offset = len(pdf)
    pdf.extend(f"xref\n0 {len(objects) + 1}\n".encode("ascii"))
    pdf.extend(b"0000000000 65535 f \n")

    for offset in offsets[1:]:
        pdf.extend(f"{offset:010d} 00000 n \n".encode("ascii"))

    pdf.extend(
        f"trailer\n<< /Size {len(objects) + 1} /Root 1 0 R >>\n"
        f"startxref\n{xref_offset}\n%%EOF"
        .encode("ascii")
    )

    return bytes(pdf)
