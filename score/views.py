from calendar import monthcalendar
import datetime
from PIL import Image
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.core.files.base import ContentFile

from django.shortcuts import render, redirect, get_object_or_404
from .models import Match, MemberCats, MatchHistory, Members
from django.http import HttpResponse, HttpResponseRedirect
from .forms import LoginForm, UserRegistrationForm, ScoreForm, CategoryForm, MembersForm, StartLists
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.db.models import Avg, Min, Max, Sum
from django.http import JsonResponse
from django.middleware import csrf
import random


def set_weight(request):
    match_id = request.POST.get('match_id', None)
    # user_id = int(request.POST.get('user_id', None))
    member_id = request.POST.get('member_id', None)
    user_id = request.user.id
    weight = float(request.POST.get('weight', None))
    owner_id = Match.objects.get(pk=match_id).owner_id
    result = None
    if user_id == owner_id:
        result = Members.objects.filter(pk=member_id).update(weight=weight)
    response = {
        'is_taken': result}
    return JsonResponse(response)


def set_winner(request):
    winner_id = request.POST.get('winner_id', None)
    category_id = request.POST.get('category_id', None)
    match_id = request.POST.get('match_id', None)
    # user_id = int(request.POST.get('user_id', None))
    user_id = request.user.id
    owner_id = Match.objects.get(pk=match_id).owner_id
    response = {
        'is_taken': winner_id}
    if user_id == owner_id:
        winner = StartLists.objects.get(category_id=category_id, member_id=winner_id)  # строка спортсмена в StartLists
        loser_id = winner.pair
        position = StartLists.objects.filter(category_id=category_id).aggregate(Max("position"))
        # print('winner=', winner.member_id, 'pos=', winner.position, 'looser=', loser_id)
        # print('max position=', position['position__max'])
        all_cat = len(StartLists.objects.filter(category_id=category_id))  # колич. участников в катег.
        try:
            last_member = StartLists.objects.get(category_id=category_id, pair=None, loses=winner.loses)  # спортсмен без пары в нужной сетке
            # print('last member без пары=', last_member.member_id, 'pos=', last_member.position)
            if winner.pk != last_member.pk:  # если нашли не сами себя (в случае если один участник)
                StartLists.objects.filter(pk=winner.pk).update(round=winner.round + 1,
                                                                      win=winner.win + 1,
                                                                      position=last_member.position + 1,
                                                                      pair=last_member.member_id)
                # а также добавляем ласт мемберу тоже пару.
                # print('нашли пару победителю pair=', last_member.member_id)
                StartLists.objects.filter(pk=last_member.pk).update(pair=winner_id)
        except ObjectDoesNotExist:  # если пары нет
            StartLists.objects.filter(pk=winner.pk).update(round=winner.round + 1, win=winner.win + 1,
                                                           position=position['position__max'] + 1 + (
                                                                   position['position__max'] % 2), pair=None)
            # print('Победитель', winner.member_id, 'position если нет пары=', position['position__max'] + 1 + (position['position__max'] % 2))
        position = StartLists.objects.filter(category_id=category_id).aggregate(Max("position"))
        # print('обновляем max position=', position['position__max'])
        # для проигравшего определяем сколько у него проражений
        try:
            # print('Обрабатываем проигравшего loser_id=', loser_id, 'category_id=', category_id)
            loser = StartLists.objects.get(category_id=category_id, member_id=loser_id)

            # сохранение истории поединков для статистики побед между спортсменами
            MatchHistory.objects.create(match=match_id, category=category_id, win_id=winner.member_id,
                                        los_id=loser.member_id)
            if loser.loses == 0:  # если это первое поражение участник опускается в Б сетку
                try:
                    # print('если у проигравшего нет поражений')
                    last_member = StartLists.objects.get(category_id=category_id, pair=None, loses=1)  # спортсмен в нашей сетке без пары
                    if loser.pk != last_member.pk:  # если это не мы сами
                        StartLists.objects.filter(pk=loser.pk).update(round=loser.round + 1,
                                                                      position=last_member.position + 1,
                                                                      pair=last_member.member_id)
                        StartLists.objects.filter(pk=last_member.pk).update(pair=loser_id)
                        # print('если нашли пару loser=', loser.member_id, 'pair=', last_member.member_id, 'pos=', last_member.position+1)
                except ObjectDoesNotExist:  # если пары не найдено
                    # print('если пары проигравшему не найдено то его position=', position['position__max'] + 1 + (position['position__max'] % 2))
                    StartLists.objects.filter(pk=loser.pk).update(round=loser.round + 1,
                                                                  position=position['position__max'] + 1 + (
                                                                          position['position__max'] % 2), pair=None)
            else:  # вылетел из соревнований
                # print('вылетел из соревнований id=', loser.member_id)
                # all_cat = len(StartLists.objects.filter(category_id=category_id))  # колич. участников в катег.
                place = StartLists.objects.filter(category_id=category_id).exclude(place=0).aggregate(
                        Min('place'))
                if place['place__min']:  # Если последее место уже кто то занял
                    StartLists.objects.filter(pk=loser.pk).update(place=place['place__min'] - 1)
                else:
                    StartLists.objects.filter(pk=loser.pk).update(place=all_cat)
            StartLists.objects.filter(pk=loser.pk).update(loses=loser.loses + 1)
        except ObjectDoesNotExist:  # если нажата кнопка где нет соперника
            print('где то была необработанная ошибка у проигравшего')
        # текущее количество участников в а и б сетках
        a_count = len(StartLists.objects.filter(category_id=category_id, loses=0))
        b_count = len(StartLists.objects.filter(category_id=category_id, loses=1))

        if a_count == 1:  # если в верхней сетке остался один участник
            if b_count == 0:  # победитель
                MemberCats.objects.filter(pk=category_id).update(min=4)
                StartLists.objects.filter(pk=winner.pk).update(place=1)
            if b_count == 2:  # полуфинал
                MemberCats.objects.filter(pk=category_id).update(min=1)
                a_member = StartLists.objects.get(category_id=category_id, loses=0)
                # b_member = StartLists.objects.get(category_id=category_id, loses=1)
                # StartLists.objects.filter(pk=a_member.pk).update(pair=b_member.member_id, position=2)
                # StartLists.objects.filter(pk=b_member.pk).update(pair=a_member.member_id, position=1)
                if all_cat > 3:
                    # Изменяем позицию финалиста, чтобы он был ниже полуфиналистов в списке
                    # print('изменяем финалиста =', a_member.member_id, 'pos=', position['position__max'] + 1)
                    StartLists.objects.filter(pk=a_member.pk).update(position=position['position__max'] + 1)
            if b_count == 1:  # финал
                a_member = StartLists.objects.get(category_id=category_id, pair=None, loses=0)
                b_member = StartLists.objects.get(category_id=category_id, pair=None, loses=1)
                StartLists.objects.filter(pk=a_member.pk).update(pair=b_member.member_id, position=2)
                StartLists.objects.filter(pk=b_member.pk).update(pair=a_member.member_id, position=1)
                MemberCats.objects.filter(pk=category_id).update(min=2)


        elif a_count == 0:
            if b_count == 1:  # победитель
                MemberCats.objects.filter(pk=category_id).update(min=4)
                StartLists.objects.filter(pk=winner.pk).update(place=1)
            if b_count == 2:  # суперфинал
                MemberCats.objects.filter(pk=category_id).update(min=3)
        else:
            MemberCats.objects.filter(pk=category_id).update(min=0)
    return JsonResponse(response)

