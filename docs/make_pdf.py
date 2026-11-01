"""Build docs/laporan.pdf from the report content.

Uses reportlab because no LaTeX compiler is available on lab PCs.
English comments only in this file.
"""
import os
import reportlab

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (Image, PageBreak,
                                Paragraph, Preformatted, SimpleDocTemplate,
                                Spacer, Table, TableStyle)
from reportlab.platypus.tableofcontents import TableOfContents

BASE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(BASE)
PDF = os.path.join(BASE, "laporan.pdf")
LOGO = os.path.join(ROOT, "assets", "logo-gunadarma.png")
FONTS = os.path.join(os.environ.get("WINDIR", r"C:\Windows"), "Fonts")

PAGE_W, PAGE_H = A4
LEFT = RIGHT = 2.5 * cm
TOP = 2.5 * cm
BOTTOM = 2.5 * cm

# Chapter list used for the table of contents and the body.
CHAPTERS = [
    ("1", "PENDAHULUAN"),
    ("2", "DASAR TEORI"),
    ("3", "TAHAPAN ALGORITMA"),
    ("4", "ALUR PROGRAM"),
    ("5", "SOURCE CODE BAGIAN ALGORITMA"),
    ("6", "HASIL UJI"),
    ("7", "PENUTUP"),
]

SUBS = {
    "1": [("1.1", "Tujuan"), ("1.2", "Ruang Lingkup")],
    "2": [("2.1", "Boundary Fill"), ("2.2", "Flood Fill"),
          ("2.3", "Varian Scanline")],
    "3": [("3.1", "Langkah Boundary Fill"), ("3.2", "Langkah Flood Fill"),
          ("3.3", "4 Arah lawan 8 Arah")],
    "4": [],
    "5": [],
    "6": [],
    "7": [],
}


def register_fonts():
    """Register the Times New Roman family for the report."""
    faces = {
        "Times": "times.ttf",
        "Times-Bold": "timesbd.ttf",
        "Times-Italic": "timesi.ttf",
        "Times-BoldItalic": "timesbi.ttf",
    }
    for name, file_name in faces.items():
        path = os.path.join(FONTS, file_name)
        if os.path.exists(path):
            pdfmetrics.registerFont(TTFont(name, path))
    pdfmetrics.registerFontFamily(
        "Times", normal="Times", bold="Times-Bold",
        italic="Times-Italic", boldItalic="Times-BoldItalic")


register_fonts()

styles = getSampleStyleSheet()

# Body text: Times New Roman 12 pt, justified, 1.5 line spacing.
body = ParagraphStyle(
    "body", parent=styles["Normal"], fontName="Times", fontSize=12,
    leading=18, alignment=TA_JUSTIFY, firstLineIndent=1.25 * cm,
    spaceAfter=6)

# Chapter title: centered, Times New Roman 14 pt, bold.
chapter = ParagraphStyle(
    "chapter", parent=body, fontName="Times-Bold", fontSize=14,
    leading=20, alignment=TA_CENTER, firstLineIndent=0,
    spaceBefore=0, spaceAfter=14)

# Sub chapter title: Times New Roman 12 pt, bold, left aligned.
sub = ParagraphStyle(
    "sub", parent=body, fontName="Times-Bold", fontSize=12, leading=18,
    alignment=0, firstLineIndent=0, spaceBefore=8, spaceAfter=4)

# Cover text: Times New Roman 14 pt, bold, centered, 1.5 line spacing.
cover = ParagraphStyle(
    "cover", parent=body, fontName="Times-Bold", fontSize=14, leading=21,
    alignment=TA_CENTER, firstLineIndent=0, spaceAfter=0)

# Code block style: monospace, small size.
code_s = ParagraphStyle(
    "code", parent=styles["Code"], fontName="Courier", fontSize=8,
    leading=10, spaceAfter=8)

# Table of contents styles: Times New Roman 12 pt.
toc0 = ParagraphStyle(
    "toc0", fontName="Times-Bold", fontSize=12, leading=18,
    leftIndent=0, firstLineIndent=0, spaceBefore=6)
