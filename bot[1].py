#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import os, asyncio
import random as ra
from pyrogram import Client, filters, errors
from pyrogram.raw import functions, types

bot_token = "توکن"
sudo = ایدی ادمین
login_temp_list = {}

if not os.path.isdir('sessions') : os.mkdir('sessions')
if not os.path.isdir('downloads') : os.mkdir('downloads')
if not os.path.exists('downloads/time.txt') :
    with open('downloads/time.txt', 'w', encoding="utf-8") as file :
        file.write('5')

async def sleep(time):
    await asyncio.sleep(time)


def app_info() :
    with open('app_info.txt', 'r') as file :
        return ra.choice(file.read().split('\n')).split()

def getAccount() :
    return [f.split('.')[0] for f in os.listdir('sessions') if os.path.isfile(os.path.join('sessions', f))]

bot = Client(
    "bot",
    bot_token = bot_token,
    api_id = "12176206",
    api_hash = "b8eff20a7e8adcdaa3daa3bc789a5b41"
)

@bot.on_message(filters.command(["start"]) & filters.chat(sudo))
def __start__(client, message):
    bot.send_message(message.from_user.id, '''<b>- به پنل مدیریت ربات اسپمر خوش آمدید.</b>

🔸 برای ذخیره خشاب روی یک فایل txt ریپلی کنید و از دستور زیر استفاده کنید :
<code>/save</code>
🔹 برای افزودن کپشن به جملات هنگام اسپم از دستور زیر استفاده کنید :
<code>/cap TEXT</code>
🔸 برای حذف کپشن از دستور زیر استفاده کنید :
<code>/delcap</code>
🔹 برای جوین دادن تمام اکانت ها به یک گروه از دستور زیر استفاده کنید :
<code>/join</code> LINK | ID
🔸 برای لفت دادن تمام اکانت ها از دستور زیر استفاده کنید :
<code>/leave</code> ID
🔹 برای تنظیم زمان اسپم به ثانیه از دستور زیر استفاده کنید :
<code>/time</code> 15
🔸 برای شروع اسپم از دستور زیر استفاده کنید :
<code>/attack</code> ID
🔹 برای فروارد پست روی پست ریپلی کرده و از دستور زیر استفاده کنید :
<code>/forward</code> ID postLink
🔸 برای پایان اسپم از دستور زیر استفاده کنید :
<code>/stop</code>
🔹 برای دریافت کد ورود تلگرام از دستور زیر استفاده کنید :
<code>/code</code> +12054789865
🔸 برای تغییر نام اکانت ها از دستور زیر استفاده کنید :
<code>/name</code> NAME
🔹 برای تنظیم عکس پروفایل اکانت ها از دستور زیر استفاده کنید :
<code>/profile</code> (reply on photo)
🔸 برای ریپورت کردن پست در کانال عمومی از دستور زیر استفاده کنید :
<code>/report</code> @Rimots MESSAGE
➖➖➖➖➖➖➖➖➖
<u>🔶 راهنمای افزودن اکانت به ربات 🔶</u>

<b>1️⃣ با استفاده از دستور زیر شماره مورد نظر را در پوشه مورد نظر ثبت کنید 👇🏻</b>
<code>/sendCode</code> +989351111111
<b>2️⃣ با استفاده از دستور زیر کد 5 رقمی تلگرام که به شماره مورد نظر ارسال شد را وارد کنید 👇🏻</b>
<code>/setCode</code> 12345
<b>3️⃣ درصورتیکه اکانت تایید دو مرحله داشت از دستور زیر استفاده نمایید 👇🏻</b>
<code>/set2FA</code> PASSWORD
<b>#️⃣ برای دریافت لیست کامل شماره ها از دستور زیر استفاده کنید👇🏻</b>
<code>/list</code>
<b>#️⃣ برای حذف اکانت از دستور زیر استفاده کنید👇🏻</b>
<code>/deleteAccount</code> +989351111111''', reply_to_message_id=message.message_id, parse_mode='html')


@bot.on_message(filters.command('list') & filters.chat(sudo))
def getAccountList(client, message):
    accounts = getAccount()
    for session in accounts:
        with open('sessionList.txt', 'a', encoding='utf-8') as file:
            file.write(str(session) + '\n')
    if os.path.isfile('sessionList.txt'):
        bot.send_document(chat_id=message.chat.id, document='./sessionList.txt', caption='<b>🔅 لیست کل سشن های ربات</b>', reply_to_message_id=message.message_id)
        os.unlink('sessionList.txt')
    else:
        message.reply(f'<b>اکانتی یافت نشد !</b>', quote=True)

