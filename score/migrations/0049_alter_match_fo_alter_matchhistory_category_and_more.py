# Generated by Django 4.2.3 on 2023-10-02 13:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('score', '0048_remove_matchhistory_los_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='match',
            name='fo',
            field=models.CharField(choices=[('1 - Республика Адыгея (Адыгея)', '1 - Республика Адыгея (Адыгея)'), ('2 - Республика Башкортостан', '2 - Республика Башкортостан'), ('3 - Республика Бурятия', '3 - Республика Бурятия'), ('4 - Республика Алтай', '4 - Республика Алтай'), ('5 - Республика Дагестан', '5 - Республика Дагестан'), ('6 - Республика Ингушетия', '6 - Республика Ингушетия'), ('7 - Кабардино-Балкарская Республика', '7 - Кабардино-Балкарская Республика'), ('8 - Республика Калмыкия', '8 - Республика Калмыкия'), ('9 - Карачаево-Черкесская Республика', '9 - Карачаево-Черкесская Республика'), ('10 - Республика Карелия', '10 - Республика Карелия'), ('11 - Республика Коми', '11 - Республика Коми'), ('12 - Республика Марий Эл', '12 - Республика Марий Эл'), ('13 - Республика Мордовия', '13 - Республика Мордовия'), ('14 - Республика Саха (Якутия)', '14 - Республика Саха (Якутия)'), ('15 - Республика Северная Осетия - Алания', '15 - Республика Северная Осетия - Алания'), ('16 - Республика Татарстан (Татарстан)', '16 - Республика Татарстан (Татарстан)'), ('17 - Республика Тыва', '17 - Республика Тыва'), ('18 - Удмуртская Республика', '18 - Удмуртская Республика'), ('19 - Республика Хакасия', '19 - Республика Хакасия'), ('20 - Чеченская Республика', '20 - Чеченская Республика'), ('21 - Чувашская Республика - Чувашия', '21 - Чувашская Республика - Чувашия'), ('22 - Алтайский край', '22 - Алтайский край'), ('23 - Краснодарский край', '23 - Краснодарский край'), ('24 - Красноярский край', '24 - Красноярский край'), ('25 - Приморский край', '25 - Приморский край'), ('26 - Ставропольский край', '26 - Ставропольский край'), ('27 - Хабаровский край', '27 - Хабаровский край'), ('28 - Амурская область', '28 - Амурская область'), ('29 - Архангельская область', '29 - Архангельская область'), ('30 - Астраханская область', '30 - Астраханская область'), ('31 - Белгородская область', '31 - Белгородская область'), ('32 - Брянская область', '32 - Брянская область'), ('33 - Владимирская область', '33 - Владимирская область'), ('34 - Волгоградская область', '34 - Волгоградская область'), ('35 - Вологодская область', '35 - Вологодская область'), ('36 - Воронежская область', '36 - Воронежская область'), ('37 - Ивановская область', '37 - Ивановская область'), ('38 - Иркутская область', '38 - Иркутская область'), ('39 - Калининградская область', '39 - Калининградская область'), ('40 - Калужская область', '40 - Калужская область'), ('41 - Камчатский край', '41 - Камчатский край'), ('42 - Кемеровская область', '42 - Кемеровская область'), ('43 - Кировская область', '43 - Кировская область'), ('44 - Костромская область', '44 - Костромская область'), ('45 - Курганская область', '45 - Курганская область'), ('46 - Курская область', '46 - Курская область'), ('47 - Ленинградская область', '47 - Ленинградская область'), ('48 - Липецкая область', '48 - Липецкая область'), ('49 - Магаданская область', '49 - Магаданская область'), ('50 - Московская область', '50 - Московская область'), ('51 - Мурманская область', '51 - Мурманская область'), ('52 - Нижегородская область', '52 - Нижегородская область'), ('53 - Новгородская область', '53 - Новгородская область'), ('54 - Новосибирская область', '54 - Новосибирская область'), ('55 - Омская область', '55 - Омская область'), ('56 - Оренбургская область', '56 - Оренбургская область'), ('57 - Орловская область', '57 - Орловская область'), ('58 - Пензенская область', '58 - Пензенская область'), ('59 - Пермский край', '59 - Пермский край'), ('60 - Псковская область', '60 - Псковская область'), ('61 - Ростовская область', '61 - Ростовская область'), ('62 - Рязанская область', '62 - Рязанская область'), ('63 - Самарская область', '63 - Самарская область'), ('64 - Саратовская область', '64 - Саратовская область'), ('65 - Сахалинская область', '65 - Сахалинская область'), ('66 - Свердловская область', '66 - Свердловская область'), ('67 - Смоленская область', '67 - Смоленская область'), ('68 - Тамбовская область', '68 - Тамбовская область'), ('69 - Тверская область', '69 - Тверская область'), ('70 - Томская область', '70 - Томская область'), ('71 - Тульская область', '71 - Тульская область'), ('72 - Тюменская область', '72 - Тюменская область'), ('73 - Ульяновская область', '73 - Ульяновская область'), ('74 - Челябинская область', '74 - Челябинская область'), ('75 - Забайкальский край', '75 - Забайкальский край'), ('76 - Ярославская область', '76 - Ярославская область'), ('77 - г. Москва', '77 - г. Москва'), ('78 - Санкт-Петербург', '78 - Санкт-Петербург'), ('79 - Еврейская автономная область', '79 - Еврейская автономная область'), ('80 - Донецкая Народная Республика', '80 - Донецкая Народная Республика'), ('81 - Луганская народная республика', '81 - Луганская народная республика'), ('82 - Республика Крым', '82 - Республика Крым'), ('83 - Ненецкий автономный округ', '83 - Ненецкий автономный округ'), ('86 - ХМАО - Югра', '86 - ХМАО - Югра'), ('87 - Чукотский автономный округ', '87 - Чукотский автономный округ'), ('89 - Ямало-Ненецкий автономный округ', '89 - Ямало-Ненецкий автономный округ'), ('92 - Севастополь', '92 - Севастополь'), ('94 - Байконур', '94 - Байконур'), ('99 - Иные территории, включая город и космодром Байконур', '99 - Иные территории, включая город и космодром Байконур')], default='77 - г. Москва', max_length=255),
        ),
        migrations.AlterField(
            model_name='matchhistory',
            name='category',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='score.membercats'),
        ),
        migrations.AlterField(
            model_name='matchhistory',
            name='match',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='score.match'),
        ),
        migrations.AlterField(
            model_name='members',
            name='fo',
            field=models.CharField(choices=[('1 - Республика Адыгея (Адыгея)', '1 - Республика Адыгея (Адыгея)'), ('2 - Республика Башкортостан', '2 - Республика Башкортостан'), ('3 - Республика Бурятия', '3 - Республика Бурятия'), ('4 - Республика Алтай', '4 - Республика Алтай'), ('5 - Республика Дагестан', '5 - Республика Дагестан'), ('6 - Республика Ингушетия', '6 - Республика Ингушетия'), ('7 - Кабардино-Балкарская Республика', '7 - Кабардино-Балкарская Республика'), ('8 - Республика Калмыкия', '8 - Республика Калмыкия'), ('9 - Карачаево-Черкесская Республика', '9 - Карачаево-Черкесская Республика'), ('10 - Республика Карелия', '10 - Республика Карелия'), ('11 - Республика Коми', '11 - Республика Коми'), ('12 - Республика Марий Эл', '12 - Республика Марий Эл'), ('13 - Республика Мордовия', '13 - Республика Мордовия'), ('14 - Республика Саха (Якутия)', '14 - Республика Саха (Якутия)'), ('15 - Республика Северная Осетия - Алания', '15 - Республика Северная Осетия - Алания'), ('16 - Республика Татарстан (Татарстан)', '16 - Республика Татарстан (Татарстан)'), ('17 - Республика Тыва', '17 - Республика Тыва'), ('18 - Удмуртская Республика', '18 - Удмуртская Республика'), ('19 - Республика Хакасия', '19 - Республика Хакасия'), ('20 - Чеченская Республика', '20 - Чеченская Республика'), ('21 - Чувашская Республика - Чувашия', '21 - Чувашская Республика - Чувашия'), ('22 - Алтайский край', '22 - Алтайский край'), ('23 - Краснодарский край', '23 - Краснодарский край'), ('24 - Красноярский край', '24 - Красноярский край'), ('25 - Приморский край', '25 - Приморский край'), ('26 - Ставропольский край', '26 - Ставропольский край'), ('27 - Хабаровский край', '27 - Хабаровский край'), ('28 - Амурская область', '28 - Амурская область'), ('29 - Архангельская область', '29 - Архангельская область'), ('30 - Астраханская область', '30 - Астраханская область'), ('31 - Белгородская область', '31 - Белгородская область'), ('32 - Брянская область', '32 - Брянская область'), ('33 - Владимирская область', '33 - Владимирская область'), ('34 - Волгоградская область', '34 - Волгоградская область'), ('35 - Вологодская область', '35 - Вологодская область'), ('36 - Воронежская область', '36 - Воронежская область'), ('37 - Ивановская область', '37 - Ивановская область'), ('38 - Иркутская область', '38 - Иркутская область'), ('39 - Калининградская область', '39 - Калининградская область'), ('40 - Калужская область', '40 - Калужская область'), ('41 - Камчатский край', '41 - Камчатский край'), ('42 - Кемеровская область', '42 - Кемеровская область'), ('43 - Кировская область', '43 - Кировская область'), ('44 - Костромская область', '44 - Костромская область'), ('45 - Курганская область', '45 - Курганская область'), ('46 - Курская область', '46 - Курская область'), ('47 - Ленинградская область', '47 - Ленинградская область'), ('48 - Липецкая область', '48 - Липецкая область'), ('49 - Магаданская область', '49 - Магаданская область'), ('50 - Московская область', '50 - Московская область'), ('51 - Мурманская область', '51 - Мурманская область'), ('52 - Нижегородская область', '52 - Нижегородская область'), ('53 - Новгородская область', '53 - Новгородская область'), ('54 - Новосибирская область', '54 - Новосибирская область'), ('55 - Омская область', '55 - Омская область'), ('56 - Оренбургская область', '56 - Оренбургская область'), ('57 - Орловская область', '57 - Орловская область'), ('58 - Пензенская область', '58 - Пензенская область'), ('59 - Пермский край', '59 - Пермский край'), ('60 - Псковская область', '60 - Псковская область'), ('61 - Ростовская область', '61 - Ростовская область'), ('62 - Рязанская область', '62 - Рязанская область'), ('63 - Самарская область', '63 - Самарская область'), ('64 - Саратовская область', '64 - Саратовская область'), ('65 - Сахалинская область', '65 - Сахалинская область'), ('66 - Свердловская область', '66 - Свердловская область'), ('67 - Смоленская область', '67 - Смоленская область'), ('68 - Тамбовская область', '68 - Тамбовская область'), ('69 - Тверская область', '69 - Тверская область'), ('70 - Томская область', '70 - Томская область'), ('71 - Тульская область', '71 - Тульская область'), ('72 - Тюменская область', '72 - Тюменская область'), ('73 - Ульяновская область', '73 - Ульяновская область'), ('74 - Челябинская область', '74 - Челябинская область'), ('75 - Забайкальский край', '75 - Забайкальский край'), ('76 - Ярославская область', '76 - Ярославская область'), ('77 - г. Москва', '77 - г. Москва'), ('78 - Санкт-Петербург', '78 - Санкт-Петербург'), ('79 - Еврейская автономная область', '79 - Еврейская автономная область'), ('80 - Донецкая Народная Республика', '80 - Донецкая Народная Республика'), ('81 - Луганская народная республика', '81 - Луганская народная республика'), ('82 - Республика Крым', '82 - Республика Крым'), ('83 - Ненецкий автономный округ', '83 - Ненецкий автономный округ'), ('86 - ХМАО - Югра', '86 - ХМАО - Югра'), ('87 - Чукотский автономный округ', '87 - Чукотский автономный округ'), ('89 - Ямало-Ненецкий автономный округ', '89 - Ямало-Ненецкий автономный округ'), ('92 - Севастополь', '92 - Севастополь'), ('94 - Байконур', '94 - Байконур'), ('99 - Иные территории, включая город и космодром Байконур', '99 - Иные территории, включая город и космодром Байконур')], default='77 - г. Москва', max_length=255),
        ),
        migrations.AlterField(
            model_name='startlists',
            name='fo',
            field=models.CharField(choices=[('1 - Республика Адыгея (Адыгея)', '1 - Республика Адыгея (Адыгея)'), ('2 - Республика Башкортостан', '2 - Республика Башкортостан'), ('3 - Республика Бурятия', '3 - Республика Бурятия'), ('4 - Республика Алтай', '4 - Республика Алтай'), ('5 - Республика Дагестан', '5 - Республика Дагестан'), ('6 - Республика Ингушетия', '6 - Республика Ингушетия'), ('7 - Кабардино-Балкарская Республика', '7 - Кабардино-Балкарская Республика'), ('8 - Республика Калмыкия', '8 - Республика Калмыкия'), ('9 - Карачаево-Черкесская Республика', '9 - Карачаево-Черкесская Республика'), ('10 - Республика Карелия', '10 - Республика Карелия'), ('11 - Республика Коми', '11 - Республика Коми'), ('12 - Республика Марий Эл', '12 - Республика Марий Эл'), ('13 - Республика Мордовия', '13 - Республика Мордовия'), ('14 - Республика Саха (Якутия)', '14 - Республика Саха (Якутия)'), ('15 - Республика Северная Осетия - Алания', '15 - Республика Северная Осетия - Алания'), ('16 - Республика Татарстан (Татарстан)', '16 - Республика Татарстан (Татарстан)'), ('17 - Республика Тыва', '17 - Республика Тыва'), ('18 - Удмуртская Республика', '18 - Удмуртская Республика'), ('19 - Республика Хакасия', '19 - Республика Хакасия'), ('20 - Чеченская Республика', '20 - Чеченская Республика'), ('21 - Чувашская Республика - Чувашия', '21 - Чувашская Республика - Чувашия'), ('22 - Алтайский край', '22 - Алтайский край'), ('23 - Краснодарский край', '23 - Краснодарский край'), ('24 - Красноярский край', '24 - Красноярский край'), ('25 - Приморский край', '25 - Приморский край'), ('26 - Ставропольский край', '26 - Ставропольский край'), ('27 - Хабаровский край', '27 - Хабаровский край'), ('28 - Амурская область', '28 - Амурская область'), ('29 - Архангельская область', '29 - Архангельская область'), ('30 - Астраханская область', '30 - Астраханская область'), ('31 - Белгородская область', '31 - Белгородская область'), ('32 - Брянская область', '32 - Брянская область'), ('33 - Владимирская область', '33 - Владимирская область'), ('34 - Волгоградская область', '34 - Волгоградская область'), ('35 - Вологодская область', '35 - Вологодская область'), ('36 - Воронежская область', '36 - Воронежская область'), ('37 - Ивановская область', '37 - Ивановская область'), ('38 - Иркутская область', '38 - Иркутская область'), ('39 - Калининградская область', '39 - Калининградская область'), ('40 - Калужская область', '40 - Калужская область'), ('41 - Камчатский край', '41 - Камчатский край'), ('42 - Кемеровская область', '42 - Кемеровская область'), ('43 - Кировская область', '43 - Кировская область'), ('44 - Костромская область', '44 - Костромская область'), ('45 - Курганская область', '45 - Курганская область'), ('46 - Курская область', '46 - Курская область'), ('47 - Ленинградская область', '47 - Ленинградская область'), ('48 - Липецкая область', '48 - Липецкая область'), ('49 - Магаданская область', '49 - Магаданская область'), ('50 - Московская область', '50 - Московская область'), ('51 - Мурманская область', '51 - Мурманская область'), ('52 - Нижегородская область', '52 - Нижегородская область'), ('53 - Новгородская область', '53 - Новгородская область'), ('54 - Новосибирская область', '54 - Новосибирская область'), ('55 - Омская область', '55 - Омская область'), ('56 - Оренбургская область', '56 - Оренбургская область'), ('57 - Орловская область', '57 - Орловская область'), ('58 - Пензенская область', '58 - Пензенская область'), ('59 - Пермский край', '59 - Пермский край'), ('60 - Псковская область', '60 - Псковская область'), ('61 - Ростовская область', '61 - Ростовская область'), ('62 - Рязанская область', '62 - Рязанская область'), ('63 - Самарская область', '63 - Самарская область'), ('64 - Саратовская область', '64 - Саратовская область'), ('65 - Сахалинская область', '65 - Сахалинская область'), ('66 - Свердловская область', '66 - Свердловская область'), ('67 - Смоленская область', '67 - Смоленская область'), ('68 - Тамбовская область', '68 - Тамбовская область'), ('69 - Тверская область', '69 - Тверская область'), ('70 - Томская область', '70 - Томская область'), ('71 - Тульская область', '71 - Тульская область'), ('72 - Тюменская область', '72 - Тюменская область'), ('73 - Ульяновская область', '73 - Ульяновская область'), ('74 - Челябинская область', '74 - Челябинская область'), ('75 - Забайкальский край', '75 - Забайкальский край'), ('76 - Ярославская область', '76 - Ярославская область'), ('77 - г. Москва', '77 - г. Москва'), ('78 - Санкт-Петербург', '78 - Санкт-Петербург'), ('79 - Еврейская автономная область', '79 - Еврейская автономная область'), ('80 - Донецкая Народная Республика', '80 - Донецкая Народная Республика'), ('81 - Луганская народная республика', '81 - Луганская народная республика'), ('82 - Республика Крым', '82 - Республика Крым'), ('83 - Ненецкий автономный округ', '83 - Ненецкий автономный округ'), ('86 - ХМАО - Югра', '86 - ХМАО - Югра'), ('87 - Чукотский автономный округ', '87 - Чукотский автономный округ'), ('89 - Ямало-Ненецкий автономный округ', '89 - Ямало-Ненецкий автономный округ'), ('92 - Севастополь', '92 - Севастополь'), ('94 - Байконур', '94 - Байконур'), ('99 - Иные территории, включая город и космодром Байконур', '99 - Иные территории, включая город и космодром Байконур')], default='77 - г. Москва', max_length=255),
        ),
    ]
