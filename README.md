# Предекодер ядра процессора MIPS и Intel
### Веб-приложение
### Курсовая работа. Была выполнена на третьем курсе обучения в университете
---
Teхнологии: 
- Библиотека - Django – свободный фреймворк для веб-приложений на языке Python, использующий шаблон проектирования MVC. Проект поддерживается организацией Django Software Foundation. Сайт на Django строится из одного или нескольких приложений, которые рекомендуется делать отчуждаемыми и подключаемыми.

- Для работы с медифайлами использовалась библиотека Pillow – это свободно распространяемая библиотека для работы с изображениями на Python

- Шаблоны веб-страниц были написаны на языке HTML – стандартизированный язык разметки документов для просмотра веб-страниц в браузере.

- Стиль и дизайн веб-страниц был проработан с помощью языка программирования CSS – язык таблиц стилей, который позволяет прикреплять стиль (например, шрифты и цвет) к структурированным документам (например, документам HTML).

- База данных, выбранная для хранения информации – SQLIte. Это встраиваемая кроссплатформенная БД, которая поддерживает достаточно полный набор команд SQL.
---
Основные методы:
- index() – метод, который обрабатывает запросы пользователей на главной странице, возвращает http-объект с контекстом и шаблоном, запрашиваемым пользователем;

- error_for_bytes_string() – метод валидации введенной пользователем строки;

- get_users_*() – метод, который возвращает необходимые данные из базы данных;

- set_users_*() – метод, который устанавливает значение для пользовательских данных в базе данных;

- process() – метод, который отвечает за процесс выполнения предекодирования для процессора MIPS;

- stream_to_commands() – метод, который возвращает декодированные команды из потока байт;

- grouper() – метод, который переводит поток байт в поток бит.
---
Результат: [predecoder.ru](https://predecoder.ru/)
