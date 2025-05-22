# =======================================================
# === 🧱 БЛОК 1: Импорт всех библиотек и настроек ========
# =======================================================

import asyncio
import os
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import Command

from aiogram.webhook.aiohttp_server import SimpleRequestHandler

# Чтение токена и адреса вебхука из переменных окружения
BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
WEBHOOK_PATH = "/webhook"

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

# Гарантируем наличие папки
Path("storage").mkdir(exist_ok=True)

# Фоновая задача напоминаний
async def reminder_background_task():
    data_file = Path("storage/data.json")
    CHECK_INTERVAL = 60  # сек
    while True:
        try:
            if not data_file.exists():
                await asyncio.sleep(CHECK_INTERVAL)
                continue
            with open(data_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            now_utc = datetime.now(ZoneInfo("UTC"))
            # тут можно вставить минимальную логику (например, просто лог)
            print(f"🔄 Напоминания проверены в {now_utc}")
        except Exception as e:
            print(f"⚠️ reminder_background_task: {e}")
        await asyncio.sleep(CHECK_INTERVAL) =======================================================
# === 🧱 БЛОК 2: Инициализация бота и диспетчера ========
# =======================================================

bot = Bot(
    token=config.BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher(storage=MemoryStorage())


# =======================================================
# === 🧱 БЛОК 3: Команда /start — главное меню ==========
# =======================================================


from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

@dp.message(Command("start"))
async def start_handler(message: Message):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="⚡ Электроэнергия")],
            [KeyboardButton(text="🔥 Газ")],
            [KeyboardButton(text="💧 Вода")],
            [KeyboardButton(text="📊 Общий долг / переплата")],
            [KeyboardButton(text="⚙ Настройки")],
        ],
        resize_keyboard=True
    )

    await message.answer(
        "👋 Привет, я Домовёнок Кузя!\n\n"
        "Я буду помогать тебе наводить порядок в твоем сундуке со сказками —              коммунальных платежах.\n\n"
        "Если ты зашел в первый раз, то зайди в ⚙️ <b>Настройки</b> и установи            текущие показания счётчиков и сумму долга (или переплаты).\n\n"
        "🧮 А теперь скажи, что будем считать сегодня? Выбери раздел:",
        reply_markup=keyboard
    )


# =======================================================
# === 🧱 БЛОК 4: Команда /add — ручной ввод показаний ===
# =======================================================

@dp.message(Command("add"))
async def add_handler(message: Message):
    try:
        from datetime import datetime
        import json
        from pathlib import Path

        # Пример команды: /add вода 23.7
        parts = message.text.strip().split()
        if len(parts) != 3:
            raise ValueError("Неверный формат. Используй: /add <тип> <значение>")

        counter_type = parts[1].lower()
        value = float(parts[2])
        user_id = str(message.from_user.id)
        today = datetime.now().strftime("%Y-%m-%d")

        # Путь к файлу с данными
        data_file = Path("storage/data.json")

        # Загрузка текущих данных
        if data_file.exists():
            with open(data_file, "r", encoding="utf-8") as f:
                data = json.load(f)
        else:
            data = {}

        # Обновление данных
        if user_id not in data:
            data[user_id] = {}
        if today not in data[user_id]:
            data[user_id][today] = {}
        data[user_id][today][counter_type] = value

        # Сохранение обратно в файл
        with open(data_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        await message.answer(f"✅ Показание сохранено: {counter_type} = {value}")
    except Exception as e:
        await message.answer(f"⚠️ Ошибка: {e}")


# =======================================================
# === 🧱 БЛОК 5: Меню ⚡ Электроэнергия — обработчик =====
# =======================================================

@dp.message(lambda message: message.text == "⚡ Электроэнергия")
async def electricity_menu_handler(message: Message):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="➕ Внести показания (электроэнергия)")],
            [KeyboardButton(text="💸 Внести оплату (электроэнергия)")],
            [KeyboardButton(text="📉 Посмотреть долг (электроэнергия)")],
            [KeyboardButton(text="📜 История показаний (электроэнергия)")],
            [KeyboardButton(text="🧾 История оплат (электроэнергия)")],
            [KeyboardButton(text="🔙 Назад")],
        ],
        resize_keyboard=True
    )

    await message.answer(
        "Вы в разделе ⚡ Электроэнергия.\nВыберите действие:",
        reply_markup=keyboard
    )


# =======================================================
# === 🧱 БЛОК 6: Меню 💧 Вода — обработчик ==============
# =======================================================

@dp.message(lambda message: message.text == "💧 Вода")
async def water_menu_handler(message: Message):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="➕ Внести показания (вода)")],
            [KeyboardButton(text="💸 Внести оплату (вода)")],
            [KeyboardButton(text="📉 Посмотреть долг (вода)")],
            [KeyboardButton(text="📜 История показаний (вода)")],
            [KeyboardButton(text="🧾 История оплат (вода)")],
            [KeyboardButton(text="🔙 Назад")],
        ],
        resize_keyboard=True
    )

    await message.answer(
        "Раздел 💧 Вода.\nВыберите действие:",
        reply_markup=keyboard
    )


# =======================================================
# === 🧱 БЛОК 7: Меню 🔥 Газ — обработчик ===============
# =======================================================

@dp.message(lambda message: message.text == "🔥 Газ")
async def gas_menu_handler(message: Message):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="➕ Внести показания (газ)")],
            [KeyboardButton(text="💸 Внести оплату (газ)")],
            [KeyboardButton(text="📉 Посмотреть долг (газ)")],
            [KeyboardButton(text="📜 История показаний (газ)")],
            [KeyboardButton(text="🧾 История оплат (газ)")],
            [KeyboardButton(text="🔙 Назад")],
        ],
        resize_keyboard=True
    )

    await message.answer(
        "Раздел 🔥 Газ.\nВыберите действие:",
        reply_markup=keyboard
    )


# =======================================================
# === 🧱 БЛОК 8: 📜 История показаний (только свет) =====
# =======================================================

@dp.message(lambda message: message.text == "📜 История показаний")
async def electricity_history(message: Message):
    await show_history(message, "электроэнергия", "кВт⋅ч")


# =======================================================
# === 🧱 БЛОК 9: FSM-состояния для ввода показаний ======
# =======================================================

from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from datetime import datetime
import json
from pathlib import Path

class ReadingState(StatesGroup):
    electricity = State()
    water = State()
    gas = State()


# =======================================================
# === 🧱 БЛОК 9.1: История показаний ⚡ Электроэнергия ===
# =======================================================

