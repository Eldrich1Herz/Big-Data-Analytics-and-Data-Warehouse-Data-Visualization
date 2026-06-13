import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
import os

def epub_to_txt(epub_file, txt_file):
    print(f"Читаю: {epub_file}")
    
    # Загружаем книгу
    book = epub.read_epub(epub_file)
    
    # Собираем весь текст
    all_text = []
    
    for item in book.get_items():
        # Берем только документы (главы)
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            # Парсим HTML
            soup = BeautifulSoup(item.get_content(), 'html.parser')
            # Извлекаем текст
            text = soup.get_text()
            if text.strip():
                all_text.append(text)
                print(f"  Обработана глава, символов: {len(text)}")
    
    # Сохраняем в файл
    with open(txt_file, 'w', encoding='utf-8') as f:
        f.write('\n\n'.join(all_text))
    
    print(f"\nГотово! Сохранено в {txt_file}")
    print(f"Всего символов: {sum(len(t) for t in all_text)}")

# Укажите пути к вашим файлам
epub_to_txt("Джон Френч_Солнечная война.epub", "Солнечная_война.txt")