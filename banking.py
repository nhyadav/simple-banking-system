import random
import sys
import sqlite3

# Write your code here
def create_account(acc, acc_book, conn, cur):
    iin = str(400000)
    while 1:
        ten_number = random.randint(100000000, 999999999)
        account_number = iin + str(ten_number)
        double_list = [2 * int(j) if i % 2 != 0 else int(j) for i, j in enumerate(account_number, 1)]
        conf_list = [(int(p) - 9) if int(p) > 9 else int(p) for p in double_list]
        last_digit = 0 if (sum(conf_list) % 10 == 0) else (10 - (sum(conf_list) % 10))
        account_number = account_number + str(last_digit)
        if account_number in acc:
            continue
        else:
            balance = 0
            pin = random.randint(1000, 9999)
            acc.append(account_number)
            acc_book[account_number] = pin
            print("Your card has been created")
            print("Your card number:")
            print(account_number)
            print("Your card PIN:")
            print(pin)
            cur.execute("INSERT INTO card(number,pin,balance) VALUES ({},{},{})".format(account_number, str(pin), balance))
            conn.commit()
            break

def logged_in_operation(account, conn, cur):
    while 1:
        print("""1. Balance
    2. Add income
    3. Do transfer
    4. close account
    5. Log out
    0. Exit""")
        choice = int(input())
        if choice == 1:
            cur.execute("SELECT balance FROM card WHERE number == {}".format(account))
            balance = cur.fetchone()
            print("Balance:", balance)
        elif choice == 2:
            amount = int(input("Enter income:\n"))
            cur.execute("SELECT balance FROM card WHERE number == {}".format(account))
            balance = cur.fetchone()
            amount = amount + balance[0]
            cur.execute("UPDATE card SET balance = {} WHERE number = {}".format(amount, account))
            conn.commit()
            print("Income was added!")
        elif choice == 3:
            print("Transfer")
            card_no = input("Enter the card:\n")
            cur.execute("SELECT number FROM card")
            cards = cur.fetchall()
            double_list = [2 * int(j) if i % 2 != 0 else int(j) for i, j in enumerate(card_no, 1)]
            conf_list = [(int(p) - 9) if int(p) > 9 else int(p) for p in double_list]
            if sum(conf_list) % 10 == 0:
                if (card_no,) in cards:
                    if card_no != account:
                        transfer_money = int(input("Enter how much money you want to transfer:\n"))
                        cur.execute("SELECT balance FROM card WHERE number = {}".format(account))
                        account_balance = cur.fetchone()[0]
                        if account_balance >= transfer_money:
                            cur.execute("SELECT balance FROM card WHERE number = {}".format(card_no))
                            bank_money = cur.fetchone()
                            cur.execute(f"UPDATE card SET balance = {bank_money[0] + transfer_money} WHERE number = {card_no}")
                            cur.execute(f"UPDATE card SET balance = {account_balance - transfer_money} WHERE number = {account}")
                            conn.commit()
                            print("Success!")
                        else:
                            print("Not enough money!")
                    else:
                        print("You can't transfer money to the same account!")
                else:
                    print("Such a card does not exist.")
            else:
                print("Probably you made a mistake in the card number. Please try again!")
        elif choice == 4:
            cur.execute("DELETE FROM card where number = {}".format(account))
            conn.commit()
            print("The account has been closed!")

        elif choice == 5:
            print("You have successfully logged out!")
            break

        elif choice == 0:
            print("Bye!")
            sys.exit()

def log_in_account(x, y, c, d) :
    card_no = input('Enter your card number:\n')
    pin_no = input("Enter your PIN:\n")
    if card_no in x:
        if int(pin_no) == y[card_no]:
            print("You have successfully logged in!")
            logged_in_operation(card_no, c, d)
        else:
            print("Wrong card number or PIN!")
            return
    else:
        print("Wrong card number or PIN!")
        return

def main(account_list, account_number_psw, conn, cur) :
    while 1:
        print("""1. Create an account
2. Log into account
0. exit""")
        choice = int(input())
        if choice == 1 :
            create_account(account_list, account_number_psw, conn, cur)
        elif choice == 2 :
            log_in_account(account_list, account_number_psw, conn, cur)
        elif choice == 0:
            sys.exit()



if __name__ == "__main__":
    account = []
    account_book = {}
    connection = sqlite3.connect('card.s3db')
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS card"
                "(id INTEGER PRIMARY KEY AUTOINCREMENT,"
                "number TEXT,"
                "pin TEXT,"
                "balance INTEGER DEFAULT 0)")
    main(account, account_book, connection, cursor)
    connection.close()