@dp.message(lambda message: message.text == "📜 История показаний (электроэнергия)")
async def electricity_history_named(message: Message):
    await show_history(message, "электроэнергия", "кВт⋅ч")


# =======================================================
# === 🧱 БЛОК 9.2: История показаний 💧 Вода =============
# =======================================================

@dp.message(lambda message: message.text == "📜 История показаний (вода)")
async def water_history(message: Message):
    await show_history(message, "вода", "м³")


# =======================================================
# === 🧱 БЛОК 9.3: История показаний 🔥 Газ ==============
# =======================================================

@dp.message(lambda message: message.text == "📜 История показаний (газ)")
async def gas_history(message: Message):
    await show_history(message, "газ", "м³")


# =======================================================
# === 🧱 БЛОК 10: Ввод показаний ⚡ Электроэнергии =======
# =======================================================

@dp.message(lambda message: message.text == "➕ Внести показания (электроэнергия)")
async def start_electricity_reading(message: Message, state: FSMContext):
    await state.set_state(ReadingState.electricity)
    last = get_last_value(message.from_user.id, "электроэнергия")
    msg = "Введите текущие показания электроэнергии (кВт⋅ч):"
    if last is not None:
        msg += f"\n_(предыдущее: {last})_"
    await message.answer(msg, parse_mode="Markdown")

@dp.message(ReadingState.electricity)
async def save_electricity_reading(message: Message, state: FSMContext):
    await save_reading(message, state, "электроэнергия")
    await state.clear()


# =======================================================
# === 🧱 БЛОК 11: Ввод показаний 💧 Воды ================
# =======================================================

@dp.message(lambda message: message.text == "➕ Внести показания (вода)")
async def start_water_reading(message: Message, state: FSMContext):
    await state.set_state(ReadingState.water)
    last = get_last_value(message.from_user.id, "вода")
    msg = "Введите текущие показания по воде (м³):"
    if last is not None:
        msg += f"\n_(предыдущее: {last})_"
    await message.answer(msg, parse_mode="Markdown")

@dp.message(ReadingState.water)
async def save_water_reading(message: Message, state: FSMContext):
    await save_reading(message, state, "вода")
    await state.clear()


# =======================================================
# === 🧱 БЛОК 12: Ввод показаний 🔥 Газа ================
# =======================================================

@dp.message(lambda message: message.text == "➕ Внести показания (газ)")
async def start_gas_reading(message: Message, state: FSMContext):
    await state.set_state(ReadingState.gas)
    last = get_last_value(message.from_user.id, "газ")
    msg = "Введите текущие показания по газу (м³):"
    if last is not None:
        msg += f"\n_(предыдущее: {last})_"
    await message.answer(msg, parse_mode="Markdown")

@dp.message(ReadingState.gas)
async def save_gas_reading(message: Message, state: FSMContext):
    await save_reading(message, state, "газ")
    await state.clear()


# =======================================================
# === 🧱 БЛОК 13: Очистка старых записей из базы данных =
# =======================================================