def validate_username(request):
    """Проверка доступности логина"""
    username = request.GET.get('username', None)
    response = {
        'is_taken': User.objects.filter(username__iexact=username).exists()
    }
    return JsonResponse(response)

def check_username(request):
    """Проверка наличия спортсмена"""
    s = []
    username = request.POST.get('surname', None)
    category_id = request.POST.get('category_id', None)
    match_id = request.POST.get('match_id', None)
    if len(username) > 2:
        members = Members.objects.filter(surname__icontains=username)
        if members:
            s.append('<div class="popover" id="popover"><ul>')
            for member in members:
                s.append('<li><form action="/dashboard/select_user/" method="POST">')
                s.append('<input type="hidden" name="csrfmiddlewaretoken" value="{}">'.format(csrf.get_token(request)))
                s.append('<input type="hidden" name="match_id" value="{}">'.format(match_id))
                s.append('<input type="hidden" name="category_id" value="{}">'.format(category_id))
                s.append('<input type="hidden" name="member_id" value="{}">'.format(member.pk))
                s.append('<input type="submit" id="go_to" value="{} {} {} {}">'
                         .format(member.surname, member.name, member.second_name, member.birthday))
                s.append('</li>')
                # s.append('<li><a href="/dashboard/select_user/?category_id={5}&match_id={6}&fo={7}'
                #          '&member_id={4}">{0} {1} {2} {3}</a></li>'.format(member.surname, member.name,
                #                                                            member.second_name, member.birthday,
                #                                                            member.pk, category_id, match_id, member.fo))
            s.append('</ul></div>')
            cal = "\n".join(s)
            response = {
                'is_taken': True,
                'members': cal
            }
        else:
            response = {
                'is_taken': False,
            }
    else:
        response = {
            'is_taken': False,
        }
    return JsonResponse(response)

def month_name(num, lang):
    en = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september',
          'october', 'november', 'december']
    ru = ['январь', 'февраль', 'март', 'апрель', 'май', 'июнь', 'июль', 'август', 'сентябрь',
          'октябрь', 'ноябрь', 'декабрь']
    if lang == 'en':
        return en[num - 1]
    else:
        return ru[num - 1]


def get_calendar(date, d):
    s = []
    sm = []
    if date.month == 1:
        pm = 12
        py = date.year - 1
    else:
        pm = date.month - 1
        py = date.year

    if date.month == 12:
        nm = 1
        ny = date.year + 1
    else:
        nm = date.month + 1
        ny = date.year

    pmatrix = monthcalendar(py, pm)
    matrix = monthcalendar(date.year, date.month)
    matrix_c = monthcalendar(date.year, date.month)
    nmatrix = monthcalendar(ny, nm)
    for item in enumerate(pmatrix[-1]):
        if matrix[0][item[0]] == 0:
            matrix[0][item[0]] = item[1]
    for item in enumerate(nmatrix[0]):
        if matrix[-1][item[0]] == 0:
            matrix[-1][item[0]] = item[1]
    m_name = month_name(date.month, 'ru')
    s.append('<table class ="datepicker">\n\t<caption class="datepicker-caption">'
             '\n\t\t<a href="?year={}&month={}" class="datepicker-prev">Previous</a>'.format(py, pm))
    s.append('\t\t<span class="datepicker-title">{} {}</span>'.format(m_name.capitalize(), date.year))
    s.append('\t\t<a href="?year={}&month={}" class="datepicker-next">Next</a>\n\t</caption>\n\t'
             '<thead class="datepicker-head">\n\t\t<tr>\n\t\t\t<th class="datepicker-th">Mo</th>'
             '\n\t\t\t<th class="datepicker-th">Tu</th>\n\t\t\t<th class="datepicker-th">We</th>'
             '\n\t\t\t<th class="datepicker-th">Th</th>\n\t\t\t<th class="datepicker-th">Fr</th>'
             '\n\t\t\t<th class="datepicker-th">Sa</th>\n\t\t\t<th class="datepicker-th">Su</th>'
             '\n\t\t</tr>\n\t</thead>\n\t<tbody class="datepicker-body">'.format(ny, nm))

    # start_date = datetime.date.fromisoformat('{0}-{1:0>2}-{2:0>2}'.format(date.year, date.month, 1))
    # end_date = datetime.date.fromisoformat('{0}-{1:0>2}-{2:0>2}'.format(date.year, date.month, max(matrix_c[-1])))
    # query = Match.objects.filter(created_at__date__range=(start_date, end_date))
    for weak in range(len(matrix)):
        s.append('\t\t<tr>')
        for day in range(7):
            if matrix_c[weak][day] == 0:
                tag = 'datepicker-td off'
            else:
                tag = 'datepicker-td'
            if (matrix_c[weak][day] == datetime.datetime.now().day) \
                    and (date.month == datetime.datetime.now().month) and (date.year == datetime.datetime.now().year):
                tag = 'datepicker-td today'
            query = Match.objects.filter(date__year=date.year, date__month=date.month, date__day=matrix_c[weak][day])
            if query:
                tag = 'datepicker-td act'
                for item in query:
                    if d:
                        if int(d) == matrix_c[weak][day]:
                            sm.append('<li class="cart-item">\n\t<span class="cart-item-pic">'
                                      '\t\t<img src="/static/media/{}">'.format(item.poster))
                            sm.append('\t</span><a href="/info/?id={}">{}</a>'.format(item.pk, item.title))
                            sm.append('<span class="cart-item-desc">{}</span>'.format(item.date))
                            sm.append('<span class="cart-item-price">{}</span>'.format(item.location))
                            sm.append('</li>')
                            break
                    else:
                        sm.append('<li class="cart-item">\n\t<span class="cart-item-pic">'
                                  '\t\t<img src="/static/media/{}">'.format(item.poster))
                        sm.append('\t</span><a href="/info/?id={}">{}</a>'.format(item.pk, item.title))
                        sm.append('<span class="cart-item-desc">{}</span>'.format(item.date))
                        sm.append('<span class="cart-item-price">{}</span>'.format(item.location))
                        sm.append('</li>')
            s.append('\t\t\t<td class="{0}"><a href="?year={1}&month={2}&day={3}">{3}</a></td>'.format(tag, date.year,
                                                                                                       date.month,
                                                                                                       matrix[weak][day]))
        s.append('\t\t</tr>')
    s.append('\t</tbody>\n</table>')
    cal = "\n".join(s)
    lst = "\n".join(sm)
    return cal, lst


def get_matches(user_id):
    matches = Match.objects.filter(owner_id=user_id)
    sm = []
    for item in matches:
        sm.append('<li class="cart-item">\n\t<span class="cart-item-pic">'
                  '\t\t<img src="/static/media/{}">'.format(item.poster))
        sm.append('\t</span><a href="/info/?id={}">{}</a>'.format(item.pk, item.title))
        sm.append('<span class="cart-item-desc">{}</span>'.format(item.date))
        sm.append('<span class="cart-item-price">{}</span>'.format(item.location))
        sm.append('</li>')
    lst = "\n".join(sm)
    return lst


