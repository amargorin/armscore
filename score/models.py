from django.db import models
from PIL import Image


class Hands(models.TextChoices):
    BOTH = "0", "Обе руки"
    RIGHT = "1", "Правая"
    LEFT = "2", "Левая"

class Hand(models.TextChoices):
    RIGHT = "1", "Правая"
    LEFT = "2", "Левая"

class FederalRegion(models.TextChoices):  # Федеральный округ
    fo1 = "1 - Республика Адыгея (Адыгея)", "1 - Республика Адыгея (Адыгея)"
    fo2 = "2 - Республика Башкортостан", "2 - Республика Башкортостан"
    fo3 = "3 - Республика Бурятия", "3 - Республика Бурятия"
    fo4 = "4 - Республика Алтай", "4 - Республика Алтай"
    fo5 = "5 - Республика Дагестан", "5 - Республика Дагестан"
    fo6 = "6 - Республика Ингушетия", "6 - Республика Ингушетия"
    fo7 = "7 - Кабардино-Балкарская Республика", "7 - Кабардино-Балкарская Республика"
    fo8 = "8 - Республика Калмыкия", "8 - Республика Калмыкия"
    fo9 = "9 - Карачаево-Черкесская Республика", "9 - Карачаево-Черкесская Республика"
    fo10 = "10 - Республика Карелия", "10 - Республика Карелия"
    fo11 = "11 - Республика Коми", "11 - Республика Коми"
    fo12 = "12 - Республика Марий Эл", "12 - Республика Марий Эл"
    fo13 = "13 - Республика Мордовия", "13 - Республика Мордовия"
    fo14 = "14 - Республика Саха (Якутия)", "14 - Республика Саха (Якутия)"
    fo15 = "15 - Республика Северная Осетия - Алания", "15 - Республика Северная Осетия - Алания"
    fo16 = "16 - Республика Татарстан (Татарстан)", "16 - Республика Татарстан (Татарстан)"
    fo17 = "17 - Республика Тыва", "17 - Республика Тыва"
    fo18 = "18 - Удмуртская Республика", "18 - Удмуртская Республика"
    fo19 = "19 - Республика Хакасия", "19 - Республика Хакасия"
    fo20 = "20 - Чеченская Республика", "20 - Чеченская Республика"
    fo21 = "21 - Чувашская Республика - Чувашия", "21 - Чувашская Республика - Чувашия"
    fo22 = "22 - Алтайский край", "22 - Алтайский край"
    fo23 = "23 - Краснодарский край", "23 - Краснодарский край"
    fo24 = "24 - Красноярский край", "24 - Красноярский край"
    fo25 = "25 - Приморский край", "25 - Приморский край"
    fo26 = "26 - Ставропольский край", "26 - Ставропольский край"
    fo27 = "27 - Хабаровский край", "27 - Хабаровский край"
    fo28 = "28 - Амурская область", "28 - Амурская область"
    fo29 = "29 - Архангельская область", "29 - Архангельская область"
    fo30 = "30 - Астраханская область", "30 - Астраханская область"
    fo31 = "31 - Белгородская область", "31 - Белгородская область"
    fo32 = "32 - Брянская область", "32 - Брянская область"
    fo33 = "33 - Владимирская область", "33 - Владимирская область"
    fo34 = "34 - Волгоградская область", "34 - Волгоградская область"
    fo35 = "35 - Вологодская область", "35 - Вологодская область"
    fo36 = "36 - Воронежская область", "36 - Воронежская область"
    fo37 = "37 - Ивановская область", "37 - Ивановская область"
    fo38 = "38 - Иркутская область", "38 - Иркутская область"
    fo39 = "39 - Калининградская область", "39 - Калининградская область"
    fo40 = "40 - Калужская область", "40 - Калужская область"
    fo41 = "41 - Камчатский край", "41 - Камчатский край"
    fo42 = "42 - Кемеровская область", "42 - Кемеровская область"
    fo43 = "43 - Кировская область", "43 - Кировская область"
    fo44 = "44 - Костромская область", "44 - Костромская область"
    fo45 = "45 - Курганская область", "45 - Курганская область"
    fo46 = "46 - Курская область", "46 - Курская область"
    fo47 = "47 - Ленинградская область", "47 - Ленинградская область"
    fo48 = "48 - Липецкая область", "48 - Липецкая область"
    fo49 = "49 - Магаданская область", "49 - Магаданская область"
    fo50 = "50 - Московская область", "50 - Московская область"
    fo51 = "51 - Мурманская область", "51 - Мурманская область"
    fo52 = "52 - Нижегородская область", "52 - Нижегородская область"
    fo53 = "53 - Новгородская область", "53 - Новгородская область"
    fo54 = "54 - Новосибирская область", "54 - Новосибирская область"
    fo55 = "55 - Омская область", "55 - Омская область"
    fo56 = "56 - Оренбургская область", "56 - Оренбургская область"
    fo57 = "57 - Орловская область", "57 - Орловская область"
    fo58 = "58 - Пензенская область", "58 - Пензенская область"
    fo59 = "59 - Пермский край", "59 - Пермский край"
    fo60 = "60 - Псковская область", "60 - Псковская область"
    fo61 = "61 - Ростовская область", "61 - Ростовская область"
    fo62 = "62 - Рязанская область", "62 - Рязанская область"
    fo63 = "63 - Самарская область", "63 - Самарская область"
    fo64 = "64 - Саратовская область", "64 - Саратовская область"
    fo65 = "65 - Сахалинская область", "65 - Сахалинская область"
    fo66 = "66 - Свердловская область", "66 - Свердловская область"
    fo67 = "67 - Смоленская область", "67 - Смоленская область"
    fo68 = "68 - Тамбовская область", "68 - Тамбовская область"
    fo69 = "69 - Тверская область", "69 - Тверская область"
    fo70 = "70 - Томская область", "70 - Томская область"
    fo71 = "71 - Тульская область", "71 - Тульская область"
    fo72 = "72 - Тюменская область", "72 - Тюменская область"
    fo73 = "73 - Ульяновская область", "73 - Ульяновская область"
    fo74 = "74 - Челябинская область", "74 - Челябинская область"
    fo75 = "75 - Забайкальский край", "75 - Забайкальский край"
    fo76 = "76 - Ярославская область", "76 - Ярославская область"
    fo77 = "77 - г. Москва", "77 - г. Москва"
    fo78 = "78 - Санкт-Петербург", "78 - Санкт-Петербург"
    fo79 = "79 - Еврейская автономная область", "79 - Еврейская автономная область"
    fo88 = "80 - Донецкая Народная Республика", "80 - Донецкая Народная Республика"
    fo89 = "81 - Луганская народная республика", "81 - Луганская народная республика"
    fo84 = "82 - Республика Крым", "82 - Республика Крым"
    fo80 = "83 - Ненецкий автономный округ", "83 - Ненецкий автономный округ"
    fo81 = "86 - ХМАО - Югра", "86 - ХМАО - Югра"
    fo82 = "87 - Чукотский автономный округ", "87 - Чукотский автономный округ"
    fo83 = "89 - Ямало-Ненецкий автономный округ", "89 - Ямало-Ненецкий автономный округ"
    fo85 = "92 - Севастополь", "92 - Севастополь"
    fo87 = "94 - Байконур", "94 - Байконур"
    fo86 = "99 - Иные территории, включая город и космодром Байконур", "99 - Иные территории, включая город и космодром Байконур"


