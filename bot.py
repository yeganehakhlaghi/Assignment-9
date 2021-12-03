
import telebot
import random
import qrcode
from khayyam import JalaliDatetime
from gtts import gTTS



number=0

bot = telebot.TeleBot("2133155022:AAESBm38gfi6Y2WUxIlPr0pVirUn_pKCYek")
@bot.message_handler(commands=['start'])
def send_welcome(message):
	bot.reply_to(message, " سلام خوش اومدی " +message.from_user.first_name)
 
@bot.message_handler(commands=['help'])
def komak(message):
	bot.reply_to(message, """   /start  خوش آمد 
    /game   بازی حدس عدد 
    /age   محاسبه سن 
    /voice   تبدیل متن به ویس 
    /max   پیدا کردن بزرگترین عدد 
    /argmax   پیدا کردن اندیس بزرگترین عدد 
    /qrcode   qrcode تبدیل متن به   """)

@bot.message_handler(commands=['game'])
def bazi1(message):
    global numb
    numb=random.randint(0,100)
    user_num=bot.send_message(message.chat.id,'من یک عدد بین 1 تا 100 انتخاب کردم. حدس بزن چند است')
    bot.register_next_step_handler(user_num, bazi2)
def bazi2(user_num):
    markup = telebot.types.ReplyKeyboardMarkup(row_width=1)
    Button = telebot.types.KeyboardButton('New Game')
    markup.add(Button)
    global numb

    if user_num.text == "New Game":
        user_num = bot.send_message(user_num.chat.id, '!!بازی جدید!!',reply_markup=markup)
        numb = random.randint(0,100)
        bot.register_next_step_handler(user_num, bazi2)
    else:  
          
        if int(user_num.text) > numb :
            user_num = bot.send_message(user_num.chat.id, 'کوچکتر انتخاب کن',reply_markup=markup)
            bot.register_next_step_handler(user_num, bazi2)
        elif int(user_num.text) < numb :
            user_num=bot.send_message(user_num.chat.id,'بزرگتر انتخاب کن',reply_markup=markup)
            bot.register_next_step_handler(user_num, bazi2)
        else :
            markup = telebot.types.ReplyKeyboardRemove(selective=True)
            user_num=bot.send_message(user_num.chat.id,'🥳برنده شدی',reply_markup=markup)  

@bot.message_handler(commands=['age'])
def age1(message):
    BD=bot.send_message(message.chat.id,' تاریخ تولدت به شمسی را وارد کن (به عنوان مثال 1300/01/01) ')
    bot.register_next_step_handler(BD,age2)
def age2(BD):
    try:
        k=BD.text.split('/')
        Time_difference=str(JalaliDatetime.now()-JalaliDatetime(k[0],k[1],k[2]))
        Years=int(Time_difference.split(' ')[0])//365
        bot.send_message(BD.chat.id, " شما " + str(Years) + " سال دارید ")
        
        #bot.send_message(BD.chat.id,"سن شما "+str(Years))+"سال است ")



        #k=BD.text.split('/')
        #Time_difference=str(JalaliDatetime.now()-JalaliDatetime(k[0],k[1],k[2]))
        #Number_Days=int(Time_difference.split(' '))
        #Years=Number_Days//365
        #bot.send_message(BD.chat.id,"سن شما "+str(Years))
        #Months=(Number_Days%365)//30
        #Days_Left=Number_Days-(Years*365 + Months*30 )
        #bot.send_message(BD.chat.id,"سن شما "+str(Years) +"سال و " +str(Months) +"ماه و " +str(Days_Left)+"است که معادل "+str(Number_Days)+"روز است")
    except:
        BDay=bot.send_message(BD.chat.id,'تاریخ تولد وارد شده درست نیس')
        bot.register_next_step_handler(BD,age2)    



        
        
    
@bot.message_handler(commands=['voice'])
def Voice1(message):
    txt=bot.send_message(message.chat.id,'متنتو به انگلیسی وارد کن')
    bot.register_next_step_handler(txt,Voice2)
def Voice2(txt):
    txt=txt.text
    language='en'
    vic=gTTS(text=txt,lang=language,slow=False)
    vic.save('vc.mp3')
    voice=open('vc.mp3','rb')
    bot.send_voice(txt.chat.id,voice)

@bot.message_handler(commands=['max'])
def maximum1(message):
    ary=bot.send_message(message.chat.id,""" اعداد مورد نظرتو وارد کن تا بزرگترینشو بهت بگم 
    (به صورت 1,2,3,5,8 وارد کن) """)
    bot.register_next_step_handler(ary,maximum2)
def maximum2(ary):    
    try:
        numbers=list(map(int,ary.text.split(',')))
        bot.send_message(ary.chat.id,'بزرگترین عدد -> '+str(max(numbers)))
    except:    
        ary=bot.send_message(ary.chat.id,'لیست اعدادتو اشتباه وارد کردی')
        bot.register_next_step_handler(ary,maximum2)

@bot.message_handler(commands=['argmax'])
def argmax1(message):
    ary=bot.send_message(message.chat.id,""" اعداد مورد نظرتو وارد کن تا اندیس بزرگترینشو بهت بگم 
    (به صورت 1,2,3,5,8 وارد کن) """)
    bot.register_next_step_handler(ary,argmax2)
def argmax2(ary):
    try:
        nums=list(map(int,ary.text.split(',')))
        bot.send_message(ary.chat.id,'ایندکس بزرگترین عدد -> '+str(nums.index(max(nums))+1))
    except:    
        ary=bot.send_message(ary.chat.id,'لیست اعدادتو اشتباه وارد کردی')
        bot.register_next_step_handler(ary,argmax2)


@bot.message_handler(commands=['qrcode'])
def Qrcode1(message):
    txt=bot.send_message(message.chat.id,"متن را وارد کن")        
    bot.register_next_step_handler(txt,Qrcode2)
def Qrcode2(txt):

    QR_img=qrcode.make(txt.text)
    QR_img.save('QRcode.png')
    Qr=open('QRcode.png','rb')
    bot.send_photo(txt.chat.id,Qr)






bot.infinity_polling()    