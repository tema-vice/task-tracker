```cmd
cd todo-app-frontend
```

```cmd
npm run dev
```

```cmd
cd todo-app-backend
```

```cmd
uvicorn main:app --port 8080 --reload
```

# Порты и процессы в Windows — шпаргалка (CMD + PowerShell)

> Пример ниже — порт **8080**. Замени `8080` на нужный порт, а `3960` — на реальный PID из вывода команды. Команды с пометкой **CMD** можно запускать прямо в терминале PyCharm, если он использует `cmd.exe`.

## 1. Узнать, кто слушает порт

**CMD:**

```cmd
netstat -ano | findstr :8080
```

Ищи строки со статусом `LISTENING` (не `TIME_WAIT`, `CLOSE_WAIT` и т. д.). Последний столбец — PID процесса. `findstr :8080` может также показать соединения, где `8080` — удалённый порт: смотри на столбец локального адреса.

**PowerShell из CMD:**

```cmd
powershell -NoProfile -Command "Get-NetTCPConnection -LocalPort 8080 -State Listen | Select-Object LocalAddress,LocalPort,OwningProcess"
```

## 2. Выяснить, что это за процесс

Допустим, PID = **3960**.

**CMD — имя процесса:**

```cmd
tasklist /FI "PID eq 3960"
```

**PowerShell из CMD — PID, родитель и команда запуска:**

```cmd
powershell -NoProfile -Command "Get-CimInstance Win32_Process -Filter 'ProcessId = 3960' | Format-List ProcessId,ParentProcessId,Name,CommandLine"
```

Если нужно найти **все Python/Uvicorn-процессы**:

```cmd
powershell -NoProfile -Command "Get-CimInstance Win32_Process | Where-Object { $_.Name -in @('python.exe','pythonw.exe') -or $_.CommandLine -match 'uvicorn' } | Format-List ProcessId,ParentProcessId,Name,CommandLine"
```

## 3. Остановить процесс

**Предпочтительно:** в терминале работающего Uvicorn нажми `Ctrl+C`.

Если не помогло, **после проверки PID и команды запуска**, в CMD:

```cmd
taskkill /PID 3960 /F
```

Если это родительский процесс и требуется завершить также его дочерние процессы:

```cmd
taskkill /PID 3960 /T /F
```

- `/PID` — конкретный идентификатор процесса;
- `/T` — завершить дочерние процессы;
- `/F` — принудительное завершение.

**Не используй** `taskkill /IM python.exe /F` без необходимости: это остановит все процессы Python, включая другие проекты.

## 4. Проверить результат

**CMD:**

```cmd
netstat -ano | findstr :8080
```

**Дополнительно — проверить HTTP-ответ:**

```cmd
curl -i http://127.0.0.1:8080/openapi.json
```

Если `curl` возвращает `200 OK`, на порту ещё работает HTTP-сервер. Если нет строк `LISTENING`, слушающий процесс отсутствует. Строки `TIME_WAIT` после остановки — нормальны и не означают запущенный сервер.

## 5. Перезапустить нужный FastAPI backend

**CMD:**

```cmd
cd /d "I:\Data\Python files\first-fastapi\todo-app-backend"
.venv\Scripts\activate.bat
python -m uvicorn main:app --host 127.0.0.1 --port 8080 --reload
```

> При `--reload` Uvicorn запускает процесс-перезагрузчик и рабочий процесс. Это нормально. Если PID указан в `netstat`, но не находится через `tasklist`, **не завершай случайные PID**: сначала проверь актуальные Python-процессы, затем при необходимости закрой старые терминалы/перезапусти IDE.

## Быстрый алгоритм

`netstat` → PID из `LISTENING` → `tasklist` / `Get-CimInstance` → проверить, что это нужный процесс → `taskkill` → снова `netstat` → запустить Uvicorn.