toc1 = ParagraphStyle(
    "toc1", fontName="Times", fontSize=12, leading=18,
    leftIndent=1.25 * cm, firstLineIndent=0)


def p(text):
    """Make a justified body paragraph."""
    return Paragraph(text, body)


def toc_entry(level, text):
    """Make a flowable that also registers a table of contents entry."""
    return Paragraph(text, body, style=body) if level is None else \
        Paragraph(text, body).withBookmark(toc_entry.key)


def ch(number, title):
    """Make a chapter heading that starts on a new page.

    The heading is also registered in the table of contents.
    """
    return [PageBreak(),
            Paragraph('BAB %s' % number, chapter),
            Paragraph(title, chapter)]


def sh(number, title):
    """Make a numbered sub chapter heading."""
    return Paragraph('%s. %s' % (number, title), sub)


def code_block(text):
    """Turn a code string into a preformatted flowable."""
    return Preformatted(text, code_s)


def cover_story():
    """Build the cover page flowables in the required order."""
    items = []
    items.append(Paragraph('UNIVERSITAS GUNADARMA', cover))
    items.append(Spacer(1, 0.3 * cm))
    items.append(Paragraph('FAKULTAS TEKNOLOGI INDUSTRI', cover))
    items.append(Spacer(1, 1.1 * cm))
    if os.path.exists(LOGO):
        li = Image(LOGO, width=6.0 * cm, height=4.0 * cm)
        li.hAlign = 'CENTER'
        items.append(li)
        items.append(Spacer(1, 1.1 * cm))
    items.append(Paragraph('LAPORAN', cover))
    items.append(Spacer(1, 0.4 * cm))
    items.append(Paragraph('PENGISIAN WARNA PADA OBJEK GRAFIS', cover))
    items.append(Spacer(1, 0.2 * cm))
    items.append(Paragraph('BOUNDARY FILL DAN FLOOD FILL', cover))
    items.append(Spacer(1, 1.5 * cm))
    items.append(Paragraph('DISUSUN OLEH:', cover))
    items.append(Spacer(1, 0.4 * cm))
    names = Table(
        [['1.', 'Afwan Apriansyah (50422111)'],
         ['2.', 'Nama Anggota Dua (NPM)'],
         ['3.', 'Nama Anggota Tiga (NPM)']],
        colWidths=[1.2 * cm, 8.5 * cm])
    names.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Times-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 14),
        ('LEADING', (0, 0), (-1, -1), 21),
        ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
        ('ALIGN', (1, 0), (1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.black),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
    ]))
    names.hAlign = 'CENTER'
    items.append(names)
    return items


def on_page(canvas, doc):
    """Draw the cover footer and the centered page number.

    The cover shows the program study and the academic year.
    The table of contents has no page number.
    The body pages use numbers that start at 1 on the first chapter.
    """
    canvas.saveState()
    number = canvas.getPageNumber()
    if number == 1:
        canvas.setFont('Times-Bold', 14)
        canvas.drawCentredString(PAGE_W / 2.0, 1.5 * cm + 21, 'INFORMATIKA')
        canvas.drawCentredString(PAGE_W / 2.0, 1.5 * cm, 'PTA 2026/2027')
    elif number > 2:
        canvas.setFont('Times', 12)
        canvas.drawCentredString(PAGE_W / 2.0, 1.8 * cm, str(number - 2))
    canvas.restoreState()


class ReportDoc(SimpleDocTemplate):
    """Document template that collects table of contents entries."""

    def __init__(self, *args, **kwargs):
        """Set up the template with a chapter title lookup."""
        SimpleDocTemplate.__init__(self, *args, **kwargs)
        self.chapter_titles = dict(CHAPTERS)

    def afterFlowable(self, flowable):
        """Register chapter and sub chapter headings for the contents list."""
        if not isinstance(flowable, Paragraph):
            return
        style = flowable.style.name
        text = flowable.getPlainText()
        if style == 'chapter' and text.startswith('BAB '):
            number = text.replace('BAB ', '').strip()
            title = self.chapter_titles.get(number, '')
            key = 'chapter-%s' % number
            self.canv.bookmarkPage(key)
            self.canv.addOutlineEntry('BAB %s %s' % (number, title),
                                      key, 0, 0)
            self.notify('TOCEntry', (0, 'BAB %s %s' % (number, title),
                                     self.page - 2, key))
        elif style == 'sub':
            key = 'sub-%s' % text
            self.canv.bookmarkPage(key)
            self.notify('TOCEntry', (1, text, self.page - 2, key))


