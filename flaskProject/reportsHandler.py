import os
from datetime import date

from docx import Document
from pptx import Presentation
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE
from pptx.util import Inches, Pt
from database.databaseHandler import DatabaseHandler
from Helper import *

# get instance of db
db = DatabaseHandler()


def generateERB(event, findingsList, systemsList):
    # Code to generate ERB Report
    prs = Presentation()
    title_slide_layout = prs.slide_layouts[0]
    slide = prs.slides.add_slide(title_slide_layout)

    title = slide.shapes.title
    subtitle = slide.placeholders[1]

    left = top = Inches(.5)
    slide.shapes.add_picture('images/Capture.PNG', left, top)

    title.text = "U.S ARMY COMBAT CAPABILITIES DEVELOPMENT COMMAND - DATA & ANALYSIS CENTER"
    subtitle.text = event.getName()
    title.text_frame.paragraphs[0].font.size = Pt(30)

    # a second page
    title_slide_layout1 = prs.slide_layouts[1]
    slide = prs.slides.add_slide(title_slide_layout1)
    body_shape = slide.shapes.placeholders[1]

    left = top = Inches(.5)
    height = Inches(1)
    slide.shapes.add_picture('images/Capture1.PNG', left, top, height=height)
    left = Inches(7.4)
    slide.shapes.add_picture('images/Capture2.PNG', left, top, height=height)
    title1 = slide.shapes.title
    title1.text = "SCOPE"
    title1.text_frame.paragraphs[0].font.size = Pt(30)

    tf = body_shape.text_frame
    tf.text = 'Systems assessed during the CVPA are as follows:'

    # get just the non-archived systems
    for system in systemsList:
        p = tf.add_paragraph()
        p.text = system.getName()
        p.level = 1

    # third page
    title_slide_layout1 = prs.slide_layouts[0]
    slide = prs.slides.add_slide(title_slide_layout1)
    body_shape1 = slide.shapes.placeholders[0]

    left = top = Inches(.5)
    height = Inches(1)
    slide.shapes.add_picture('images/Capture1.PNG', left, top, height=height)
    left = Inches(7.4)
    slide.shapes.add_picture('images/Capture2.PNG', left, top, height=height)
    title1 = slide.shapes.title
    title1.text = "FINDINGS"
    title1.text_frame.paragraphs[0].font.size = Pt(30)

    # create table and then add a row per each finding
    cols = 5
    rows = 10
    top = Inches(1.7)
    left = Inches(0.5)
    width = Inches(9.0)
    height = Inches(1)

    table = slide.shapes.add_table(rows, cols, left, top, width, height).table

    # set column widths
    table.columns[0].width = Inches(1.8)
    table.columns[1].width = Inches(1.8)
    table.columns[2].width = Inches(1.8)
    table.columns[3].width = Inches(1.8)
    table.columns[4].width = Inches(1.8)

    # write column headings
    table.cell(0, 0).text = 'ID'
    table.cell(0, 1).text = 'System'
    table.cell(0, 2).text = 'Finding'
    table.cell(0, 3).text = 'Impact'
    table.cell(0, 4).text = 'Risk'

    row = 1
    for finding in findingsList:
        # write body cells
        table.cell(row, 0).text = str(finding.getid())
        table.cell(row, 1).text = finding.getHostName()
        table.cell(row, 2).text = finding.getType()
        table.cell(row, 3).text = str(finding.getImpactLevel())
        table.cell(row, 4).text = finding.getRisk()
        row += 1

    # change font size for the table
    for cell in iter_cells(table):
        for paragraph in cell.text_frame.paragraphs:
            for run in paragraph.runs:
                run.font.size = Pt(14)

    # fourth page
    for finding in findingsList:

        title_slide_layout1 = prs.slide_layouts[1]
        slide = prs.slides.add_slide(title_slide_layout1)
        body_shape1 = slide.shapes.placeholders[1]
        left = top = Inches(.5)
        height = Inches(1)
        slide.shapes.add_picture('images/Capture1.PNG', left, top, height=height)
        left = Inches(7.4)
        slide.shapes.add_picture('images/Capture2.PNG', left, top, height=height)
        title1 = slide.shapes.title
        title1.text = finding.getType()
        title1.text_frame.paragraphs[0].font.size = Pt(30)

        # create table and then add a row per each finding
        cols = 10
        rows = 14
        top = Inches(1.5)
        left = Inches(0.5)
        width = Inches(11.0)
        height = Inches(1)

        fTable = slide.shapes.add_table(rows, cols, left, top, width, height).table
        fTable.columns[0].width = Inches(.5)
        fTable.columns[3].width = Inches(1.7)
        fTable.columns[4].width = Inches(1)
        fTable.columns[7].width = Inches(.5)
        fTable.columns[8].width = Inches(.5)
        fTable.columns[9].width = Inches(.5)

        fTable.cell(1, 0).text = 'ID'
        fTable.cell(1, 1).text = str(finding.getid())

        fTable.cell(2, 0).text = 'Host Names'
        fTable.cell(3, 0).text = str(finding.getHostName())
        fTable.cell(2, 2).text = 'IP:PORT'
        fTable.cell(3, 2).text = str(finding.getIpPort())

        fTable.cell(1, 3).text = 'Impact Score'
        fTable.cell(1, 4).text = str(finding.getImpactScore())
        fTable.cell(2, 3).text = 'Cat'
        fTable.cell(2, 4).text = str(finding.getSeverityCategoryCode().name)
        fTable.cell(3, 3).text = 'Cat Score'
        fTable.cell(3, 4).text = str(finding.getSeverityCategoryScore())
        fTable.cell(4, 3).text = 'Vs Score'
        fTable.cell(4, 4).text = str(finding.getVulnerabilitySeverity())
        fTable.cell(5, 3).text = 'Vq'
        fTable.cell(5, 4).text = str(finding.getQualitativeVulnerabilitySeverity())
        fTable.cell(6, 3).text = 'Impact Rationale'
        fTable.cell(6, 4).text = str(finding.getImpactDescription())

        fTable.cell(1, 5).text = 'Status'
        fTable.cell(1, 6).text = finding.getStatus().name
        fTable.cell(2, 5).text = 'Likelihood'
        fTable.cell(2, 6).text = finding.getLikelihood()
        fTable.cell(3, 5).text = 'Impact'
        fTable.cell(3, 6).text = finding.getImpactLevel().name
        fTable.cell(4, 5).text = 'Risk'
        fTable.cell(4, 6).text = finding.getRisk()
        fTable.cell(5, 5).text = 'CM'
        fTable.cell(5, 6).text = str(finding.getCountermeasureEffectivenessRating().name)

        fTable.cell(1, 7).text = 'Posture'
        fTable.cell(2, 7).text = finding.getPosture()

        fTable.cell(3, 7).text = 'C'
        fTable.cell(4, 7).text = finding.getConfidentiality()
        fTable.cell(3, 8).text = 'I'
        fTable.cell(4, 8).text = finding.getIntegrity()
        fTable.cell(3, 9).text = 'A'
        fTable.cell(4, 9).text = finding.getAvailability()

        fTable.cell(7, 1).text = 'Type'
        fTable.cell(7, 2).text = finding.getType()

        fTable.cell(8, 2).text = finding.getDescription()
        fTable.cell(9, 0).text = 'Description'
        fTable.cell(9, 1).text = finding.getLongDescription()

        fTable.cell(10, 2).text = finding.getMitigationBriefDescription()
        fTable.cell(11, 0).text = 'Mitigation'
        fTable.cell(11, 1).text = finding.getMitigationLongDescription()

        fTable.cell(12, 0).text = 'Reference'
        fTable.cell(12, 2).text = 'Figure x'
        fTable.cell(13, 0).text = 'C-CONFIDENTIALITY  I-INTEGRITY  A-AVAILABILITY  CM-COUNTERMEASURE'

        # expand the column from 0 to 1 at row 2
        cell = fTable.cell(2, 0)
        other_cell = fTable.cell(2, 1)
        cell.merge(other_cell)
        # expand the column from 0 to 1
        cell = fTable.cell(3, 0)
        other_cell = fTable.cell(6, 1)
        cell.merge(other_cell)

        cell = fTable.cell(3, 2)
        other_cell = fTable.cell(6, 2)
        cell.merge(other_cell)

        cell = fTable.cell(6, 4)
        other_cell = fTable.cell(6, 6)
        cell.merge(other_cell)

        cell = fTable.cell(1, 7)
        other_cell = fTable.cell(1, 9)
        cell.merge(other_cell)
        cell = fTable.cell(2, 7)
        other_cell = fTable.cell(2, 9)
        cell.merge(other_cell)

        cell = fTable.cell(7, 0)
        other_cell = fTable.cell(7, 1)
        cell.merge(other_cell)

        cell = fTable.cell(7, 2)
        other_cell = fTable.cell(7, 9)
        cell.merge(other_cell)

        cell = fTable.cell(8, 1)
        other_cell = fTable.cell(8, 9)
        cell.merge(other_cell)
        cell = fTable.cell(10, 1)
        other_cell = fTable.cell(10, 9)
        cell.merge(other_cell)

        cell = fTable.cell(9, 1)
        other_cell = fTable.cell(9, 9)
        cell.merge(other_cell)
        cell = fTable.cell(11, 1)
        other_cell = fTable.cell(11, 9)
        cell.merge(other_cell)

        cell = fTable.cell(12, 0)
        other_cell = fTable.cell(12, 1)
        cell.merge(other_cell)

        cell = fTable.cell(12, 2)
        other_cell = fTable.cell(12, 9)
        cell.merge(other_cell)

        cell = fTable.cell(13, 0)
        other_cell = fTable.cell(13, 9)
        cell.merge(other_cell)

        for cell in iter_cells(fTable):
            for paragraph in cell.text_frame.paragraphs:
                for run in paragraph.runs:
                    run.font.size = Pt(12)

    # histogram page
    title_slide_layout1 = prs.slide_layouts[1]
    slide = prs.slides.add_slide(title_slide_layout1)
    body_shape = slide.shapes.placeholders[1]

    left = top = Inches(.5)
    height = Inches(1)
    slide.shapes.add_picture('images/Capture1.PNG', left, top, height=height)
    left = Inches(7.6)
    slide.shapes.add_picture('images/Capture2.PNG', left, top, height=height)
    title1 = slide.shapes.title
    title1.text = "Findings Histogram"
    title1.text_frame.paragraphs[0].font.size = Pt(30)

    subtitle = slide.placeholders[1]
    subtitle.text = "Finding Risk"

    # define chart data ---------------------
    info = 0
    veryLow = 0
    low = 0
    medium = 0
    high = 0
    veryHigh = 0
    for f in findingsList:
        if f.getRisk() == 'I':
            info += 1
        if f.getRisk() == 'VL':
            veryLow += 1
        if f.getRisk() == 'L':
            low += 1
        if f.getRisk() == 'M':
            medium += 1
        if f.getRisk() == 'H':
            high += 1
        if f.getRisk() == 'VH':
            veryHigh += 1

    chart_data = CategoryChartData()
    chart_data.categories = ['INFO', 'VERY LOW', 'LOW', 'MEDIUM', 'HIGH', 'VERY HIGH']
    chart_data.add_series('Series 1', (info, veryLow, low, medium, high, veryHigh))

    # add chart to slide --------------------
    x, y, cx, cy = Inches(1), Inches(2.5), Inches(8), Inches(4.5)
    slide.shapes.add_chart(
        XL_CHART_TYPE.COLUMN_CLUSTERED, x, y, cx, cy, chart_data
    )

    prs.save(os.path.expanduser('~/Downloads/ERBReport.pptx'))


