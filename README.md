# Shmiede
It's one of my first projects learning how to program and create websites. This was my second webframework to learn.
The live version should be online and reachable under https://shmiede.de 
## How to start everything

```bash
cd djangoShmiedeSecond/mysite
sudo docker-compose down -v
sudo docker-compose -f docker-compose.prod.yml up -d --build

sudo docker-compose -f docker-compose.prod.yml exec web python manage.py migrate --noinput

sudo docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic --no-input --clear

sudo docker-compose logs -f
```