async def cleanup_old_records(user_id: str):
    data_file = Path("storage/data.json")
    if not data_file.exists():
        return

    try:
        with open(data_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        if user_id not in data:
            return

        user_data = data[user_id]
        settings = user_data.get("настройки", {})  # Сохраняем настройки
        tariffs = user_data.get("тарифы", {})  # Сохраняем тарифы

        # Сортируем записи по дате
        entries = [(date, items) for date, items in user_data.items() 
                  if isinstance(items, dict) and date not in ["настройки", "тарифы"]]
        entries.sort(reverse=True)  # Сортируем по дате в обратном порядке

        # Создаем новый словарь данных пользователя
        new_user_data = {
            "настройки": settings,
            "тарифы": tariffs
        }

        # Оставляем только последние 12 записей
        for date, items in entries[:12]:
            new_user_data[date] = items

        # Обновляем данные пользователя
        data[user_id] = new_user_data

        # Сохраняем обновленные данные
        with open(data_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    except Exception as e:
        print(f"Ошибка при очистке старых записей: {e}")


# =======================================================
# === 🧱 БЛОК 14: Сохранение новых показаний (NEW) ======
# =======================================================
#
# • После записи расхода обнуляем служебные поля
#   next_try / last_sent у соответствующего счётчика, чтобы
#   напоминания возобновились только в следующем месяце.
#
async def save_reading(message: Message, state: FSMContext, counter_type: str):
    try:
        value = float(message.text.strip().replace(',', '.'))  # поддержка «1,23»
        user_id = str(message.from_user.id)
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data_file = Path("storage/data.json")

        data = {}
        if data_file.exists():
            with open(data_file, "r", encoding="utf-8") as f:
                data = json.load(f)

        user_blob = data.setdefault(user_id, {})
        # ======= Запись показаний =======
        user_blob[now] = {}
        prev_value = get_last_value(user_id, counter_type) or 0
        user_blob[now][counter_type] = value
        usage = value - prev_value if prev_value else 0

        # ======= Начисление =======
        tariff_key = f"{counter_type}_тариф"
        tariff = user_blob.get("тарифы", {}).get(tariff_key, 1.8)
        cost = usage * tariff
        user_blob[now].setdefault("начисления", {})[counter_type] = cost

        # ======= Сброс служебных полей напоминания =======
        settings = user_blob.setdefault("настройки", {})
        cfg = settings.setdefault(f"{counter_type}_напоминание", {})
        cfg.pop("next_try", None)
        cfg.pop("last_sent", None)

        # ======= Чистка старых записей =======
        await cleanup_old_records(user_id)

        # ======= Сохранение файла =======
        with open(data_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        units = {"электроэнергия": "кВт⋅ч", "вода": "м³", "газ": "м³"}
        await message.answer(
            f"✅ Показания сохранены: {value}\n"
            f"📊 Расход: {usage:.2f} {units.get(counter_type, '')} • "
            f"Сумма: {cost:.2f} грн"
        )
    except ValueError:
        await message.answer("⚠️ Ошибка: введите корректное число")
    except Exception as e:
        await message.answer(f"⚠️ Ошибка: {e}")


# =======================================================
# === 🧱 БЛОК 15: Получение последних показаний ==========
# =======================================================

def get_last_value(user_id, counter_type):
    user_id = str(user_id)
    data_file = Path("storage/data.json")
    if data_file.exists():
        with open(data_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        if user_id in data:
            # Сначала проверяем историю показаний
            dates = sorted([d for d in data[user_id].keys() 
                          if isinstance(data[user_id][d], dict) and 
                          counter_type in data[user_id][d]], reverse=True)
            if dates:
                return data[user_id][dates[0]][counter_type]

            # Если истории нет, проверяем начальные показания
            if "настройки" in data[user_id]:
                initial_key = f"{counter_type}_показания"
                if initial_key in data[user_id]["настройки"]:
                    return data[user_id]["настройки"][initial_key]
    return None


# =======================================================
# === 🧱 БЛОК 16: FSM-состояния для внесения оплаты =====
# =======================================================

class PaymentState(StatesGroup):
    electricity = State()
    water = State()
    gas = State()


# =======================================================
# === 🧱 БЛОК 17: Обработка оплаты ⚡ Электроэнергии =====
# =======================================================

@dp.message(lambda message: message.text == "💸 Внести оплату (электроэнергия)")
async def start_electricity_payment(message: Message, state: FSMContext):
    await state.set_state(PaymentState.electricity)
    await message.answer("Введите сумму оплаты за электроэнергию (грн):")

@dp.message(PaymentState.electricity)
async def save_electricity_payment(message: Message, state: FSMContext):
    await save_payment(message, state, "электроэнергия")
    await state.clear()


# =======================================================
# === 🧱 БЛОК 18: Обработка оплаты 💧 Воды ===============
# =======================================================

@dp.message(lambda message: message.text == "💸 Внести оплату (вода)")
async def start_water_payment(message: Message, state: FSMContext):
    await state.set_state(PaymentState.water)
    await message.answer("Введите сумму оплаты за воду (грн):")

@dp.message(PaymentState.water)
async def save_water_payment(message: Message, state: FSMContext):
    await save_payment(message, state, "вода")
    await state.clear()


# =======================================================
# === 🧱 БЛОК 19: Обработка оплаты 🔥 Газа ===============
# =======================================================

@dp.message(lambda message: message.text == "💸 Внести оплату (газ)")
async def start_gas_payment(message: Message, state: FSMContext):
    await state.set_state(PaymentState.gas)
    await message.answer("Введите сумму оплаты за газ (грн):")

@dp.message(PaymentState.gas)
async def save_gas_payment(message: Message, state: FSMContext):
    await save_payment(message, state, "газ")
    await state.clear()


# =======================================================
# === 🧱 БЛОК 20: Общая функция сохранения оплаты =======
# =======================================================

async def save_payment(message: Message, state: FSMContext, counter_type: str):
    try:
        amount = float(message.text.strip().replace(',', '.'))  # Поддержка запятой
        user_id = str(message.from_user.id)
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        file_path = Path("storage/data.json")

        if file_path.exists():
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        else:
            data = {}

        if user_id not in data:
            data[user_id] = {}

        # Сохраняем оплату с временной меткой
        data[user_id][now] = {
            f"{counter_type}_оплата": amount
        }

        # Очистка старых записей
        await cleanup_old_records(user_id)

        # Получаем текущий долг для информативного сообщения
        total = 0.0
        paid = 0.0
        initial_debt = 0.0

        if "настройки" in data[user_id]:
            initial_debt = float(data[user_id]["настройки"].get(f"{counter_type}_долг", 0))

        for date in sorted(data[user_id].keys()):
            items = data[user_id][date]
            if isinstance(items, dict):
                if "начисления" in items and counter_type in items["начисления"]:
                    total += float(items["начисления"][counter_type])
                payment_key = f"{counter_type}_оплата"
                if payment_key in items:
                    paid += float(items[payment_key])

        total += initial_debt
        remaining_debt = total - paid

        # Сохранение
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        # Формируем сообщение об оплате
        message_text = [
            f"💸 Оплата сохранена: {amount:.2f} грн",
            f"💰 Остаток: {'+' if remaining_debt < 0 else ''}{abs(remaining_debt):.2f} грн"
        ]

        if remaining_debt > 0:
            message_text.append("❗ Есть задолженность")
        elif remaining_debt < 0:
            message_text.append("💫 Есть переплата")
        else:
            message_text.append("✅ Долг полностью погашен")

        await message.answer("\n".join(message_text))
    except ValueError:
        await message.answer("⚠️ Ошибка: введите корректное число")
    except Exception as e:
        await message.answer(f"⚠️ Ошибка: {e}")


# =======================================================
# === 🧱 БЛОК 21: Просмотр долга ⚡ Электроэнергия =======
# =======================================================

@dp.message(lambda message: message.text == "📉 Посмотреть долг (электроэнергия)")
async def view_debt_electricity(message: Message):
    await show_debt(message, "электроэнергия")


# =======================================================
# === 🧱 БЛОК 22: Просмотр долга 💧 Вода ================
# =======================================================

@dp.message(lambda message: message.text == "📉 Посмотреть долг (вода)")
async def view_debt_water(message: Message):
    await show_debt(message, "вода")


# =======================================================
# === 🧱 БЛОК 23: Просмотр долга 🔥 Газ =================
# =======================================================

@dp.message(lambda message: message.text == "📉 Посмотреть долг (газ)")
async def view_debt_gas(message: Message):
    await show_debt(message, "газ")


# =======================================================
# === 🧱 БЛОК 23.1: Просмотр общего долга / переплаты ===
# =======================================================

@dp.message(lambda message: message.text == "📊 Общий долг / переплата")
async def view_total_balance(message: Message):
    try:
        user_id = str(message.from_user.id)
        data_file = Path("storage/data.json")
        if not data_file.exists():
            await message.answer("📭 Нет данных.")
            return

        with open(data_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        if user_id not in data:
            await message.answer("📭 Данные отсутствуют.")
            return

        resources = {
            "электроэнергия": "⚡ Электроэнергия",
            "вода": "💧 Вода",
            "газ": "🔥 Газ"
        }

        lines = []
        total_balance = 0.0

        for key, label in resources.items():
            total = 0.0
            paid = 0.0
            initial_debt = 0.0

            user_data = data[user_id]

            if "настройки" in user_data:
                initial_debt = float(user_data["настройки"].get(f"{key}_долг", 0))

            for date, items in user_data.items():
                if isinstance(items, dict):
                    if "начисления" in items and key in items["начисления"]:
                        total += float(items["начисления"][key])
                    payment_key = f"{key}_оплата"
                    if payment_key in items:
                        paid += float(items[payment_key])

            balance = initial_debt + total - paid
            total_balance += balance

            if balance > 0:
                lines.append(f"{label} — долг: {balance:.2f} грн ❗")
            elif balance < 0:
                lines.append(f"{label} — переплата: {abs(balance):.2f} грн 💫")
            else:
                lines.append(f"{label} — нет задолженности ✅")

        lines.append("")
        if total_balance > 0:
            lines.append(f"🧮 Итоговая задолженность по коммунальным: <b>{total_balance:.2f} грн</b> ❗")
        elif total_balance < 0:
            lines.append(f"🧮 Итоговая переплата по коммунальным: <b>{abs(total_balance):.2f} грн</b> 💫")
        else:
            lines.append(f"🧮 Всё оплачено: <b>0.00 грн</b> ✅")

        await message.answer("\n".join(lines))
    except Exception as e:
        await message.answer(f"⚠️ Ошибка: {e}")


# =======================================================
# === 🧱 БЛОК 24: Общая функция расчёта долга ==========
# =======================================================

async def show_debt(message: Message, counter_type: str):
    try:
        user_id = str(message.from_user.id)
        data_file = Path("storage/data.json")

        total = 0.0
        paid = 0.0
        initial_debt = 0.0
        last_reading_val = None
        last_reading_date = None

        if data_file.exists():
            with open(data_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            if user_id in data:
                if "настройки" in data[user_id]:
                    initial_debt = float(data[user_id]["настройки"].get(f"{counter_type}_долг", 0))

                for date_str in sorted(data[user_id].keys()):
                    items = data[user_id][date_str]
                    if isinstance(items, dict):
                        if "начисления" in items and counter_type in items["начисления"]:
                            total += float(items["начисления"][counter_type])
                            if counter_type in items:
                                last_reading_val = float(items[counter_type])
                            last_reading_date = date_str

                        payment_key = f"{counter_type}_оплата"
                        if payment_key in items:
                            paid += float(items[payment_key])

        total += initial_debt
        debt = total - paid

        def fmt_date(d):
            try:
                return datetime.strptime(d, "%Y-%m-%d %H:%M:%S").strftime("%d.%m.%Y")
            except:
                try:
                    return datetime.strptime(d, "%Y-%m-%d").strftime("%d.%m.%Y")
                except:
                    return d or "-"

        # Определяем единицу измерения
        units = {
            "электроэнергия": "кВт⋅ч",
            "вода": "м³",
            "газ": "м³"
        }

        details = []

        usage_note = ""
        if last_reading_val and last_reading_date:
            unit = units.get(counter_type, "")
            usage_note = f" (включая начисления по последним показаниям {last_reading_val} {unit} от {fmt_date(last_reading_date)})"

        details.append(f"📉 <b>{counter_type.capitalize()}</b>:")
        if debt > 0:
            details.append(f"Итоговый долг{usage_note}:\n<b>{debt:.2f} грн</b>")
        elif debt < 0:
            details.append(f"Итоговая переплата{usage_note}:\n<b>{abs(debt):.2f} грн</b>")
        else:
            details.append(f"💰 Всё оплачено{usage_note}:\n<b>0.00 грн</b>")

        await message.answer("\n".join(details))
    except Exception as e:
        await message.answer(f"⚠️ Ошибка при расчёте долга: {e}")


# =======================================================
# === 🧱 БЛОК 25: Обработка кнопки 🔙 Назад в меню ======
# =======================================================

@dp.message(lambda message: message.text == "🔙 Назад")
async def back_to_main_menu(message: Message):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="⚡ Электроэнергия")],
            [KeyboardButton(text="🔥 Газ")],
            [KeyboardButton(text="💧 Вода")],
            [KeyboardButton(text="📊 Общий долг / переплата")],
            [KeyboardButton(text="⚙ Настройки")],
        ],
        resize_keyboard=True
    )

    await message.answer(
        "🔙 Возврат в главное меню. Выбери раздел:",
        reply_markup=keyboard
    )

# ===========================================================
# === 🧱 БЛОК 26: Общая функция вывода истории показаний ===
# ===========================================================

async def show_history(message: Message, counter_type: str, unit: str):
    try:
        user_id = str(message.from_user.id)
        data_file = Path("storage/data.json")
        entries = []
        initial_reading = None

        if data_file.exists():
            with open(data_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            if user_id in data:
                # Получаем начальное показание
                if "настройки" in data[user_id]:
                    initial_key = f"{counter_type}_показания"
                    if initial_key in data[user_id]["настройки"]:
                        initial_reading = float(data[user_id]["настройки"][initial_key])

                # Собираем все показания
                for date_str, items in data[user_id].items():
                    if isinstance(items, dict) and counter_type in items:
                        try:
                            dt = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
                        except ValueError:
                            try:
                                dt = datetime.strptime(date_str, "%Y-%m-%d")
                            except ValueError:
                                continue
                        val = float(items[counter_type])
                        entries.append((dt, val))

        entries.sort()

        if entries:
            lines = []

            for i in range(len(entries)):
                dt, val = entries[i]
                if i == 0 and initial_reading is not None:
                    diff = val - initial_reading
                    lines.append(
                        f"{dt.strftime('%d/%m/%y %H:%M')} — {val} {unit}\n"
                        f"└─ Разница с начальными показаниями: {diff:+.2f} {unit}"
                    )
                else:
                    prev_val = entries[i - 1][1]
                    diff = val - prev_val
                    lines.append(
                        f"{dt.strftime('%d/%m/%y %H:%M')} — {val} {unit}\n"
                        f"└─ Разница: {diff:+.2f} {unit}"
                    )

            message_text = "📜 История показаний:\n" + "\n".join(lines)
            if len(message_text) > 4000:
                parts = [message_text[i:i+4000] for i in range(0, len(message_text), 4000)]
                for part in parts:
                    await message.answer(part)
            else:
                await message.answer(message_text)
        else:
            await message.answer("📭 История пуста.")
    except Exception as e:
        await message.answer(f"⚠️ Ошибка: {e}")


# =======================================================
# === 🧱 БЛОК 27: Общая функция вывода истории оплат =====
# =======================================================

async def show_payment_history(message: Message, counter_type: str):
    try:
        user_id = str(message.from_user.id)
        data_file = Path("storage/data.json")
        entries = []

        if data_file.exists():
            with open(data_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            if user_id in data:
                for date_str, items in data[user_id].items():
                    # поддержка формата с датой и временем
                    try:
                        dt = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
                    except ValueError:
                        try:
                            dt = datetime.strptime(date_str, "%Y-%m-%d")
                        except ValueError:
                            continue
                    key = f"{counter_type}_оплата"
                    if key in items:
                        val = items[key]
                        entries.append((dt, val))

        # берём последние 12 записей, сортируем по дате
        last_entries = sorted(entries)[-12:]
        if last_entries:
            lines = [
                f"{dt.strftime('%d/%m/%y %H:%M')} — {val} грн"
                for dt, val in last_entries
            ]
            await message.answer("🧾 История оплат:\n" + "\n".join(lines))
        else:
            await message.answer("📭 История оплат пуста.")
    except Exception as e:
        await message.answer(f"⚠️ Ошибка: {e}")


# =======================================================
# === 🧱 БЛОК 28: История оплат ⚡ Электроэнергия =========
# =======================================================

@dp.message(lambda message: message.text == "🧾 История оплат (электроэнергия)")
async def electricity_payment_history(message: Message):
    await show_payment_history(message, "электроэнергия")


# =======================================================
# === 🧱 БЛОК 29: История оплат 💧 Вода ==================
# =======================================================

@dp.message(lambda message: message.text == "🧾 История оплат (вода)")
async def water_payment_history(message: Message):
    await show_payment_history(message, "вода")


# =======================================================
# === 🧱 БЛОК 30: История оплат 🔥 Газ ===================
# =======================================================

@dp.message(lambda message: message.text == "🧾 История оплат (газ)")
async def gas_payment_history(message: Message):
    await show_payment_history(message, "газ")    


# =======================================================
# === 🧱 БЛОК 31: FSM-состояния для ввода тарифов ========
# =======================================================

class TariffState(StatesGroup):
    electricity = State()
    water = State()
    gas = State()


# =======================================================
# === 🧱 БЛОК 32: Ввод тарифа ⚡ Электроэнергия ==========
# =======================================================

@dp.message(lambda message: message.text == "💰 Ввести тариф за свет")
async def start_electricity_tariff(message: Message, state: FSMContext):
    await state.set_state(TariffState.electricity)
    await message.answer("Введите тариф за электроэнергию (грн/кВт⋅ч):")

@dp.message(TariffState.electricity)
async def save_electricity_tariff(message: Message, state: FSMContext):
    await save_tariff(message, state, "электроэнергия")
    await state.clear()


# =======================================================
# === 🧱 БЛОК 33: Ввод тарифа 💧 Вода ====================
# =======================================================

@dp.message(lambda message: message.text == "💰 Ввести тариф за воду")
async def start_water_tariff(message: Message, state: FSMContext):
    await state.set_state(TariffState.water)
    await message.answer("Введите тариф за воду (грн/м³):")

@dp.message(TariffState.water)
async def save_water_tariff(message: Message, state: FSMContext):
    await save_tariff(message, state, "вода")
    await state.clear()


# =======================================================
# === 🧱 БЛОК 34: Ввод тарифа 🔥 Газ =====================
# =======================================================

@dp.message(lambda message: message.text == "💰 Ввести тариф за газ")
async def start_gas_tariff(message: Message, state: FSMContext):
    await state.set_state(TariffState.gas)
    await message.answer("Введите тариф за газ (грн/м³):")

@dp.message(TariffState.gas)
async def save_gas_tariff(message: Message, state: FSMContext):
    await save_tariff(message, state, "газ")
    await state.clear()


# =======================================================
# === 🧱 БЛОК 35: Общая функция сохранения тарифа =======
# =======================================================

async def save_tariff(message: Message, state: FSMContext, counter_type: str):
    try:
        # Заменяем запятую на точку для корректного преобразования в число
        tariff = float(message.text.strip().replace(',', '.'))
        user_id = str(message.from_user.id)
        data_file = Path("storage/data.json")

        if data_file.exists():
            with open(data_file, "r", encoding="utf-8") as f:
                data = json.load(f)
        else:
            data = {}

        if user_id not in data:
            data[user_id] = {}
        if "тарифы" not in data[user_id]:
            data[user_id]["тарифы"] = {}

        # Сохраняем тариф в отдельной секции
        tariff_key = f"{counter_type}_тариф"
        data[user_id]["тарифы"][tariff_key] = tariff

        with open(data_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        await message.answer(f"✅ Тариф сохранён: {tariff} грн")
    except ValueError:
        await message.answer("⚠️ Ошибка: введите корректное число")
    except Exception as e:
        await message.answer(f"⚠️ Ошибка: {e}")


# =======================================================
# === 🧱 БЛОК 36: Обработка кнопки ⚙ Настройки ==========
# =======================================================

@dp.message(lambda message: message.text == "⚙ Настройки")
async def settings_menu_handler(message: Message):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="⚡ Настройки электроэнергии")],
            [KeyboardButton(text="💧 Настройки воды")],
            [KeyboardButton(text="🔥 Настройки газа")],
            [KeyboardButton(text="🗑 Очистить данные")],
            [KeyboardButton(text="🔙 Назад")],
        ],
        resize_keyboard=True
    )
    await message.answer(
        "⚙ Настройки.\nВыберите раздел для настройки:",
        reply_markup=keyboard
    )


# =======================================================
# === 🧱 БЛОК 36.1: Подменю очистки данных по ресурсам ==
# =======================================================

@dp.message(lambda message: message.text == "🗑 Очистить данные")
async def clear_data_menu(message: Message):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🗑 Очистить данные (электроэнергия)")],
            [KeyboardButton(text="🗑 Очистить данные (вода)")],
            [KeyboardButton(text="🗑 Очистить данные (газ)")],
            [KeyboardButton(text="🔙 К настройкам")],
        ],
        resize_keyboard=True
    )
    await message.answer(
        "Выберите, данные какого ресурса нужно очистить:",
        reply_markup=keyboard
    )


