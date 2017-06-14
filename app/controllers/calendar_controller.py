import datetime
import os

from flask import url_for
from werkzeug.routing import RequestRedirect

from app import g, app
from app.models import Calendar_el


def get_empty_days(monday, weekday):
    empty_days = []
    for num, day in enumerate(monday + datetime.timedelta(days=x) for x in range(0, weekday + 1 if weekday > 0 else 7)):
        if not Calendar_el.first(user_id=g.user.id, date=day):
            empty_days.append(num)
    return empty_days


def string_time(minutes):
    minutes = app.i(minutes, None)
    if minutes is None:
        return ''
    hours, minutes = divmod(minutes, 60)
    return "%02d:%02d" % (hours, minutes)


def autofinish_day():
    if g.user.last_started_day:
        need_finish = g.user.last_started_day != datetime.date.today()

        task_time = 0
        sys_times = {}
        for el in Calendar_el.all(user_id=g.user.id, date=g.user.last_started_day):
            if el.type:
                sys_times[el.type] = el.time
            else:
                task_time += el.time

        sum_time = sys_times.get(Calendar_el._type.Start, 0) + \
                   sys_times.get(Calendar_el.type.Food, 0) + task_time - \
                   sys_times.get(Calendar_el._type.NotOffice, 0)

        if sum_time == sys_times.get(Calendar_el._type.End, 9999999):
            if need_finish:
                g.user.last_started_day = None
                g.user.save()
                raise RequestRedirect(url_for('calendar'))
            elif need_finish or sys_times.get(Calendar_el._type.End):
                return "Время не сходится (%s)" % string_time(sum_time)
    return ""


def export_timesheet():
    import xlwt, xlrd
    from xlutils.copy import copy
    import io
    import locale

    today = datetime.date.today()

    def _getOutCell(outSheet, colIndex, rowIndex):
        """
        Функция получения ячейки
        :param outSheet: лист xls-таблицы
        :param colIndex: номер столбца
        :param rowIndex: номер строки
        :return: ячейка таблицы
        """
        # получаем строку
        row = outSheet._Worksheet__rows.get(rowIndex)
        if not row: return None

        # получаем ячейку в строке
        cell = row._Row__cells.get(colIndex)
        return cell

    def setOutCell(outSheet, col, row, value):
        """
        Функция установки значения в ячейку
        :param outSheet: лист xls-таблицы
        :param col: номер столбца
        :param row: номер строки
        :param value: значение, которое надо установить
        """
        # получаем начальное состояние ячейки
        previousCell = _getOutCell(outSheet, col, row)

        # записываем значение
        outSheet.write(row, col, value)

        # восстанавливаем исходное форматирование
        if previousCell:
            newCell = _getOutCell(outSheet, col, row)
            if newCell:
                newCell.xf_idx = previousCell.xf_idx

    # создаем буфер, в который потом сохраним наш xls
    f = io.BytesIO()

    filename = 'timesheet.xls'

    # открываем шаблон документа для выгрузки
    rb = xlrd.open_workbook(os.path.join(g.UPLOAD_FOLDER, filename), formatting_info=True)
    wb = copy(rb)
    ws = wb.get_sheet(0)

    # устанавливаем имя пользователя
    setOutCell(ws, 3, 7, str(g.user))

    locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')
    # устанавливаем месяц и дату выгрузки отчета
    setOutCell(ws, 9, 7, today.strftime("%b.%y"))
    setOutCell(ws, 9, 9, datetime.date.today().strftime("%d.%m.%Y"))

    coord = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L']

    # заполняем основное пространство таблицы
    for i in range(31):
        row = 14 + i
        setOutCell(ws, 10, row - 1, xlwt.Formula("SUM(D%s:H%s)" % (row, row)))

    for i in range(8):
        col = 3 + i
        colL = coord[col]

        setOutCell(ws, col, 44, xlwt.Formula("SUM(%s14:%s44)" % (colL, colL)))
        setOutCell(ws, col, 45, xlwt.Formula("%s45/8" % colL))

    projects = {}  # список проектов, над которыми работал пользователь
    projectTiming = {}  # время, затраченное на задачи по проекту

    timeFrom = datetime.date(today.year, today.month, 1)  # дата начала месяца
    timeTo = datetime.date(today.year, 12, 31) if today.month == 12 else \
        (datetime.date(today.year, today.month + 1, 1) - datetime.timedelta(days=1))  # дата конца месяца

    # выбираем все записи учета времени из БД для данного пользователя в указанный выше промежуток времени
    # и для каждой заносим информацию в соотв массив
    for t in Calendar_el.all(user=g.user, type=0).filter(Calendar_el.date <= timeTo).filter(
                    Calendar_el.date >= timeFrom):
        projectId = t.task.release.project.id
        day = t.date.day - 1

        if not projectId in projectTiming:
            projectTiming[projectId] = {}
            projects[projectId] = t.task.release.project.name

        if not day in projectTiming[projectId]: projectTiming[projectId][day] = 0

        projectTiming[projectId][day] += t.time

    i = 0
    # заносим данные по времени для каждого проекта в xls-таблицу
    for projectId, projectName in projects.items():
        col = 3 + i
        setOutCell(ws, col, 11, projectName)

        for j in range(31):
            if j in projectTiming[projectId]:
                row = 13 + j
                setOutCell(ws, col, row, projectTiming[projectId][j] / 60.)

        i += 1

    # сохраняем данные xls-документа в буфер
    wb.save(f)

    # устанавливаем указатель в начало файла
    f.seek(0)

    # возвращаем буфер
    return f
