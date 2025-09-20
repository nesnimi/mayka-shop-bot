# bot.py
import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    FSInputFile,
    InputMediaPhoto
)
from aiogram.filters import Command
import datetime
import os

# === НАСТРОЙКИ ===
TOKEN = "8326145485:AAGdTFDqyAXwY0A6HmF8vP5hoRbaU-k2Rfg"
TOKEN = os.getenv("BOT_TOKEN")  # ⚠️ СРОЧНО ЗАМЕНИТЕ НА СВОЙ ТОКЕН!
bot = Bot(token=TOKEN)
dp = Dispatcher()

# === ПРОВЕРКА ФАЙЛОВ ===
print("📁 Файлы в папке:", os.listdir("."))

# === ЛОГИРОВАНИЕ ===
def log_event(user_id: int, username: str, action: str):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{now}] Пользователь {username} (ID: {user_id}) → {action}")

# === БАЗА ТОВАРОВ ===
from products import PRODUCTS as products

# === КОРЗИНА И ЗАКАЗЫ ===
cart = {}  # cart[user_id] = [{"brand": "Nike", "product": product, "index": 0}, ...]
active_orders = []  # Список всех оформленных заказов

# === СПИСОК АДМИНОВ ===
ADMIN_IDS = {7335580942}  # ⚠️ Добавьте свои ID, например: {7335580942, 123456789}

# === ОТПРАВКА УВЕДОМЛЕНИЙ АДМИНАМ ===
async def notify_admins(text: str):
    for admin_id in ADMIN_IDS:
        try:
            await bot.send_message(admin_id, text, parse_mode="Markdown")
        except Exception as e:
            print(f"❌ Не удалось отправить сообщение админу {admin_id}: {e}")

# === ГЛАВНОЕ МЕНЮ (динамическое) ===
def main_menu(user_id: int):
    buttons = [
        [InlineKeyboardButton(text="🛍 Сделать Заказ", callback_data="menu_order")],
        [InlineKeyboardButton(text="🛒 Корзина", callback_data="view_cart")],
        [InlineKeyboardButton(text="📢 Официальный Канал", callback_data="menu_channel")],
        [InlineKeyboardButton(text="📞 Связь", callback_data="menu_contact")]
    ]
    if user_id in ADMIN_IDS:
        buttons.append([InlineKeyboardButton(text="🔐 Админ-панель", callback_data="admin_orders_page_0")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

# === СЕТКА БРЕНДОВ (2 в строке) ===
def get_brands_keyboard():
    brands = list(products.keys())
    keyboard = []
    for i in range(0, len(brands), 2):
        row = [
            InlineKeyboardButton(
                text=f"{brands[i]} [{len(products[brands[i]])}]",
                callback_data=f"brand_{brands[i]}"
            )
        ]
        if i + 1 < len(brands):
            row.append(InlineKeyboardButton(
                text=f"{brands[i+1]} [{len(products[brands[i+1]])}]",
                callback_data=f"brand_{brands[i+1]}"
            ))
        keyboard.append(row)
    keyboard.append([InlineKeyboardButton(text="⬅️ Назад", callback_data="menu_main")])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

# === КНОПКИ ТОВАРА ===
def get_product_keyboard(brand: str, index: int):
    total = len(products[brand])
    buttons = []

    # Листание
    if total > 1:
        nav_buttons = []
        if index > 0:
            nav_buttons.append(InlineKeyboardButton(text="⬅️", callback_data=f"prev_{brand}_{index}"))
        if index < total - 1:
            nav_buttons.append(InlineKeyboardButton(text="➡️", callback_data=f"next_{brand}_{index}"))
        if nav_buttons:
            buttons.append(nav_buttons)

    # Добавить в корзину
    buttons.append([InlineKeyboardButton(text="➕ Добавить в корзину", callback_data=f"add_{brand}_{index}")])

    # Корзина и назад
    buttons.append([
        InlineKeyboardButton(text="🛒 Корзина", callback_data="view_cart"),
        InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_brands")
    ])

    return InlineKeyboardMarkup(inline_keyboard=buttons)

# === /start ===
@dp.message(Command("start"))
async def start(message: Message):
    user_name = message.from_user.first_name or "Пользователь"
    log_event(message.from_user.id, user_name, "Начал взаимодействие (/start)")
    await message.answer(
        "👋 Добро пожаловать в *Mayka Shop*!\n\nВыберите действие:",
        reply_markup=main_menu(message.from_user.id),
        parse_mode="Markdown"
    )

# === ОБРАБОТКА МЕНЮ ===
@dp.callback_query(F.data.startswith("menu_"))
async def handle_menu(call: CallbackQuery):
    user_name = call.from_user.first_name or "Пользователь"
    log_event(call.from_user.id, user_name, f"Нажал кнопку: {call.data}")
    await call.answer()

    if call.data == "menu_order":
        try:
            await call.message.edit_media(media=None)
        except:
            pass
        await call.message.edit_text("💼 Выберите бренд:", reply_markup=get_brands_keyboard())

    elif call.data == "menu_channel":
        channel_link = "https://t.me/maykashop"
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Перейти в канал", url=channel_link)],
            [InlineKeyboardButton(text="⬅️ Назад", callback_data="menu_main")]
        ])
        try:
            await call.message.edit_media(media=None)
        except:
            pass
        await call.message.edit_text("🔔 Подпишитесь на наш официальный канал:", reply_markup=keyboard)

    elif call.data == "menu_contact":
        support_link = "https://t.me/M1HCK"
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="📩 Написать менеджеру", url=support_link)],
            [InlineKeyboardButton(text="⬅️ Назад", callback_data="menu_main")]
        ])
        try:
            await call.message.edit_media(media=None)
        except:
            pass
        await call.message.edit_text("📞 По всем вопросам — пишите менеджеру:", reply_markup=keyboard)

    elif call.data == "menu_main":
        try:
            await call.message.edit_media(media=None)
        except:
            pass
        await call.message.edit_text(
            "👋 Добро пожаловать в *Mayka Shop*!\n\nВыберите действие:",
            reply_markup=main_menu(call.from_user.id),
            parse_mode="Markdown"
        )

