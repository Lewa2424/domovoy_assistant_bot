from keep_alive import keep_alive
keep_alive()


# =======================================================
# === 🧱 БЛОК 1: Импорт всех библиотек и настроек ========
# =======================================================

import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import Command
import config


# =======================================================
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
        "Если ты зашел в первый раз, то загляни в ⚙️ <b>Настройки</b> и установи         текущие показания счётчиков и сумму долга (или переплаты).\n\n"
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
            [KeyboardButton(text="💰 Ввести тариф за свет")],
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
            [KeyboardButton(text="💰 Ввести тариф за воду")],
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
            [KeyboardButton(text="💰 Ввести тариф за газ")],
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
# === 🧱 БЛОК 14: Сохранение новых показаний счётчика ====
# =======================================================

async def save_reading(message: Message, state: FSMContext, counter_type: str):
    try:
        value = float(message.text.strip().replace(',', '.'))  # Поддержка запятой
        user_id = str(message.from_user.id)
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data_file = Path("storage/data.json")

        if data_file.exists():
            with open(data_file, "r", encoding="utf-8") as f:
                data = json.load(f)
        else:
            data = {}

        if user_id not in data:
            data[user_id] = {}

        # Используем now как уникальный ключ (дата+время)
        data[user_id][now] = {}

        # Предыдущее значение
        prev_value = get_last_value(user_id, counter_type) or 0
        data[user_id][now][counter_type] = value
        usage = value - prev_value if prev_value else 0

        # Получение тарифа из данных
        tariff_key = f"{counter_type}_тариф"
        tariff = data[user_id].get("тарифы", {}).get(tariff_key, 1.8)  # Значение по умолчанию 1.8
        cost = usage * tariff

        # Сохраняем начисление в тот же временной слот
        if "начисления" not in data[user_id][now]:
            data[user_id][now]["начисления"] = {}
        data[user_id][now]["начисления"][counter_type] = cost

        # Очистка старых записей
        await cleanup_old_records(user_id)

        # Сохранение
        with open(data_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        await message.answer(
            f"✅ Показания сохранены: {value}\n"
            f"📊 Расход: {usage:.2f} • Сумма: {cost:.2f} грн"
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

        for date, items in data[user_id].items():
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
            f"💰 Остаток: {remaining_debt:.2f} грн"
        ]

        # Добавляем уведомление о состоянии
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
            lines.append(f"🧮 Итоговый баланс: <b>{total_balance:.2f} грн</b>")
        elif total_balance < 0:
            lines.append(f"🧮 Переплата: <b>{abs(total_balance):.2f} грн</b>")
        else:
            lines.append(f"🧮 Всё оплачено: <b>0.00 грн</b> ✅")

        await message.answer("\n".join(lines))
    except Exception as e:
        await message.answer(f"⚠️ Ошибка: {e}")


# =======================================================
# === 🧱 БЛОК 24: Общая функция расчёта долга ===========
# =======================================================

async def show_debt(message: Message, counter_type: str):
    try:
        user_id = str(message.from_user.id)
        data_file = Path("storage/data.json")

        total = 0.0
        paid = 0.0
        initial_debt = 0.0

        if data_file.exists():
            with open(data_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            if user_id in data:
                # Получаем начальный долг из настроек
                if "настройки" in data[user_id]:
                    initial_debt = float(data[user_id]["настройки"].get(f"{counter_type}_долг", 0))

                # Собираем все начисления и оплаты
                for date, items in data[user_id].items():
                    if isinstance(items, dict):
                        # Учитываем начисления
                        if "начисления" in items and counter_type in items["начисления"]:
                            total += float(items["начисления"][counter_type])

                        # Учитываем оплаты
                        payment_key = f"{counter_type}_оплата"
                        if payment_key in items:
                            paid += float(items[payment_key])

        # Добавляем начальный долг к общей сумме
        total += initial_debt
        debt = total - paid

        await message.answer(
            f"📉 <b>{counter_type.capitalize()}</b>:\n"
            f"Начальный долг: {initial_debt:.2f} грн\n"
            f"Начислено: {(total - initial_debt):.2f} грн\n"
            f"Оплачено: {paid:.2f} грн\n"
            f"Итоговый долг: <b>{debt:.2f} грн</b>"
        )
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
                        initial_date = datetime.min  # Для правильной сортировки
                        entries.append((initial_date, initial_reading))

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

        # Сортируем все записи по дате
        entries.sort()

        # Формируем вывод с разницей между показаниями
        if entries:
            lines = []
            if initial_reading is not None:
                lines.append(f"📌 Начальное показание: {initial_reading} {unit}")

            for i in range(len(entries)):
                dt, val = entries[i]
                if dt == datetime.min:  # Пропускаем начальное показание в основном списке
                    continue

                # Расчет разницы с предыдущим показанием
                prev_val = entries[i-1][1] if i > 0 else initial_reading or val
                diff = val - prev_val

                lines.append(
                    f"{dt.strftime('%d/%m/%y %H:%M')} — {val} {unit}\n"
                    f"└─ Разница: {diff:+.2f} {unit}"
                )

            message_text = "📜 История показаний:\n" + "\n".join(lines)
            # Если сообщение слишком длинное, разбиваем на части
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
    await message.answer("⏰ Введите день и время напоминания для электроэнергии через пробел:\n<b>20 08:00</b>")


@dp.message(ReminderState.electricity)
async def save_reminder_electricity(message: Message, state: FSMContext):
    await save_reminder_time(message, state, "электроэнергия")


@dp.message(lambda message: message.text == "⏰ Установить напоминание (вода)")
async def set_reminder_water(message: Message, state: FSMContext):
    await state.set_state(ReminderState.water)
    await message.answer("⏰ Введите день и время напоминания для воды через пробел:\n<b>20 08:00</b>")


@dp.message(ReminderState.water)
async def save_reminder_water(message: Message, state: FSMContext):
    await save_reminder_time(message, state, "вода")


@dp.message(lambda message: message.text == "⏰ Установить напоминание (газ)")
async def set_reminder_gas(message: Message, state: FSMContext):
    await state.set_state(ReminderState.gas)
    await message.answer("⏰ Введите день и время напоминания для газа через пробел:\n<b>20 08:00</b>")


@dp.message(ReminderState.gas)
async def save_reminder_gas(message: Message, state: FSMContext):
    await save_reminder_time(message, state, "газ")


# =======================================================
# === 🧱 БЛОК 40.2: Общая функция сохранения напоминания ==
# =======================================================

async def save_reminder_time(message: Message, state: FSMContext, counter_type: str):
    try:
        from datetime import datetime
        import json
        from pathlib import Path

        input_text = message.text.strip()
        parts = input_text.split()

        if len(parts) != 2:
            raise ValueError("Неверное количество компонентов")

        day_str, time_str = parts
        day = int(day_str)
        if not (1 <= day <= 31):
            raise ValueError("Недопустимый день месяца")

        # Проверка формата времени
        datetime.strptime(time_str, "%H:%M")

        user_id = str(message.from_user.id)
        data_file = Path("storage/data.json")

        if data_file.exists():
            with open(data_file, "r", encoding="utf-8") as f:
                data = json.load(f)
        else:
            data = {}

        if user_id not in data:
            data[user_id] = {}
        if "настройки" not in data[user_id]:
            data[user_id]["настройки"] = {}

        key = f"{counter_type}_напоминание"
        data[user_id]["настройки"][key] = {
            "день": day,
            "время": time_str
        }

        with open(data_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        await message.answer(f"✅ Напоминание для «{counter_type}» установлено: {day} числа каждого месяца в {time_str}")
    except ValueError:
        await message.answer("⚠️ Неверный формат. Введите день и время через пробел, например:\n<b>20 08:00</b>")
    except Exception as e:
        await message.answer(f"⚠️ Ошибка при сохранении напоминания: {e}")
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


# ===================================
# === 🧱 БЛОК 51: Запуск бота ========
# ===================================

async def main():
    try:
        me = await bot.get_me()
        print(f"✅ Бот @{me.username} запущен и готов к работе")

        asyncio.create_task(reminder_background_task())
        await dp.start_polling(bot)

    except asyncio.CancelledError:
        print("⚠️ Получен сигнал отмены asyncio. Завершаем...")

    except KeyboardInterrupt:
        print("🛑 Бот остановлен вручную")

    except Exception as e:
        print(f"❌ Неожиданная ошибка: {e}")

    finally:
        print("🔁 Все задачи завершены. До новых встреч!")


# =======================================================
# === 🧱 БЛОК 51.1: Фоновая задача по напоминаниям ======
# =======================================================

async def reminder_background_task():
    from datetime import datetime, timedelta
    import json
    from pathlib import Path

    CHECK_INTERVAL = 7200  # каждые 2 часа

    while True:
        try:
            data_file = Path("storage/data.json")
            if not data_file.exists():
                await asyncio.sleep(CHECK_INTERVAL)
                continue

            with open(data_file, "r", encoding="utf-8") as f:
                data = json.load(f)

            now = datetime.now()
            current_day = now.day
            current_time = now.strftime("%H:%M")

            updated = False  # чтобы не перезаписывать JSON без нужды

            for user_id, user_data in data.items():
                if not isinstance(user_data, dict):
                    continue

                settings = user_data.setdefault("настройки", {})
                sent_flags = settings.setdefault("напоминания_отправлены", {})

                for resource in ["электроэнергия", "вода", "газ"]:
                    reminder_key = f"{resource}_напоминание"
                    if reminder_key not in settings:
                        continue

                    reminder_config = settings.get(reminder_key)
                    if not isinstance(reminder_config, dict):
                        continue  # устаревший формат

                    if (
                        reminder_config.get("день") != current_day or
                        reminder_config.get("время") != current_time
                    ):
                        continue  # не сегодня или не сейчас

                    # Проверка последнего напоминания
                    last_sent_str = sent_flags.get(resource)
                    last_sent_dt = None
                    if last_sent_str:
                        try:
                            last_sent_dt = datetime.strptime(last_sent_str, "%Y-%m-%d %H:%M")
                        except ValueError:
                            pass

                    if last_sent_dt and (now - last_sent_dt).days < 5:
                        continue  # уже напоминали недавно

                    # Ищем последние показания
                    last_date = None
                    for date_str in sorted(user_data.keys(), reverse=True):
                        if date_str in ["тарифы", "настройки"]:
                            continue
                        if resource in user_data[date_str]:
                            try:
                                last_date = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
                            except ValueError:
                                try:
                                    last_date = datetime.strptime(date_str, "%Y-%m-%d")
                                except ValueError:
                                    continue
                            break

                    if not last_date or (now - last_date).days >= 2:
                        try:
                            from config import BOT_TOKEN
                            from aiogram import Bot
                            bot = Bot(token=BOT_TOKEN, parse_mode="HTML")

                            emojis = {
                                "электроэнергия": "⚡",
                                "вода": "💧",
                                "газ": "🔥"
                            }

                            text = (
                                f"⏰ Напоминание!\n"
                                f"{emojis[resource]} Пора внести показания за <b>{resource}</b>.\n"
                                f"Если уже внесли — это уведомление исчезнет."
                            )
                            await bot.send_message(chat_id=user_id, text=text)

                            # Обновляем флаг
                            sent_flags[resource] = now.strftime("%Y-%m-%d %H:%M")
                            updated = True
                        except Exception as e:
                            print(f"❌ Ошибка отправки напоминания: {e}")

            if updated:
                with open(data_file, "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)

        except Exception as e:
            print(f"⚠️ Ошибка в фоновой задаче: {e}")

        await asyncio.sleep(CHECK_INTERVAL)





if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass  # уже обработано в main()
