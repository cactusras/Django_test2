from myApp.models import Client

#Client Register

#api var
inputRegis_clie_name = input("Client name = ")
inputRegis_clie_email = input("Client email = ")
inputRegis_clie_phone = input("Client phone = ")

if inputRegis_clie_email.__contains__("@"):
    if len(inputRegis_clie_name) <=100:
        if not (str(inputRegis_clie_phone).isdecimal()):
            if len(inputRegis_clie_phone) <= 15:
                if not (Client.object.filter(email = inputRegis_clie_email).exists()):
                    #用戶成功註冊
                    clie_regis = Client(name = inputRegis_clie_name, email = inputRegis_clie_email, phone = inputRegis_clie_phone)
                    clie_regis.save()
                else:
                    print("信箱已被註冊過")
            else:
                print("電話不能超過15個數字")
        else:
            print("電話僅能包含數字")
    else:
        print("名字不能超過100個字")
else:
    print("email不符合格式")


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

#連結到Hiring Entity
#先把資料存到Doctor跟Clinic 再存到Hiring entity