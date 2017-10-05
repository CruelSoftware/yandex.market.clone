# yandex.market.clone
Simple flask yandex.market clone with no JS (currently),

just HTML templates and css

# Setup

1. Configure your database in config.py (project uses postgresql) or
create database/user/password as "yandex/yandex/yandex" on your localhost PostgreSQL server.

2.
```
    << pip install -r ./requirements/base.txt
    << python ./manage.py db init
    << python ./manage.py db migrate
    << python ./manage.py db upgrade
    << python ./manage.py alchemydumps restore -d 20171005071016
```

3. Run development server with:
```
<< python ./manage.py runserver --host=0.0.0.0
--host is not required parameter
```

4. Profit!

5. Additionals:

```
url /admin/ - admin panel with no athentication, here you may add new items and edit exists.
User model is just for future, no practice usage for now.
```
