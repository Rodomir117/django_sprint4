# Blogicum

## Проект django_sprint4

* создана учетная запись администратора

      Имя пользователя: admin
      Пароль: 1 
 * для изменения пароля учетной записи **admin** используется команда:
        
        ./manage.py changepassword admin 

## Инструкция для пользователей Windows

 1.Клонировать репозиторий и перейти в папку **django_sprint4**:

        git clone git@github.com:Rodomir117/django_sprint4.git
        cd django_sprint4

2.Cоздать и активировать виртуальное окружение:

        py -m venv venv
        source venv/Scripts/activate

3.Установить зависимости из файла requirements.txt:

        pip install -r requirements.txt

5.Перейти в папку проекта **blogicum** и запустить его:

        cd blogicum
        ./manage.py migrate
        ./manage.py loaddata db.json 
        ./manage.py runserver 1234

6.Перейти на локальный сервер:

        http://127.0.0.1:1234/

7.Перейти в панель администратора:

       http://127.0.0.1:1234/admin/ 