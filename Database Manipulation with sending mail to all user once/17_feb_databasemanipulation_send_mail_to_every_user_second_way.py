
import mysql.connector
import userdetails
import logging
import tkinter
from tkinter import filedialog
import csv
import smtplib

class Demo:
    logging.basicConfig(filename="database.log",level=logging.DEBUG)

    def __init__(self, database):
        self.database = database
        # self.table_name = table_name

    def create_table(self):
        db_connection = None

        try:
            db_connection = mysql.connector.connect(user=userdetails.user_name, password=userdetails.password, host='127.0.0.1', database=self.database)
            my_cursor = db_connection.cursor()
            t_name = input("Enter the table name to be created : ")
            id = input("Enter first column name : ")
            id_type = input("Data type : ")
            f_name = input("Enter second column name : ")
            f_name_type = input("Data type : ")
            l_name = input("Enter third column name : ")
            l_name_type = input("Data type : ")
            address = input("Enter fourth column name : ")
            address_type = input("Data type : ")
            # (ID Integer, F_NAME text, L_NAME text, ADDRESS text)
            query = f'CREATE TABLE {t_name} ({id} {id_type},{f_name} {f_name_type}, {l_name} {l_name_type} , {address} {address_type})'
            my_cursor.execute(query)
            db_connection.commit()
            massege = "Your table has been created..."
            self.send_mail(massege)
            print("CREATED")
            logging.debug("Suscessfully table created")

        except Exception as e:
            print(e)
            self.send_mail(e)
            logging.debug(e)

        finally:
            if db_connection != None:
                db_connection.close()


    def insert_data_to_table(self):
        db_connection = None

        try:
            db_connection = mysql.connector.connect(user=userdetails.user_name, password=userdetails.password, host='127.0.0.1', database=self.database)
            my_cursor = db_connection.cursor()
            t_name = input("Enter the table name in which you want to insert data : ")
            print("Please insert these details to add it to the table :  ")
            id = input("Enter the id of student : ")
            f_name = input("Enter the first name of student : ")
            l_name = input("Enter the last name of student : ")
            add = input("Enter the address of student : ")
            query = f'INSERT INTO {t_name} values(%s, %s, %s, %s)'
            val = (id, f_name, l_name, add)
            my_cursor.execute(query,val)
            db_connection.commit()
            massege = "Your data has been successfully inserted into table.."
            self.send_mail(massege)
            print("Inserted")
            logging.debug("Successfully inserted data")

        except Exception as e:
            print(e)
            self.send_mail(e)
            logging.debug(e)

        finally:
            if db_connection != None:
                db_connection.close()



    def delete_from_table(self):
        db_connection = None

        try:
            db_connection = mysql.connector.connect(user=userdetails.user_name, password=userdetails.password, host='127.0.0.1', database='mydatabase')
            my_cursor = db_connection.cursor()
            t_name = input("Enter the table name to delete the data : ")
            id = int(input('Enter the ID of the student which u want to delete : '))
            query = f'DELETE FROM {t_name} WHERE ID={id}'
            my_cursor.execute(query)
            db_connection.commit()
            massege = "Row has been successfully deleted from the table.."
            self.send_mail(massege)
            print("Deleted...")
            logging.debug( "Successfully deleted from table")

        except Exception as e:
            print(e)
            self.send_mail(e)
            logging.debug(e)

        finally:
            if db_connection != None:
                db_connection.close()


    def update_table_data(self):
        db_connection = None

        try:
            db_connection = mysql.connector.connect(user=userdetails.user_name, password=userdetails.password, host='127.0.0.1', database=self.database)
            my_cursor = db_connection.cursor()
            t_name = input("Enter the table name to update table data : ")
            print("Enter details to Update table data : ")
            id = int(input("Enter the student proper Id : "))
            val = input("Enter the value which you want to update : ")
            column_name = input("Enter the column name whose data you want to update : ")

            query = f'UPDATE {t_name} set {column_name} = "{val}" WHERE ID={id}'
            my_cursor.execute(query)
            db_connection.commit()
            massege = "Your table has been successfully updated with new data.."
            self.send_mail(massege)
            print("UPDATED...")
            logging.warning('Successfully updated data into table')

        except Exception as e:
            print(e)
            self.send_mail(e)
            logging.warning(e)

        finally:
            if db_connection != None:
                db_connection.close()


    def drop_a_table(self):
        db_connection = None

        try:
            db_connection = mysql.connector.connect(user=userdetails.user_name, password=userdetails.password, host='127.0.0.1', database=self.database)
            my_cursor = db_connection.cursor()
            t_name = input("Enter the table name drop : ")
            query = f'DROP TABLE {t_name}'
            my_cursor.execute(query)
            db_connection.commit()
            massege = "Your table has been successfully dropped.."
            self.send_mail(massege)
            print("Table dropped....")
            logging.debug( "Successfully dropped table")

        except Exception as e:
            print(e)
            self.send_mail(e)
            logging.debug(e)

        finally:
            if db_connection != None:
                db_connection.close()


    def show_data_from_table(self):
        db_connection = None

        try:
            db_connection = mysql.connector.connect(user=userdetails.user_name, password=userdetails.password, host='127.0.0.1', database=self.database)
            my_cursor = db_connection.cursor()
            t_name = input("Enter the table name to view data : ")
            query = f'SELECT * FROM {t_name}'
            my_cursor.execute(query)
            data = my_cursor.fetchall()

            for datas in data:
                print(datas)
            db_connection.commit()
            massege = "YOu requested data is available"
            self.send_mail(massege)
            print("Displaying....")
            logging.debug("Successfully fetched all data")

        except Exception as e:
            print(e)
            self.send_mail(e)
            logging.debug(e)

        finally:
            if db_connection != None:
                db_connection.close()

    def show_tables(self):
        db_connetion = None

        try:
            db_connetion = mysql.connector.connect(user=userdetails.user_name, password=userdetails.password,
                                                   host='127.0.0.1', database=self.database)
            my_cursor = db_connetion.cursor()
            my_cursor.execute("""SHOW TABLES""")
            data = my_cursor.fetchall()
            for i in range(len(data)):
                print(i + 1, ". ", data[i][0])
            db_connetion.commit()
            return data

        except Exception as e:
            print(e)

        finally:
            if db_connetion != None:
                db_connetion.close()

    def read_data_from_csv(self):
        root = tkinter.Tk()
        root.withdraw()

        file = filedialog.askopenfilename()
        l_email = []
        with open(file, 'r') as file_obj:
            csv_obj = csv.reader(file_obj)
            header = next(csv_obj)

            for i in csv_obj:
                l_email.append(i[0])

        return l_email

    def send_mail(self,message):
        mail = smtplib.SMTP('smtp.gmail.com', 587)
        mail.starttls()
        mail.login(userdetails.s_email, userdetails.s_password)
        lst = self.read_data_from_csv()
        for i in lst:
            mail.sendmail(userdetails.s_email, i, message)
        mail.quit()
        print("Email sent Successfully")

database = input("Enter your databse name : ")

while True:
    d = Demo(database)
    user_choice = int(input('''Enter your choice :
1.CREATE TABLE
2.INSERT DATA
3.DELETE FROM TABLE
4.UPDATE TABLE DATA
5.DROP A TABLE
6.SHOW DATA
7.SHOW ALL TABLES\n'''))

    if user_choice == 1:
        d.create_table()
    elif user_choice == 2:
        d.insert_data_to_table()
    elif user_choice == 3:
        d.delete_from_table()
    elif user_choice == 4:
        d.update_table_data()
    elif user_choice == 5:
        d.drop_a_table()
    elif user_choice == 6:
        d.show_data_from_table()
    elif user_choice == 7:
        d.show_tables()
    else:
        print("INVALID INPUT......")

    choice = input("Do you want to continue (y/n) : ")
    if choice == 'y' or choice == 'Y':
        continue
    else:
        break
