from reportlab.pdfgen import canvas
from database.models import *

def export_mark_overview(request, year):
#    metadata = MetaData.objects.get(id=1)
#    year = metadata.current_year
    modules = Module.objects.filter(year=year)
    for module in modules:
        data = []
        anonymous_marks = AnonymousMarks.objects.filter(module=module)
        columns = ['Anonymous ID',]
        for marks in anonymous_marks:
            row = {}
            row['id'] = marks.exam_id
            if marks.assessment_1:
                if 'assessment_1' not in columns:
                    columns.append('assessment_1')
                row['assessment_1'] = marks.assessment_1
            if marks.assessment_2:
                if 'assessment_2' not in columns:
                    columns.append('assessment_2')
                row['assessment_2'] = marks.assessment_2
            if marks.assessment_3:
                if 'assessment_3' not in columns:
                    columns.append('assessment_3')
                row['assessment_3'] = marks.assessment_3
            if marks.assessment_4:
                if 'assessment_4' not in columns:
                    columns.append('assessment_4')
                row['assessment_4'] = marks.assessment_4
            if marks.assessment_5:
                if 'assessment_5' not in columns:
                    columns.append('assessment_5')
                row['assessment_5'] = marks.assessment_5
            if marks.assessment_6:
                if 'assessment_6' not in columns:
                    columns.append('assessment_6')
                row['assessment_6'] = marks.assessment_6
            if marks.exam:
                if 'exam' not in columns:
                    columns.append('exam')
                row['exam'] = marks.exam
            if marks.r_assessment_1:
                if 'r_assessment_1' not in columns:
                    columns.append('r_assessment_1')
                row['r_assessment_1'] = marks.r_assessment_1
            if marks.r_assessment_2:
                if 'r_assessment_2' not in columns:
                    columns.append('r_assessment_2')
                row['r_assessment_2'] = marks.r_assessment_2
            if marks.r_assessment_3:
                if 'r_assessment_3' not in columns:
                    columns.append('r_assessment_3')
                row['r_assessment_3'] = marks.r_assessment_3
            if marks.r_assessment_4:
                if 'r_assessment_4' not in columns:
                    columns.append('r_assessment_4')
                row['r_assessment_4'] = marks.r_assessment_4
            if marks.r_assessment_5:
                if 'r_assessment_5' not in columns:
                    columns.append('r_assessment_5')
                row['r_assessment_5'] = marks.r_assessment_5
            if marks.r_assessment_6:
                if 'r_assessment_6' not in columns:
                    columns.append('r_assessment_6')
                row['r_assessment_6'] = marks.r_assessment_6
            if marks.r_exam:
                if 'r_exam' not in columns:
                    columns.append('r_exam')
                row['r_exam'] = marks.r_exam
            if marks.q_assessment_1:
                if 'q_assessment_1' not in columns:
                    columns.append('q_assessment_1')
                row['q_assessment_1'] = marks.q_assessment_1
            if marks.q_assessment_2:
                if 'q_assessment_2' not in columns:
                    columns.append('q_assessment_2')
                row['q_assessment_2'] = marks.q_assessment_2
            if marks.q_assessment_3:
                if 'q_assessment_3' not in columns:
                    columns.append('q_assessment_3')
                row['q_assessment_3'] = marks.q_assessment_3
            if marks.q_assessment_4:
                if 'q_assessment_4' not in columns:
                    columns.append('q_assessment_4')
                row['q_assessment_4'] = marks.q_assessment_4
            if marks.q_assessment_5:
                if 'q_assessment_5' not in columns:
                    columns.append('q_assessment_5')
                row['q_assessment_5'] = marks.q_assessment_5
            if marks.q_assessment_6:
                if 'q_assessment_6' not in columns:
                    columns.append('q_assessment_6')
                row['q_assessment_6'] = marks.q_assessment_6
            if marks.q_exam:
                if 'q_exam' not in columns:
                    columns.append('q_exam')
                row['q_exam'] = marks.q_exam
            data.append(row)
        table = []
        header = []
        for item in columns:
            if item == "id":
                header.append("Anonymous ID")
            elif item == "assessment_1":
                header.append(module.assessment_1_title)
            elif item == "assessment_2":
                header.append(module.assessment_2_title)
            elif item == "assessment_3":
                header.append(module.assessment_3_title)
            elif item == "assessment_4":
                header.append(module.assessment_4_title)
            elif item == "assessment_5":
                header.append(module.assessment_5_title)
            elif item == "assessment_6":
                header.append(module.assessment_6_title)
            elif item == "exam":
                header.append("Exam")
            elif item == "r_assessment_1":
                title = module.assessment_1_title + " ([Re]sit)"
                header.append(title)
            elif item == "r_assessment_2":
                title = module.assessment_2_title + " ([Re]sit)"
                header.append(title)
            elif item == "r_assessment_3":
                title = module.assessment_3_title + " ([Re]sit)"
                header.append(title)
            elif item == "r_assessment_4":
                title = module.assessment_4_title + " ([Re]sit)"
                header.append(title)
            elif item == "r_assessment_5":
                title = module.assessment_5_title + " ([Re]sit)"
                header.append(title)
            elif item == "r_assessment_6":
                title = module.assessment_6_title + " ([Re]sit)"
                header.append(title)
            elif item == "r_exam":
                header.append("Exam ([Re]sit)")
            elif item == "q_assessment_1":
                title = module.assessment_1_title + " (QLD [Re]sit)"
                header.append(title)
            elif item == "q_assessment_2":
                title = module.assessment_2_title + " (QLD [Re]sit)"
                header.append(title)
            elif item == "q_assessment_3":
                title = module.assessment_3_title + " (QLD [Re]sit)"
                header.append(title)
            elif item == "q_assessment_4":
                title = module.assessment_4_title + " (QLD [Re]sit)"
                header.append(title)
            elif item == "q_assessment_5":
                title = module.assessment_5_title + " (QLD [Re]sit)"
                header.append(title)
            elif item == "q_assessment_6":
                title = module.assessment_6_title + " (QLD [Re]sit)"
                header.append(title)
            elif item == "q_exam":
                header.append("Exam (QLD [Re]sit)")

        table.append(columns)
        for row in data:
            table_row = []
            for item in columns:
                table_row.append(row[item])
            table.append(table_row)
        print table
    printstring = "juppie"
    title = "juppie"
pass
