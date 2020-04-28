# -*- coding: utf-8 -*-
from django.views.generic.base import TemplateView
from .forms import UserForm
from .models import Students,Subjects,Score
from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    submitbutton = request.POST.get("submit")
    firstname = ''
    lastname = ''
    fullname = ''
    if request.method == "POST":
        #form = UserForm(request.POST or None)
        form = UserForm(request.POST)
        if form.is_valid():
            firstname = form.cleaned_data.get('name')
            lastname = form.cleaned_data.get('surname')
            fullname = form.cleaned_data.get('full_name')
            form = UserForm()
            context = IndexView.get_context_data()
            context['form'] = form
            context['firstname'] = firstname
            context['lastname'] = lastname
            context['fullname'] = fullname
            context['submitbutton'] = submitbutton
        return render(request, 'index.html', context)


class IndexView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        students_list = Student().get_students()
        statistics = Statistics()
        students_list_with_average_bals = statistics.calculate_average_bals(students_list)
        students_list_with_perfomance= statistics.calculate_performance(students_list_with_average_bals)
        #####################
        # students_list_with_perfomance['form'] = data['form']
        # students_list_with_perfomance['firstname'] = data['firstname']
        # students_list_with_perfomance['lastname'] = data['lastname']
        # students_list_with_perfomance['fullname'] = data['fullname']
        # students_list_with_perfomance['submitbutton'] = data['submitbutton']
        #####################
        context = super(IndexView, self).get_context_data(**kwargs)
        context.update(
            students_list_with_perfomance
        )
        return context

    # def get_form(self, request):
    #     submitbutton = request.POST.get("submit")
    #     firstname = ''
    #     lastname = ''
    #     fullname = ''
    #     form = UserForm(request.POST or None)
    #     if form.is_valid():
    #         firstname = form.cleaned_data.get('name')
    #         lastname = form.cleaned_data.get('surname')
    #         fullname = form.cleaned_data.get('full_name')
    # 
    #     data = {'form': form, 'firstname': firstname, 'lastname': lastname,
    #             'fullname': fullname, 'submitbutton': submitbutton}
    #     return data

class Student:
    def get_students(self):
        stud_list = Students.objects.all().values()
        score_list = Score.objects.all().values()
        subject_list = Subjects.objects.all().values()
        result_list = []
        #student_dict = {}
        for student in stud_list:
            student_dict = {}
            student_dict["id"] = student["id"]
            student_dict["full_name"] = student["full_name"]
            result_list.append(student_dict)

        stud_list_full_name = result_list
        for student in stud_list_full_name:
            for subject in subject_list:
                student[subject["name"]] = '0'

        stud_list_subject_bal = stud_list_full_name
        for student in stud_list_subject_bal:
            for subject in score_list:
                if student["full_name"] == subject["full_name"]:
                    student[subject["subject"]] = subject["bal"]

        big_dict = {
            'students_statistics': stud_list_subject_bal
        }
        return big_dict


class Statistics:
    def calculate_average_bals(self,big_dict):
        array_statistics = big_dict['students_statistics']
        len_big_dict = len(array_statistics)

        # расчет среднего бала по каждому студенту
        for student in range(len_big_dict):
            dict_statistics = array_statistics[student]
            real_average = float(0.0)
            for key, value in dict_statistics.items():
                if key != 'id' and key != 'full_name':
                    real_average += float(value)

            real_average = '{:.2f}'.format(real_average / 5)
            dict_statistics['average'] = real_average

        new_big_dict = big_dict
        new_big_dict['students_statistics'] = array_statistics
        return new_big_dict

    def calculate_performance(self,big_dict):
        # у кого меньше проходного те на отчисление, у кого больше exellent тот отличник
        min_average_bal = float(3.0)
        exellent_bal = float(4.5)
        #big_dict = self.dict_students
        array_statistics = big_dict['students_statistics']
        len_big_dict = len(array_statistics)
        bad_students_array = []  # список студентов на отчисление
        excellent_students_array = []  # список студентов отличников
        # расчет по каждому студенту
        for student in range(len_big_dict):
            dict_statistics = array_statistics[student]
            real_average = 0
            if 'average' in dict_statistics:
                real_average = dict_statistics['average']
                if float(real_average) < min_average_bal:  # меньше проходного не включая
                    bad_students_array.append(dict_statistics)
                elif float(real_average) >= exellent_bal:  # больше или равно отличный бал
                    excellent_students_array.append(dict_statistics)
            else:
                real_average = "У студента, id:" + \
                               str(dict_statistics['id']) + \
                               "; ФИО:" + dict_statistics['fio'] + \
                               "; нет среднего бала."

        new_dict = big_dict
        new_dict['excellent_students'] = excellent_students_array
        new_dict['bad_students'] = bad_students_array

        return new_dict


class Subject:
    # def create(self,request):
    #     if request.method == "POST":
    #         table_subjects = Subjects()
    #         table_subjects.name = request.POST.get("name")
    #         table_subjects.save()
    #     return HttpResponseRedirect("/")
    pass

class Scores:
    pass