class MemberCats(models.Model):
    class AgeCategory(models.TextChoices):  # возрастная категория
        MAN = "Мужчины", "Мужчины"
        WOM = "Женщины", "Женщины"
        JM1 = "Юниоры 19-21", "Юниоры 19-21"
        JW1 = "Юниорки 19-21", "Юниорки 19-21"
        JM2 = "Юниоры 16-18", "Юниоры 16-18"
        JW2 = "Юниорки 16-18", "Юниорки 16-18"
        JM3 = "Юноши 14-15", "Юноши 14-15"
        JW3 = "Девушки 14-15", "Девушки 14-15"
        MMA = "Мужчины Мастера 40+", "Мужчины Мастера 40+"
        WMA = "Женщины Мастера 40+", "Женщины Мастера 40+"
        MGM = "Мужчины Гранд мастера 50+", "Мужчины Гранд мастера 50+"
        WGM = "Женщины Гранд мастера 50+", "Женщины Гранд мастера 50+"
        MSG = "Мужчины Сеньор гранд мастера 60+", "Мужчины Сеньор гранд мастера 60+"
        WSG = "Женщины Сеньор гранд мастера 60+", "Женщины Сеньор гранд мастера 60+"


    class GroupCategory(models.TextChoices):  # категория групп участников
        GEN = "Общая", "Общая"
        NEW = "Любители", "Любители"
        PRO = "Профессионалы", "Профессионалы"
        INV = "Инвалиды", "Инвалиды"
        VIZ = "Инвалиды VIZ", "Инвалиды VIZ"
        STA = "Инвалиды STAND", "Инвалиды STAND"
        HEA = "Инвалиды HEAR", "Инвалиды HEAR"
        SIT = "Инвалиды SIT", "Инвалиды SIT"


    class WeightCategory(models.TextChoices):
        C55 = "55 КГ", "55 КГ"
        C60 = "60 КГ", "60 КГ"
        C65 = "65 КГ", "65 КГ"
        C70 = "70 КГ", "70 КГ"
        C75 = "75 КГ", "75 КГ"
        C80 = "80 КГ", "80 КГ"
        C85 = "85 КГ", "85 КГ"
        C90 = "90 КГ", "90 КГ"
        C10 = "100 КГ", "100 КГ"
        C11 = "110 КГ", "110 КГ"
        C12 = "110+ КГ", "110+ КГ"
        С13 = "Абсолютная", "Абсолютная"

    match_id = models.IntegerField(blank=True, null=True)
    age_category = models.CharField(max_length=40, choices=AgeCategory.choices, default=AgeCategory.MAN)
    group_category = models.CharField(max_length=40, choices=GroupCategory.choices, default=GroupCategory.GEN)
    weight_category = models.CharField(max_length=40, choices=WeightCategory.choices, default=WeightCategory.C55)
    hand = models.CharField(max_length=1, choices=Hand.choices, default=Hand.RIGHT)  # на какой руке категория
    table = models.IntegerField(blank=True, null=True)  # на каком столе будет проводиться данная категория
    started = models.BooleanField(default=False)  # Признак что соревнование начато и жеребьевка состоялась
    min = models.IntegerField(blank=True, null=True)  # определения полуфинала, финала и суперфинала, результат (1,2,3,4)