# === ПОКАЗ ПЕРВОГО ТОВАРА ===
@dp.callback_query(F.data.startswith("brand_"))
async def show_first_product(call: CallbackQuery):
    brand = call.data.split("_", 1)[1]
    if brand not in products:
        await call.answer("Бренд не найден")
        return
    await call.answer()
    await show_product(call, brand, 0)

# === ПОКАЗ ТОВАРА С ФОТО ===
async def show_product(call: CallbackQuery, brand: str, index: int):
    product = products[brand][index]
    total = len(products[brand])
    caption = f"""
<b>🖼️ {product['name']}</b>
<b>💰 Стоимость:</b> {product['price']}₽

{product['description']}
<b>📌 [{index + 1} из {total}]</b>

{product.get('more_photos', '')}
    """.strip()

    media = InputMediaPhoto(
        media=(product["image"]),
        caption=caption,
        parse_mode="HTML"
    )
    keyboard = get_product_keyboard(brand, index)

    try:
        await call.message.edit_media(media=media, reply_markup=keyboard)
    except Exception:
        sent = await call.message.answer_photo(
            photo=product["image"],
            caption=caption,
            reply_markup=keyboard,
            parse_mode="HTML"
        )
        await call.message.delete()

# === ЛИСТАНИЕ ===
@dp.callback_query(F.data.startswith("prev_"))
async def prev_product(call: CallbackQuery):
    _, brand, index_str = call.data.split("_")
    index = int(index_str) - 1
    if index < 0:
        await call.answer()
        return
    await call.answer()
    await show_product(call, brand, index)

@dp.callback_query(F.data.startswith("next_"))
async def next_product(call: CallbackQuery):
    _, brand, index_str = call.data.split("_")
    index = int(index_str) + 1
    if index >= len(products[brand]):
        await call.answer()
        return
    await call.answer()
    await show_product(call, brand, index)

# === ВОЗВРАТ К БРЕНДАМ ===
@dp.callback_query(F.data == "back_to_brands")
async def back_to_brands(call: CallbackQuery):
    await call.answer()
    try:
        await call.message.edit_media(media=None)
    except:
        pass
    try:
        await call.message.edit_text("💼 Выберите бренд:", reply_markup=get_brands_keyboard())
    except Exception:
        sent = await call.message.answer("💼 Выберите бренд:", reply_markup=get_brands_keyboard())
        await call.message.delete()