@bot.on_message(filters.regex('/sendCode ') & filters.chat(sudo))
def sendCode(client, message):
    phone_number = message.text.replace('/sendCode ', '').replace(' ', '').replace('+', '').replace('-', '')
    if os.path.isfile(f'sessions/{phone_number}.session') :
        message.reply('<b>شماره مورد نظر از قبل وجود داشت.</b>', quote=True)
    else :
        global login_temp_list
        random_api = app_info()
        login_temp_list['api_id'] = random_api[1]
        login_temp_list['api_hash'] = random_api[0]
        login_temp_list['phone_number'] = phone_number
        login_temp_list['client'] = Client(f'sessions/{phone_number}', int(login_temp_list['api_id']), login_temp_list['api_hash'])
        try :
            login_temp_list['client'].connect()
            login_temp_list['response'] = login_temp_list['client'].send_code(phone_number)
        except errors.BadRequest :
            message.reply('<b>خطایی رخ داد !</b>', quote=True)
        else:
            message.reply(f'<b>کد 5 رقمی به شماره {phone_number} ارسال شد ✅</b>', quote=True)


@bot.on_message(filters.regex('/setCode ') & filters.chat(sudo))
def setCode(client, message):
    telegram_code = message.text.split()[1].replace(' ', '').replace('-', '')
    global login_temp_list
    if len(login_temp_list.values()) == 0 :
        message.reply('<b>لطفا ابتدا از دستور sendCode استفاده نمایید.</b>', quote=True)
    else :
        try :
            login_temp_list['client'].sign_in(login_temp_list['phone_number'], login_temp_list['response'].phone_code_hash, telegram_code)
            login_temp_list['client'].disconnect()
            login_temp_list = {}
        except errors.SessionPasswordNeeded :
            password_hint = login_temp_list['client'].get_password_hint()
            message.reply(f'''اکانت شما دارای تایید دو مرحله ای میباشد.
راهنمای رمز : {password_hint}

لطفا با استفاده از دستور مربوطه رمز تایید دو مرحله را ارسال نمایید.''', quote=True)
        except errors.BadRequest :
            message.reply('<b>خطایی رخ داد !</b>', quote=True)
        else:
            message.reply('<b>اکانت با موفقیت اضافه شد ✅</b>', quote=True)


@bot.on_message(filters.regex('/set2FA ') & filters.chat(sudo))
def set2FA(client, message):
    telegram_2fa_password = message.text.split()[1]
    global login_temp_list
    if len(login_temp_list.values()) == 0 :
        message.reply('<b>لطفا ابتدا از دستور sendCode استفاده نمایید.</b>', quote=True)
    else :
        try :
            login_temp_list['client'].check_password(telegram_2fa_password)
        except errors.BadRequest :
            message.reply('<b>رمز وارد شده اشتباه میباشد, لطفا مجدد تلاش نمایید.</b>', quote=True)
        else:
            login_temp_list['client'].disconnect()
            login_temp_list = {}
            message.reply('<b>اکانت با موفقیت اضافه شد ✅</b>', quote=True)


@bot.on_message(filters.regex('/deleteAccount ') & filters.chat(sudo))
def deleteAccount(client, message):
    phone_number = message.text.replace('/deleteAccount ', '').replace(' ', '').replace('+', '').replace('-', '')
    main_path = f'sessions/{phone_number}.session'
    if not os.path.isfile(main_path) :
        message.reply('<b>شماره مورد نظر یافت نشد.</b>', quote=True)
    else :
        os.unlink(main_path)
        message.reply('<b>شماره مورد نظر با موفقیت از ربات حذف شد.</b>', quote=True)


@bot.on_message(filters.command('save') & filters.chat(sudo))
def __SAVE__(client, message) :
    try :
        if message.reply_to_message.document.file_size / 1024 / 1024 <= 5 :
            bot.download_media(message.reply_to_message.document.file_id, file_name='file.txt')
            bot.send_message(message.chat.id, '''<b>فایل خشاب ذخیره شد ✅</b>''', reply_to_message_id=message.reply_to_message.message_id, parse_mode='html')
    except :
        bot.send_message(message.chat.id, '''<b>خطایی رخ داد ❗️</b>''', reply_to_message_id=message.message_id, parse_mode='html')


