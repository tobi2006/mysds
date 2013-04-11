from django.forms.models import modelformset_factory, inlineformset_factory
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.decorators import login_required, user_passes_test

from database.models import Student, Module, Course, Performance, MetaData
from database import functions
from database.forms import StudentForm, ModuleForm, CSVUploadForm, CSVParseForm, generate_mark_form

def is_teacher(user):
    if user:
        if user.groups.filter(name='teachers').count() == 1:
            return True
        else:
            return False
    else:
        return False

@login_required
@user_passes_test(is_teacher)
def module_view(request, module_id, year):
    module_dict = functions.modules_for_menubar()
    modules = Module.objects.filter(code=module_id, year=year)
    module = modules[0]
    students = module.student_set.all()
    number_of_groups = 1
    performances = {}
    for student in students:
        performance = Performance.objects.get(student=student, module=module)
        if performance.seminar_group > number_of_groups:
            number_of_groups = performance.seminar_group
        performances[student] = performance

    #create string to make it iterable
    groupstring = ''
    for i in range(0, number_of_groups):
        groupstring += str(i+1)

    return render_to_response('module_view.html',
            {'current_module': module, 'performances': performances, 
            'number_of_groups': groupstring, 'module_dict': module_dict},
            context_instance = RequestContext(request)
            )

@login_required
@user_passes_test(is_teacher)
def module_overview(request, year):
    module_dict = functions.modules_for_menubar()
    modules = Module.objects.filter(year=year)
    return render_to_response('module_overview.html',
            {'modules': modules, 'year': year, 'module_dict': module_dict},
            context_instance = RequestContext(request)
        )

@login_required
@user_passes_test(is_teacher)
def year_view(request, year):
    module_dict = functions.modules_for_menubar()
    students = Student.objects.filter(year=year)
    ug = False
    pg = False
    phd = False
    alumnus = False
    if int(year) < 7:
        ug = True
    elif int(year) == 7:
        pg = True
    elif int(year) == 8:
        phd = True
    elif int(year) == 9:
        alumnus = True
    
    return render_to_response('year_view.html',
            {'students': students, 'year': year, 
            'ug': ug, 'pg':pg, 'phd': phd, 'alumnus': alumnus,
            'module_dict': module_dict},
            context_instance = RequestContext(request)
        )

@login_required
@user_passes_test(is_teacher)
def student_view(request, student_id):
    students = Student.objects.filter(student_id__icontains=student_id)
    current_student = students[0]
    module_dict = functions.modules_for_menubar()
    return render_to_response('student_view.html',
            {'current_student': current_student,'module_dict': module_dict},
            context_instance = RequestContext(request)
        )



@login_required
@user_passes_test(is_teacher)
def search_student(request):
    module_dict = functions.modules_for_menubar()
    if 'q' in request.GET and request.GET['q']:
        q = request.GET['q']
        students = Student.objects.filter(last_name__icontains=q)
        if len(students) == 1:
            student = students[0]
            return render_to_response('student_view.html',
                {'current_student': student,'module_dict': module_dict},
                context_instance = RequestContext(request)
            )
        else:
            return render_to_response('search_results.html',
                    {'students': students, 'query': q, 'module_dict': module_dict},
                    context_instance = RequestContext (request)
                )
    else:
        return HttpResponse('Please submit a search term.')

@login_required
@user_passes_test(is_teacher)
def add_student(request):
    module_dict = functions.modules_for_menubar()
    if request.method == 'POST':
        form = StudentForm(data=request.POST)
        if form.is_valid():
            student = form.save()
            return HttpResponseRedirect(student.get_absolute_url())
    else:
        form = StudentForm()
    return render_to_response(
        'student_form.html', 
        {'student_form': form, 'add': True, 'module_dict': module_dict}, 
        context_instance = RequestContext(request)
    )

