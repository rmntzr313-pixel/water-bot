import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# بياناتك الصحيحة
API_TOKEN = '8639015999:AAGWSlRzBmV5nQLoG_Mam2Ym2s41NE4A6hQ'
GROUP_ID = -1003398516819

bot = telebot.TeleBot(API_TOKEN)

# حذف الويب هوك لضمان التشغيل على السيرفر
bot.delete_webhook()

@bot.message_handler(func=lambda message: True)
def handle_orders(message):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("تم التنزيل ✅", callback_data="pre_done"), 
               InlineKeyboardButton("إلغاء ❌", callback_data="pre_cancel"))
    try:
        bot.send_message(GROUP_ID, f"📦 طلب جديد من المحاسب:\n\n{message.text}", reply_markup=markup)
        bot.reply_to(message, "✅ تم إرسال الطلب للعمال.")
    except Exception as e:
        print(f"Error: {e}")

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    bot.answer_callback_query(call.id)
    user_name = call.from_user.first_name
    
    if call.data == "pre_done":
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("نعم، أكدت التنزيل 👍", callback_data="final_delete"),
                   InlineKeyboardButton("تراجع 🔙", callback_data="back_home"))
        bot.edit_message_text(f"⚠️ {user_name}، متأكد من الإتمام؟\n{call.message.text}", call.message.chat.id, call.message.id, reply_markup=markup)

    elif call.data == "pre_cancel":
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("نعم، أريد الإلغاء ❌", callback_data="final_delete"),
                   InlineKeyboardButton("تراجع 🔙", callback_data="back_home"))
        bot.edit_message_text(f"⚠️ {user_name}، متأكد من الإلغاء؟\n{call.message.text}", call.message.chat.id, call.message.id, reply_markup=markup)

    elif call.data == "final_delete":
        try:
            bot.delete_message(call.message.chat.id, call.message.id)
        except:
            pass

    elif call.data == "back_home":
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("تم التنزيل ✅", callback_data="pre_done"), 
                   InlineKeyboardButton("إلغاء ❌", callback_data="pre_cancel"))
        bot.edit_message_text(f"📦 طلب جديد:\n{call.message.text.split('؟')[-1]}", call.message.chat.id, call.message.id, reply_markup=markup)

bot.infinity_polling()
