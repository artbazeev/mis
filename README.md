# MIS 

### Инструкция по запуску проекта
1. Клонируем проект
```bash
git clone https://github.com/artbazeev/mis
```
2. Переходим в mis
```bash
cd mis
```
3. Запускаем контейнеры
```bash
docker-compose up --build -d
```
5. Переходим в контейнер web
```bash
docker-compose exec web bash
```
6. Применяем миграции
```bash
python manage.py migrate
```
7. Заполняем файлы static для админки и отображения swagger
```bash
python manage.py collectstatic
```
8. Создаем пользователя для админки и отображения swagger
```bash
python manage.py createsuperuser
```

10. **https://<ip-хоста>/admin - доступ к админ.панели

11. **https://<ip-хоста>/api/v1/swagger - доступ к апи, если сваггер не отображается выполнить шаг 7


Основные эндпоинты:

/api/v1/user/ - эндпоинт для управления пользователями, включая регистрацию, логин, просмотр деталей пользователя или его роли.


/api/v1/doctor/ - эндпоинт для создания и управления докторами (для user_id идем в /api/v1/user/) 