def get_menu(request):
    auth = request.user.is_authenticated
    s = []
    if auth:
        s.append('<a href="/accounts/logout/" class="button">Выйти</a>')
        s.append('<a href="/dashboard/matches/" class="button">Мои турниры</a>')
        s.append('<form action="/dashboard/match/" method="post">')
        s.append('<input type="hidden" name="csrfmiddlewaretoken" value="{}">'.format(csrf.get_token(request)))
        s.append('<input type="hidden" name="selector" value="add_match">')
        s.append('<input type="submit" class="btn" id="go_to_match" value="Создать турнир">')
        s.append('</form>')
        # s.append('<a href="/dashboard/matches/" class="button">Создать турнир</a>')
    else:
        s.append('<a href="/accounts/login/" class="button">Войти</a>')
    s.append('<a href="/accounts/login/" class="button">Рейтинги</a>')
    s.append('<a href="/members/" class="button">Спортсмены</a>')
    s.append('<a href="/accounts/login/" class="button">Организаторы</a>')
    s.append('<a href="/accounts/login/" class="button">Клубы</a>')
    s.append('<a href="/" class="button">Главная</a>')
    # s.append('')
    result = "\n".join(s)
    return result


def get_menu_cat(match_id, request):
    user_id = request.user.id
    owner_id = Match.objects.get(pk=match_id).owner_id
    s = []
    if user_id == owner_id:
        s.append('<form method="post" action="/dashboard/match/">')
        s.append('<input type="hidden" name="csrfmiddlewaretoken" value="{}">'.format(csrf.get_token(request)))
        s.append('<input type="hidden" name="selector" value="add_category" />')
        s.append('<input type="hidden" name="match_id" value={} />'.format(match_id))
        s.append('<input type="submit" id="go_to_match"  value="Добавить категорию" />')
        s.append('</form>')
        s.append('<form method="post" action="/dashboard/match/">')
        s.append('<input type="hidden" name="csrfmiddlewaretoken" value="{}">'.format(csrf.get_token(request)))
        s.append('<input type="hidden" name="selector" value="start_match" />')
        # s.append('<input type="hidden" name="hand" value="2" />')
        s.append('<input type="hidden" name="match_id" value={} />'.format(match_id))
        s.append('<input type="submit" id="go_to_match"  value="Турнир" />')
        s.append('</form>')
        s.append('</form>')
        s.append('<form method="post" action="/dashboard/match/">')
        s.append('<input type="hidden" name="csrfmiddlewaretoken" value="{}">'.format(csrf.get_token(request)))
        s.append('<input type="hidden" name="selector" value="reset_match" />')
        s.append('<input type="hidden" name="match_id" value={} />'.format(match_id))
        s.append('<input type="submit" id="go_to_match"  value="Сбросить турнир" />')
        s.append('</form>')
        s.append('<form method="post" action="/dashboard/match/">')
        s.append('<input type="hidden" name="csrfmiddlewaretoken" value="{}">'.format(csrf.get_token(request)))
        s.append('<input type="hidden" name="selector" value="set_weight" />')
        s.append('<input type="hidden" name="match_id" value={} />'.format(match_id))
        s.append('<input type="submit" id="go_to_match"  value="Взвешивание" />')
        s.append('</form>')
    s.append('<form method="post" action="/dashboard/match/">')
    s.append('<input type="hidden" name="csrfmiddlewaretoken" value="{}">'.format(csrf.get_token(request)))
    s.append('<input type="hidden" name="selector" value="start_lists" />')
    s.append('<input type="hidden" name="match_id" value={} />'.format(match_id))
    s.append('<input type="submit" id="go_to_match"  value="Стартовые списки" />')
    s.append('</form>')
    s.append('<form method="post" action="/dashboard/match/">')
    s.append('<input type="hidden" name="csrfmiddlewaretoken" value="{}">'.format(csrf.get_token(request)))
    s.append('<input type="hidden" name="selector" value="table_list" />')
    s.append('<input type="hidden" name="match_id" value={} />'.format(match_id))
    s.append('<input type="submit" id="go_to_match"  value="Табло онлайн" />')
    s.append('</form>')
    result = "\n".join(s)
    return result


def get_match_list(match_id, category_id):  # если указан только category_id выводим только категорию иначе все категории
    if category_id:
        cats = MemberCats.objects.filter(pk=category_id)
    elif match_id:
        cats = MemberCats.objects.filter(match_id=match_id).order_by("table")
    else:
        return ObjectDoesNotExist
    s = []
    for category in cats:
        if category.hand == '1':
            hand = 'правая рука'
        else:
            hand = 'левая рука'
        members = StartLists.objects.filter(category_id=category.pk).order_by("category_id", "place", "position")
        if category_id:  # если выводим одну категорию, это для показа стола добавляем фото участников
            s.append('<div class="add_category">')
            s.append('<div class="profile"><div class="member_pic">')
            s.append('<img src="/static/media/{}" class="img-circle member_img"></div>'.format(
                Members.objects.get(pk=members[0].member_id).photo))
            s.append('<div class="member_pic">')
            s.append('<img src="/static/media/{}" class="img-circle member_img"></div>'.format(
                Members.objects.get(pk=members[1].member_id).photo))
            s.append('</div></div>')
        s.append('<div class="add_category">')
        s.append('<table class="tab_group">\n\t<tbody>\n\t\t<tr class="row_cat">\n\t\t\t<th colspan="4">'
                 'Категория: {} {} {}'.format(category.age_category, category.weight_category, hand))
        if category.table:
            s.append('<a href="/dashboard/table/?id={}">( Стол:{} )</a>'.format(category.pk, category.table))
        s.append('</th></tr>')
        if category.min == 1:
            s.append('<tr class="row_cat"><th colspan="4" class="coll_field">Полуфинал</th></tr>')
        elif category.min == 2:
            s.append('<tr class="row_cat"><th colspan="4" class="coll_field">Финал</th></tr>')
        elif category.min == 3:
            s.append('<tr class="row_cat"><th colspan="4" class="coll_field">Суперфинал</th></tr>')
        elif category.min == 4:
            s.append('<tr class="row_cat"><th colspan="4" class="coll_field">Результаты</th></tr>')
        s.append('</tbody></table></div>')
        s.append('<div class="add_category">')
        s.append('<table class="tab_group">\n\t<tbody>')
        for item in members:
            member = Members.objects.get(pk=item.member_id)
            parity = item.position % 2
            if item.loses < 2:
                if parity:
                    s.append('<tr class="row_member">')
                    if item.loses == 0:
                        if category.min == 4:  # выводим победителя соревнований
                            s.append('<td class="coll_min">1 место</td>')
                            s.append('<td colspan="2" class="coll_name">{} {} {}</td>'.format(
                                member.surname, member.name, member.second_name))
                            s.append('<td class="coll_min">{}/{}</td>'.format(
                                item.win, item.loses))
                            continue
                        else:
                            s.append('<td class="coll_min">А</td>')
                    if item.loses == 1:
                        if category.min == 4:  # выводим победителя соревнований
                            s.append('<td class="coll_min">1 место</td>')
                            s.append('<td colspan="2" class="coll_name">{} {} {}</td>'.format(
                                member.surname, member.name, member.second_name))
                            s.append('<td class="coll_min">{}/{}</td>'.format(
                                item.win, item.loses))
                            continue
                        else:
                            s.append('<td class="coll_min">B</td>')
                    s.append('<td class="coll_name">{} {} {}</td>'.format(member.surname, member.name, member.second_name))
                else:
                    s.append('<td class="coll_name">{} {} {}</td>'.format(member.surname, member.name, member.second_name))
                    if item.loses == 0:
                        s.append('<td class="coll_min">А</td>')
                    if item.loses == 1:
                        s.append('<td class="coll_min">B</td>')
                    s.append('</tr>')
            else:  # закончившие турнир
                s.append('<tr class="row_member"><td class="coll_min">{} место</td>'.format(item.place))
                s.append('<td colspan="2" class="coll_name">{} {} {}</td>'.format(
                    member.surname, member.name, member.second_name))
                s.append('<td class="coll_min">{}/{}</td></tr>'.format(
                    item.win, item.loses))
        s.append('</tbody></table></div>')

    result = "\n".join(s)
    return result