# =======================================================
# === 🧱 БЛОК 37: Подменю ⚡ Настройки электроэнергии ====
# =======================================================

@dp.message(lambda message: message.text == "⚡ Настройки электроэнергии")
async def electricity_settings_handler(message: Message):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📝 Внести начальные показания электроэнергии")],
            [KeyboardButton(text="💰 Внести начальный долг за электроэнергию")],
            [KeyboardButton(text="💰 Ввести тариф за свет")],
            [KeyboardButton(text="⏰ Установить напоминание (электроэнергия)")],
            [KeyboardButton(text="🔙 К настройкам")],
        ],
        resize_keyboard=True
    )
    await message.answer(
        "⚡ Настройки электроэнергии.\nВыберите действие:",
        reply_markup=keyboard
    )


# =======================================================
# === 🧱 БЛОК 38: Подменю 💧 Настройки воды ==============
# =======================================================

@dp.message(lambda message: message.text == "💧 Настройки воды")
async def water_settings_handler(message: Message):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📝 Внести начальные показания воды")],
            [KeyboardButton(text="💰 Внести начальный долг за воду")],
            [KeyboardButton(text="💰 Ввести тариф за воду")],
            [KeyboardButton(text="⏰ Установить напоминание (вода)")],
            [KeyboardButton(text="🔙 К настройкам")],
        ],
        resize_keyboard=True
    )
    await message.answer(
        "💧 Настройки воды.\nВыберите действие:",
        reply_markup=keyboard
    )


