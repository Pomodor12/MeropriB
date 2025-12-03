# Берём официальный образ Python 3.11
FROM python:3.11-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы зависимостей и ставим их
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем все файлы проекта
COPY . .

# Запуск бота
CMD ["python", "main.py"]
