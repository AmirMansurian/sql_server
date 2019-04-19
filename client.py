import requests
import os
import time
import platform
import sys

PARAMS = CMD = USERNAME = PASSWORD = TOKEN = ""
HOST = "localhost"
PORT = "1104"


def __postcr__():
    return "http://"+HOST+":"+PORT+"/"+CMD+"?"


def clear():
    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear')


def show_func():
    print("_______________________________________________________________")

    print("USERNAME : "+USERNAME+"\n"+"TOKEN : " + TOKEN)
    print("""What Do You Want To Do :
    
    1. Send Ticket
    2. replay Ticket (admin only)
    3. Change Ticket Status (member)
    4. Change Ticket Status (admin)
    5. Get Tickets (member)
    6. Get Tickets (admin)
    7. Logout
    8. Exit
    """)



while True :
    clear()
    print("_____________________________________")
    print("""WELCOME TO TICKET MARKETING
       Please Choose What You Want To Do :
       1. login
       2. signup
       3. exit
       """)

    choose=input()

    if choose ==1:
        clear()
        while True:
            print("USERNAME : ")
            USERNAME = sys.stdin.readline()[:-1]
            print("PASSWORD : ")
            PASSWORD = sys.stdin.readline()[:-1]
            CMD = "login"
            PARAMS = {'username': USERNAME, 'password': PASSWORD}
            r = requests.post(__postcr__(), PARAMS).json()

            if r['code'] == '200':
                clear()
                TOKEN = r['token']
                print(r['message'])
                print("token : "),
                print (r['token'])
                time.sleep(2)
                break


            else:
                clear()

                print (r['message'])
                time.sleep(2)



        while True:
            clear()
            show_func()

            command=input()

            if command==1:
                clear()
                CMD="sendticket"
                print("Subject of the ticket : ")
                subject=sys.stdin.readline()[:-1]
                print("Write body of ticket : ")
                body=sys.stdin.readline()[:-1]

                PARAMS={'token': TOKEN, 'subject': subject, 'body': body}
                response=requests.post(__postcr__(), PARAMS).json()
                clear()
                print(response['message'])
                id=response['id']
                print("id : " ),
                print(id)
                time.sleep(2)


            elif command==2:
                clear()
                CMD="restoticketmod"
                print("Enter id of ticket : ")
                id=input()
                print("Write your replay to ticket : ")
                body=sys.stdin.readline()[:-1]

                PARAMS={'token': TOKEN, 'id': id, 'body': body}
                response=requests.post(__postcr__(), PARAMS).json()
                clear()

                if response['code']=='200':
                    print(response['message'])
                    time.sleep(2)

                else:
                    print(response['message'])
                    time.sleep(2)



            elif command==3:
                clear()
                CMD="closeticket"
                print("Enter id of ticket to close : ")
                id=input()

                PARAMS={'token': TOKEN, 'id': id}
                response=requests.post(__postcr__(), PARAMS).json()
                print(response['message'])
                time.sleep(2)


            elif command==4:
                clear()
                CMD="changestatus"
                print("Enter id of ticket to change status : ")
                id=input()
                print("Enter the staus : ")
                status=sys.stdin.readline()[:-1]

                PARAMS={'token': TOKEN, 'id': id, 'status':status}
                response=requests.post(__postcr__(), PARAMS).json()
                print(response['message'])
                time.sleep(2)


            elif command == 5:
                clear()
                CMD = "getticketcli"

                PARAMS = {'token': TOKEN}
                response = requests.post(__postcr__(), PARAMS).json()
                print (response['tickets'])
                print("_____________________________________\n")

                for x in range(len(response) - 2):
                    temp = 'block ' + str(x)
                    json = response[temp]
                    print("subject : "),
                    print(json['subject'])
                    print("body : "),
                    print(json['body'])
                    print("status : "),
                    print(json['status'])
                    print("id : "),
                    print(json['id'])
                    print("date : "),
                    print(json['date'])
                    print("_____________________________________")

                sys.stdin.readline()[:-1]


            elif command==6:
                clear()
                CMD = "getticketmod"

                PARAMS = {'token': TOKEN}
                response = requests.post(__postcr__(), PARAMS).json()
                print (response['tickets'])
                print("_____________________________________\n")

                for x in range(len(response) - 2):
                    temp = 'block ' + str(x)
                    json = response[temp]
                    print("subject : "),
                    print(json['subject'])
                    print("body : "),
                    print(json['body'])
                    print("status : "),
                    print(json['status'])
                    print("id : "),
                    print(json['id'])
                    print("date : "),
                    print(json['date'])
                    print("_____________________________________")

                sys.stdin.readline()[:-1]


            elif command==7:
                clear()
                CMD="logout"
                PARAMS={'username': USERNAME, 'password': PASSWORD}
                response=requests.post(__postcr__(), PARAMS).json()
                print(response['message'])
                time.sleep(2)
                break


            elif command==8:
                clear()
                CMD = "logout"
                PARAMS = {'username': USERNAME, 'password': PASSWORD}
                response = requests.post(__postcr__(), PARAMS).json()
                sys.exit()



    elif choose==2:

        clear()
        while True:
            print("USERNAME : ")
            USERNAME = sys.stdin.readline()[:-1]
            print("PASSWORD : ")
            PASSWORD = sys.stdin.readline()[:-1]
            print("FIRSTNAME : ")
            firstname = sys.stdin.readline()[:-1]
            print("LASTNAME : ")
            lastname = sys.stdin.readline()[:-1]
            print(""""member/admin?
            
            0.member
            1.admin
         
            """)

            type=sys.stdin.readline()[:-1]

            CMD = "signup"
            PARAMS = {'username': USERNAME, 'password': PASSWORD, 'firstname': firstname, 'lastname': lastname, 'type': type}
            r = requests.post(__postcr__(), PARAMS).json()

            if r['code'] == '200':
                clear()
                print(r['message'])
                time.sleep(2)
                break

            else :
                clear()
                print(r['message'])
                time.sleep(2)


    elif choose==3:
        sys.exit()


    else:
        print("Wrong input!!!")
