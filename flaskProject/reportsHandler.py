import os

from pptx import Presentation
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE
from pptx.util import Inches, Pt
from Helper import *


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