def get_tables(user_id, match_id, token):  # TODO: тут расчитывается вывод проведения поединков
    owner_id = Match.objects.get(pk=match_id).owner_id
    cats = MemberCats.objects.filter(match_id=match_id).order_by("hand", "table")
    # cats = MemberCats.objects.filter(match_id=match_id).order_by('hand', 'weight_category')
    s = []
    for category in cats:
        members = StartLists.objects.filter(category_id=category.pk).order_by("category_id", "place", "position")
        if category.hand == '1':
            h = 'правая рука'
        else:
            h = 'левая рука'
        s.append('<div class="add_category">')
        s.append('<table class="tab_group">\n\t<tbody>\n\t\t<tr class="row_cat">\n\t\t\t<th colspan="4">'
                 'Категория: {} {} {} ({})</th>'.format(category.age_category, category.weight_category,
                                                        category.group_category, h))
        s.append('</tr>')
        if category.min == 1:
            s.append('<tr class="row_cat"><th colspan="4" class="coll_field">Полуфинал</th></tr>')
        elif category.min == 2:
            s.append('<tr class="row_cat"><th colspan="4" class="coll_field">Финал</th></tr>')
        elif category.min == 3:
            s.append('<tr class="row_cat"><th colspan="4" class="coll_field">Суперфинал</th></tr>')
        elif category.min == 4:
            s.append('<tr class="row_cat"><th colspan="4" class="coll_field">Результаты (победы/поражения)</th></tr>')
        if (user_id == owner_id) and (category.min < 4):
            s.append('<tr class="row_cat">')
            s.append('\t\t\t<td class="coll_min">')
            if members.count() > 0:
                s.append('<form method="post" action="/dashboard/match/" id="{}_{}">'.format(category.pk, members[0].pk))
                s.append('<input type="hidden" name="csrfmiddlewaretoken" value="{}">'.format(token))
                s.append('<input type="hidden" name="selector" value="winner_category" />')
                s.append('<input type="hidden" name="winner_id" value={} />'.format(members[0].member_id))
                s.append('<input type="hidden" name="category_id" value={} />'.format(category.pk))
                s.append('<input type="hidden" name="match_id" value={} />'.format(match_id))
                s.append('</form>')
                s.append('<button id="{}_{}" class="button">Победил</button>'.format(category.pk, members[0].pk))
                s.append('\t\t\t</td>')
            s.append('<td colspan="2"></td>')
            s.append('\t\t\t<td class="coll_min">')
            if members.count() > 1:
                s.append('<form method="post" action="/dashboard/match/" id="{}_{}">'.format(category.pk, members[1].pk))
                s.append('<input type="hidden" name="csrfmiddlewaretoken" value="{}">'.format(token))
                s.append('<input type="hidden" name="selector" value="winner_category" />')
                s.append('<input type="hidden" name="winner_id" value={} />'.format(members[1].member_id))
                s.append('<input type="hidden" name="category_id" value={} />'.format(category.pk))
                s.append('<input type="hidden" name="match_id" value={} />'.format(match_id))
                s.append('</form>\n')
                s.append('<button id="{}_{}" class="button">Победил</button>'.format(category.pk, members[1].pk))
                s.append('\t\t\t</td></tr>')
            s.append('</tbody></table></div>')
            s.append('<div class="add_category">')
            s.append('<table class="tab_group">\n\t<tbody>')
        for member in members:
            m = Members.objects.get(pk=member.member_id)
            parity = member.position % 2
            if member.loses < 2:  # если спортсмен еще участвует в соревновании
                if parity:  # если у спортсмена нечетный номер в position
                    s.append('<tr class="row_member">')
                    if member.loses == 0:  # если у спортсмена нет поражений
                        if category.min == 4:  # если результат выводим победителя соревнований
                            s.append('<td class="coll_min">1 место</td>')
                            s.append('<td colspan="2" class="coll_name">{} {} {}</td>'.format(
                                m.surname, m.name, m.second_name))
                            s.append('<td class="coll_min">{}/{}</td>'.format(
                                member.win, member.loses))
                            continue
                        else:  # если нет поражений но соревнование продолжается то спортсмен в группе А
                            s.append('<td class="coll_min">А</td>')
                    if member.loses == 1:  # если у спортсмена 1 поражение
                        if category.min == 4:  # если результат выводим победителя соревнований
                            s.append('<td class="coll_min">1 место</td>')
                            s.append('<td colspan="2" class="coll_name">{} {} {}</td>'.format(
                                m.surname, m.name, m.second_name))
                            s.append('<td class="coll_min">{}/{}</td>'.format(
                                member.win, member.loses))
                            continue
                        else:  # если 1 поражение и соревнование продолжается то спортсмен в группе В
                            s.append('<td class="coll_min">B</td>')
                    s.append('<td class="coll_name">{} {} {}</td>'.format(m.surname, m.name, m.second_name))
                else:
                    s.append('<td class="coll_name">{} {} {}</td>'.format(m.surname, m.name, m.second_name))
                    if member.loses == 0:
                        s.append('<td class="coll_min">А</td>')
                    if member.loses == 1:
                        s.append('<td class="coll_min">B</td>')
                    s.append('</tr>')
            else:
                s.append('<tr class="row_member"><td class="coll_min">{} место</td>'.format(member.place))
                s.append('<td colspan="2" class="coll_name">{} {} {}</td>'.format(
                    m.surname, m.name, m.second_name))
                s.append('<td class="coll_min">{}/{}</td></tr>'.format(
                    member.win, member.loses))

        s.append('</tbody></table></div>')
    lst = "\n".join(s)
    return lst