# === ДОБАВЛЕНИЕ В КОРЗИНУ ===
@dp.callback_query(F.data.startswith("add_"))
async def add_to_cart(call: CallbackQuery):
    _, brand, index_str = call.data.split("_")
    index = int(index_str)
    if brand not in products or index >= len(products[brand]):
        await call.answer("Товар не найден")
        return

    product = products[brand][index]
    user_id = call.from_user.id
    username = call.from_user.username
    full_name = call.from_user.full_name

    if user_id not in cart:
        cart[user_id] = []

    cart[user_id].append({"brand": brand, "product": product, "index": index})

    user_link = f"@{username}" if username else f"[{full_name}](tg://user?id={user_id})"
    await notify_admins(
        f"🛒 *Новое добавление в корзину*\n\n"
        f"Пользователь: {user_link}\n"
        f"Товар: {product['name']}\n"
        f"Цена: {product['price']}₽\n"
        f"Бренд: {brand}"
    )

    await call.answer(f"✅ {product['name']} добавлен в корзину!", show_alert=False)

# === ПРОСМОТР КОРЗИНЫ ===
@dp.callback_query(F.data == "view_cart")
async def view_cart_handler(call: CallbackQuery):
    user_id = call.from_user.id
    user_cart = cart.get(user_id, [])

    if not user_cart:
        await call.answer("🛒 Ваша корзина пуста")
        return

    total_price = sum(item["product"]["price"] for item in user_cart)
    text = "🛒 *Ваша корзина:*\n\n"
    for i, item in enumerate(user_cart, 1):
        text += f"{i}. {item['product']['name']} — {item['product']['price']}₽\n"
    text += f"\n💰 *Итого: {total_price}₽*"

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🗑 Очистить корзину", callback_data="clear_cart")],
        [InlineKeyboardButton(text="✅ Оформить заказ", callback_data="checkout")],
        [InlineKeyboardButton(text="⬅️ Назад к товарам", callback_data="back_to_brands")]
    ])

    # УБИРАЕМ ФОТО ПЕРЕД ПОКАЗОМ ТЕКСТА
    try:
        await call.message.edit_media(media=None)  # Удаляем фото
        await call.message.edit_text(text=text, reply_markup=keyboard, parse_mode="Markdown")
    except Exception:
        # Если не получилось — отправляем новое сообщение
        try:
            await call.message.delete()
        except:
            pass
        await call.message.answer(text=text, reply_markup=keyboard, parse_mode="Markdown")

# === ОЧИСТКА КОРЗИНЫ ===
@dp.callback_query(F.data == "clear_cart")
async def clear_cart(call: CallbackQuery):
    user_id = call.from_user.id
    cart.pop(user_id, None)
    await call.answer("🗑 Корзина очищена!")
    await back_to_brands(call)

# === ОФОРМЛЕНИЕ ЗАКАЗА ===
@dp.callback_query(F.data == "checkout")
async def checkout(call: CallbackQuery):
    user_id = call.from_user.id
    user_cart = cart.get(user_id, [])
    if not user_cart:
        await call.answer("Корзина пуста!")
        return
    total_price = sum(item["product"]["price"] for item in user_cart)
    items_list = "\n".join([f"• {item['product']['name']} — {item['product']['price']}₽" for item in user_cart])
    username = call.from_user.username
    full_name = call.from_user.full_name
    user_link = f"@{username}" if username else f"[{full_name}](tg://user?id={user_id})"
    
    # Сохраняем заказ
    order = {
        "user_id": user_id,
        "username": username,
        "full_name": full_name,
        "items": user_cart.copy(),
        "total": total_price,
        "status": "new"
    }
    active_orders.append(order)
    
    # Уведомляем админа
    await notify_admins(
        f"✅ *НОВЫЙ ЗАКАЗ*\n"
        f"Пользователь: {user_link}\n"
        f"Товары:\n{items_list}\n"
        f"💰 Итого: {total_price}₽"
    )
    
    # Очищаем корзину
    cart.pop(user_id, None)

    # Формируем текст и клавиатуру ДО попытки редактирования
    text = f"""
✅ *Заказ оформлен!*
Товары:
{items_list}
💰 Общая сумма: {total_price}₽
📦 Мы свяжемся с вами в течение 24 часов.
🚚 Доставка по России и СНГ.
Спасибо за покупку! 💼
    """.strip()

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⬅️ Вернуться к товарам", callback_data="menu_order")]
    ])

    # Пытаемся заменить сообщение
    try:
        # Сначала удаляем медиа (если есть), затем редактируем текст
        await call.message.edit_media(media=None)  # Может выбросить ошибку
        await call.message.edit_text(text=text, reply_markup=keyboard, parse_mode="Markdown")
    except Exception:
        # Если не получилось — удаляем старое и отправляем новое
        try:
            await call.message.delete()
        except:
            pass
        await call.message.answer(text=text, reply_markup=keyboard, parse_mode="Markdown")

    await call.answer()