@bot.on_message(filters.regex('/cap ') & filters.chat(sudo))
def __ADD__(client, message) :
    add = message.text.replace('/cap ', '')
    with open('downloads/caption.txt', 'w', encoding="utf-8") as file :
        file.write(add)
    bot.send_message(message.chat.id, '''<b>جمله مورد نظر به خشاب اضافه شد ✅</b>''', reply_to_message_id=message.message_id, parse_mode='html')


@bot.on_message(filters.regex('/time ') & filters.chat(sudo))
def __ADD__(client, message) :
    time = message.text.replace('/time ', '')
    with open('downloads/time.txt', 'w', encoding="utf-8") as file :
        file.write(time)
    bot.send_message(message.chat.id, '''<b>زمان اسپم با موفقیت تنظیم شد ✅</b>''', reply_to_message_id=message.message_id, parse_mode='html')


@bot.on_message(filters.regex('/join ') & filters.chat(sudo))
def __join__(client, message):
    link = message.text.split()[1].replace('@', '').replace('+', 'joinchat/')
    if len(getAccount()) == 0 :
        bot.send_message(message.from_user.id, f'<b>اکانتی یافت نشد !</b>', reply_to_message_id=message.message_id, parse_mode='html')
    else :
        accs = len(getAccount())
        bot.send_message(message.from_user.id, f'<b>♻️ عملیات عضویت با {accs} اکانت شروع شد ...</b>', reply_to_message_id=message.message_id, parse_mode='html')
        id = ''
        title = ''
        for session in getAccount() :
            info = app_info()
            try :
                with Client(f'sessions/{session}', info[1], info[0]) as cli :
                    cli.join_chat(link)
                    get_chat = cli.get_chat(link)
                    title = get_chat.title
                    bot.send_message(message.from_user.id, f'<b>اکانت [ {session} ] با موفقیت در [ {title} ] عضو شد ✅</b>', reply_to_message_id=message.message_id, parse_mode='html')
                    asyncio.run(sleep(1))
            except :
                bot.send_message(message.from_user.id, f'<b>اکانت [ {session} ] هنگام عضویت با خطا مواجه شد ❗️</b>', reply_to_message_id=message.message_id, parse_mode='html')
        bot.send_message(message.from_user.id, f'<b>عملیات جوین با موفقیت به پایان رسید ✅</b>', reply_to_message_id=message.message_id, parse_mode='html')


@bot.on_message(filters.regex('/leave ') & filters.chat(sudo))
def __left__(client, message):
    link = message.text.split()[1]
    if len(getAccount()) == 0 :
        bot.send_message(message.from_user.id, f'<b>اکانتی یافت نشد !</b>', reply_to_message_id=message.message_id, parse_mode='html')
    else :
        accs = len(getAccount())
        bot.send_message(message.from_user.id, f'<b>♻️ عملیات لفت با {accs} اکانت شروع شد ...</b>', reply_to_message_id=message.message_id, parse_mode='html')
        id = 0
        for session in getAccount() :
            info = app_info()
            try :
                with Client(f'sessions/{session}', info[1], info[0]) as cli :
                    get_chat = cli.get_chat(link)
                    title = get_chat.title
                    cli.leave_chat(link, delete=True)
                    bot.send_message(message.from_user.id, f'<b>اکانت [ {session} ] با موفقیت از [ {title} ] خارج شد ✅</b>', reply_to_message_id=message.message_id, parse_mode='html')
                    asyncio.run(sleep(1))
            except :
                bot.send_message(message.from_user.id, f'<b>اکانت [ {session} ] هنگام لفت با خطا مواجه شد ❗️</b>', reply_to_message_id=message.message_id, parse_mode='html')
        bot.send_message(message.from_user.id, f'<b>عملیات لفت با موفقیت به پایان رسید ✅</b>', reply_to_message_id=message.message_id, parse_mode='html')


@bot.on_message(filters.regex('/attack ') & filters.chat(sudo))
def __attack__(client, message) :
    link = message.text.split()[1]
    time2sleep = int(open('downloads/time.txt', 'r').read())
    if os.path.exists('stop') :
        os.unlink('stop')
    if os.path.exists('downloads/file.txt') == False :
        bot.send_message(message.chat.id, '''<b>خشابی یافت نشد ❗️</b>''', reply_to_message_id=message.message_id, parse_mode='html')
    else :
        bot.send_message(message.chat.id, '''<b>عملیات اسپم شروع شد ✅</b>''', reply_to_message_id=message.message_id, parse_mode='html')
        with open('downloads/file.txt', 'r', encoding="utf-8") as mf : data = mf.read()
        while True:
            if os.path.exists('stop') :
                break
            for session in getAccount() :
                if os.path.exists('stop') :
                    break
                else:
                    line = ra.choice(data.split('\n')).strip()
                    if os.path.exists('downloads/caption.txt') :
                        with open('downloads/caption.txt', 'r', encoding="utf-8") as tfile :
                            line += '\n\n' + tfile.read()
                    info = app_info()
                    if line == None or len(line) < 2 :
                        continue
                    try :
                        with Client(f'sessions/{session}', info[1], info[0]) as cli :
                            cli.send_message(link, line, parse_mode='html')
                        asyncio.run(sleep(time2sleep))
                    except :
                        continue
        bot.send_message(message.chat.id, f'<b>عملیات اسپم در {link} با موفقیت به پایان رسید ✅</b>', reply_to_message_id=message.message_id, parse_mode='html')


