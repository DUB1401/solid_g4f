# solid_g4f
**solid_g4f** – это модуль для расширения параметров генерации библиотеки [gpt4free](https://github.com/xtekky/gpt4free) и выноса самого процесса общения с нейросетью в отдельный процесс.

Поддерживается ротация прокси из списка строк внутри файла _Proxies.txt_ в стандартном формате, а также проверка локализации ответа, длины, ограничение времени ожидания, установка количества повторных попыток генерации, выбор модели.

## Порядок установки
1. Клонировать репозиторий.
2. Убедиться в доступности на вашем устройстве Python версии 3.10 или новее.
3. Открыть каталог со скриптом в консоли: можно воспользоваться командой `cd` или встроенными возможностями файлового менеджера.
4. Создать виртуальное окружение Python.
```Bash
python -m venv .venv
```
5. Активировать вирутальное окружение. 
```Bash
# Для Windows.
.venv\Scripts\activate.bat

# Для Linux или MacOS.
source .venv/bin/activate
```
6. Установить зависимости.
```Bash
pip install -r requirements.txt
```
7. Для автоматического запуска рекомендуется провести инициализацию сервиса через [systemd](systemd/README.md) на Linux или путём добавления его в автозагрузку на Windows.

## Использование через CLI
Для получения документации по использованию CLI активируйте вирутальную среду и запустите главный файл.
```Bash
python main.py help
```
Ниже приведён пример генерации ответа на вопрос: _Как дела?_

В качестве параметров передаётся максимальная длина ответа, время ожидания, ожидаемый язык, количество попыток генерации при неудовлетворительном результате.
```Bash
python main.py generate "Как дела?" --length 250 --model gpt-4o --language ru
```

## Использование через API
Активируйте виртуальную среду и запустите сервер обработки обращений.
```Bash
uvicorn server:api --port 8000
```

Отправьте запрос на генерацию, например из вашего скрипта Python.
```Python
from solid_g4f.Connection.API import Options, Requestor

# Создание опций запроса.
Settings = Options()
Settings.set_max_length(250)
Settings.set_model("gpt-4o")
Settings.set_language("ru")

# Отправка запроса на генерацию.
Master = Requestor(Settings)
Response = Master.generate("Как дела?")
print(Response.text)
```
Доступно также псевдоасинхронное выполнение запросов.
```Python
# Словарь для ответов.
Results = {
	1: None,
	2: None,
	3: None
}

# Каждая генерация ниже запускается в отедльном потоке.
# Ответы помещаются в словарь под соответствующим ключом.
Master.start_thread_generation("Чем накормить кота?", Results, 1)
Master.start_thread_generation("Любит ли кот есть рыбу?", Results, 2)
Master.start_thread_generation("Где обитает рыба?", Results, 3)

# Ожидаем ответы на вопросы в нужном порядке.
# Общее время генерации снижается в разы.
print(Master.wait_thread_generation(Results, 1).json["text"])
print(Master.wait_thread_generation(Results, 2).json["text"])
print(Master.wait_thread_generation(Results, 3).json["text"])
```

_Copyright © DUB1401. 2025._