def get_list(match_id, request):
    user_id = request.user.id
    owner_id = Match.objects.get(pk=match_id).owner_id
    s = []
    categories = MemberCats.objects.filter(match_id=match_id)
    for category in categories:
        members = StartLists.objects.filter(category_id=category.pk)
        if category.hand == '1':
            hand = 'правая рука'
        else:
            hand = 'левая рука'
        s.append('<div class="add_category">')
        s.append('<table class="tab_group">\n\t<tbody>\n\t\t<tr class="row_cat">\n\t\t\t<th colspan="3">'
                 'Категория: {} {} {} ({})</th>'.format(category.age_category, category.weight_category,
                                                        category.group_category, hand))
        if user_id == owner_id:
            s.append('\t\t\t<td class="coll_button">')
            s.append('<form method="post" action="/dashboard/match/">')
            s.append('<input type="hidden" name="csrfmiddlewaretoken" value="{}">'.format(csrf.get_token(request)))
            s.append('<input type="hidden" name="selector" value="delete_category" />')
            s.append('<input type="hidden" name="category_id" value={} />'.format(category.pk))
            s.append('<input type="hidden" name="match_id" value={} />'.format(match_id))
            s.append('<input type="submit" id="row_cat"  value="Удалить категорию" />')
            s.append('</form>\n\t\t\t</td>')
            s.append('\t\t\t<td class="coll_button">')
            s.append('<form method="post" action="/dashboard/match/">')
            s.append('<input type="hidden" name="csrfmiddlewaretoken" value="{}">'.format(csrf.get_token(request)))
            s.append('<input type="hidden" name="selector" value="add_member" />')
            s.append('<input type="hidden" name="category_id" value={} />'.format(category.pk))
            s.append('<input type="hidden" name="match_id" value={} />'.format(match_id))
            s.append('<input type="submit" id="row_cat"  value="Добавить участника" />')
            s.append('</form>\n\t\t\t</td>')
        s.append('</tr>')
        s.append('</tbody></table></div>')
        s.append('<table class="tab_group">\n\t<tbody>')
        s.append('<tr class="row_header">')
        s.append('\t<th class="coll_field">Фамилия, Имя, Отчество</th>')
        s.append('\t<th class="coll_field">Спортивное звание</th>')
        s.append('\t<th class="coll_field">Дата рождения</th>')
        s.append('\t<th class="coll_field">Федеральный округ</th>')
        s.append('\t<th class="coll_field">Команда</th>')
        s.append('\t<th class="coll_field">Вес</th>')
        s.append('\t<th class="coll_field" colspan=2></th>')
        s.append('</tr>')
        for member in members:
            try:  # есть ли спортсмен
                m = Members.objects.get(pk=member.member_id)
            except ObjectDoesNotExist:  # если спортсмен был удален (но остался в списках, то удаляем его из списков)
                StartLists.objects.filter(member_id=member.member_id).delete()
                continue
            s.append('<tr class="row_member">')
            s.append('\t\t\t<td class="coll_name">{} {} {}</td>'.format(m.surname, m.name, m.second_name))
            s.append('\t\t\t<th class="coll_field">{}</th>'.format(m.rank))
            if m.birthday:
                s.append('\t\t\t<th class="coll_field">{}</th>'.format(m.birthday))
            else:
                s.append('\t\t\t<td class="coll_field"></td>')
            s.append('\t\t\t<th class="coll_name">{}</th>'.format(m.fo))
            s.append('\t\t\t<th class="coll_field">{}</th>'.format(m.team))
            if m.weight:
                s.append('\t\t\t<th class="coll_field">{}</th>'.format(m.weight))
            else:
                s.append('\t\t\t<th class="coll_field">-</th>')
            if user_id == owner_id:
                s.append('\t\t\t<td class="coll_button">')
                s.append('<form method="post" action="/dashboard/match/">')
                s.append('<input type="hidden" name="csrfmiddlewaretoken" value="{}">'.format(csrf.get_token(request)))
                s.append('<input type="hidden" name="selector" value="change_member" />')
                s.append('<input type="hidden" name="member_id" value={} />'.format(member.member_id))
                s.append('<input type="hidden" name="category_id" value={} />'.format(category.pk))
                s.append('<input type="hidden" name="match_id" value={} />'.format(match_id))
                s.append('<input type="submit" id="row_cat"  value="Изменить категорию" />')
                s.append('</form>\n\t\t\t</td>')
                s.append('\t\t\t<td class="coll_button">')
                s.append('<form method="post" action="/dashboard/match/">')
                s.append('<input type="hidden" name="csrfmiddlewaretoken" value="{}">'.format(csrf.get_token(request)))
                s.append('<input type="hidden" name="selector" value="delete_member" />')
                s.append('<input type="hidden" name="member_id" value={} />'.format(member.member_id))
                s.append('<input type="hidden" name="category_id" value={} />'.format(category.pk))
                s.append('<input type="hidden" name="match_id" value={} />'.format(match_id))
                s.append('<input type="submit" id="row_cat"  value="Удалить участника" />')
                s.append('</form>\n\t\t\t</td>')
            s.append('</tr>')
        s.append('</tbody></table>')
    result = "\n".join(s)
    return result


def get_weight_list(user_id, match_id, token):
    s = []
    owner_id = Match.objects.get(pk=match_id).owner_id
    items = StartLists.objects.filter(match_id=match_id).order_by("fo")
    if user_id == owner_id:
        s.append('<table class="tab_group">\n\t<tbody>')
        s.append('<tr class="row_header">')
        s.append('\t<th class="coll_field">Фамилия, Имя, Отчество</th>')
        s.append('\t<th class="coll_field">Дата рождения</th>')
        s.append('\t<th class="coll_field">Федеральный округ</th>')
        s.append('\t<th class="coll_field">Вес</th>')
        s.append('\t<th class="coll_field"></th>')
        s.append('</tr>')
        for item in items:
            member = Members.objects.get(pk=item.member_id)
            s.append('<tr class="row_member">')
            s.append(
                '\t\t\t<td class="coll_name">{} {} {}</td>'.format(member.surname, member.name, member.second_name))
            if member.birthday:
                s.append('\t\t\t<th class="coll_field">{}</th>'.format(member.birthday))
            else:
                s.append('\t\t\t<td class="coll_field"></td>')
            s.append('\t\t\t<th class="coll_field">{}</th>'.format(member.fo))
            if member.weight:
                #     s.append('\t\t\t<th colspan="2" class="coll_field">{}</th>'.format(member.weight))
                s.append('\t\t\t<td class="coll_field">'
                         '<form id="weight_id_{1}">'
                         '<input type="number" name="weight" placeholder="{2}" step="0.01" min="0">'
                         '<input type="hidden" name="match_id" value="{0}">'
                         '<input type="hidden" name="member_id" value="{1}">'.format(match_id, member.pk, member.weight))
                s.append('<input type="hidden" name="csrfmiddlewaretoken" value="{}">'.format(token))
                s.append('</form>\n\t\t</td>')
                s.append('<td><button id="{}" class="button">Сохранить</button></td>'.format(member.pk))
            else:
                s.append('\t\t\t<td class="coll_field">'
                         '<form id="weight_id_{1}">'
                         '<input type="number" name="weight" placeholder="1.0" step="0.01" min="0">'
                         '<input type="hidden" name="match_id" value="{0}">'
                         '<input type="hidden" name="member_id" value="{1}">'.format(match_id, member.pk))
                s.append('<input type="hidden" name="csrfmiddlewaretoken" value="{}">'.format(token))
                s.append('</form>\n\t\t</td>')
                s.append('<td><button id="{}" class="button">Сохранить</button></td>'.format(member.pk))
            s.append('</tr>')
        s.append('</tbody></table>')
    result = "\n".join(s)
    return result


def get_header(user):
    s = []
    if user:
        s.append('<div class="header-login">Вы вошли как {0}</div>'.format(user))
    s.append('<div class="header-text">Система проведения турниров по армрестлингу</div>')
    result = "\n".join(s)
    return result


