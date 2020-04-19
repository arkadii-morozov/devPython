# -*- coding: utf-8 -*-
from django.views.generic.base import TemplateView


class IndexView(TemplateView):
    template_name = "index.html"

    students_list = Student.get_students()
    average_bals_students = Statistics.calculate_average_bals(students_list)
    perfomance_students = Statistics.calculate_performance(average_bals_students)


    def get_context_data(self, **kwargs):

        context = super(IndexView, self).get_context_data(**kwargs)
        context.update(
            perfomance_students
        )
        return context


class Student:
    big_dict = {
        'students_statistics': [
            {
                'id': 1,
                'fio': 'Петров А.В.',
                'matan': 2,
                'bjd': 3,
                'philosophy': 4,
                'english': 5,
                'sport': 2.3,
                'average': 2.0,
            },
            {
                'id': 2,
                'fio': 'Сидоров В.Г.',
                'matan': 3.5,
                'bjd': 3.1,
                'philosophy': 3.4,
                'english': 2,
                'sport': 3.9,
            },
            {
                'id': 3,
                'fio': 'Иванов К.Ю.',
                'matan': 3.6,
                'bjd': 3,
                'philosophy': 3.6,
                'english': 3.7,
                'sport': 3.5,
            },
            {
                'id': 4,
                'fio': 'Попов А.Р.',
                'matan': 3.4,
                'bjd': 4,
                'philosophy': 4.1,
                'english': 3.2,
                'sport': 3.7,
            },
            {
                'id': 5,
                'fio': 'Абрамова О.К.',
                'matan': 3.0,
                'bjd': 3.8,
                'philosophy': 4.5,
                'english': 3.7,
                'sport': 3.3,
            },
            {
                'id': 6,
                'fio': 'Петрова А.Н.',
                'matan': 4.2,
                'bjd': 3.2,
                'philosophy': 4.1,
                'english': 4.1,
                'sport': 3.2,
            },
            {
                'id': 7,
                'fio': 'Трунина П.Н.',
                'matan': 3.2,
                'bjd': 4.0,
                'philosophy': 3.1,
                'english': 3.4,
                'sport': 4.0,
            },
        ],
    }

    def get_students(self):
        return self.big_dict


class Statistics:
    # student_id, [Scores]
    #dict_students = Student.get_students()

    def calculate_average_bals(self,big_dict):
        #big_dict = self.dict_students
        array_statistics = big_dict['students_statistics']
        len_big_dict = len(array_statistics)

        # расчет среднего бала по каждому студенту
        for student in range(len_big_dict):
            dict_statistics = array_statistics[student]
            real_average = 0
            for key, value in dict_statistics.items():
                if key != 'id' and key != 'fio':
                    real_average += value

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

        new_big_dict = big_dict
        new_big_dict['excellent_students'] = excellent_students_array
        new_big_dict['bad_students'] = bad_students_array

        return new_big_dict

class Subject:
    pass

class Score:
    # Subject, Student, value
    pass

'''
students_list = Student.get_students()
average_bals_students = Statistics.calculate_average_bals(students_list)
perfomance_students = Statistics.calculate_performance(average_bals_students)
'''