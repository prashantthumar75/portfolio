from django.shortcuts import render, HttpResponse, redirect
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from .forms import ContactForm
from .models import ContactModel
import datetime

from xlutils.copy import copy # http://pypi.python.org/pypi/xlutils
from xlrd import open_workbook # http://pypi.python.org/pypi/xlrd
from django.core.mail import SafeMIMEText, EmailMessage
from django.conf import settings
import os


# Create your views here.

class TmpView(TemplateView):
    template_name = 'index.html'


class ContactView(CreateView):
    form_class = ContactForm
    template_name = 'index.html'
    success_url = '/excel'


def excel(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'inline'; filename="users.xls"
    # response['Content-Disposition'] = 'attachment; filename="users.xls"'

    path = os.path.dirname(__file__)
    file = os.path.join(path, 'sample2.xls')

    rb = open_workbook(file, formatting_info=True)
    r_sheet = rb.sheet_by_index(0)
    columns = ['date', 'Name', 'Email Address', 'Contact No.', 'Message']

    wb = copy(rb)
    ws = wb.get_sheet(0)

    row_num = 2  # index start from 0

    for col_num in range(len(columns)):
        print(f'row_num{row_num}')
        ws.write(row_num, col_num, columns[col_num])  # at 0 row 0 column


    rows = ContactModel.objects.all().values_list('name', 'email', 'number', 'message')
    date_Today = datetime.date.today()  # Returns 2018-01-15
    time_Today = datetime.datetime.now()  # Returns 2018-01-15 09:00


    print(f'time_todat{time_Today} date_todat {date_Today}')

    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            print(f'col_num{col_num}, row_num =={row_num}')
            ws.write(row_num, col_num+1, row[col_num])

    ws.write(row_num, 0, str(time_Today))

    wb.save(file + os.path.splitext(file)[-1]) # will save file where the excel file is
    wb.save(file) # will replace original file

    # wb.save(response)
    # return HttpResponse('Your information has benn sent!! \n\n Will Response Soon')
    return redirect('/email')


def contact(request):
        rows = ContactModel.objects.last()
        name_ = rows.name
        email_ = rows.email
        cont = rows.number
        msg = rows.message
        date_Today = datetime.date.today()  # Returns 2018-01-15
        time_Today = datetime.datetime.now()  # Returns 2018-01-15 09:00
        print(f'time_todat{time_Today} date_todat {date_Today}')
        print('-----------------------------------------------')
        print(f'rows.name{name_} rows.email{email_} rows.cont {cont} rows.msg{msg}')

        path = os.path.dirname(__file__)
        file = os.path.join(path, 'sample2.xls')

        mail = EmailMessage(  # subject
            "all list",
            # message
            # ('User file', file, 'sample/xls'),
            'New Customer Raised Question Below Are Details\n\n'
            + 'you can find Sheet Attact below\n'
              'Name:- ' + name_ + '\n Email:- ' + email_ + '\nContact Number:- ' + str(cont) + '\n Message:- ' + msg,
            #     'name',
            # from_email
            settings.EMAIL_HOST_USER,
            # recipient_list
            ['parthardeshana82@gmail.com']
            # ['pp119740@gmail.com']
        )
        mail.attach_file(file)
        mail.send()
        # return render(request, 'contactEmail.html')
        return redirect('/')
