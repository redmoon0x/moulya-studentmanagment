from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageTemplate, Frame, BaseDocTemplate, Image
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.colors import HexColor
import pandas as pd
from datetime import datetime

class StudentReportGenerator:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        # Softer color scheme
        self.primary_color = HexColor('#2c3e50')  # Softer dark blue
        self.secondary_color = HexColor('#34495e')  # Softer medium blue
        self.accent_color = HexColor('#f5f6fa')  # Very light grey
        self.border_color = HexColor('#bdc3c7')  # Light grey for borders
        
        # Main college heading style (centered)
        self.college_name_style = ParagraphStyle(
            'CollegeName',
            parent=self.styles['Heading1'],
            fontSize=20,
            alignment=TA_CENTER,
            spaceAfter=10,
            textColor=self.primary_color,
            fontName='Helvetica-Bold',
            leading=24
        )
        
        # Student report subheading style (centered)
        self.report_title_style = ParagraphStyle(
            'ReportTitle',
            parent=self.styles['Heading2'],
            fontSize=16,
            alignment=TA_CENTER,
            spaceAfter=20,
            textColor=self.secondary_color,
            fontName='Helvetica-Bold'
        )
        
        self.heading_style = ParagraphStyle(
            'CustomHeading',
            parent=self.styles['Heading2'],
            fontSize=13,
            spaceAfter=10,
            spaceBefore=10,
            textColor=self.secondary_color,
            fontName='Helvetica-Bold',
            alignment=TA_LEFT
        )
        
        self.detail_label_style = ParagraphStyle(
            'DetailLabel',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=self.primary_color,
            fontName='Helvetica-Bold'
        )
        
        self.detail_value_style = ParagraphStyle(
            'DetailValue',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=colors.black,
            fontName='Helvetica'
        )

    def create_header(self, logo_path):
        """Create header with logo and college name in same row."""
       # Resize logo to be more proportional
        logo = Image(logo_path, width=1*inch, height=1*inch)
        
        # Create college name paragraph with left alignment to match logo
        college_name = Paragraph(
            "Dr. B.B. Hegde First Grade College Kundapura", 
            ParagraphStyle(
                'CollegeNameAligned',
                parent=self.college_name_style,
                alignment=TA_LEFT,  # Align text to left to match logo
                leftIndent=10  # Add some padding after logo
            )
        )
        
        # Create a table with logo and college name
        header_table = Table(
            [[logo, college_name]], 
            colWidths=[1.5*inch, 5*inch],  # Adjust column widths
            rowHeights=[1.2*inch]  # Slightly taller row
        )
        
        header_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),  # Left align entire row
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # Vertically center contents
            ('LEFTPADDING', (1, 0), (1, 0), 10),  # Add some space between logo and text
            ('RIGHTPADDING', (0, 0), (0, 0), 10),  # Add padding to logo cell
        ]))
        
        return header_table

    def create_title(self, student_name, reg_no, roll_no, logo_path):
        """Create the report title section with logo and refined styling."""
        header = self.create_header(logo_path)
        title = Paragraph("Student Report", self.report_title_style)
        
        # Consistent table widths and spacing
        details = [
            [Paragraph("Name:", self.detail_label_style), 
             Paragraph(student_name, self.detail_value_style)],
            [Paragraph("Registration Number:", self.detail_label_style), 
             Paragraph(reg_no, self.detail_value_style)],
            [Paragraph("Roll Number:", self.detail_label_style), 
             Paragraph(roll_no, self.detail_value_style)],
            [Paragraph("Report Generated:", self.detail_label_style), 
             Paragraph(datetime.now().strftime('%d-%m-%Y'), self.detail_value_style)]
        ]
        
        detail_table = Table(details, colWidths=[2.5*inch, 3.5*inch])
        detail_table.setStyle(TableStyle([
            ('GRID', (0, 0), (-1, -1), 0.25, self.border_color),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('PADDING', (0, 0), (-1, -1), 6),
            ('ROWBACKGROUNDS', (0, 0), (-1, -1), [colors.white, self.accent_color]),
        ]))
        
        # Reduced spacing between elements
        return [header, Spacer(1, 5), title, Spacer(1, 10), detail_table, Spacer(1, 15)]

    def create_attendance_summary_table(self, subject_wise_attendance):
        """Create the attendance summary table with consistent styling."""
        if subject_wise_attendance.empty:
            return []
        
        header = ['Subject', 'Total Classes', 'Classes Attended', 'Overall Percentage']
        data = [header]
        
        for _, row in subject_wise_attendance.iterrows():
            percentage = float(row['Overall Percentage'])
            percentage_color = (
                HexColor('#27ae60') if percentage >= 75 else
                HexColor('#e74c3c') if percentage < 65 else
                HexColor('#f39c12')
            )
            
            data.append([
                row['Subject'],
                str(row['Total Classes']),
                str(row['Classes Attended']),
                Paragraph(f"{percentage}%", 
                         ParagraphStyle('Percentage', 
                                      parent=self.styles['Normal'],
                                      textColor=percentage_color,
                                      fontSize=10,
                                      fontName='Helvetica'))
            ])
        
        # Match the width of the student details table
        table = Table(data, colWidths=[2.5*inch, 1.25*inch, 1.25*inch, 1*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), self.primary_color),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.25, self.border_color),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, self.accent_color]),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        
        return [
            Paragraph("Attendance Summary", self.heading_style),
            table,
            Spacer(1, 15)
        ]

    def create_marks_table(self, marks_data):
        """Create the marks table with consistent styling."""
        if marks_data.empty:
            return []
        
        header = ['Subject', 'Internal 1', 'Internal 2']
        data = [header]
        
        for _, row in marks_data.iterrows():
            int1 = str(row['Internal 1']) if pd.notna(row['Internal 1']) else 'N/A'
            int2 = str(row['Internal 2']) if pd.notna(row['Internal 2']) else 'N/A'
            
            def get_mark_color(mark):
                if mark == 'N/A':
                    return colors.grey
                mark = float(mark)
                if mark >= 18:
                    return HexColor('#27ae60')
                elif mark < 10:
                    return HexColor('#e74c3c')
                return HexColor('#f39c12')
            
            data.append([
                row['Subject'],
                Paragraph(int1, ParagraphStyle('Marks1', 
                                             parent=self.styles['Normal'],
                                             textColor=get_mark_color(int1),
                                             fontSize=10)),
                Paragraph(int2, ParagraphStyle('Marks2',
                                             parent=self.styles['Normal'],
                                             textColor=get_mark_color(int2),
                                             fontSize=10))
            ])
        
        # Match the width of other tables
        table = Table(data, colWidths=[2.5*inch, 1.75*inch, 1.75*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), self.primary_color),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.25, self.border_color),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, self.accent_color]),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        
        return [
            Paragraph("Internal Assessment Marks", self.heading_style),
            table,
            Spacer(1, 15)
        ]

    def add_watermark(self, canvas, doc):
        """Add centered watermark and page numbers."""
        canvas.saveState()
        canvas.setFont('Helvetica', 8)
        canvas.setFillColor(HexColor('#95a5a6'))
        canvas.drawCentredString(
            doc.pagesize[0] / 2,
            doc.bottomMargin / 2,
            "Moulya Student Management System"
        )
        canvas.setFont('Helvetica', 9)
        canvas.drawRightString(
            doc.width + doc.leftMargin,
            doc.bottomMargin / 2,
            f"Page {canvas.getPageNumber()}"
        )
        canvas.restoreState()

    def generate_report(self, student_name, reg_no, roll_no, subject_wise_attendance, marks_data, output_path, logo_path):
        """Generate the complete PDF report."""
        doc = BaseDocTemplate(
            output_path,
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=36,  # Reduced top margin
            bottomMargin=72
        )
        
        doc.addPageTemplates([
            PageTemplate(
                id='watermark',
                frames=[Frame(
                    doc.leftMargin,
                    doc.bottomMargin,
                    doc.width,
                    doc.height,
                    id='normal',
                    showBoundary=0
                )],
                onPage=self.add_watermark
            )
        ])
        
        content = []
        content.extend(self.create_title(student_name, reg_no, roll_no, logo_path))
        content.extend(self.create_attendance_summary_table(subject_wise_attendance))
        content.extend(self.create_marks_table(marks_data))
        
        doc.build(content)
        return output_path