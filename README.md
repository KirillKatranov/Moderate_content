

# 🛡️ NSFW Moderation Server

FastAPI-приложение для модерации изображений на наличие неприемлемого (NSFW) контента через Hugging Face NSFW Classifier.

---

## 🚀 Описание

Сервер принимает изображение (JPEG, PNG) и определяет, содержит ли оно NSFW-контент, отправляя запрос в модель Hugging Face `giacomoarienti/nsfw-classifier`.

---

## 📥 Эндпоинт

### POST /moderate

**Описание:**  
Проверка изображения на NSFW.

**Принимает:**

- `file` (form-data, required): изображение `.jpg` или `.png`

**Возвращает:**

- `{"status": "OK"}` — если изображение безопасно (nsfw_score ≤ 0.7)
- `{"status": "REJECTED", "reason": "NSFW content"}` — если найден неприемлемый контент (nsfw_score > 0.7)

---

### 🧪 Пример запроса (curl)

```bash
curl -X POST -F "file=@example.jpg" http://localhost:8000/moderate
````

---

## ⚠️ Возможные ошибки

| Код | Описание                                                                                          |
| --- | ------------------------------------------------------------------------------------------------- |
| 400 | Неверный формат файла (принимаются только .jpg и .png)                                            |
| 500 | Ошибка при обращении к Hugging Face API (например, недействительный токен или недоступная модель) |

---

## 🔧 Установка и запуск

1. **Клонируйте репозиторий**

```bash
git clone <your_repo_url>
cd <your_repo_dir>
```

2. **Создайте виртуальное окружение**

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

3. **Установите зависимости**

```bash
pip install -r requirements.txt
```

4. **Создайте .env файл**

```env
HF_TOKEN=your_hugging_face_token
```

Токен можно получить в [Hugging Face settings → Access Tokens](https://huggingface.co/settings/tokens) (роль: Read).

5. **Запустите приложение**

```bash
uvicorn app:app --reload
```

---

## 📂 Структура проекта

```
.
├── app.py
├── Schemas.py
├── config.py
├── requirements.txt
└── README.md
```

---

## 📌 Зависимости

* fastapi
* uvicorn
* requests
* pydantic
* python-multipart

---

## 🔑 Переменные окружения

| Переменная | Описание                                                      |
| ---------- | ------------------------------------------------------------- |
| HF\_TOKEN  | Токен Hugging Face с правами Read для доступа к Inference API |

---

## 📝 Примечания

* При первом вызове модель может возвращать `503 Model is loading` — подождите 1-2 минуты.
* Бесплатный тариф Hugging Face имеет ограничения по количеству запросов в минуту.

---