def iter_cells(table):
    for row in table.rows:
        for cell in row.cells:
            yield cell

def generateFinalTecReport(event,findingsList):
    # Code to generate RiskMatrixReport
    document = Document()
    document.add_picture('images/Capture4.PNG', width=Inches(4))
    today = date.today()
    section = document.sections[0]
    header = section.header
    paragraph = header.paragraphs[0]
    paragraph.text = "\t\t" + today.strftime("%B %d, %Y")
    document.add_heading("Combat Capabilities Development Command (CCDC) Data &amp; Analysis Center (DAC) Enter "
                         "System Name Enter Event Type (e.g., CVPA, CVI, VoF, etc) Report", level=1)

    # get event team, get the analysts ann their first and last name here
    names = []
    for analyst in db.getAllAnalyst():
        for initial in event.getEventTeam():
            if initial == analyst.getInitial():
                mystr = analyst.getFirstName()
                mystr += " "
                mystr += analyst.getLastName()
                names.append(mystr)
    my_string = ', '.join(names)
    p = document.add_paragraph()
    p.add_run("by " + my_string).bold = True

    document.add_paragraph("classified by:" + event.getClassifiedBy())
    document.add_paragraph("Derived from:" + event.getSecurityClassificationTitleGuide())
    document.add_paragraph("Declassify on:" + event.getDeclassificationDate())

    # add a new page
    document.add_page_break()
    document.add_heading("DESTRUCTION NOTICE")
    document.add_paragraph("Destroy by any method that will prevent disclosure of contents or reconstruction of the "
                           "document.")
    document.add_heading("DISCLAIMER")
    document.add_paragraph(
        "The findings in this report are not to be construed as an official Department of the Army position unless so specified by other official documentation.")
    document.add_heading("WARNING")
    document.add_paragraph(
        "Information and data contained in this document are based on the input available at the time of preparation.")
    document.add_heading("TRADE NAMES")
    document.add_paragraph(
        "The use of trade names in this report does not constitute an official endorsement or approval of the use of such commercial hardware or software. The report may not be cited for purposes of advertisement.")

    # next page
    document.add_page_break()
    document.add_picture('images/Capture4.PNG', width=Inches(4))
    document.add_heading("Combat Capabilities Development Command (CCDC) Data &amp; Analysis Center (DAC) Enter "
                         "System Name Enter Event Type (e.g., CVPA, CVI, VoF, etc) Report", level=1)

    # get event team, get the analysts ann their first and last name here
    p = document.add_paragraph()
    p.add_run("by ...").bold = True

    document.add_paragraph("CCDC Data & Analysis Center")
    document.add_paragraph("Author(s)")
    document.add_paragraph("Affiliation")

    document.add_paragraph("classified by:" + event.getClassifiedBy())
    document.add_paragraph("Derived from:" + event.getSecurityClassificationTitleGuide())
    document.add_paragraph("Declassify on:" + event.getDeclassificationDate())

    # next page
    document.add_page_break()

    table = document.add_table(rows=31, cols=15)
    table.style = 'TableGrid'
    hdr_cells = table.rows[0].cells
    hdr_cells[0].text = 'REPORT DOCUMENTATION PAGE'

    a = table.cell(0, 0)
    b = table.cell(0, 9)
    a.merge(b)
    a = table.cell(0, 10)
    b = table.cell(0, 14)
    a.merge(b)

    hdr_cells = table.rows[1].cells
    hdr_cells[0].text = ''
    a = table.cell(1, 0)
    b = table.cell(1, 14)
    a.merge(b)

    hdr_cells = table.rows[2].cells
    hdr_cells[0].text = '1. REPORT DATE \n' + today.strftime("%B %d, %Y")
    a = table.cell(2, 0)
    b = table.cell(3, 4)
    a.merge(b)

    hdr_cells[5].text = '2. REPORT TYPE \n' + event.getType()
    a = table.cell(2, 5)
    b = table.cell(3, 10)
    a.merge(b)

    hdr_cells[11].text = '3. DATES COVERED'
    a = table.cell(2, 11)
    b = table.cell(3, 14)
    a.merge(b)

    hdr_cells = table.rows[4].cells
    hdr_cells[
        0].text = '4. TITLE AND SUBTITLE \n' + "Combat Capabilities Development Command (CCDC) Data &amp; Analysis Center (DAC) " + event.getType() + " Report."
    a = table.cell(4, 0)
    b = table.cell(6, 10)
    a.merge(b)
    hdr_cells[11].text = '5a. CONTRACT NUMBER'
    a = table.cell(4, 11)
    b = table.cell(4, 14)
    a.merge(b)

    hdr_cells = table.rows[5].cells
    hdr_cells[11].text = '5b. CONTRACT NUMBER'
    a = table.cell(5, 11)
    b = table.cell(5, 14)
    a.merge(b)

    hdr_cells = table.rows[6].cells
    hdr_cells[11].text = '5c. PROGRAM ELEMENT NUMBER'
    a = table.cell(6, 11)
    b = table.cell(6, 14)
    a.merge(b)

    hdr_cells = table.rows[7].cells
    hdr_cells[11].text = '5d. PROJECT NUMBER'
    a = table.cell(7, 11)
    b = table.cell(7, 14)
    a.merge(b)
    hdr_cells[0].text = '6. AUTHOR(S) \n' + my_string
    a = table.cell(7, 0)
    b = table.cell(10, 10)
    a.merge(b)

    hdr_cells = table.rows[8].cells
    hdr_cells[11].text = '5e. TASK NUMBER'
    a = table.cell(8, 11)
    b = table.cell(8, 14)
    a.merge(b)

    hdr_cells = table.rows[9].cells
    hdr_cells[11].text = '5f. WORK UNIT NUMBER'
    a = table.cell(9, 11)
    b = table.cell(9, 14)
    a.merge(b)

    hdr_cells = table.rows[10].cells
    hdr_cells[11].text = '8. PERFORMING ORGANIZATION REPORT NUMBER'
    a = table.cell(10, 11)
    b = table.cell(13, 14)
    a.merge(b)

    hdr_cells = table.rows[11].cells
    hdr_cells[
        0].text = '7. PERFORMING ORGANIZATION NAME(S) AND ADDRESS(ES) \n' + "Director U.S. Army CCDC Data & Analysis Center 6896 Mauchly Street Aberdeen Proving Ground, MD"
    a = table.cell(11, 0)
    b = table.cell(13, 10)
    a.merge(b)

    hdr_cells = table.rows[14].cells
    hdr_cells[0].text = '9. SPONSORING / MONITORING AGENCY NAME(S) AND ADDRESS(ES)'
    a = table.cell(14, 0)
    b = table.cell(17, 10)
    a.merge(b)
    hdr_cells[11].text = '10. SPONSOR/MONITOR’S ACRONYM(S)'
    a = table.cell(14, 11)
    b = table.cell(15, 14)
    a.merge(b)

    hdr_cells = table.rows[16].cells
    hdr_cells[11].text = '11. SPONSOR/MONITOR’S REPORT NUMBER(S)'
    a = table.cell(16, 11)
    b = table.cell(17, 14)
    a.merge(b)

    hdr_cells = table.rows[18].cells
    hdr_cells[0].text = '12. DISTRIBUTION / AVAILABILITY STATEMENT'
    a = table.cell(18, 0)
    b = table.cell(20, 14)
    a.merge(b)

    hdr_cells = table.rows[21].cells
    hdr_cells[0].text = '13. SUPPLEMENTARY NOTES'
    a = table.cell(21, 0)
    b = table.cell(23, 14)
    a.merge(b)

    hdr_cells = table.rows[23].cells
    hdr_cells[0].text = '14. ABSTRACT'
    a = table.cell(23, 0)
    b = table.cell(24, 14)
    a.merge(b)

    hdr_cells = table.rows[25].cells
    hdr_cells[0].text = '15. SUBJECT TERMS \n' + event.getType()
    a = table.cell(25, 0)
    b = table.cell(26, 14)
    a.merge(b)

    hdr_cells = table.rows[27].cells
    hdr_cells[0].text = '16. SECURITY CLASSIFICATION OF:'
    a = table.cell(27, 0)
    b = table.cell(28, 8)
    a.merge(b)

    hdr_cells[9].text = '17. LIMITATION OF ABSTRACT \n' + event.getEventClassification()
    a = table.cell(27, 9)
    b = table.cell(30, 10)
    a.merge(b)
    hdr_cells[11].text = '18. NUMBER OF PAGES \n' + "23"
    a = table.cell(27, 11)
    b = table.cell(30, 12)
    a.merge(b)
    hdr_cells[13].text = '19a. NAME OF RESPONSIBLE PERSON \n Person'
    a = table.cell(27, 13)
    b = table.cell(28, 14)
    a.merge(b)

    hdr_cells = table.rows[29].cells
    hdr_cells[0].text = 'a. REPORT \n' + event.getEventClassification()
    a = table.cell(29, 0)
    b = table.cell(30, 2)
    a.merge(b)
    hdr_cells[13].text = '19b. TELEPHONE NUMBER \n Phone'
    a = table.cell(29, 13)
    b = table.cell(30, 14)
    a.merge(b)
    hdr_cells[3].text = 'b. ABSTRACT \n' + event.getEventClassification()
    a = table.cell(29, 3)
    b = table.cell(30, 5)
    a.merge(b)
    hdr_cells[6].text = 'c. THIS PAGE \n' + event.getEventClassification()
    a = table.cell(29, 6)
    b = table.cell(30, 8)
    a.merge(b)

    # next page
    document.add_page_break()
    document.add_heading("Table of Contents")
    table = document.add_table(rows=15, cols=15)
    hdr_cells = table.rows[0].cells
    hdr_cells[0].text = 'List of Figures'
    hdr_cells[14].text = 'iv'
    a = table.cell(0, 0)
    b = table.cell(0, 10)
    a.merge(b)

    hdr_cells = table.rows[1].cells
    hdr_cells[0].text = 'List of Tables'
    hdr_cells[14].text = 'v'
    a = table.cell(1, 0)
    b = table.cell(1, 10)
    a.merge(b)

    hdr_cells = table.rows[2].cells
    hdr_cells[0].text = 'Acknowledgements'
    hdr_cells[14].text = 'vi'
    a = table.cell(2, 0)
    b = table.cell(2, 10)
    a.merge(b)

    hdr_cells = table.rows[3].cells
    hdr_cells[0].text = 'Executive summary'
    hdr_cells[14].text = 'vii'
    a = table.cell(3, 0)
    b = table.cell(3, 10)
    a.merge(b)

    hdr_cells = table.rows[4].cells
    hdr_cells[0].text = '1. (U) INTRODUCTION'
    hdr_cells[14].text = '8'
    a = table.cell(4, 0)
    b = table.cell(4, 12)
    a.merge(b)

    hdr_cells = table.rows[5].cells
    hdr_cells[1].text = '1.1 (U) System/Network Architecture'
    hdr_cells[14].text = '9'
    a = table.cell(5, 1)
    b = table.cell(5, 10)
    a.merge(b)
    hdr_cells = table.rows[6].cells
    hdr_cells[1].text = '1.2 (U) Test Setup and Network Postures'
    hdr_cells[14].text = '10'
    a = table.cell(6, 1)
    b = table.cell(6, 10)
    a.merge(b)
    hdr_cells = table.rows[7].cells
    hdr_cells[1].text = '1.3 (U) Limitations'
    hdr_cells[14].text = '10'
    a = table.cell(7, 1)
    b = table.cell(7, 10)
    a.merge(b)

    hdr_cells = table.rows[8].cells
    hdr_cells[0].text = '2. ENTER EVENT TYPE (E.G., CVPA, CVI, VOF, ETC) FINDING'
    hdr_cells[14].text = '11'
    a = table.cell(8, 0)
    b = table.cell(8, 12)
    a.merge(b)

    hdr_cells = table.rows[9].cells
    hdr_cells[1].text = '2.1 (U) Lack of Encryption'
    hdr_cells[14].text = '12'
    a = table.cell(9, 1)
    b = table.cell(9, 10)
    a.merge(b)
    hdr_cells = table.rows[10].cells
    hdr_cells[1].text = '2.2 (U) Missing Patches'
    hdr_cells[14].text = '14'
    a = table.cell(10, 1)
    b = table.cell(10, 10)
    a.merge(b)

    hdr_cells = table.rows[11].cells
    hdr_cells[0].text = '3. CONCLUSIONS AND RECOMMENDATIONS'
    hdr_cells[14].text = '16'
    a = table.cell(11, 0)
    b = table.cell(11, 12)
    a.merge(b)

    hdr_cells = table.rows[12].cells
    hdr_cells[0].text = 'Appendix A - List of Acronym'
    hdr_cells[14].text = 'A-1'
    a = table.cell(12, 0)
    b = table.cell(12, 12)
    a.merge(b)
    hdr_cells = table.rows[13].cells
    hdr_cells[0].text = '3. Appendix B - Distribution List'
    hdr_cells[14].text = 'B-1'
    a = table.cell(13, 0)
    b = table.cell(13, 12)
    a.merge(b)

    # next page
    document.add_page_break()
    document.add_heading("List of Figures")

    # next page
    document.add_page_break()
    document.add_heading("List of Tables")
    table = document.add_table(rows=15, cols=15)
    hdr_cells = table.rows[0].cells
    hdr_cells[0].text = 'Table 1. (S) List of Findings'
    hdr_cells[14].text = '11'
    a = table.cell(0, 0)
    b = table.cell(0, 10)
    a.merge(b)
    hdr_cells = table.rows[1].cells
    hdr_cells[0].text = 'Table 2 describes the Lack of Encryption vulnerability.'
    hdr_cells[14].text = '12'
    a = table.cell(1, 0)
    b = table.cell(1, 10)
    a.merge(b)
    hdr_cells = table.rows[2].cells
    hdr_cells[0].text = 'Table 3 describes the missing Patches vulnerability.'
    hdr_cells[14].text = '14'
    a = table.cell(2, 0)
    b = table.cell(2, 10)
    a.merge(b)

    # next page
    document.add_page_break()
    document.add_heading("Acknowledgements", level=1)
    document.add_paragraph("The U.S Army Combat Capabilities De")
    # next page
    document.add_page_break()
    document.add_heading("Executive Summary", level=1)
    # next page
    document.add_page_break()
    document.add_heading("(U) INTRODUCTION", level=1)
    # next page
    document.add_page_break()
    document.add_heading("(U) System/Network Architecture", level=1)

    # next page
    document.add_page_break()
    document.add_paragraph("1.2 Test Setup and Network Postures")
    document.add_paragraph("Limitations")
    document.add_heading("(U) ENTER EVENT TYPE (E.G., CVPA, CVI, VOF, ETC) FINDINGS", level=1)
    document.add_paragraph("(U) Table 1 lists vulnerabilities identified and validated by CCDC DAC during the Enter "
                           "Event Type (e.g., CVPA, CVI, VoF, etc) with their associated technical risk.")
    document.add_heading("Table 1. (S) List of Findings", level=1)

    table = document.add_table(rows=1, cols=9)
    table.style = 'TableGrid'
    hdr_cells = table.rows[0].cells
    hdr_cells[0].text = 'ID'
    hdr_cells[1].text = 'DESCRIPTION'
    hdr_cells[6].text = 'LIKELIHOOD'
    hdr_cells[7].text = 'IMPACT'
    hdr_cells[8].text = 'RISK'

    row = 0
    a = table.cell(row, 1)
    b = table.cell(row, 5)
    a.merge(b)
    for finding in findingsList:
        table.add_row()
        row += 1
        hdr_cells = table.rows[row].cells
        hdr_cells[0].text = str(finding.getid())
        hdr_cells[1].text = finding.getDescription()
        hdr_cells[6].text = finding.getLikelihood()
        hdr_cells[7].text = str(finding.getImpactLevel())
        hdr_cells[8].text = finding.getRisk()
        a = table.cell(row, 1)
        b = table.cell(row, 5)
        a.merge(b)

    # next page
    document.add_page_break()
    document.add_heading("(U) Lack of Encryption")
    document.add_paragraph("Table 2 describes the Lack of Encryption vulnerability")
    document.add_heading("Table 2. Lack of Encryption")

    lackEnc = None
    for finding in findingsList:
        if finding.getType().value == 'Encryption':
            lackEnc = finding

    missPatch = None
    for finding in findingsList:
        if finding.getType().value == 'Missing Patches':
            missPatch = finding

    # create a table for the finding with the encryption type
    table = document.add_table(rows=16, cols=12)
    table.style = 'TableGrid'
    hdr_cells = table.rows[0].cells
    hdr_cells[0].text = 'ID'
    hdr_cells[1].text = str(lackEnc.getid())
    a = table.cell(0, 1)
    b = table.cell(0, 2)
    a.merge(b)
    hdr_cells[3].text = ''

    hdr_cells[4].text = 'IMPACT SCORE'
    hdr_cells[5].text = str(lackEnc.getImpactScore())

    hdr_cells[6].text = 'STATUS'
    hdr_cells[7].text = lackEnc.getStatus()
    a = table.cell(0, 7)
    b = table.cell(0, 8)
    a.merge(b)
    a = table.cell(1, 7)
    b = table.cell(1, 8)
    a.merge(b)
    hdr_cells[9].text = 'POSTURE'
    a = table.cell(0, 9)
    b = table.cell(0, 11)
    a.merge(b)
    a = table.cell(1, 9)
    b = table.cell(1, 11)
    a.merge(b)
    #
    #
    hdr_cells = table.rows[1].cells
    hdr_cells[0].text = 'HOST NAMES'
    hdr_cells[2].text = 'IP:PORT'
    hdr_cells[4].text = 'CAT'
    hdr_cells[5].text = str(lackEnc.getSeverityCategoryCode().value)
    hdr_cells[6].text = 'LIKELIHOOD'
    hdr_cells[7].text = lackEnc.getLikelihood()
    hdr_cells[9].text = lackEnc.getPosture()

    a = table.cell(1, 0)
    b = table.cell(1, 1)
    a.merge(b)

    a = table.cell(1, 2)
    b = table.cell(1, 3)
    a.merge(b)
    a = table.cell(2, 2)
    b = table.cell(4, 3)
    a.merge(b)
    a = table.cell(2, 0)
    b = table.cell(4, 1)
    a.merge(b)
    a = table.cell(1, 9)
    b = table.cell(2, 11)
    a.merge(b)

    hdr_cells = table.rows[2].cells
    hdr_cells[0].text = lackEnc.getHostName()
    hdr_cells[2].text = lackEnc.getIpPort()
    hdr_cells[4].text = 'CAT SCORE'
    hdr_cells[5].text = str(lackEnc.getSeverityCategoryScore())
    hdr_cells[6].text = 'IMPACT'
    hdr_cells[7].text = str(lackEnc.getImpactLevel().value)
    a = table.cell(2, 7)
    b = table.cell(2, 8)
    a.merge(b)

    hdr_cells = table.rows[3].cells
    hdr_cells[4].text = 'Vs Score'
    hdr_cells[5].text = str(lackEnc.getSeverityCategoryScore())
    hdr_cells[6].text = 'Risk'
    hdr_cells[7].text = str(lackEnc.getImpactLevel().value)
    hdr_cells[9].text = 'C'
    hdr_cells[10].text = 'I'
    hdr_cells[11].text = 'A'

    a = table.cell(3, 7)
    b = table.cell(3, 8)
    a.merge(b)

    hdr_cells = table.rows[4].cells
    hdr_cells[4].text = 'Vs'
    hdr_cells[5].text = str(lackEnc.getSeverityCategoryCode().value)
    hdr_cells[6].text = 'CM'
    hdr_cells[7].text = str(lackEnc.getCountermeasureEffectivenessRating().value)
    hdr_cells[9].text = lackEnc.getConfidentiality()
    hdr_cells[10].text = lackEnc.getIntegrity()
    hdr_cells[11].text = lackEnc.getAvailability()

    a = table.cell(4, 7)
    b = table.cell(4, 8)
    a.merge(b)

    hdr_cells = table.rows[5].cells
    hdr_cells[0].text = 'TYPE'
    hdr_cells[4].text = 'Encryption'
    a = table.cell(5, 4)
    b = table.cell(5, 11)
    a.merge(b)
    a = table.cell(5, 0)
    b = table.cell(5, 3)
    a.merge(b)

    hdr_cells = table.rows[6].cells
    hdr_cells[0].text = ''
    hdr_cells[1].text = lackEnc.getDescription()
    a = table.cell(6, 1)
    b = table.cell(6, 11)
    a.merge(b)

    hdr_cells = table.rows[7].cells
    hdr_cells[0].text = 'DESCRIPTION'
    hdr_cells[1].text = lackEnc.getLongDescription()
    a = table.cell(7, 1)
    b = table.cell(9, 11)
    a.merge(b)
    a = table.cell(7, 0)
    b = table.cell(9, 0)
    a.merge(b)

    hdr_cells = table.rows[10].cells
    hdr_cells[0].text = ''
    hdr_cells[1].text = lackEnc.getMitigationBriefDescription()
    a = table.cell(7, 1)
    b = table.cell(7, 11)
    a.merge(b)
    a = table.cell(10, 1)
    b = table.cell(10, 11)
    a.merge(b)

    hdr_cells = table.rows[11].cells
    hdr_cells[0].text = 'MITIGATION'
    hdr_cells[1].text = lackEnc.getMitigationLongDescription()
    a = table.cell(11, 1)
    b = table.cell(13, 11)
    a.merge(b)
    a = table.cell(11, 0)
    b = table.cell(13, 0)
    a.merge(b)

    hdr_cells = table.rows[14].cells
    hdr_cells[0].text = 'REFERENCE'
    hdr_cells[4].text = 'FIGURE X'
    a = table.cell(14, 0)
    b = table.cell(14, 3)
    a.merge(b)
    a = table.cell(14, 4)
    b = table.cell(14, 11)
    a.merge(b)

    hdr_cells = table.rows[15].cells
    hdr_cells[0].text = 'C-CONFIDENTIALITY  I-INTEGRITY  A-AVAILABILITY  CM-COUNTERMEASURE'
    a = table.cell(15, 0)
    b = table.cell(15, 11)
    a.merge(b)

    # next page
    document.add_page_break()
    document.add_heading("2.2 (U) Missing Patches")
    document.add_paragraph("Table 3 describes the missing patches vulnerability")
    document.add_heading("Table 3. Missing Patches")

    # create a table for the finding with the missing patches type
    table = document.add_table(rows=16, cols=12)
    table.style = 'TableGrid'
    hdr_cells = table.rows[0].cells
    hdr_cells[0].text = 'ID'
    hdr_cells[1].text = str(missPatch.getid())
    a = table.cell(0, 1)
    b = table.cell(0, 2)
    a.merge(b)
    hdr_cells[3].text = ''

    hdr_cells[4].text = 'IMPACT SCORE'
    hdr_cells[5].text = str(missPatch.getImpactScore())

    hdr_cells[6].text = 'STATUS'
    hdr_cells[7].text = missPatch.getStatus()
    a = table.cell(0, 7)
    b = table.cell(0, 8)
    a.merge(b)
    a = table.cell(1, 7)
    b = table.cell(1, 8)
    a.merge(b)
    hdr_cells[9].text = 'POSTURE'
    a = table.cell(0, 9)
    b = table.cell(0, 11)
    a.merge(b)
    a = table.cell(1, 9)
    b = table.cell(1, 11)
    a.merge(b)
    #
    #
    hdr_cells = table.rows[1].cells
    hdr_cells[0].text = 'HOST NAMES'
    hdr_cells[2].text = 'IP:PORT'
    hdr_cells[4].text = 'CAT'
    hdr_cells[5].text = str(missPatch.getSeverityCategoryCode().value)
    hdr_cells[6].text = 'LIKELIHOOD'
    hdr_cells[7].text = missPatch.getLikelihood()
    hdr_cells[9].text = missPatch.getPosture()

    a = table.cell(1, 0)
    b = table.cell(1, 1)
    a.merge(b)

    a = table.cell(1, 2)
    b = table.cell(1, 3)
    a.merge(b)
    a = table.cell(2, 2)
    b = table.cell(4, 3)
    a.merge(b)
    a = table.cell(2, 0)
    b = table.cell(4, 1)
    a.merge(b)
    a = table.cell(1, 9)
    b = table.cell(2, 11)
    a.merge(b)

    hdr_cells = table.rows[2].cells
    hdr_cells[0].text = missPatch.getHostName()
    hdr_cells[2].text = missPatch.getIpPort()
    hdr_cells[4].text = 'CAT SCORE'
    hdr_cells[5].text = str(missPatch.getSeverityCategoryScore())
    hdr_cells[6].text = 'IMPACT'
    hdr_cells[7].text = str(missPatch.getImpactLevel().value)
    a = table.cell(2, 7)
    b = table.cell(2, 8)
    a.merge(b)

    hdr_cells = table.rows[3].cells
    hdr_cells[4].text = 'Vs Score'
    hdr_cells[5].text = str(missPatch.getSeverityCategoryScore())
    hdr_cells[6].text = 'Risk'
    hdr_cells[7].text = str(missPatch.getImpactLevel().value)
    hdr_cells[9].text = 'C'
    hdr_cells[10].text = 'I'
    hdr_cells[11].text = 'A'

    a = table.cell(3, 7)
    b = table.cell(3, 8)
    a.merge(b)

    hdr_cells = table.rows[4].cells
    hdr_cells[4].text = 'Vs'
    hdr_cells[5].text = str(missPatch.getSeverityCategoryCode().value)
    hdr_cells[6].text = 'CM'
    hdr_cells[7].text = str(missPatch.getCountermeasureEffectivenessRating().value)
    hdr_cells[9].text = missPatch.getConfidentiality()
    hdr_cells[10].text = missPatch.getIntegrity()
    hdr_cells[11].text = missPatch.getAvailability()

    a = table.cell(4, 7)
    b = table.cell(4, 8)
    a.merge(b)

    hdr_cells = table.rows[5].cells
    hdr_cells[0].text = 'TYPE'
    hdr_cells[4].text = 'Missing Patches'
    a = table.cell(5, 4)
    b = table.cell(5, 11)
    a.merge(b)
    a = table.cell(5, 0)
    b = table.cell(5, 3)
    a.merge(b)

    hdr_cells = table.rows[6].cells
    hdr_cells[0].text = ''
    hdr_cells[1].text = missPatch.getDescription()
    a = table.cell(6, 1)
    b = table.cell(6, 11)
    a.merge(b)

    hdr_cells = table.rows[7].cells
    hdr_cells[0].text = 'DESCRIPTION'
    hdr_cells[1].text = missPatch.getLongDescription()
    a = table.cell(7, 1)
    b = table.cell(9, 11)
    a.merge(b)
    a = table.cell(7, 0)
    b = table.cell(9, 0)
    a.merge(b)

    hdr_cells = table.rows[10].cells
    hdr_cells[0].text = ''
    hdr_cells[1].text = missPatch.getMitigationBriefDescription()
    a = table.cell(7, 1)
    b = table.cell(7, 11)
    a.merge(b)
    a = table.cell(10, 1)
    b = table.cell(10, 11)
    a.merge(b)

    hdr_cells = table.rows[11].cells
    hdr_cells[0].text = 'MITIGATION'
    hdr_cells[1].text = missPatch.getMitigationLongDescription()
    a = table.cell(11, 1)
    b = table.cell(13, 11)
    a.merge(b)
    a = table.cell(11, 0)
    b = table.cell(13, 0)
    a.merge(b)

    hdr_cells = table.rows[14].cells
    hdr_cells[0].text = 'REFERENCE'
    hdr_cells[4].text = 'FIGURE X'
    a = table.cell(14, 0)
    b = table.cell(14, 3)
    a.merge(b)
    a = table.cell(14, 4)
    b = table.cell(14, 11)
    a.merge(b)

    hdr_cells = table.rows[15].cells
    hdr_cells[0].text = 'C-CONFIDENTIALITY  I-INTEGRITY  A-AVAILABILITY  CM-COUNTERMEASURE'
    a = table.cell(15, 0)
    b = table.cell(15, 11)
    a.merge(b)

    # next page
    document.add_page_break()
    document.add_heading("3. CONCLUSIONS AND RECOMMENDATIONS")
    document.add_paragraph("Insert conclusions write up here")

    # next page
    document.add_page_break()
    document.add_heading("Appendix A - List of Acronym")

    # next page
    document.add_page_break()
    document.add_paragraph("CCDC           Combat Capabilities Development Command")
    document.add_paragraph("DAC            Data & Analysis Center")

    # next page
    document.add_page_break()
    document.add_heading("Appendix B - Distribution List")

    # next page
    document.add_page_break()
    document.add_heading("Organization")

    document.save(os.path.expanduser('~/Downloads/FinalTechnicalReport.docx'))