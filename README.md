# test task

## 

использован фастапи и алхимия 2.0
для парсинга экселя - пандас

- docker compose up
- docker compose exec backend alembic upgrade head
- идем на сваггер http://127.0.0.1:8000/docs/ 
- находим эндпоинт с компаниями, создаем company1 и company2
- грузим эксель на companies/upload
- кидаем дату в формате 2023-04-20 (от 1 до 20 числа) на companies/total
- получаем результат