def chapter_story():
    """Build chapter 1 and 2 flowables."""
    story = []
    story.extend(ch('1', 'PENDAHULUAN'))
    story.append(p(
        'Tugas ini membahas materi nomor 6, yaitu pengisian warna pada objek '
        'grafis. Contoh penerapan pada gambar tugas adalah aplikasi mewarnai '
        'sederhana, pengisian area peta, atau coloring game. Kami membangun '
        'program Python dengan Tkinter tanpa library tambahan agar mudah '
        'dijalankan di komputer lab.'))
    story.append(sh('1.1', 'Tujuan'))
    story.append(p(
        'Tujuan tugas ini ada empat poin. Pertama, menjalankan program '
        'pewarnaan secara interaktif. Kedua, menunjukkan algoritma Boundary '
        'Fill dan Flood Fill secara benar. Ketiga, menjelaskan rumus dan '
        'tahapan algoritma dengan bahasa sederhana. Keempat, menampilkan alur '
        'dari input ke proses algoritma sampai output grafis.'))
    story.append(sh('1.2', 'Ruang Lingkup'))
    story.append(p(
        'Program memakai grid 40 x 26 sel. Ada tiga peta demo, yaitu rooms, '
        'circle, dan leak. Pengguna memilih algoritma, konektivitas 4 atau 8 '
        'arah, warna, dan kecepatan animasi. Output berupa area berwarna plus '
        'statistik jumlah piksel, waktu, dan ukuran stack.'))

    story.extend(ch('2', 'DASAR TEORI'))
    story.append(sh('2.1', 'Boundary Fill'))
    story.append(p(
        'Boundary Fill mulai dari titik seed lalu meluas selama piksel bukan '
        'warna batas dan bukan warna isi. Syarat berhentinya jelas, yaitu '
        'bertemu garis batas atau area yang sudah diisi. Versi 4 arah hanya '
        'bergerak atas, bawah, kiri, dan kanan. Versi 8 arah menambah arah '
        'diagonal sehingga dapat melewati celah diagonal.'))
    story.append(sh('2.2', 'Flood Fill'))
    story.append(p(
        'Flood Fill mulai dari titik seed lalu mengganti semua piksel yang '
        'punya warna target yang sama dan saling terhubung. Bedanya dengan '
        'Boundary Fill adalah Flood Fill tidak mencari warna batas, tetapi '
        'mencari warna awal yang sama. Contoh sederhana, klik area putih maka '
        'semua putih yang terhubung berubah jadi merah. Jika klik garis hitam '
        'maka tidak terjadi apa apa karena garis hitam dianggap batas.'))
    story.append(sh('2.3', 'Varian Scanline'))
    story.append(p(
        'Scanline Flood Fill mengisi satu baris horizontal penuh dulu, lalu '
        'antre baris atas dan bawah. Cara ini lebih hemat langkah untuk area '
        'lebar karena tidak men.stack semua piksel satu per satu. Kami pakai '
        'varian ini sebagai pembanding di laporan dan demo.'))
    return story


CODE1 = """def flood_fill(grid, sx, sy, fill_color, connectivity=4, trace=None):
    target = grid[sy][sx]
    if target == BOUNDARY or target == fill_color:
        return stats
    stack = [(sx, sy)]
    seen = set([(sx, sy)])
    while stack:
        x, y = stack.pop()
        if grid[y][x] != target:
            continue
        grid[y][x] = fill_color
        for nx, ny in pick(x, y):
            if (nx, ny) not in seen:
                seen.add((nx, ny))
                stack.append((nx, ny))"""