# =======================================================
# === 🧱 БЛОК 39: Подменю 🔥 Настройки газа ==============
# =======================================================

@dp.message(lambda message: message.text == "🔥 Настройки газа")
async def gas_settings_handler(message: Message):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📝 Внести начальные показания газа")],
            [KeyboardButton(text="💰 Внести начальный долг за газ")],
            [KeyboardButton(text="💰 Ввести тариф за газ")],
            [KeyboardButton(text="⏰ Установить напоминание (газ)")],
            [KeyboardButton(text="🔙 К настройкам")],
        ],
        resize_keyboard=True
    )
    await message.answer(
        "🔥 Настройки газа.\nВыберите действие:",
        reply_markup=keyboard
    )


# =======================================================
# === 🧱 БЛОК 40: FSM-состояния для ввода начальных данных
# =======================================================

class SettingsState(StatesGroup):
    electricity_initial = State()
    electricity_debt = State()
    water_initial = State()
    water_debt = State()
    gas_initial = State()
    gas_debt = State()


# =======================================================
# === 🧱 БЛОК 40.1: FSM для установки напоминаний =======
# =======================================================

class ReminderState(StatesGroup):
    electricity = State()
    water = State()
    gas = State()


@dp.message(lambda message: message.text == "⏰ Установить напоминание (электроэнергия)")
async def set_reminder_electricity(message: Message, state: FSMContext):
    await state.set_state(ReminderState.electricity)
    await message.answer("⏰ Введите день и время напоминания для электроэнергии через пробел:\n<b>01 08:00</b>")


