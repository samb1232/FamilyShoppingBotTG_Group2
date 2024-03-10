from familybot.db.crud import *
from familybot.db.models import Person

# Создаем таблицы
create_tables()

# Вставляем пользователя
insert_persons([Person(telegram_tag='gelbal', name='Gleb')])

# Получаем объект пользователя, чтобы проверить функции (можно было сначала его объявить, а потом добавить, как с продуктом)
me = get_person_by_tg('gelbal')

dad = Person(telegram_tag='dad_tag', name='Dad')

# Создаем объект продукта с привязкой к создателю
chocolate = Purchase(text='choco', creator=me)

milk = Purchase(text='milk', creator=dad)
bread = Purchase(text='bread', creator=dad)

dad.purchases = [milk, bread]

insert_persons([dad])

# Добавляем продукт в таблицу
insert_purchase([chocolate])

# Выводим все
print(get_all_persons())
print(get_all_purchases())

print(me.purchases) # Ура! Оно работает!
print(dad.purchases)

# Пробуем создать семью
dad.create_family(name='My Family')
me.family = dad.family
insert_persons([me]) # Что бы обновить данные

print(get_all_families())

print(type(me.family))
print(get_family_purchases(me.family))