class Match(models.Model):  # Общая информация о турнире
    owner_id = models.IntegerField(blank=True, null=True)  # ид пользователя личного кабинета
    title = models.CharField(max_length=255)  # Название турнира
    location = models.CharField(max_length=255, null=True)  # Место проведения турнира
    fo = models.CharField(max_length=255, choices=FederalRegion.choices, default="77 - г. Москва")  # Федеральный округ РФ
    date = models.DateField(null=True)  # Дата проведения турнира
    gj = models.CharField(max_length=255, null=True)  # Главный судья
    gs = models.CharField(max_length=255, null=True)  # Главный секретарь
    table_count = models.IntegerField(blank=True, null=True)  # Количество столов для борьбы
    arch = models.BooleanField(default=False)  # признак закончившегося соревнования ( 0 = текущее, 1 = архивное)
    logo = models.ImageField(default='', null=True)  # логотип турнира
    current = models.IntegerField(blank=True, default=0)  # На какой руке прооходить матч 2 = на левой 1 =на правой
    hands = models.CharField(max_length=1, choices=Hands.choices, default=Hands.BOTH)  # на какой руке турнир
    contacts = models.CharField(max_length=255, null=True)  # Контактная информация
    poster = models.ImageField(default='default_poster.png', upload_to='')  # Афиша соревнования
    public = models.BooleanField(default=False)  # Признак анонсировать соревнование на главной странице

    def save(self):  # перекрываем метод для форматирования афиш турниров
        super().save()
        img = Image.open(self.poster.path)
        print(self.poster.path)
        width = img.width
        height = img.height
        max_size = max(width, height)
        if max_size > 256:
            output_size = (
                round(width / max_size * 256),  # Сохраняем пропорции
                round(height / max_size * 256))
            img.thumbnail(output_size)
            img.save(self.poster.path)


class StartLists(models.Model): # Стартовые списки
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    category = models.ForeignKey(MemberCats, on_delete=models.CASCADE, default=0)  # категория MembersCats.id
    # информация о спортсмене
    member_id = models.IntegerField(blank=True, default=0)  # id спортсмена Members
    place = models.IntegerField(blank=True, default=0)  # текущее место в категории
    fo = models.CharField(max_length=255, choices=FederalRegion.choices,
                          default="77 - г. Москва")  # Федеральный округ РФ
    # информация для расчета позиции участника при проведении соревнования
    position = models.IntegerField(blank=True, null=True, default=0)  # Позиция после жеребьевки и далее в туре
    round = models.IntegerField(blank=True, null=True, default=0)  # Текущий тур
    loses = models.IntegerField(blank=True, null=True, default=0)  # Количество поражений
    win = models.IntegerField(blank=True, null=True, default=0)  # Количество побед
    pair = models.IntegerField(blank=True, null=True, default=0)  # ид пары в текущем поединке


class Members(models.Model):
    name = models.CharField(max_length=25)  # Имя участника
    surname = models.CharField(max_length=25)  # Фамилия участника
    second_name = models.CharField(max_length=25, default='')  # Отчество участника
    weight = models.FloatField(default=0)  # собственный вес
    far_passport = models.CharField(max_length=30, default='')  # номер паспорта ФАР
    team = models.CharField(max_length=255, default='')  # Название команды
    rank = models.CharField(max_length=10, default='')  # спортивное звание.
    birthday = models.DateField(null=True)  # Дата рождения
    trener = models.CharField(max_length=255, default='')  # Тренер
    fo = models.CharField(max_length=255, choices=FederalRegion.choices,
                          default="77 - г. Москва")  # Федеральный округ РФ
    photo = models.ImageField(default='Man.png', upload_to='')  # фото участника


    def save(self):  # перекрываем метод для форматирования фотографий участников
        super().save()
        img = Image.open(self.photo.path)
        width = img.width
        height = img.height
        max_size = max(width, height)
        if max_size > 256:
            output_size = (
                round(width / max_size * 256),  # Сохраняем пропорции
                round(height / max_size * 256))
            img.thumbnail(output_size)
            img.save(self.photo.path)

class MatchHistory(models.Model):
    match = models.IntegerField(default=0)
    category = models.IntegerField(default=0)  # категория MembersCats.id
    win_id = models.IntegerField(default=0)  # Имя участника
    los_id = models.IntegerField(default=0)  # Имя участника