@login_required
@user_passes_test(is_teacher)
def edit_student(request, student_id):
    module_dict = functions.modules_for_menubar()
    students = Student.objects.filter(student_id__icontains=student_id)
    student = students[0]
    if request.method == 'POST':
        form = StudentForm(instance=student, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(student.get_absolute_url())
    else:
        form = StudentForm(instance=student)
    return render_to_response(
        'student_form.html', 
        {'student_form': form, 'add': False, 'object': student, 'module_dict': module_dict}, 
        context_instance = RequestContext(request)
    )


@login_required
@user_passes_test(is_teacher)
def edit_module(request, module_id, year):
    module_dict = functions.modules_for_menubar()
    modules = Module.objects.filter(code=module_id, year=year)
    module = modules[0]
    if request.method == 'POST':
        form = ModuleForm(instance=module, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(module.get_absolute_url())
    else:
        form = ModuleForm(instance=module)
    return render_to_response(
        'module_form.html', 
        {'module_form': form, 'add': False, 'object': module, 'module_dict': module_dict}, 
        context_instance = RequestContext(request)
    )

@login_required
@user_passes_test(is_teacher)
def add_module(request):
    module_dict = functions.modules_for_menubar()
    if request.method == 'POST':
        form = ModuleForm(data=request.POST)
        if form.is_valid():
            module = form.save()
            return HttpResponseRedirect(module.get_absolute_url())
    else:
        form = ModuleForm()
    return render_to_response(
        'module_form.html', 
        {'module_form': form, 'add': True, 'module_dict': module_dict}, 
        context_instance = RequestContext(request)
    )


@login_required
@user_passes_test(is_teacher)
def mark(request, module_id, year, assessment):
    pass
    module_dict = functions.modules_for_menubar()
    module = Module.objects.get(code=module_id, year=year)
    students = module.student_set.all()
    performances = {}
    for student in students:
        performance = Performance.objects.get(student=student, module=module)
        performances[student] = performance
    if assessment == "exam":
        to_change = 9
    else:
        tmp = assessment.split("_")
        to_change = int(tmp[1])
    if request.method == 'POST':
        students = module.student_set.all()
        for student in students:
            if student.student_id in request.POST:
                tmp = request.POST[student.student_id]
                try:
                    mark = int(tmp)
                    if mark in range(0, 100):
                        performance = Performance.objects.get(student=student, module=module)
                        if to_change == 1:
                            performance.assessment_1 = mark
                        elif to_change == 2:
                            performance.assessment_2 = mark
                        elif to_change == 3:
                            performance.assessment_3 = mark
                        elif to_change == 4:
                            performance.assessment_4 = mark
                        elif to_change == 5:
                            performance.assessment_5 = mark
                        elif to_change == 6:
                            performance.assessment_6 = mark
                        elif to_change == 9:
                            performance.exam = mark
                    performance.save_with_avg()
                except ValueError:
                    pass
        return HttpResponseRedirect(module.get_absolute_url())
    return render_to_response(
            'mark.html',
            {'current_module': module, 'performances': performances, 'to_mark': to_change,
                'module_dict': module_dict},
            context_instance = RequestContext(request)
        )

@login_required
@user_passes_test(is_teacher)
def absences(request, module_id, year, group):
    module_dict = functions.modules_for_menubar()
    module = Module.objects.get(code=module_id, year=year)
    students = module.student_set.all()
    performances = {}
    for student in students:
        performance = Performance.objects.get(student=student, module=module)
        if group == "all":
            performances[student] = performance
        else:
            if performance.seminar_group == int(group):
                performances[student] = performance

    if request.method == 'POST':
        return HttpResponseRedirect(module.get_absolute_url())

    else:
        attendances = {}
        sessions = module.number_of_sessions
        for student, performance in performances.iteritems():
            attendances[student] = performance.attendance

    #Go on here

    return render_to_response(
            'absences.html',
            {'current_module': module, 'attendances': attendances, 'module_dict': module_dict},
            context_instance = RequestContext(request)
        )


    
@login_required
@user_passes_test(is_teacher)
def seminar_groups(request, module_id, year):
    test = "test"
    module_dict = functions.modules_for_menubar()
    module = Module.objects.get(code=module_id, year=year)
    students = module.student_set.all()
    student_ids = []
    performances = {}
    for student in students:
        student_ids.append(student.student_id)
        performance = Performance.objects.get(student=student, module=module)
        performances[student] = performance
    random_options={}
    for i in range(1,10): 
        # Up to 10 Seminar groups. Create a dictionary that lists the options
        # and the maximum number of students per group
        all = len(students)
        number = all / i
        left = all % i
        if left > 0:
            number = number + 1
        random_options[i]=number

    if request.method == 'POST':
        for student in students:
            if student.student_id in request.POST:
                tmp = request.POST[student.student_id]
                try:
                    seminar_group = int(tmp)
                    if seminar_group in range(0, 99):
                        performance = Performance.objects.get(student=student, module=module)
                        performance.seminar_group = seminar_group
                        performance.save()
                except ValueError:
                        pass
        return HttpResponseRedirect(module.get_absolute_url())
    return render_to_response(
            'seminar_groups.html',
            {'current_module': module, 'performances': performances, 'random_options': random_options,
                'students': student_ids, 'module_dict': module_dict},
            context_instance = RequestContext(request)
        )


@login_required
@user_passes_test(is_teacher)
def add_students_to_module(request, module_id, year):
    module_dict = functions.modules_for_menubar()
    module = Module.objects.get(code=module_id, year=year)
    llb = Course.objects.get(title="LLB (Hons) Bachelor Of Law")
    students_in_module = module.student_set.all()
    if len(module.eligible) > 1:
        more_than_one_year = True
    else:
        more_than_one_year = False
    students = []
    for number in module.eligible:
        year = int(number) # Find out which students are eligible
        meta_stuff = MetaData.objects.get(data_id=1)
        current_year = meta_stuff.current_year
        time_difference = module.year - current_year
        year = year - time_difference
        students_in_year = Student.objects.filter(year = year)
        for student in students_in_year:
            if student not in students_in_module:
                students.append(student)

    if request.method == 'POST':
        students_to_add = request.POST.getlist('selected_student_id')
        for student_id in students_to_add:
            student_to_add = Student.objects.get(student_id = student_id)
            student_to_add.modules.add(module)
            # Generate Performance entry for the student
            performance = Performance(
                    student = student_to_add,
                    module = module
                )
            performance.save()

        return HttpResponseRedirect(module.get_absolute_url())
    return render_to_response(
            'add_students_to_module.html',
            {'module': module, 'more_than_one_year': more_than_one_year, 
                'students': students, 'llb': llb, 'module_dict': module_dict},
            context_instance = RequestContext(request)
        )

@login_required
@user_passes_test(is_teacher)
def parse_csv(request):
    module_dict = functions.modules_for_menubar()
    importdata = request.session.get('csv_data')
    table = []
    for line in importdata:
        row = line.split(',')
        table.append(row)
    first_row = table[0]
    no_of_columns = len(first_row)
    if request.method == "POST":
        form = CSVParseForm(request.POST)
        if form.is_valid():
            list_of_columns = []
            if no_of_columns > 0:
                list_of_columns.append(form.cleaned_data['column_1'])
                if no_of_columns > 1:
                    list_of_columns.append(form.cleaned_data['column_2'])
                    if no_of_columns > 2:
                        list_of_columns.append(form.cleaned_data['column_3'])
                        if no_of_columns > 3:
                            list_of_columns.append(form.cleaned_data['column_4'])
                            if no_of_columns > 4:
                                list_of_columns.append(form.cleaned_data['column_5'])
                                if no_of_columns > 5:
                                    list_of_columns.append(form.cleaned_data['column_6'])
                                    if no_of_columns > 6:
                                        list_of_columns.append(form.cleaned_data['column_7'])
                                        if no_of_columns > 7:
                                            list_of_columns.append(form.cleaned_data['column_8'])
                                            if no_of_columns > 8:
                                                list_of_columns.append(form.cleaned_data['column_9'])
                                                if no_of_columns > 9:
                                                    list_of_columns.append(form.cleaned_data['column_10'])
                                                    if no_of_columns > 10:
                                                        list_of_columns.append(form.cleaned_data['column_11'])
                                                        if no_of_columns > 11:
                                                            list_of_columns.append(form.cleaned_data['column_12'])
            successful_entrys = 0
            for row in table:
                result = {}
                counter = 0
                for entry in row:
                    column = list_of_columns[counter]
                    if column != 'ignore':
                        result[column] = entry
                    counter += 1
                try: # Check if student is already in and add new data / amend existing
                    current = Student.objects.get(student_id=result['student_id'])
                    if 'first_name' in result:
                        current.first_name = result['first_name']
                    if 'last_name' in result:
                        current.last_name = result['last_name']
                    if 'since' in result:
                        current.since = result['since']
                    if 'year' in result:
                        tmp = result['year']
                        current.year = int(tmp[0])
                    if 'is_part_time' in result:
                        current.is_part_time = result['is_part_time']
                    if 'email' in result:
                        current.email = result['email']
                    if 'course' in result:
                        courses = Course.objects.filter(title__icontains = result['course'])
                        if courses:
                            course = courses[0]
                            current.course = course
                        else:
                            new_course = Course(title = result['course'])
                            new_course.save()
                            current.course = new_course
                    if 'qld' in result:
                        current.qld = result['qld']
                    if 'tutor' in result:
                        tutor_results = Tutor.objects.filter(name = result['tutor'])
                        tutor = tutors[0]
                        current.tutor = tutor
                    if 'notes' in result:
                        current.notes = current.notes + '\n' + result['notes']
                    if 'lsp' in result:
                        current.lsp = result['lsp']
                    if 'permanent_email' in result:
                        current.permanent_email = result['permanent_email']
                    if 'achieved_grade' in result:
                        current.achieved_grade = result['achieved_grade']
                    if 'address' in result:
                        current.address = result['address']
                    if 'home_address' in result:
                        current.home_address = result['home_address']
                    current.save()

                except Student.DoesNotExist: # Enter new student
                    if 'first_name' not in result:
                        result['first_name'] = ""
                    if 'last_name' not in result:
                        result['last_name'] = ""
                    if 'since' not in result:
                        result['since'] = ""
                    if 'year' not in result:
                        result['year'] = None
                    else:
                        tmp = result['year']
                        result['year'] = int(tmp[0])
                    if 'is_part_time' not in result:
                        result['is_part_time'] = False 
                    if 'email' not in result:
                        result['email'] = ""
                    if 'course' not in result:
                        result['course'] = None
                    else:
                        courses = Course.objects.filter(title__icontains = result['course'])
                        if courses:
                            course = courses[0]
                            result['course'] = course
                        else:
                            new_course = Course(title = result['course'])
                            new_course.save()
                            result['course'] = new_course
                    result['modules'] = ""
                    if 'qld' not in result:
                        result['qld'] = False
                    if 'tutor' not in result:
                        result['tutor'] = ""
                    else:
                        tutors = Tutor.objects.filter(name = result['tutor'])
                        tutor = tutors[0]
                        result['tutor'] = tutor
                    if 'notes' not in result:
                        result['notes'] = ""
                    result['highlighted'] = False
                    result['active'] = True
                    if 'lsp' not in result:
                        result['lsp'] = ""
                    if 'permanent_email' not in result:
                        result['permanent_email'] = ""
                    if 'achieved_grade' not in result:
                        result['achieved_grade'] = ""
                    if 'address' not in result:
                        result['address'] = ""
                    if 'home_address' not in result:
                        result['home_address'] = ""
                    new = Student(
                            student_id = result['student_id'],
                            first_name = result['first_name'],
                            last_name = result['last_name'],
                            #since = int(result['since']),
                            year = result['year'],
                            is_part_time = result['is_part_time'],
                            email = result['email'],
                            course = result['course'],
                            qld = result['qld'],
                            notes = result['notes'],
                            highlighted = result['highlighted'],
                            active = result['active'],
                            lsp = result['lsp'],
                            permanent_email = result['permanent_email'],
                            achieved_grade = result['achieved_grade'],
                            address = result['address'],
                            home_address = result['home_address']
                        )
                    new.save()
                    successful_entrys += 1
            request.session['number_of_imports'] = successful_entrys
            return HttpResponseRedirect('/import_success')
    else:
        form = CSVParseForm()
    return render_to_response(
            'parse_csv.html',
            {'form': form, 'csv_list': table, 'first_row': first_row, 'module_dict': module_dict},
            context_instance = RequestContext(request)
        )

@login_required
@user_passes_test(is_teacher)
def upload_csv(request):
    module_dict = functions.modules_for_menubar()
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            f = request.FILES['csvfile']
            f.read()
            csv_list = []
            for line in f:
                csv_list.append(line)
            request.session['csv_data'] = csv_list
            return HttpResponseRedirect('/parse_csv')
    else:
        form = CSVUploadForm()
    return render_to_response('upload_csv.html', {'form': form, 'module_dict': module_dict}, context_instance=RequestContext(request))

@login_required
@user_passes_test(is_teacher)
def import_success(request):
    module_dict = functions.modules_for_menubar()
    successful_entrys = request.session.get('number_of_imports')
    printstring = 'CSV File imported successfully: %s students added to the database' % (successful_entrys)
    title = 'CCCU Law DB: Data'
    return render_to_response('blank.html', {'printstring': printstring, 'title': title, 'module_dict': module_dict})