# === АДМИН-ПАНЕЛЬ С ПАГИНАЦИЕЙ ===
@dp.callback_query(F.data.startswith("admin_orders_page_"))
async def admin_orders_page(call: CallbackQuery):
    if call.from_user.id not in ADMIN_IDS:
        await call.answer("❌ Доступ запрещён.")
        return

    page = int(call.data.split("_")[-1])

    if not active_orders:
        text = "📦 *Нет активных заказов*"
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🔄 Обновить", callback_data="admin_orders_page_0")],
            [InlineKeyboardButton(text="⬅️ Назад в меню", callback_data="menu_main")]
        ])
        try:
            await call.message.edit_text(text, reply_markup=keyboard, parse_mode="Markdown")
        except:
            await call.message.delete()
            await call.message.answer(text, reply_markup=keyboard, parse_mode="Markdown")
        return

    total_pages = len(active_orders)
    if page >= total_pages:
        page = total_pages - 1
    if page < 0:
        page = 0

    order = active_orders[page]
    user_link = f"@{order['username']}" if order['username'] else f"[{order['full_name']}](tg://user?id={order['user_id']})"
    items_text = "\n".join([f"• {item['product']['name']} — {item['product']['price']}₽" for item in order['items']])

    text = f"""
📦 *Заказ #{page + 1} из {total_pages}*

👤 Пользователь: {user_link}
🛒 Товары:
{items_text}
💰 Сумма: {order['total']}₽
    """.strip()

    # Кнопки навигации
    nav_buttons = []
    if page > 0:
        nav_buttons.append(InlineKeyboardButton(text="⬅️", callback_data=f"admin_orders_page_{page-1}"))
    nav_buttons.append(InlineKeyboardButton(text="✅ Выполнено", callback_data=f"admin_order_done_{page}"))
    if page < total_pages - 1:
        nav_buttons.append(InlineKeyboardButton(text="➡️", callback_data=f"admin_orders_page_{page+1}"))

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        nav_buttons,
        [InlineKeyboardButton(text="🔄 Обновить", callback_data="admin_orders_page_0")],
        [InlineKeyboardButton(text="⬅️ Назад в меню", callback_data="menu_main")]
    ])

    try:
        await call.message.edit_text(text, reply_markup=keyboard, parse_mode="Markdown")
    except:
        await call.message.delete()
        await call.message.answer(text, reply_markup=keyboard, parse_mode="Markdown")

# === ОТМЕТИТЬ ЗАКАЗ КАК ВЫПОЛНЕННЫЙ ===
@dp.callback_query(F.data.startswith("admin_order_done_"))
async def admin_order_done(call: CallbackQuery):
    if call.from_user.id not in ADMIN_IDS:
        await call.answer("❌ У вас нет прав.")
        return

    page = int(call.data.split("_")[-1])
    if page >= len(active_orders):
        await call.answer("Заказ не найден")
        return

    order = active_orders.pop(page)
    user_link = f"@{order['username']}" if order['username'] else order['full_name']

    await call.answer("✅ Заказ отмечен как выполненный")
    await call.message.edit_text(
        f"✅ Заказ от пользователя {user_link} выполнен и удалён.",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="⬅️ Назад к заказам", callback_data="admin_orders_page_0")]
        ])
    )

# === ЗАПУСК ===
async def main():
    print("🚀 Бот запущен на aiogram 3.x")
    await dp.start_polling(bot, allowed_updates=["message", "callback_query"])

if __name__ == "__main__":
    asyncio.run(main())