@dp.message(ReminderState.electricity)
async def save_reminder_electricity(message: Message, state: FSMContext):
    await save_reminder_time(message, state, "электроэнергия")


@dp.message(lambda message: message.text == "⏰ Установить напоминание (вода)")
async def set_reminder_water(message: Message, state: FSMContext):
    await state.set_state(ReminderState.water)
    await message.answer("⏰ Введите день и время напоминания для воды через пробел:\n<b>01 08:00</b>")


@dp.message(ReminderState.water)
async def save_reminder_water(message: Message, state: FSMContext):
    await save_reminder_time(message, state, "вода")


@dp.message(lambda message: message.text == "⏰ Установить напоминание (газ)")
async def set_reminder_gas(message: Message, state: FSMContext):
    await state.set_state(ReminderState.gas)
    await message.answer("⏰ Введите день и время напоминания для газа через пробел:\n<b>01 08:00</b>")


@dp.message(ReminderState.gas)
async def save_reminder_gas(message: Message, state: FSMContext):
    await save_reminder_time(message, state, "газ")


# =======================================================
# === 🧱 БЛОК 40.2: сохранение напоминания   (NEW) ======
# =======================================================
#
# • При каждой установке стираем служебные поля
#   next_try / last_sent, чтобы цикл начал работу с «чистого листа».
# • Логика ввода (день-время) не менялась.
#
async def save_reminder_time(message: Message, state: FSMContext, counter_type: str):
    try:
        from datetime import datetime
        from pathlib import Path
        import json

        day_str, time_str = message.text.strip().split()
        day = int(day_str)
        if not (1 <= day <= 31):
            raise ValueError("Недопустимый день")

        datetime.strptime(time_str, "%H:%M")  # проверка формата HH:MM

        user_id = str(message.from_user.id)
        data_file = Path("storage/data.json")

        if data_file.exists():
            with open(data_file, "r", encoding="utf-8") as f:
                data = json.load(f)
        else:
            data = {}

        settings = data.setdefault(user_id, {}).setdefault("настройки", {})

        key = f"{counter_type}_напоминание"
        cfg = settings.setdefault(key, {})
        cfg["день"] = day
        cfg["время"] = time_str
        # — сброс служебных полей —
        cfg.pop("next_try", None)
        cfg.pop("last_sent", None)

        with open(data_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        await message.answer(
            f"✅ Напоминание для «{counter_type}» установлено: "
            f"{day} числа каждого месяца в {time_str}"
        )
    except ValueError:
        await message.answer(
            "⚠️ Неверный ввод. Пример правильного формата:\n<b>01 08:00</b>"
        )
    except Exception as e:
        await message.answer(f"⚠️ Ошибка при сохранении: {e}")
    finally:
        await state.clear()


# =======================================================
# === 🧱 БЛОК 41: Ввод начальных показаний ⚡ Электроэнергия
# =======================================================

@dp.message(lambda message: message.text == "📝 Внести начальные показания электроэнергии")
async def start_electricity_initial(message: Message, state: FSMContext):
    await state.set_state(SettingsState.electricity_initial)
    await message.answer("Введите начальные показания счётчика электроэнергии (кВт⋅ч):")

@dp.message(SettingsState.electricity_initial)
async def save_electricity_initial(message: Message, state: FSMContext):
    await save_initial_reading(message, state, "электроэнергия")


# =======================================================
# === 🧱 БЛОК 42: Ввод начальных показаний 💧 Вода =========
# =======================================================

@dp.message(lambda message: message.text == "📝 Внести начальные показания воды")
async def start_water_initial(message: Message, state: FSMContext):
    await state.set_state(SettingsState.water_initial)
    await message.answer("Введите начальные показания счётчика воды (м³):")

@dp.message(SettingsState.water_initial)
async def save_water_initial(message: Message, state: FSMContext):
    await save_initial_reading(message, state, "вода")


# =======================================================
# === 🧱 БЛОК 43: Ввод начальных показаний 🔥 Газ ==========
# =======================================================

@dp.message(lambda message: message.text == "📝 Внести начальные показания газа")
async def start_gas_initial(message: Message, state: FSMContext):
    await state.set_state(SettingsState.gas_initial)
    await message.answer("Введите начальные показания счётчика газа (м³):")

@dp.message(SettingsState.gas_initial)
async def save_gas_initial(message: Message, state: FSMContext):
    await save_initial_reading(message, state, "газ")


# =======================================================
# === 🧱 БЛОК 44: Ввод начального долга ⚡ Электроэнергия ==
# =======================================================

@dp.message(lambda message: message.text == "💰 Внести начальный долг за электроэнергию")
async def start_electricity_debt(message: Message, state: FSMContext):
    await state.set_state(SettingsState.electricity_debt)
    await message.answer("Введите сумму начального долга за электроэнергию (грн):")

@dp.message(SettingsState.electricity_debt)
async def save_electricity_debt(message: Message, state: FSMContext):
    await save_initial_debt(message, state, "электроэнергия")


# =======================================================
# === 🧱 БЛОК 45: Ввод начального долга 💧 Вода ============
# =======================================================

@dp.message(lambda message: message.text == "💰 Внести начальный долг за воду")
async def start_water_debt(message: Message, state: FSMContext):
    await state.set_state(SettingsState.water_debt)
    await message.answer("Введите сумму начального долга за воду (грн):")

@dp.message(SettingsState.water_debt)
async def save_water_debt(message: Message, state: FSMContext):
    await save_initial_debt(message, state, "вода")


# =======================================================
# === 🧱 БЛОК 46: Ввод начального долга 🔥 Газ =============
# =======================================================

@dp.message(lambda message: message.text == "💰 Внести начальный долг за газ")
async def start_gas_debt(message: Message, state: FSMContext):
    await state.set_state(SettingsState.gas_debt)
    await message.answer("Введите сумму начального долга за газ (грн):")

@dp.message(SettingsState.gas_debt)
async def save_gas_debt(message: Message, state: FSMContext):
    await save_initial_debt(message, state, "газ")


# =======================================================
# === 🧱 БЛОК 47: Сохранение начальных показаний ==========
# =======================================================

async def save_initial_reading(message: Message, state: FSMContext, counter_type: str):
    try:
        value = float(message.text.strip().replace(',', '.'))
        user_id = str(message.from_user.id)
        data_file = Path("storage/data.json")
        import json
        if data_file.exists():
            with open(data_file, "r", encoding="utf-8") as f:
                data = json.load(f)
        else:
            data = {}
        if user_id not in data:
            data[user_id] = {}
        if "настройки" not in data[user_id]:
            data[user_id]["настройки"] = {}
        data[user_id]["настройки"][f"{counter_type}_показания"] = value
        with open(data_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        await message.answer(f"✅ Начальные показания {counter_type} сохранены: {value}")
    except ValueError:
        await message.answer("⚠️ Ошибка: введите корректное число")
    except Exception as e:
        await message.answer(f"⚠️ Ошибка: {e}")
    finally:
        await state.clear()


# =======================================================
# === 🧱 БЛОК 48: Сохранение начального долга =============
# =======================================================

async def save_initial_debt(message: Message, state: FSMContext, counter_type: str):
    try:
        value = float(message.text.strip().replace(',', '.'))
        user_id = str(message.from_user.id)
        data_file = Path("storage/data.json")
        import json
        if data_file.exists():
            with open(data_file, "r", encoding="utf-8") as f:
                data = json.load(f)
        else:
            data = {}
        if user_id not in data:
            data[user_id] = {}
        if "настройки" not in data[user_id]:
            data[user_id]["настройки"] = {}
        data[user_id]["настройки"][f"{counter_type}_долг"] = value
        with open(data_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        await message.answer(f"✅ Начальный долг за {counter_type} сохранён: {value} грн")
    except ValueError:
        await message.answer("⚠️ Ошибка: введите корректное число")
    except Exception as e:
        await message.answer(f"⚠️ Ошибка: {e}")
    finally:
        await state.clear()


# =======================================================
# === 🧱 БЛОК 49: Очистка данных по типу счётчика =======
# =======================================================

@dp.message(lambda message: message.text in [
    "🗑 Очистить данные (электроэнергия)",
    "🗑 Очистить данные (вода)",
    "🗑 Очистить данные (газ)",
])
async def clear_counter_data(message: Message):
    try:
        mapping = {
            "🗑 Очистить данные (электроэнергия)": "электроэнергия",
            "🗑 Очистить данные (вода)": "вода",
            "🗑 Очистить данные (газ)": "газ"
        }
        counter_type = mapping.get(message.text)
        if not counter_type:
            await message.answer("⚠️ Неизвестный тип счетчика")
            return

        user_id = str(message.from_user.id)
        data_file = Path("storage/data.json")

        if data_file.exists():
            with open(data_file, "r", encoding="utf-8") as f:
                data = json.load(f)

            if user_id in data:
                dates_to_remove = []
                for date, items in data[user_id].items():
                    if isinstance(items, dict) and date not in ["тарифы", "настройки"]:
                        has_counter_data = False

                        # Проверка наличия показаний, оплат и начислений
                        if (counter_type in items or
                            f"{counter_type}_оплата" in items or
                            ("начисления" in items and counter_type in items["начисления"])):
                            has_counter_data = True

                        # Если только один тип данных — можно удалить полностью
                        if has_counter_data and len(items) == 1:
                            dates_to_remove.append(date)
                        elif has_counter_data:
                            items.pop(counter_type, None)
                            items.pop(f"{counter_type}_оплата", None)
                            if "начисления" in items:
                                items["начисления"].pop(counter_type, None)
                                if not items["начисления"]:
                                    del items["начисления"]

                for date in dates_to_remove:
                    del data[user_id][date]

                with open(data_file, "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)

                await message.answer(f"✅ Данные по '{counter_type}' успешно очищены")
            else:
                await message.answer("ℹ️ Нет данных для очистки")
        else:
            await message.answer("ℹ️ Нет данных для очистки")
    except Exception as e:
        await message.answer(f"⚠️ Ошибка при очистке данных: {e}")


# =======================================================
# === 🧱 БЛОК 50: Кнопка возврата 🔙 К настройкам ======
# =======================================================

@dp.message(lambda message: message.text == "🔙 К настройкам")
async def back_to_settings_menu(message: Message):
    await settings_menu_handler(message)


# ==============================================
# === 🧱 БЛОК 51: Запуск бота на сервере (Webhook)
# ==============================================

import os
import asyncio
from fastapi import FastAPI
from contextlib import asynccontextmanager
from aiogram.webhook.aiohttp_server import SimpleRequestHandler

from config import dp, bot, reminder_background_task  # убедись, что эти импорты у тебя уже есть

WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # например, https://yourbot.onrender.com/webhook

@asynccontextmanager
async def lifespan(app: FastAPI):
    await bot.set_webhook(WEBHOOK_URL)
    asyncio.create_task(reminder_background_task())
    print(f"✅ Webhook установлен: {WEBHOOK_URL}")
    yield
    await bot.delete_webhook()
    print("🔻 Webhook удалён")

app = FastAPI(lifespan=lifespan)

# Обработка входящих запросов от Telegram
SimpleRequestHandler(dispatcher=dp, bot=bot).register(app, path=WEBHOOK_PATH)

# Основной запуск
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 10000)))


# =======================================================
# === 🧱 БЛОК 51.1: Фоновая задача по напоминаниям v2 ===
# =======================================================
#
#  • Ночная «тишина» 22:00 – 08:00 (Europe/Kyiv ± user TZ)
#  • Повтор каждые 4 ч → next_try
#  • «Мягкое» уведомление, если показания < 2 суток
#  • Сброс next_try после ввода новых показаний (см. блок 14)
#
# В settings["<ресурс>_напоминание"] теперь храним:
#   {"день": 21, "время": "17:30", "next_try": "...", "last_sent": "..."}
#
import asyncio
from datetime import datetime, timedelta, time as dtime
from pathlib import Path
import json
from zoneinfo import ZoneInfo
from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
import os
BOT_TOKEN = os.getenv("BOT_TOKEN")

# ————————————————————————————————————————————————
BOT = Bot(token=BOT_TOKEN,
          default=DefaultBotProperties(parse_mode=ParseMode.HTML))

TZ_FALLBACK = ZoneInfo("Europe/Kyiv")
NIGHT_START = 22  # 22:00
NIGHT_END = 8     # 08:00
CHECK_INTERVAL = 60  # сек

EMOJI = {"электроэнергия": "⚡",
         "вода": "💧",
         "газ": "🔥"}


def is_night(dt: datetime) -> bool:
    """22:00 ≤ t < 24:00  or  00:00 ≤ t < 08:00."""
    return dt.hour >= NIGHT_START or dt.hour < NIGHT_END


def bump_to_morning(dt: datetime) -> datetime:
    """Перенести dt на ближайшие 08:00 local morning."""
    if dt.hour >= NIGHT_START:
        dt = (dt + timedelta(days=1)).replace(hour=NIGHT_END, minute=0,
                                              second=0, microsecond=0)
    else:  # среди ночи
        dt = dt.replace(hour=NIGHT_END, minute=0,
                        second=0, microsecond=0)
    return dt


async def reminder_background_task():
    lock = asyncio.Lock()          # защита от одновременной записи
    data_file = Path("storage/data.json")

    while True:
        try:
            if not data_file.exists():
                await asyncio.sleep(CHECK_INTERVAL)
                continue

            async with lock:
                with open(data_file, "r", encoding="utf-8") as f:
                    data = json.load(f)

            from datetime import UTC                 # в начале файла, рядом с другими import
            now_utc = datetime.now(UTC)              # объект сразу «aware»
            updated = False

            # ======= Цикл по пользователям =========
            for user_id, user_data in data.items():
                if not isinstance(user_data, dict):
                    continue

                # попытка вытащить ТZ, если ранее сохраняли
                user_tz = ZoneInfo(
                    user_data.get("настройки", {}).get("tz", "UTC"))
                if str(user_tz) == "UTC":
                    user_tz = TZ_FALLBACK

                now = now_utc.astimezone(user_tz)
                current_day = now.day

                settings = user_data.setdefault("настройки", {})
                for resource in ("электроэнергия", "вода", "газ"):
                    cfg = settings.get(f"{resource}_напоминание")
                    if not cfg or not isinstance(cfg, dict):
                        continue

                    # --- плановое время текущего месяца ---
                    if cfg.get("день") != current_day:
                        continue

                    try:
                        hh, mm = map(int, cfg["время"].split(":"))
                        plan_dt = now.replace(hour=hh, minute=mm,
                                              second=0, microsecond=0)
                    except Exception:
                        continue  # некорректное «время»

                    # --- следующий слот ---
                    next_try = None
                    if "next_try" in cfg:
                        try:
                            next_try = datetime.fromisoformat(
                                cfg["next_try"]).astimezone(user_tz)
                        except ValueError:
                            cfg.pop("next_try", None)

                    # due_to_send? ------------------------------------------------
                    due = False
                    if next_try:
                        if now >= next_try:
                            due = True
                    else:  # первая попытка
                        if abs((now - plan_dt).total_seconds()) <= 120:
                            due = True

                    if not due:
                        continue

                    # ночное окно? переносим, но пишем next_try
                    if is_night(now):
                        cfg["next_try"] = bump_to_morning(now).isoformat()
                        updated = True
                        continue

                    # «мягкое»? ищем дату последнего показания
                    last_read_dt = None
                    for date_str in sorted(user_data.keys(), reverse=True):
                        if date_str in ("тарифы", "настройки"):
                            continue
                        if resource in user_data[date_str]:
                            try:
                                last_read_dt = datetime.strptime(
                                    date_str, "%Y-%m-%d %H:%M:%S")
                            except ValueError:
                                try:
                                    last_read_dt = datetime.strptime(
                                        date_str, "%Y-%m-%d")
                                except ValueError:
                                    pass
                            break

                    soft = (last_read_dt and
                            (now - last_read_dt).days < 2)

                    if soft:
                        msg = (f"⏰ Напоминание!\n"
                               f"{EMOJI[resource]} Вы вносили показания "
                               f"<b>{last_read_dt.strftime('%d.%m.%Y %H:%M')}</b>.\n"
                               f"При необходимости можно обновить.")
                    else:
                        msg = (f"⏰ Напоминание!\n"
                               f"{EMOJI[resource]} Пора внести показания "
                               f"за <b>{resource}</b>.")

                    # --- отправка ---------------------------------------------
                    try:
                        await BOT.send_message(int(user_id), msg)
                    except Exception as e:
                        print(f"❌ send_message {user_id}: {e}")

                    # --- записываем служебные поля ----------------------------
                    cfg["last_sent"] = now.isoformat()
                    nxt = now + timedelta(hours=4)
                    if is_night(nxt):
                        nxt = bump_to_morning(nxt)
                    cfg["next_try"] = nxt.isoformat()
                    updated = True

            # ======= запись файла при изменениях =========
            if updated:
                async with lock:
                    with open(data_file, "w", encoding="utf-8") as f:
                        json.dump(data, f, ensure_ascii=False, indent=2)

        except Exception as e:
            print(f"⚠️ reminder_background_task: {e}")

        await asyncio.sleep(CHECK_INTERVAL)




if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 10000)))
