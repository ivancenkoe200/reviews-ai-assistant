from google_play_scraper import reviews, Sort
import pandas as pd
import time

# Используем правильный ID
app_id = "com.deliveryclub" 

print(f"Начинаю сбор отзывов для {app_id}...")

all_reviews = []
# Пробуем собрать отзывы с разными параметрами и сортировками
for sort_type in [Sort.NEWEST, Sort.MOST_RELEVANT]:
    try:
        # Добавим count побольше, чтобы точно захватить
        result, _ = reviews(
            app_id,
            lang='ru',      
            country='ru',   
            sort=sort_type,
            count=100  # Попробуем запросить больше
        )
        if result:
            print(f"Успех! Собрано {len(result)} отзывов (сортировка: {sort_type})")
            all_reviews.extend(result)
        else:
            print(f"Сортировка {sort_type}: отзывов не найдено.")
        time.sleep(2) # Увеличим паузу, чтобы не злить Google
    except Exception as e:
        print(f"Ошибка при сборе (сортировка {sort_type}): {e}")

# Проверяем, есть ли данные
if not all_reviews:
    print("Не удалось собрать отзывы. Возможно, Google временно ограничил доступ.")
else:
    # Преобразуем в таблицу
    df = pd.DataFrame(all_reviews)
    df = df[['at', 'score', 'content']].rename(columns={'at':'date', 'score':'rating', 'content':'text'})
    df['source'] = 'google_play'
    
    # Убираем дубликаты и пустые отзывы
    df = df.dropna(subset=['text']).drop_duplicates(subset=['text'])
    
    df.to_csv('raw_reviews.csv', index=False)
    print(f"ГОТОВО! Собрано уникальных отзывов: {len(df)}")
    print("Файл raw_reviews.csv сохранен.")