def get_match_info(match_id, user_id, request):
    s = []
    item = Match.objects.get(pk=match_id)
    s.append('<div class=cart>')
    s.append('\t\t<div class="cart-top"><h2 class="cart-top-title">{}</h2></div>'.format(item.title))
    s.append('<ul>\n<li class="cart-item"><span class="poster-item-pic">'
             '<img src="/static/media/{}">\n</span>'.format(item.poster))
    s.append('<span class="cart-item-desc">Дата проведения: {}</span>'.format(item.date))
    s.append('<span class="cart-item-desc">Регион: {}</span>'.format(item.fo))
    s.append('<span class="cart-item-desc">Место проведения: {}</span>'.format(item.location))
    s.append('<span class="cart-item-desc">Главный судья: {}</span>'.format(item.gj))
    s.append('<span class="cart-item-desc">Главный секретарь: {}</span>'.format(item.gs))
    if item.hands == '0':
        hands = 'Борьба на обоих руках'
    elif item.hands == '1':
        hands = 'Борьба на правой руке'
    else:
        hands = 'Борьба на левой руке'
    s.append('<span class="cart-item-desc">{}</span>'.format(hands))
    s.append('<span class="cart-item-desc">Количество столов: {}</span>'.format(item.table_count))
    s.append('<span class="cart-item-desc">Контакты: {}</span>'.format(item.contacts))
    s.append('<span class="cart-item-desc">Положение турнира: {}</span>'.format(item.gs))
    s.append('</li>\n</ul>')
    s.append('<form method="post" action="/dashboard/match/">')
    s.append('<input type="hidden" name="csrfmiddlewaretoken" value="{}">'.format(csrf.get_token(request)))
    s.append('<input type="hidden" name="match_id" value="{}">'.format(match_id))
    s.append('<input type="hidden" name="selector" value="start_lists">')
    s.append('<input type="submit" id="go_to_match" value="Стартовые списки">\n</form>')
    if item.owner_id == user_id:
        s.append('<form method="post" action="/dashboard/match/">')
        s.append('<input type="hidden" name="csrfmiddlewaretoken" value="{}">'.format(csrf.get_token(request)))
        s.append('<input type="hidden" name="selector" value="edit_match">')
        s.append('<input type="hidden" name="match_id" value="{}">'.format(match_id))
        s.append('<input type="submit" id="go_to_match" value="Редактировать">\n</form>')
        s.append('<form method="post" action="/dashboard/match/">')
        s.append('<input type="hidden" name="csrfmiddlewaretoken" value="{}">'.format(csrf.get_token(request)))
        s.append('<input type="hidden" name="match_id" value="{}">'.format(match_id))
        s.append('<input type="hidden" name="selector" value="delete_match">')
        s.append('<input type="submit" id="go_to_match" value="Удалить">\n</form>')
    s.append('</div>')

    match = "\n".join(s)
    return match


def get_annonce(date):
    sm = []
    end_date = datetime.date.fromisoformat('{0}-{1:0>2}-{2:0>2}'.format(date.year, 12, 31))
    query = Match.objects.filter(date__range=(date, end_date))
    # print(query.count())
    for item in query:
        sm.append('<li class="cart-item">\n\t<span class="cart-item-pic">'
                  '\t\t<img src="/static/media/{}">'.format(item.poster))
        sm.append('\t</span><a href="/info/?id={}">{}</a>'.format(item.pk, item.title))
        sm.append('<span class="cart-item-desc">{}</span>'.format(item.date))
        sm.append('<span class="cart-item-price">{}</span>'.format(item.location))
        sm.append('</li>')
    match = "\n".join(sm)
    return match

def index(request):  # точка входа в приложение, по результатам авторизации
    data = {}
    date = datetime.datetime.now()
    month = date.month
    user = None
    day = None
    if request.method == 'GET':
        month = request.GET.get("month", "")
        day = request.GET.get("day", "")
        year = request.GET.get("year", "")
        if year:
            if day:
                date = datetime.date.fromisoformat('{0}-{1:0>2}-{2:0>2}'.format(year, month, day))
            else:
                date = datetime.date.fromisoformat('{0}-{1:0>2}-{2:0>2}'.format(year, month, 1))
    if request.user.is_authenticated == True:
        user = request.user
        data['username'] = user
    data['header'] = get_header(user)
    cal, lst = get_calendar(date, day)
    data['calendar'] = cal
    data['matches'] = lst
    data['menu'] = get_menu(request)
    data['annonce'] = get_annonce(datetime.datetime.now())
    if month:
        data['month_name'] = 'Турниры за {}'.format(month_name(int(month), 'ru'))
    return render(request, "pages/index.html", context=data)


def info(request):
    data = {}
    user_id = None
    if request.user.is_authenticated == True:
        user = request.user
        user_id = request.user.id
        data['username'] = user
        data['header'] = get_header(user)
    data['menu'] = get_menu(request)
    if request.method == 'GET':
        match_id = request.GET.get("id", "")
        if match_id:
            match = get_match_info(match_id, user_id, request)
            data['match'] = match
            return render(request, "pages/match_info.html", context=data)
        else:
            return redirect("/")

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    user_id = request.user.id
                    matches = Match.objects.filter(owner_id=user_id, arch=0)
                    # return render(request, 'pages/dashboard.html', {"username": user, 'matches': matches})
                    return redirect("/")
                else:
                    return HttpResponse('Disabled pages')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})


def user_logout(request):
    return render(request, 'registration/logged_out.html')


def user_password_change(request):
    return render(request, 'registration/password_change_form.html')

def user_password_change_done(request):
    return render(request, 'registration/password_change_done.html')

def user_password_reset(request):
    return render(request, 'registration/password_reset_form.html')

def user_password_reset_done(request):
    return render(request, 'registration/password_reset_done.html')

def password_reset_confirm(request):
    return render(request, 'registration/password_reset_confirm.html')

def password_reset_done(request):
    return render(request, 'registration/password_reset_done.html')


def user_registration(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            return render(request, 'registration/login.html', {})
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})


def show_match_list(request):
    if request.user.is_authenticated:
        user = request.user
        data = {}
        if user:
            if user.is_active:
                login(request, user)
                user_id = request.user.id
                data['header'] = get_header(user)
                data['menu'] = get_menu(request)
                data['page_name'] = 'Мои турниры'
                data['matches'] = get_matches(user_id)
            return render(request, 'pages/dashboard.html', context=data)
    return render(request, 'pages/index.html', {})