@bot.on_message(filters.regex('/forward ') & filters.chat(sudo))
def __forward__(client, message) :
    link = message.text.split()[1]
    channel = message.text.split()[2].split('/')[3]
    msg_id = int(message.text.split()[2].split('/')[4])
    time2sleep = int(open('downloads/time.txt', 'r').read())
    if os.path.exists('stop') :
        os.unlink('stop')
    bot.send_message(message.chat.id, '''<b>عملیات اسپم شروع شد ✅</b>''', reply_to_message_id=message.message_id, parse_mode='html')
    while True:
        if os.path.exists('stop') :
            break
        for session in getAccount() :
            if os.path.exists('stop') :
                break
            else:
                info = app_info()
                try :
                    with Client(f'sessions/{session}', info[1], info[0]) as cli :
                        cli.forward_messages(link, channel, msg_id)
                    asyncio.run(sleep(time2sleep))
                except :
                    continue
    bot.send_message(message.chat.id, f'<b>عملیات اسپم در {link} با موفقیت به پایان رسید ✅</b>', reply_to_message_id=message.message_id, parse_mode='html')



@bot.on_message(filters.command('stop') & filters.chat(sudo))
def __stop__(client, message) :
    with open('stop', 'w', encoding="utf-8") as file :
        file.write('yes')
    bot.send_message(message.chat.id, '''<b>تمامی عملیات های ربات با موفقیت کنسل شد ✅</b>''', reply_to_message_id=message.message_id, parse_mode='html')


@bot.on_message(filters.command('delcap') & filters.chat(sudo))
def __stop__(client, message) :
    if os.path.exists('downloads/caption.txt') :
        os.unlink('downloads/caption.txt')
    bot.send_message(message.chat.id, '''<b>کپشن با موفقیت حذف شد ✅</b>''', reply_to_message_id=message.message_id, parse_mode='html')


@bot.on_message(filters.regex('/code ') & filters.chat(sudo))
def __code__(client, message):
    number = message.text.split()[1].replace(' ', '').replace('+', '')
    if not os.path.exists(f'sessions/{number}.session') :
        bot.send_message(message.from_user.id, '''<b>شماره مورد نظر وجود ندارد.</b>''', reply_to_message_id=message.message_id, parse_mode='html')
    else :
        try :
            info = app_info()
            with Client(f'sessions/{number}', info[1], info[0]) as cli :
                text = cli.get_history(777000, limit=1)[0]['text']
                if text :
                    bot.send_message(message.from_user.id, text, reply_to_message_id=message.message_id, parse_mode='html')
                else :
                    bot.send_message(message.from_user.id, '''پیامی از طرف تلگرام یافت نشد !''', reply_to_message_id=message.message_id, parse_mode='html')
        except :
            bot.send_message(message.from_user.id, '''<b>هنگام فراخوانی سشن خطایی رخ داد ❗️</b>''', reply_to_message_id=message.message_id, parse_mode='html')


@bot.on_message(filters.regex('/name ') & filters.chat(sudo))
def __name__(client, message):
    name = message.text.replace('/name ', '')
    if len(getAccount()) == 0 :
        bot.send_message(message.from_user.id, f'<b>اکانتی یافت نشد !</b>', reply_to_message_id=message.message_id, parse_mode='html')
    else :
        accs = len(getAccount())
        bot.send_message(message.from_user.id, f'<b>♻️ عملیات تغییر نام پروفایل با {accs} اکانت شروع شد ...</b>', reply_to_message_id=message.message_id, parse_mode='html')
        for session in getAccount() :
            info = app_info()
            try :
                with Client(f'sessions/{session}', info[1], info[0]) as cli :
                    cli.update_profile(first_name=name, last_name="")
                    bot.send_message(message.from_user.id, f'<b>نام پروفایل اکانت [ {session} ] با موفقیت به [ {name} ] تغییر یافت ✅</b>', reply_to_message_id=message.message_id, parse_mode='html')
                    asyncio.run(sleep(1))
            except :
                bot.send_message(message.from_user.id, f'<b>اکانت [ {session} ] هنگام تغییر نام با خطا مواجه شد ❗️</b>', reply_to_message_id=message.message_id, parse_mode='html')
        bot.send_message(message.from_user.id, f'<b>عملیات تغییر نام با موفقیت به پایان رسید ✅</b>', reply_to_message_id=message.message_id, parse_mode='html')


