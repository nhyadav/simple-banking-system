import random
import sys
import sqlite3


account = []
id = [1]
while True:

    conn = sqlite3.connect('card.s3db')
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS card"
                "(id INTEGER PRIMARY KEY AUTOINCREMENT,"
                "number TEXT,"
                "pin TEXT,"
                "balance INTEGER DEFAULT 0)")
    conn.commit()
    print('''1. Create an account
2. log into account
0. Exit''')
    n = int(input())

    if n == 1:
      
        while True:
            balance = 0
            acc_no = random.randint(100000000,999999999)
            start_no = '400000'+str(acc_no)
            last_no = 10 - (sum([int(i) for i in start_no]) % 10)
            doble_list = [2 * int(j) if i % 2 != 0 else int(j) for i,j in enumerate(start_no, 1)]
            conf_list = [(int(p) - 9) if int(p) > 9 else int(p) for p in doble_list]
            last_digit = 10 - (sum(conf_list) % 10)
            if last_digit == last_no:

                card_no = start_no + str(last_digit)
                pin_no = random.randint(1000, 9999)
                print('Your card has been created')
                print('Your card number:')
                print(card_no)
                print('Your card PIN:')
                print(pin_no)
                account.append([card_no, pin_no])
                # idd = max(id)
                # idd += 1
                # id.append(idd)

                cur.execute("INSERT INTO card(number,pin,balance) VALUES ({},{},{})".format(card_no, str(pin_no), balance))
                conn.commit()


                break

            else:
                continue
                
    elif n == 2:
        print('Enter your card number:')
        crd_no = input()
        print('Enter your PIN:')
        pin = int(input())
        cur.execute("select number, pin from card")
        account_pin = cur.fetchall()
        # print(account_pin)
        data = [crd_no, pin]
        if data in account:
            print('You have successfully logged in!')
            while True:
                print('''1. Balance
            2. Add income
            3. Do transfer
            4. Close account
            5. Log out
            0. exit''')


                n = int(input())
                if n == 1:
                    cur.execute("select balance from card where number = {}".format(card_no))
                    bal = cur.fetchone()
                    print('Balance:', bal)
                    continue

                elif n == 2:
                    inc = int(input("Enter income:"))

                    cur.execute("update card set balance = balance + {} where number = {}".format(inc, card_no))
                    print('Income was added!')
                    conn.commit()
                    continue
                elif n == 3:
                    print("Transfer")
                    acc_no = input("Enter card number:")
                    cur.execute("select number from card")
                    card_no = cur.fetchall()
                    last_no = 10 - (sum([int(i) for i in acc_no]) % 10)
                    doble_list = [2 * int(j) if i % 2 != 0 else int(j) for i, j in enumerate(acc_no, 1)]
                    conf_list = [(int(p) - 9) if int(p) > 9 else int(p) for p in doble_list]
                    last_digit = 10 - (sum(conf_list) % 10)


                    if last_no == last_digit :
                        if (acc_no) in card_no :
                            if crd_no != acc_no:
                                amount_no = input("Enter how much money you want to transfer:")
                                cur.execute("select balance from card where number = {}".format(crd_no))
                                bal = cur.fetchone()
                                if bal > amount_no:
                                    cur.execute("update card set balance = balance - {} where number = {}".format(amount_no, crd_no))
                                    conn.commit()
                                    cur.execute("update card set balance = balance + {} where number = {}".format(amount_no, acc_no))
                                    conn.commit()
                                    print("Success!")
                                    continue
                                else:
                                    print("Not enough money!")
                                    continue
                            else:
                                print("You can't transfer money to the same account!")
                                continue
                        else:
                            print("Such a card does not exist.")
                            continue
                    else:
                        print("Probably you made a mistake in the card number. Please try again!")
                        continue
                elif n == 4:
                    cur.execute("delete  from card where number = {}".format(crd_no))
                    conn.commit()
                    print("The account has been closed!")
                    break
                elif n == 5:
                    print("You have successfully logged out!")

                    break
                elif n == 0:
                    print('Bye!')
                    conn.commit()
                    conn.close()
                    exit()

        else:
            print('Wrong card number or PIN!')
        


    else:
        print("Bye!")
        conn.commit()
        conn.close()
        exit()

