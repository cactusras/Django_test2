from myApp.models import Client

#允許input為null
def beNull(strInput):
    if len(strInput) == 0:
        strInput = None
    return strInput

#Client Register

#api var
inputRegis_clie_name = input("Client name = ")
inputRegis_clie_email = input("Client email = ")
inputRegis_clie_phone = input("Client phone = ")
inputRegis_clie_pw = input("Client password = ")
inputRegis_clie_addr = input("Client address = ")
inputRegis_clie_birth = input("Client birth date = ")
inputRegis_clie_gender = input("Client gender = ")
inputRegis_clie_occup = input("Client occupation = ")
inputRegis_clie_isNotify = bool(input("Client get notifications = "))

if len(inputRegis_clie_name) <=100:
    if inputRegis_clie_email.__contains__("@"):
        if not (str(inputRegis_clie_phone).isdecimal()):
            if len(inputRegis_clie_phone) <= 15:
                if not (Client.object.filter(email = inputRegis_clie_email).exists()):
                    #用戶成功註冊
                    print("Register succeed")
                else:
                    print("信箱已被註冊過")
            else:
                print("電話不能超過15個數字")
        else:
            print("電話僅能包含數字")
    else:
        print("email不符合格式")
else:
    print("名字不能超過100個字")


#Client Login

#api var
inputLogin_clie_email = input("Client email = ")
inputLogin_clie_pw = input("Client password = ")

if Client.object.filter(email = inputLogin_clie_email).exists():
    if(Client.object.filter(email = inputLogin_clie_email).values_list('password', flat=True)):
        print("登入成功")
    else:
        print("密碼錯誤")
else:
    print("帳號不存在")


#Clinic Register

#api var
inputRegis_clin_name = input("Clinic name = ")
inputRegis_clin_licenNum = input("Clinic license number = ")
inputRegis_clin_email = input("Clinic email = ")
inputRegis_clin_phone = input("Clinic phone = ")
inputRegis_clin_pw = input("Clinic password = ")
inputRegis_clin_addr = input("Clinic address = ")
inputRegis_clin_intro = input("Clinic introduction = ")
inputRegis_clin_photo = input("Clinic photo url = ")

if len(inputRegis_clin_name) <=100:
    if inputRegis_clin_email.__contains__("@"):
        if not (str(inputRegis_clin_phone).isdecimal()):
            if len(inputRegis_clin_phone) <= 15:
                if not (Client.object.filter(email = inputRegis_clin_email).exists()):
                    #用戶成功註冊
                    clin_regis = Client(name = inputRegis_clin_name, email = inputRegis_clin_email, phone = inputRegis_clin_phone,
                                        password = inputRegis_clin_pw, address = inputRegis_clin_addr, licenNum = inputRegis_clin_licenNum
                                        )
                    clin_regis.save()
                else:
                    print("信箱已被註冊過")
            else:
                print("電話不能超過15個數字")
        else:
            print("電話僅能包含數字")
    else:
        print("email不符合格式")
else:
    print("名字不能超過100個字")


#連結到Hiring Entity
#def clinic_doctor register() ->診所註冊時點選"填醫生資料"的時候會執行的function
#此function跟db無關 僅先暫存在array list之類的 等到診所成功註冊的時候再一次匯進db
#先把資料存到Doctor跟Clinic 再存到Hiring entity