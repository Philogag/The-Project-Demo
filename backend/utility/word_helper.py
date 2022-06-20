

from docx.oxml.ns import qn


def set_table_cell_style(cell, font='宋体', font_extra=None):
    """设置文档内表格某一单元格的样式"""
    try:
        run = cell.paragraphs[0].runs[0]
        run.font.name = font
        run._element.rPr.rFonts.set(qn('w:eastAsia'), font)
        if font_extra is not None:
            for k, v in font_extra.items():
                setattr(run.font, k, v)
    except IndexError:
        pass


def insert_table_row(table, row_data: list):
    cells = table.add_row().cells

    for c, s in zip(cells, row_data):
        c.text = str(s)
    