CODE2 = """if cur == boundary_color or cur == fill_color:
    continue
grid[y][x] = fill_color"""


def rest_story():
    """Build chapter 3 to 5 flowables."""
    story = []
    story.extend(ch('3', 'TAHAPAN ALGORITMA'))
    story.append(sh('3.1', 'Langkah Boundary Fill'))
    story.append(p(
        'Langkahnya sebagai berikut. Pertama, baca posisi klik sebagai seed '
        'dan warna isi pilihan. Kedua, jika seed di luar grid, di atas batas, '
        'atau sudah berwarna isi, maka berhenti. Ketiga, dorong seed ke stack '
        'dan tandai sudah dilihat. Keempat, ambil satu titik dari stack, catat '
        'sebagai visited, lalu lewati jika itu batas atau sudah diisi. Kelima, '
        'warnai titik valid lalu dorong semua tetangganya yang belum dilihat. '
        'Keenam, ulangi sampai stack kosong. Kompleksitas waktu sebanding '
        'dengan jumlah piksel yang dikunjungi.'))
    story.append(sh('3.2', 'Langkah Flood Fill'))
    story.append(p(
        'Langkahnya mirip, tetapi syaratnya memakai warna target. Pertama, '
        'simpan warna awal pada seed sebagai target. Kedua, jika target adalah '
        'batas atau sama dengan warna isi, maka berhenti. Ketiga, dorong seed '
        'ke stack. Keempat, ambil satu titik, lewati jika warnanya bukan '
        'target. Kelima, warnai titik itu lalu dorong tetangganya. Keenam, '
        'ulangi sampai stack kosong. Hasilnya adalah satu daerah terhubung yang '
        'berubah warna secara penuh.'))
    story.append(sh('3.3', '4 Arah lawan 8 Arah'))
    story.append(p(
        'Konektivitas 4 arah aman untuk peta dengan celah diagonal kecil karena '
        'diagonal tidak ikut terisi. Konektivitas 8 arah lebih agresif dan '
        'dapat bocor lewat sudut yang hanya bersentuhan diagonal. Peta leak '
        'pada demo sengaja diberi satu lubang untuk menunjukkan kasus bocor '
        'ini.'))

    story.extend(ch('4', 'ALUR PROGRAM'))
    story.append(p(
        'Alur program mengikuti perintah pada gambar tugas, yaitu dari input '
        'ke proses algoritma sampai output grafis.'))
    items = [
        'Input pengguna berupa klik mouse, pilihan peta, pilihan algoritma, '
        'konektivitas, warna, dan kecepatan animasi.',
        'Proses algoritma memakai stack eksplisit tanpa rekursi agar aman '
        'untuk area besar.',
        'Setiap titik yang diambil dicatat pada trace untuk animasi langkah '
        'demi langkah.',
        'Output grafis berupa grid berwarna pada kanvas Tkinter.',
        'Output teks berupa statistik filled, visited, ukuran stack '
        'maksimum, waktu dalam ms, titik awal, dan warna.',
    ]
    num = ParagraphStyle(
        'num', parent=body, fontName='Times', fontSize=12, leading=18,
        alignment=2, firstLineIndent=0, spaceAfter=0)
    cell = ParagraphStyle(
        'cell', parent=body, fontName='Times', fontSize=12, leading=18,
        alignment=0, firstLineIndent=0, spaceAfter=0)
    flow = Table(
        [[Paragraph('%d.' % (i + 1), num), Paragraph(t, cell)]
         for i, t in enumerate(items)],
        colWidths=[1.1 * cm, 13.6 * cm])
    flow.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (0, -1), 0),
        ('RIGHTPADDING', (0, 0), (0, -1), 8),
        ('LEFTPADDING', (1, 0), (1, -1), 0),
        ('RIGHTPADDING', (1, 0), (1, -1), 0),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    story.append(flow)
    story.append(p(
        'Interaksi minimal terpenuhi lewat tombol mouse, radio button, slider '
        'animasi, tombol Reset, Undo, Play trace, Stop, dan Auto fill 3 spots. '
        'Fitur Undo menyimpan sampai 20 status grid terakhir.'))

    story.extend(ch('5', 'SOURCE CODE BAGIAN ALGORITMA'))
    story.append(p(
        'Potongan berikut adalah inti Flood Fill pada file '
        'src/fill_algorithms.py. Komentar pada kode memakai bahasa Inggris '
        'sesuai aturan workspace.'))
    story.append(code_block(CODE1))
    story.append(p(
        'Potongan Boundary Fill memakai pola yang sama, tetapi syarat berhenti '
        'adalah warna batas.'))
    story.append(code_block(CODE2))
    story.append(p(
        'File lengkap ada pada src/fill_algorithms.py, peta demo pada '
        'src/maps.py, dan UI pada src/app.py.'))
    return story