def match(request):
    data = {}
    user_id = None
    user = None
    if request.user.is_authenticated:
        user = request.user
        user_id = request.user.id
    data['header'] = get_header(user)
    data['menu'] = get_menu(request)

    if request.method == 'GET':  # редирект
        match_id = request.GET.get("id")
        if match_id:
            data['start_list'] = get_list(match_id, request)
            data['menu_cat'] = get_menu_cat(match_id, request)
            query = Match.objects.get(pk=match_id)
            data['title'] = query.title

    if request.method == 'POST':
        # form = ScoreForm(request.POST) # заполнить форму данными
        action = request.POST.get("selector", "Undefined")
        match_id = request.POST.get("match_id")
        if match_id:
            query = Match.objects.get(pk=match_id)
            data['title'] = query.title
            data['date'] = query.date
            data['menu_cat'] = get_menu_cat(match_id, request)
        else:  # если редирект то возвращаем стартовые списки
            pass
        if action == 'edit_match':
            match = Match.objects.get(pk=match_id)
            form = ScoreForm(initial={'title': match.title, 'location': match.location, 'fo': match.fo,
                                     'date': '{0}-{1:0>2}-{2:0>2}'.format(match.date.year, match.date.month, match.date.day),
                                     'gj': match.gj, 'gs': match.gs, 'table_count': match.table_count,
                                     'contacts': match.contacts, 'hands': match.hands, 'poster': match.poster})
            form.match_id = match.pk
            form.owner_id = match.owner_id
            data['edit_form'] = form
            data['match_id'] = match_id
            return render(request, 'pages/edit_match.html', context=data)

        if action == 'update_match':
            user_id = request.user.id
            instance = get_object_or_404(Match, id=match_id)
            form = ScoreForm(request.POST or None, request.FILES, instance=instance)
            if form.is_valid():
                form.match_id = match_id
                form.owner_id = user_id
                form.save()
            return redirect('/info/?id={}'.format(match_id))

        if action == 'add_match':
            form = ScoreForm()
            data['score_form'] = form
            return render(request, 'pages/match.html', context=data)

        if action == 'set_match':
            user_id = request.user.id  # id пользователя организатора соревнования
            form = ScoreForm(request.POST, request.FILES)
            form.match_id = match_id
            form.owner_id = user_id
            if form.is_valid():
                last = form.save()
                return redirect('/info/?id={}'.format(last.pk))
            return redirect(request.path)

        if action == 'reset_match':  # сброс турнира
            if match_id:
                MemberCats.objects.filter(match_id=match_id).update(started=False, table=None)
                StartLists.objects.filter(match_id=match_id).update(place=0, position=0, round=0, loses=0, win=0, pair=None)
                data['start_list'] = get_list(match_id, request)

        if action == 'delete_match':  # удаление турнира
            if match_id:
                Match.objects.filter(id=match_id).delete()
                MatchHistory.objects.filter(match=match_id).delete()
            return redirect('/')

        if action == 'add_category':  # добавление категории
            form = CategoryForm()
            data['category_form'] = form

        if action == 'set_category':
            form = CategoryForm(request.POST, request.FILES)
            form.match_id = match_id
            if form.is_valid():
                form.save()
            data['start_list'] = get_list(match_id, request)
            return redirect("/dashboard/match/?id={}".format(match_id))

        if action == 'delete_category':  # удаление категории
            category_id = request.POST.get('category_id')
            MemberCats.objects.filter(pk=category_id).delete()
            data['start_list'] = get_list(match_id, request)
            MatchHistory.objects.filter(category=category_id).delete()

        if action == 'add_member':
            form = MembersForm()
            data['category_id'] = request.POST.get('category_id')
            data['match_id'] = request.POST.get('match_id')
            data['members_form'] = form
            return render(request, 'pages/add_member.html', context=data)

        if action == 'set_member':
            category_id = request.POST.get('category_id')
            form = MembersForm(request.POST, request.FILES)
            form.match_id = match_id
            form.category_id = category_id
            if form.is_valid():
                just_created = form.save()
                StartLists.objects.create(member_id=just_created.id, category_id=category_id, match_id=match_id,
                                          fo=just_created.fo)
            data['start_list'] = get_list(match_id, request)

        if action == 'start_lists':
            data['start_list'] = get_list(match_id, request)

        if action == 'delete_sportsmen':
            if request.user.is_superuser:
                member_id = request.POST.get("member_id", "0")
                if member_id:
                    Members.objects.filter(pk=member_id).delete()
            return redirect(request.path)

        if action == 'delete_member':  # удалить участника из категории
            owner_id = Match.objects.get(pk=match_id).owner_id
            if request.user.id == owner_id:
                member_id = request.POST.get("member_id", "0")
                category_id = request.POST.get("category_id", "0")
                data['match_id'] = match_id
                if member_id:
                    # Members.objects.filter(pk=member_id).delete()
                    StartLists.objects.filter(category_id=category_id, member_id=member_id).delete()
            data['start_list'] = get_list(match_id, request)
            return redirect('/dashboard/match/?id={}'.format(match_id))

        if action == 'change_member':  # изменить категорию у участника
            member_id = request.POST.get("member_id", "0")
            category_id = request.POST.get("category_id", "0")
            data['member_item'] = Members.objects.get(pk=member_id)
            data['member'] = StartLists.objects.get(category_id=category_id, member_id=member_id)
            data['new_categories'] = MemberCats.objects.filter(match_id=match_id)
            data['category_id'] = category_id

        if action == 'new_category':
            member_id = request.POST.get("member_id", "0")
            category_id = request.POST.get("category_id", "0")
            StartLists.objects.filter(pk=member_id).update(category_id=category_id)
            data['start_list'] = get_list(match_id, request)

        if action == 'to_score':
            return redirect('/dashboard/tables/')

        if action == 'start_match':
            cats = MemberCats.objects.filter(match_id=match_id).order_by('hand', 'weight_category')  # Список категорий
            count = Match.objects.get(pk=match_id).table_count  # Количество столов в турнире
            table = 1
            for cat in cats:  # для каждой категории
                if not cat.started:  # если жеребьевка еще не проводилась
                    MemberCats.objects.filter(pk=cat.pk).update(table=table, started=True, min=0)  # Определяем стол для категории
                    table = table + 1
                    if table > count:
                        count = 1
                    list_id = list(StartLists.objects.filter(category_id=cat.pk).values_list("id", flat=True))  # id участников в категории
                    random.shuffle(list_id)  # перемешиваем для жеребьевки
                    position = 1
                    while list_id:  # жеребьевка для категории, кому не хватило пары уходит в тур 2 с одной победой
                        m_id = list_id.pop(0)
                        if list_id:
                            p_id = list_id.pop(0)
                            p_mem = StartLists.objects.get(pk=p_id).member_id
                            m_mem = StartLists.objects.get(pk=m_id).member_id
                            StartLists.objects.filter(pk=m_id).update(round=1, loses=0, win=0, position=position,
                                                                      pair=p_mem, place=0) #TODO переделать pair
                            position = position + 1
                            StartLists.objects.filter(pk=p_id).update(round=1, loses=0, win=0, position=position,
                                                                      pair=m_mem, place=0)
                            position = position + 1
                        else:
                            StartLists.objects.filter(pk=m_id).update(round=2, loses=0, win=1, position=position,
                                                                      pair=None, place=0)
            data['start_list'] = get_tables(user_id, match_id, csrf.get_token(request))
            data['match_id'] = match_id

        if action == 'set_weight':
            data['weight_list'] = get_weight_list(user_id, match_id, csrf.get_token(request))
            return render(request, 'pages/weights.html', context=data)

        if action == 'table_list':
            data['match_list'] = get_match_list(match_id, None)
            return render(request, 'pages/tables.html', context=data)

    if match_id:
        data['match_id'] = match_id
        return render(request, 'pages/match.html', context=data)  #
    else:
        return render(request, 'pages/dashboard.html', context=data)



def one_table(request):
    data = {}
    category_id = request.GET.get("id")
    data['members'] = get_match_list(match_id=None, category_id=category_id)
    return render(request, 'pages/table.html', context=data)