@bot.on_message(filters.command('profile'))
def __profile__(client, message) :
    if len(getAccount()) == 0 :
        bot.send_message(message.from_user.id, f'<b>اکانتی یافت نشد !</b>', reply_to_message_id=message.message_id, parse_mode='html')
    else :
        try :
            bot.download_media(message.reply_to_message.photo.file_id, file_name='photo.png')
        except :
            bot.send_message(message.chat.id, '''<b>خطایی رخ داد ❗️</b>''', reply_to_message_id=message.message_id, parse_mode='html')
        if os.path.exists('downloads/photo.png') :
            accs = len(getAccount())
            bot.send_message(message.from_user.id, f'<b>♻️ عملیات تغییر عکس پروفایل با {accs} اکانت شروع شد ...</b>', reply_to_message_id=message.message_id, parse_mode='html')
            for session in getAccount() :
                info = app_info()
                try :
                    with Client(f'sessions/{session}', info[1], info[0]) as cli :
                        cli.set_profile_photo(photo='downloads/photo.png')
                        bot.send_message(message.from_user.id, f'<b>عکس پروفایل اکانت [ {session} ] با موفقیت تغییر یافت ✅</b>', reply_to_message_id=message.message_id, parse_mode='html')
                        asyncio.run(sleep(1))
                except :
                    bot.send_message(message.from_user.id, f'<b>اکانت [ {session} ] هنگام تغییر عکس پروفایل با خطا مواجه شد ❗️</b>', reply_to_message_id=message.message_id, parse_mode='html')
            os.unlink('downloads/photo.png')
            bot.send_message(message.from_user.id, f'<b>عملیات تغییر عکس پروفایل با موفقیت به پایان رسید ✅</b>', reply_to_message_id=message.message_id, parse_mode='html')


@bot.on_message(filters.regex('/report ') & filters.chat(sudo))
def __report__(client, message) :
    if len(getAccount()) == 0 :
        bot.send_message(message.from_user.id, f'<b>اکانتی یافت نشد !</b>', reply_to_message_id=message.message_id, parse_mode='html')
    else :
        username = message.text.split()[1].replace('@', '')
        msg_id = int(message.text.split()[2])
        accs = len(getAccount())
        bot.send_message(message.from_user.id, f'<b>♻️ عملیات ریپورت پست با {accs} اکانت شروع شد ...</b>', reply_to_message_id=message.message_id, parse_mode='html')
        for session in getAccount() :
            info = app_info()
            with Client(f'sessions/{session}', info[1], info[0]) as cli :
                try:
                    get_chat = cli.send(
                    functions.channels.GetFullChannel(
                        channel=cli.resolve_peer(username)
                    )
                    )
                    chatsid = get_chat.chats[0].id
                    access_hash = get_chat.chats[0].access_hash
                    Report = cli.send(functions.messages.Report(
                    peer = types.InputPeChannel(channel_id = chatsid, access_hash = access_hash), 
                    id = [msg_id], 
                    reason = types.InputReportReasoornography() ,
                    message = '',
                    )
                    )
                    bot.send_message(message.from_user.id, f'<b>اکانت [ {session} ] با موفقیت پست رو ریپورت کرد ✅</b>', reply_to_message_id=message.message_id, parse_mode='html')
                    asyncio.run(sleep(1))
                except :
                    bot.send_message(message.from_user.id, f'<b>اکانت [ {session} ] در هنگام ریپورت پست با خطا مواجه شد ❗️</b>', reply_to_message_id=message.message_id, parse_mode='html')
        postLink = f'https://t.me/{username}/{msg_id}'
        accs = len(getAccount())
        bot.send_message(message.from_user.id, f'<b>برای پست [ {postLink} ] با [ {accs} ] اکانت گذارش پورنوگرافی ارسال شد✅</b>', reply_to_message_id=message.message_id, parse_mode='html')


bot.run()