

import os
import smtplib
from tkinter import  messagebox
import PyPDF2
from datetime import datetime
import mysql.connector
import userdetails


class ENCRYPTFILE:
    def __init__(self, file_name, emailid):
        self.file_name = file_name
        self.emailid = emailid

    # Method to chose and open the file from any directory
    def Openfile(self):
        folder = os.listdir(r'C:\Users\Sachin.Pal\Desktop\New folder')
        pdf_file_lst = []
        for file in folder:
            if file.endswith(".pdf"):
                pdf_file_lst.append(file)
        return pdf_file_lst

    def Chose_file(self):
        lst = self.Openfile()
        if lst.count(self.file_name) == 1:
            return self.file_name
        else:
            return "No such file in directory"

    # Method to print the successful alert
    def Suscess_box(self):
        messagebox.showwarning('Successful', "Encryption is Successful")

    # Method to encrypt the file
    def Encryptfile(self):
        file = self.Chose_file()
        pdf_in_file = open(file, 'rb')
        inputpdf = PyPDF2.PdfFileReader(file)
        pages_no = inputpdf.numPages
        output = PyPDF2.PdfFileWriter()

        O_file = file.split(".")
        output_file_name = O_file[0]
        Password = output_file_name+'@123'
        for i in range(pages_no):
            inputpdf = PyPDF2.PdfFileReader(pdf_in_file)
            output.addPage(inputpdf.getPage(i))
            output.encrypt(Password)

        #
        t_stamp = self.Date_time()

        with open("output_"+output_file_name+"_"+t_stamp+".pdf", "wb") as outputStream:
            output.write(outputStream)
        self.Suscess_box()

        return "output_"+output_file_name+"_"+t_stamp+".pdf", "Password"
        # print(output_file_name+t_stamp)

    def Send_Mail(self):
        # senders_mail = input("Enter mail id : ")
        mail  = smtplib.SMTP('smtp.gmail.com', 587)
        mail.starttls()
        mail.login(userdetails.s_email,userdetails.s_password)
        message = "Your file is successfully encrypted....THANK YOU...."
        mail.sendmail(userdetails.s_email, self.emailid, message)
        mail.quit()
        print("email sent successfully")

    def Date_time(self):
        cur_time = datetime.now().replace(microsecond=0)
        time_format = '%m_%d_%H_%M_%S'
        t_stamp = datetime.strftime(cur_time, time_format)
        return t_stamp

    # Method to find the size of the file
    def SizeOfFile(self,size_file):
        size = os.path.getsize(size_file)
        in_mb = size / 1024 ** 2
        return round(in_mb, 3)

    # METHOD TO ADD DATA IN DATABASE
    def AddDataToDatabase(self):
        cnx = mysql.connector.connect(user=userdetails.user_name, password=userdetails.password, host="127.0.0.1", database="mydatabase")
        my_cursor = cnx.cursor(prepared=True)
        # query = """CREATE TABLE records( DATE_CREATION text, NAME_OF_FILE text, SIZE_OF_FILE int, PASSWORD text, EMAIL text)"""
        # my_cursor.execute(query)
        name = self.Encryptfile()[0]
        p = name.split('_')
        password = p[1]+"@123"
        email = self.emailid
        date = self.Date_time()
        size = self.SizeOfFile(name)
        query1 = ("INSERT INTO records "
                    "(DATE_CREATION, NAME_OF_FILE, SIZE_OF_FILE, PASSWORD, EMAIL) "
                    "VALUES (?,?,?,?,?)")
        data = (date, name, size, password, email)
        my_cursor.execute(query1, data)
        cnx.commit()
        cnx.close()
        messagebox.showwarning("Successful", "Record has been successfully inserted into database")


if __name__ == "__main__":

    folder = os.listdir(r'C:\Users\Sachin.Pal\Desktop\New folder')
    pdf_file_lst = []
    for file in folder:
        if file.endswith(".pdf"):
            pdf_file_lst.append(file)
    print(pdf_file_lst)
    st1 = input("Enter the file name from above file option :")
    st2 = input("Enter reciever's mail id : ")
    en = ENCRYPTFILE(st1, st2)
    en.AddDataToDatabase()
    en.Send_Mail()