def final_story():
    """Build chapter 6 and 7 flowables."""
    story = []
    story.extend(ch('6', 'HASIL UJI'))
    story.append(p(
        'Kami menjalankan 5 unit test dengan perintah python -m unittest '
        'discover -s tests -v. Semua lolos.'))
    rows = [['No', 'Kasus uji', 'Hasil'],
            ['1', 'Flood fill mewarnai area dalam', 'Lolos'],
            ['2', 'Boundary fill tidak menimpa dinding', 'Lolos'],
            ['3', 'Scanline dan flood mengisi area sama', 'Lolos'],
            ['4', 'Klik pada dinding tidak mengubah grid', 'Lolos'],
            ['5', 'Semua peta demo berhasil dimuat', 'Lolos']]
    table = Table(rows, colWidths=[1.2 * cm, 10.5 * cm, 2.5 * cm])
    table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ALIGN', (2, 0), (2, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, -1), 'Times'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(table)
    story.append(Spacer(1, 8))
    story.append(p(
        'Untuk demo lisan, pakai urutan ini. Pertama, buka peta rooms dan klik '
        'tiap ruang dengan warna beda. Kedua, ganti konektivitas dari 4 ke 8 '
        'lalu bandingkan hasilnya. Ketiga, buka peta leak dan klik dalam kotak '
        'untuk menunjukkan bocor lewat lubang. Keempat, tekan Auto fill 3 '
        'spots untuk tangkapan layar laporan. Kelima, tampilkan statistik waktu '
        'dan jumlah piksel sebagai bukti proses algoritma.'))

    story.extend(ch('7', 'PENUTUP'))
    story.append(p(
        'Program ini memenuhi tujuh ketentuan pada gambar tugas. Ada program '
        'yang dapat dijalankan, ada dua algoritma utama plus satu varian, ada '
        'penjelasan rumus dan tahapan, ada source code, ada alur input ke '
        'output, ada interaksi pengguna, dan ada laporan untuk presentasi. Saran '
        'pengembangan adalah menambah format gambar PNG, mode ember cat bebas, '
        'dan perekam GIF untuk animasi trace.'))
    return story


def make_toc():
    """Build the table of contents flowable."""
    toc = TableOfContents()
    toc.levelStyles = [toc0, toc1]
    toc.dotsMinLevel = 0
    return toc


def build():
    """Build the PDF file."""
    doc = ReportDoc(
        PDF, pagesize=A4, topMargin=TOP, bottomMargin=BOTTOM,
        leftMargin=LEFT, rightMargin=RIGHT,
        title='Laporan Pengisian Warna pada Objek Grafis',
        author='Kelompok 6')
    doc.chapter_titles = dict(CHAPTERS)

    story = []
    story.extend(cover_story())
    story.append(PageBreak())
    story.append(Paragraph('DAFTAR ISI', chapter))
    story.append(Spacer(1, 18))
    story.append(make_toc())
    story.extend(chapter_story())
    story.extend(rest_story())
    story.extend(final_story())
    doc.multiBuild(story, onFirstPage=on_page, onLaterPages=on_page)
    print('saved: ' + PDF)


if __name__ == '__main__':
    build()