def select_user(request):
    if request.user.is_authenticated:
        data = {}
        user = request.user
        member_id = request.POST.get("member_id")
        category_id = request.POST.get("category_id")
        match_id = request.POST.get("match_id")
        fo = Members.objects.get(pk=member_id).fo
        order = StartLists.objects.filter(match_id=match_id, category_id=category_id, member_id=member_id, fo=fo)
        if not order:  # если мы не ошиблись и не пытаемся добавить спортсмена еще раз в категорию
            query = StartLists(match_id=match_id, category_id=category_id, member_id=member_id, fo=fo)
            query.save()
            Members.objects.filter(pk=member_id).update(weight=0)  # Обнуляем вес участника
        query = Match.objects.get(pk=match_id)
        data['title'] = query.title
        data['date'] = query.date
        data['start_list'] = get_list(match_id, request)
        data['match_id'] = match_id
        data['header'] = get_header(user)
        data['menu'] = get_menu(request)
        data['menu_cat'] = get_menu_cat(match_id, request)
        return render(request, 'pages/match.html', context=data)
    else:
        return redirect('/')

def show_members(request):
    member_id = None
    if request.method == 'POST':
        member_id = request.POST.get("member_id")
    if request.method == 'GET':
        member_id = request.GET.get("id")
    data = {}
    s = []
    data['menu'] = get_menu(request)
    if not member_id:
        s.append('<table class="tab_group">\n\t<tbody>')
        s.append('<tr class="row_header">')
        s.append('\t<th class="coll_field">Фамилия, Имя, Отчество</th>')
        s.append('\t<th class="coll_field">Дата рождения</th>')
        s.append('\t<th class="coll_field">Субъект РФ</th>')
        s.append('\t<th class="coll_field">Спортивное звание</th>')
        s.append('\t<th class="coll_field"></th>')
        s.append('</tr>')
        items = Members.objects.filter().order_by('surname')
        for member in items:
            s.append('<tr class="row_member">')
            s.append(
                '\t\t\t<td class="coll_name">{} {} {}</td>'.format(member.surname, member.name, member.second_name))
            if member.birthday:
                s.append('\t\t\t<th class="coll_field">{}</th>'.format(member.birthday))
            else:
                s.append('\t\t\t<td class="coll_field"></td>')
            s.append('\t\t\t<th class="coll_field">{}</th>'.format(member.rank))
            s.append('\t\t\t<th class="coll_name">{}</th>'.format(member.fo))

            s.append('\t\t\t<td class="coll_field">'
                     '<form method="post" action="/members/">'
                     '<input type="hidden" name="member_id" value="{}">'.format(member.pk))
            s.append('<input type="hidden" name="csrfmiddlewaretoken" value="{}">'.format(csrf.get_token(request)))
            s.append('<input type="submit" class="btn" id="go_to_match" value="Перейти">')
            s.append('</form>\n\t\t</td>')
            s.append('</tr>')
        s.append('</tbody></table>')
        data['members'] = "\n".join(s)
    else:
        member = Members.objects.get(pk=member_id)
        s.append('<div class=member-item>')
        s.append('<div class="profile"><div class="member_pic">')
        s.append('<img src="/static/media/{}"  class="img-circle member_img">'.format(member.photo))
        s.append('</div></div>')
        s.append('<span class="member-item-name">{} {} {}</span>'.format(member.surname, member.name, member. second_name))
        s.append('<span class="member-item-birthday">дата рождения: {}</span>'.format(member.birthday))
        s.append('<span class="member-item-rank">Спортивное звание: {}</span>'.format(member.rank))
        s.append('<span class="member-item-fo">Субъект РФ: {}</span>'.format(member.fo))
        s.append('<span class="member-item-team">Выступает за команду: {}</span>'.format(member.team))
        s.append('<span class="member-item-tr">Тренируется у: {}</span>'.format(member.trener))
        if request.user.is_superuser:
            s.append('<form method="post" class="member-item-btn" enctype="multipart/form-data" action="/set_user_photo/">'
                     '<input type="hidden" name="member_id" value="{}">'.format(member.pk))
            s.append('<input type="hidden" name="csrfmiddlewaretoken" value="{}">'.format(csrf.get_token(request)))
            s.append('<input type="file" name="photo" accept="image/png, image/jpeg" />')
            s.append('<input type="submit" class="btn" id="go_to_match" value="Загрузить фото">')
            s.append('</form>')
            s.append(
                '<form method="post" class="member-item-btn2" enctype="multipart/form-data" action="/dashboard/match/">'
                '<input type="hidden" name="member_id" value="{}">'.format(member.pk))
            s.append('<input type="hidden" name="csrfmiddlewaretoken" value="{}">'.format(csrf.get_token(request)))
            s.append('<input type="hidden" name="selector" value="delete_sportsmen">')
            s.append('<input type="submit" class="btn" id="go_to_match" value="Удалить спортсмена">')
            s.append('</form>')
        s.append('</div>')
        s.append('<table class="tab_group">\n\t<tbody>')
        s.append('<tr class="row_header">')
        s.append('\t<th colspan="3" class="coll_field">Победил спортсменов:</th>')
        s.append('</tr>')
        items = MatchHistory.objects.filter(win_id=member_id)
        for item in items:
            member = Members.objects.get(pk=item.los_id)
            match = Match.objects.get(pk=item.match)
            s.append('<tr class="row_member">')
            s.append(
                '\t\t\t<td class="coll_name">{} {} {}</td>'.format(member.surname, member.name, member.second_name))
            s.append('\t\t\t<th class="coll_min">{}</th>'.format(member.rank))
            s.append('\t\t\t<td class="coll_name">{} {}</td>'.format(match.title, match.date))
            s.append('</tr>')
        s.append('</tbody></table>')
        s.append('<table class="tab_group">\n\t<tbody>')
        s.append('<tr class="row_header">')
        s.append('\t<th colspan="3" class="coll_field">Проиграл спортсменам:</th>')
        s.append('</tr>')
        items = MatchHistory.objects.filter(los_id=member_id)
        for item in items:
            member = Members.objects.get(pk=item.win_id)
            match = Match.objects.get(pk=item.match)
            s.append('<tr class="row_member">')
            s.append(
                '\t\t\t<td class="coll_name">{} {} {}</td>'.format(member.surname, member.name, member.second_name))
            s.append('\t\t\t<th class="coll_min">{}</th>'.format(member.rank))
            s.append('\t\t\t<td class="coll_name">{} {}</td>'.format(match.title, match.date))
            s.append('</tr>')
        s.append('</tbody></table>')
        data['member'] = "\n".join(s)
    return render(request, 'pages/member.html', context=data)


def set_user_photo(request):
    if request.method == 'POST' and request.FILES['photo']:
        file = request.FILES['photo']
        fss = FileSystemStorage()
        new_file = fss.save(file.name, file)
        file_url = fss.url(new_file)
        member_id = request.POST.get('member_id')
        upload_path = settings.MEDIA_ROOT + fss.url(file_url)
        img = Image.open(upload_path)
        width = img.width
        height = img.height
        max_size = max(width, height)
        if max_size > 256:
            output_size = (
                round(width / max_size * 256),  # Сохраняем пропорции
                round(height / max_size * 256))
            img.thumbnail(output_size)
            img.save(upload_path)
        Members.objects.filter(pk=member_id).update(photo=new_file)
    return redirect('/members/?id={}'.format(member_id))


