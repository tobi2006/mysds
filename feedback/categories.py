# Feedback Categories

# When adding a new one, add the category to the available marksheet tuple
# to make sure it appears in the Module form.

AVAILABLE_MARKSHEETS = (
        ('PRESENTATION', 'Oral Presentation'),
        ('ESSAY', 'Essay'),
        ('LEGAL_PROBLEM', 'Legal Problem'),
        ('ONLINE_TEST_COURT_REPORT', 'Online Test / Court Report'),
        ('NEGOTIATION_WRITTEN', 'Negotiation / Written Submission'),
        ('ESSAY_LEGAL_PROBLEM', 'Essay / Legal Problem')
        )

CATEGORIES = {
        'PRESENTATION': {
                'title': 'Oral Presentation',
                'i_1': 'Understanding, Analysis and Content',
                'i_1_helptext': """80+ very full and perceptive awareness of socio-legal issues, with original critical and analytical assessment of the issues and an excellent grasp of their wider significance. Balanced argument. Exceptionally well-argued. Excellent response to questions. In-depth critical analysis.
70+ Comprehensive awareness of socio-legal issues and a clear grasp of their wider significance. Balanced argument. Well argued.  Very good response to questions. Good critical analysis of issues.
60 - 69 very good awareness of socio-legal issues and a serious understanding of their wider significance. Balanced argument with evidence of some critical discussion. Good response to questions.
50 - 59 some awareness of issues and their wider significance. Clear argument. Limited critical discussion. Reasonable responses to questions.
40 - 49 limited awareness of issues and their wider significance. Argument not always clearly advanced. No critical discussion. Lack of understanding of key concepts, principles etc. Some difficulty in answering questions/response to questions limited.
Fail - very poor awareness of issues and of their wider significance, with incoherent argument and structure. Some major inaccuracies re- key principles etc. Unable to provide more than a very basic response to questions.""",
                'i_2': 'Organisation and Application of Material',
                'i_2_helptext': """80+ Exceptionally well-structured and well-planned presentation. Clear, coherent progression between points. Extensive range of academic sources used. Material applied to offer critical and persuasive analysis of issues.
70+ Very well-structured and well-planned presentation. Clear progression between points. Wide range of academic sources used. Material applied to offer critical and persuasive analysis of issues.
60 - 69 Well-structured and well organised presentation. Clear progression between points. Range of relevant academic sources used. Material applied to offer somewhat critical analysis of issues.
50 - 59 Generally well-structured and organised presentation. Progression between points. Some relevant academic sources used. Material applied to offer analysis of issues.
40 - 49 Poorly organised presentation. Little progression between points. Very few academic sources used. Limited application of material.
Fail - very poorly organised presentation. No reference to academic sources. No application of material.""",
                'i_3': 'Delivery (inc visual aides, timing, planning)',
                'i_3_helptext': """80+ excellent delivery of material - excellent eye contact. Confident. Engaging presentation delivered without the use of prompts. Well-paced, well-timed. Excellent use and range of visual aides.
70+ Confident delivery of material - very good eye contact. Engaging presentation delivered without the use of prompts. Well-paced, well-timed. Very good use and range of visual aides. Visual aides clear, accurate and concise.
60 - 69 Confident delivery of material - good eye contact. Engaging presentation delivered with limited use of prompts. Well-paced, well-timed. Good use and range of clear and reasonably concise visual aides.
50 - 59 Good delivery of material - good eye contact. Over-reliance of prompts. Fair pace. Some engagement with audience. Visual aides used, but too detailed or lacking in clarity. Some errors in visual aides. 
40 - 49 Limited eye contact. Presentation mainly delivered by reading from script. Very little engagement with audience. Limited use of visual aides. Visual aides unclear/poorly presented with a number of errors.
Fail - No eye contact. Direct reading from script. No engagement with audience. Exceptionally poorly paced. No/very limited use of visual aides. Visual aides very clear/poorly presented with a significant number of errors."""
        },

        'ESSAY': {
                'title': 'Essay',
                'i_1': 'Reading and Knowledge',
                'i_1_helptext': """80+ extensive reading and exceptionally comprehensive knowledge.
70+ wide reading and comprehensive knowledge.
60 - 69 good range of reading and adequate knowledge.
50 - 59 fair range of reading and reasonable knowledge.
40 - 49 limited reading and incomplete knowledge.
Below 40 very limited reading and knowledge.""",
                'i_2': 'Understanding and Analysis',
                'i_2_helptext': """80+ very full and perceptive awareness of issues, with original critical and analytical assessment of the issues and an excellent grasp of their wider significance.
70+ full and perceptive awareness of issues and a clear grasp of their wider significance.
60 - 69 adequate awareness of issues and a serious understanding of their wider significance.
50 - 59 some awareness of issues and their wider significance.
40 - 49 limited awareness of issues and their wider significance.
Below 40 very limited awareness of issues and of their wider significance.""",
                'i_3': 'Argument',
                'i_3_helptext': """80+ clear evidence of independent and original thought and the ability to defend a position logically and convincingly, with arguments presented that are sophisticated and highly challenging.
70+ clear evidence of independent thought and the ability to defend a position logically and convincingly.
60 - 69 evidence of thought with a well-developed argument.
50 - 59 some evidence of thought with a serious attempt at an argument.
40 - 49 limited thought and argument.
Below 40 very limited thought and very meagre argument.""",
                'i_4': 'Organisation and Presentation',
                'i_4_helptext': """80+ excellent arrangement and development of material and argument, where the material has been handled with great dexterity. The work will be in excellent English and the presentation meticulous, with immaculate footnotes and extensive bibliography.

70+ careful thought has been given to the arrangement and development of material and argument.  The work will be in excellent English with appropriate footnotes and comprehensive bibliography.
60 - 69 adequate arrangement and development of material and argument.  The work will be in good English with appropriate footnotes and bibliography.
50 - 59 effort to organise the material and argument.  The work will be in adequate English with reasonable footnoting and a bibliography.
40 - 49 limited effort to organise the material and argument.  The work generally will be in satisfactory English but with limited footnoting and bibliography.
30 - 39 very little effort at organising the material.  The work will show significant errors in English and have poor footnoting and bibliography."""
                },

        'LEGAL_PROBLEM': {
                'title': 'Legal Problem',
                'i_1': 'Analysis of Issues',
                'i_1_helptext': """80+ identification of all core issues and almost all peripheral issues.
70+ identification of all core issues and most marginal issues.
60 - 69 identification of all (or nearly all) core issues.
50 - 59 identification of at least half the core issues.
40 - 49 identification of some relevant issues.
30 - 39 identification of very few issues. 
Below 30 no issues are correctly identified""",
                'i_2': 'Rule Identification',
                'i_2_helptext': '',
                'i_3': 'Analysis and Application of Law',
                'i_3_helptext': """80+ excellent issue analysis is excellent: an in-depth understanding and application of legal principles, cases and legislation, going beyond the main authorities.
70+ very good issue analysis and understanding and application of legal principles, cases and legislation, going beyond the main authorities.
60 - 69  good issue analysis and understanding of legal principles and effective use of main cases/legislation.
50 - 59 fair issue analysis which goes beyond a descriptive account with some understanding of relevant legal principles and some use of main cases and legislation.
40 - 49 issue analysis mainly descriptive with very little application of legal principles, cases or legislation.
30 - 39 unclear presentation and application of the law to the facts.
Below 30 lack of coherency in the presentation of the law and/or fails to demonstrate the ability to apply the law.""",
                'i_4': 'Structure and Presentation',
                'i_4_helptext': ''
                },

        'NEGOTIATION_WRITTEN': {
                'title': 'Negotiation / Written Submission',
                'i_1': 'Individual performance in assessed negotiation',
                'i_2': 'Research trail and notes',
                'i_3': 'Critical review',
                'i_4': 'Individual marks deducted for absences',
                'i_4_helptext': """
                    1. Tutor Led Seminar on 4th March: 2 mark deduction.
                    2. Lecture on 4th March: 2 mark deduction.
                    3. Seminar on 18th March: 2 mark deduction.
                    4. Student led LAU meetings on 25th February, 11th March, 18th
                        March and  22nd April (or substituted date for that week): 1 mark
                        deduction for each missed meeting as assessed from registers.
                    5. Absence from the assessed negotiation: 2 mark deduction""",
                'g_1': 'Team work during assessed negotiation',
                'g_2': 'Written pre-negotiation strategy and rationale',
                'g_3': 'Post negotiation review',
                'g_4': 'Final letter to client after negotiation',
                },

        'ONLINE_TEST_COURT_REPORT': {
                'title': 'Online Test / Court Report',
                'i_1': 'Reading and Knowledge',
                'i_1_helptext': """80+ extensive reading and exceptionally comprehensive knowledge.
70+ wide reading and comprehensive knowledge.
60 - 69 good range of reading and adequate knowledge.
50 - 59 fair range of reading and reasonable knowledge.
40 - 49 limited reading and incomplete knowledge.
Below 40 very limited reading and knowledge.""",
                'i_2': 'Understanding and Analysis',
                'i_2_helptext': """80+ very full and perceptive awareness of issues, with original critical and analytical assessment of the issues and an excellent grasp of their wider significance.
70+ full and perceptive awareness of issues and a clear grasp of their wider significance.
60 - 69 adequate awareness of issues and a serious understanding of their wider significance.
50 - 59 some awareness of issues and their wider significance.
40 - 49 limited awareness of issues and their wider significance.
Below 40 very limited awareness of issues and of their wider significance.""",
                'i_3': 'Argument',
                'i_3-helptext': """80+ clear evidence of independent and original thought and the ability to defend a position logically and convincingly, with arguments presented that are sophisticated and highly challenging.
70+ clear evidence of independent thought and the ability to defend a position logically and convincingly.
60 - 69 evidence of thought with a well-developed argument.
50 - 59 some evidence of thought with a serious attempt at an argument.
40 - 49 limited thought and argument.
Below 40 very limited thought and very meagre argument.""",
                'i_4': 'Organisation and Presentation',
                'i_4_helptext': """80+ excellent arrangement and development of material and argument, where the material has been handled with great dexterity. The work will be in excellent English and the presentation meticulous, with immaculate footnotes and extensive bibliography.
70+ careful thought has been given to the arrangement and development of material and argument.  The work will be in excellent English with appropriate footnotes and comprehensive bibliography.
60 - 69 adequate arrangement and development of material and argument.  The work will be in good English with appropriate footnotes and bibliography.
50 - 59 effort to organise the material and argument.  The work will be in adequate English with reasonable footnoting and a bibliography.
40 - 49 limited effort to organise the material and argument.  The work generally will be in satisfactory English but with limited footnoting and bibliography.
30 - 39 very little effort at organising the material.  The work will show significant errors in English and have poor footnoting and bibliography."""
                },
        }
