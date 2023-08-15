from tkinter import *
from tkinter import messagebox
from PIL import ImageTk,Image
import logging
import os
import serial
import serial.tools.list_ports
import winreg
import webbrowser
import pyodbc
from datetime import datetime
import time
import sys
sys.path.append(r"dll dosyanızın bulunduğu dosya yolu")
from pythonnet import load
load("coreclr")
import clr
clr.AddReference(".dll uzantılı dll dosyanızın adı 'örnek.dll' ise buraya 'örnek' yazılır")
from DllDosyasıAdı import DlldekiAnaFonksiyonunAdı

# print("SQL bağlantısı oluşturma")
conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=SQLdeki kullanıcı adınız\\SQLEXPRESS01;'
                      'Database=DataBaseIsminiz;'
                      'Trusted_Connection=yes;')
# print("Güncel zamanı alma")
now = datetime.now()
formatted_datetime = now.strftime("%Y-%m-%d %H:%M:%S")
created_date = datetime.strptime(formatted_datetime, "%Y-%m-%d %H:%M:%S")

def sql_insert_into(isim_1, durum_1, created_date_1):
    cursor2 = conn.cursor()
    sql_satir_ekle_1 = "INSERT INTO UserLogs (UserName,Message,CreatedDate) VALUES (?, ?, ?)"
    # conn.commit()
    cursor2.execute(sql_satir_ekle_1, isim_1, durum_1, created_date_1)
    conn.commit()

# sql_insert_into(isim, durum, created_date)

def is_dotnet_installed(version):
    try:
        reg_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                                 fr"SOFTWARE\\Microsoft\\NET Framework Setup\\NDP\\v{version}")
        winreg.CloseKey(reg_key)
        return True
    except OSError:
        return False

def open_dotnet_download_page():
    url = "https://dotnet.microsoft.com/download/dotnet"
    webbrowser.open(url)


if is_dotnet_installed("4.0"):
    print(".NET Framework 4.0 veya üstü yüklü.")
else:
    print(".NET Framework 4.0 veya üstü yüklü değil.")
    print(".NET sitesine yönlendirileceksiniz, güncel versiyonu indiriniz")
    open_dotnet_download_page()

log_dir1 = os.path.join(r"Log kaydını yazmak istediğiniz dosya yolu")
log_file_path1 = os.path.join(log_dir1, "logfile1.txt")
logger1 = logging.getLogger('logger1')
handler1 = logging.FileHandler(log_file_path1)
formatter1 = logging.Formatter('%(asctime)s \t %(message)s', datefmt='%d/%m/%Y %I:%M:%S %p')
handler1.setFormatter(formatter1)
logger1.addHandler(handler1)
logger1.setLevel(logging.INFO)

log_dir2 = os.path.join(r"Log kaydını yazmak istediğiniz dosya yolu")
log_file_path2 = os.path.join(log_dir2, "logfile2.txt")
logger2 = logging.getLogger('logger2')
handler2 = logging.FileHandler(log_file_path2)
formatter2 = logging.Formatter('%(asctime)s \t %(message)s', datefmt='%d/%m/%Y %I:%M:%S %p')
handler2.setFormatter(formatter2)
logger2.addHandler(handler2)
logger2.setLevel(logging.INFO)

def log_in():
    while 1:
        if (E1.get() == str("i")) and (E2.get() == str("u")):
            logger1.error("ismail Basarili giris")
            sql_insert_into("ismail", "basarılı", created_date)
            # sql connection kapatma
            conn.close()
            break
            # L3["text"]=("Hosgeldiniz İsmail Bey "
        elif (E1.get() == str("e")) and (E2.get() == str("ş")):
            logger1.error('Emre Bey Basarili giris')
            sql_insert_into("emre", "basarılı", created_date)
            # sql connection kapatma
            conn.close()
            break
        elif (E1.get() == str("s")) and (E2.get() == str("ş")):
            logger1.error("Selçuk Bey basarili giris")
            sql_insert_into("selcuk", "basarılı", created_date)
            # sql connection kapatma
            conn.close()
            break
        elif (E1.get() == str("m")) and (E2.get() == str("a")):
            logger1.error("Mustafa Bey basarili giris")
            sql_insert_into("mustafa", "basarılı", created_date)
            # sql connection kapatma
            conn.close()
            break
        elif (E1.get() == str("k")) and (E2.get() == str("f")):
            logger1.error("Kagan Bey basarili giris")
            sql_insert_into("kagan", "basarılı", created_date)
            # sql connection kapatma
            conn.close()
            break
        else:
            messagebox.showerror("HATA", "Giriş bilgileri yanlış")
            logger1.error('basarisiz giris denemesi')
            sql_insert_into("tanımlanamadı", "basarısız", created_date)
            # sql connection kapatma
            conn.close()
            tk.destroy()


bd = None
def giris():
    log_in()

    messagebox.showinfo("hoşgeldiniz", "kolay gelsin")
    tk.destroy()

    def scroll_display(string):
        mylist.insert(END, string)

    tk1 = Tk()
    tk1.title("TESTING WINDOW")
    tk1.geometry("800x500")
    scrollbar = Scrollbar(tk1)
    scrollbar.pack(side=RIGHT, fill=Y)
    mylist = Listbox(tk1, yscrollcommand=scrollbar.set)
    mylist.pack(side=RIGHT, fill=X, expand=1)
    scrollbar.config(command=mylist.yview)
    port_list = [port.device for port in serial.tools.list_ports.comports()]
    while 1:
        if len(port_list) == 0:
            time.sleep(1)
            print("LUTFEN OPTİK PORT BAĞLANTISINI YENİLEYİNİZ")
        else:
            break
    selected_port_var = StringVar(tk1)
    selected_port_var.set(port_list[0])
    port_menu = OptionMenu(tk1, selected_port_var, *port_list)
    port_menu.pack()

    def select_comport():
        selected_port = selected_port_var.get()
        return selected_port

    select_comport = select_comport()

    while 1:
        try:
            optik1 = serial.Serial(port=select_comport, bytesize=serial.SEVENBITS, parity=serial.PARITY_EVEN,
                                   stopbits=serial.STOPBITS_ONE, timeout=1)
            if optik1.isOpen():
                print("Seri port kullanılabilir.")
                # break
        except serial.SerialException:
            time.sleep(1)
            print("Seri port açma hatası, port bağlantısını yineleyiniz")
        break

    def destroy():
        tk1.destroy()

    def baudrate_ayarla():
        global bd
        try:
            bd = int(E3.get())  # Giriş kutusundan tamsayı değerini al
        except ValueError:
            print("Geçersiz tamsayı!")

    def yaz_saati_kontrol():
        print("yaz saati kontrolü basladı")
        logger2.error("yaz saati kontrolü basladı")
        scroll_display("yaz saati kontrolü basladı")
        y = int(input("kaç yıllık yaz saati testi istersiniz?  :"))
        print("BaudRate : ", bd)
        logger2.error("BaudRate : " + str(bd) + " seçildi")
        scroll_display("BaudRate : " + str(bd) + " seçildi")
        readMode = "R2"
        writeMode = "W2"
        # executeMode = "E2"

        optik = serial.Serial(port=select_comport, bytesize=serial.SEVENBITS, parity=serial.PARITY_EVEN,
                              stopbits=serial.STOPBITS_ONE, timeout=1)
        if optik.isOpen():  # Seri port meşgul değilse devam et
            print("Seri port açıldı.")
        else:
            print("Seri port meşgul durumda.")

        def parse_yil_oku():
            tarih_oku_str = tarih_oku_obis.decode("utf-8")
            ac_parantez_yil = tarih_oku_str.find("(")
            ilk_tire_yil = tarih_oku_str.find("-")
            parse_tarih_yil = tarih_oku_str[ac_parantez_yil + 1:ilk_tire_yil]
            # print("parse_tarih_yil :",parse_tarih_yil)
            return parse_tarih_yil

        def createobiscode(pm, obis, parameter):
            obiscode = pm + "\u0002" + obis + "(" + parameter + ")" + "\u0003"
            obiscode = "\u0001" + pm + "\u0002" + obis + "(" + parameter + ")" + "\u0003" + \
                       chr(calculatebcc(obiscode)) + "\r\n"
            return obiscode

        def calculatebcc(obis_code):
            bcc = 0
            res = bytes(obis_code, 'utf-8')
            for k in range(len(res)):
                bcc ^= res[k]
            return bcc

        create_obis_tarih_oku = createobiscode(readMode, "0.9.2", "00")
        create_obis_saat_oku = createobiscode(readMode, "0.9.1", "00")

        def analyze_buffer_for_meter_id(buffer):
            retval = buffer
            replacements = {
                #Bu bölümde model bazlı isim değişimleri yapılıyor
            }

        def sifre_hesapla():
            #Bu bölümde dll dosyanızın ilgili şifre fonksiyonlarını çağırmalısınız
            obj = DlldekiAnaFonksiyonunAdı()
            obj.analyzeMeterID(flag_after_anlyze)
            # print("analyzeMeterID :", analyzeMeterID)
            obj.calculateProgrammingPassword(string_serino)
            # print("calculateProgrammingPassword  :",calculateProgrammingPassword)
            get_password = obj.get_password()
            # print("get_password  :",get_password)
            take_get_password_answer = createobiscode("P1", "", str(get_password))
            # print("take_get_password_answer :",take_get_password_answer)
            return take_get_password_answer

        debug = 0

        def send_serial(data, serialport, startbaudrate, baudrate, waittime):
            if debug:
                print("send_serial_1")
            serialport.baudrate = startbaudrate
            # print("data: ", data)
            serialport.write(data.encode())
            time.sleep(waittime)
            if debug:
                print("send_serial_2")
            serialport.baudrate = baudrate
            buffer = read_serial(serialport)
            return buffer

        def read_serial(serialport):
            if debug:
                print("read_serial_1")
            # print(serialport.baudrate)
            return serialport.readline()

        def tailflag():
            t = flag.decode()
            # print(type(t))
            ac_parantez_flag = t.find(">")
            kapa_parantez_flag = t.find(")")
            ham_tail_flag = t[ac_parantez_flag + 1:kapa_parantez_flag + 1]
            # print("tail_flag :", tail_flag)
            return ham_tail_flag

        def headflag():
            h = flag.decode()
            ac_parantez_flag = h.find("/")
            kapa_parantez_flag = h.find(">")
            ham_head_flag = h[ac_parantez_flag: kapa_parantez_flag + 1]
            # print("head_flag :", head_flag)
            return ham_head_flag

        def programlama_gecisi():
            flag2 = send_serial("/?!\r\n", optik, 300, 300, 0.3)
            print(flag2)
            send_serial("\u0006061\r\n", optik, 300, bd, 0.3)
            get_programming_password_answer2 = send_serial(sifre_hesapla, optik, bd, bd, 0.1)
            while True:
                if len(get_programming_password_answer2) == 1:
                    print("sifre_hesapla : ACK")
                    break
                else:
                    print("sifre_hesapla : NACK")
                    time.sleep(1)

        def tarih_obis_oku():
            tarih_oku = send_serial(create_obis_tarih_oku, optik, bd, bd, 0.3)
            # print("tarih_oku :", tarih_oku)
            while True:
                if len(tarih_oku) == 18:
                    tarih_oku_hex = tarih_oku.hex()
                    hex_tarih_okuma_head = tarih_oku_hex[0:14]
                    hex_tarih_okuma_tail = tarih_oku_hex[30:32]
                    if ((hex_tarih_okuma_head == "02302e392e3228") and (hex_tarih_okuma_tail == "29")) \
                            or ((hex_tarih_okuma_head == "41302e392e3228") and (hex_tarih_okuma_tail == "29")) \
                            or ((hex_tarih_okuma_head == "40302e392e3228") and (hex_tarih_okuma_tail == "29")):
                        # print("tarih okuma : ACK ")
                        break
                    else:
                        print("tarih okuma : NACK tekrar denenecek")
                        time.sleep(7)
                        send_serial("/?!\r\n", optik, 300, 300, 0.3)
                        send_serial("\u0006061\r\n", optik, 300, bd, 0.3)
                        time.sleep(0.16)
                        tarih_oku = send_serial(create_obis_tarih_oku, optik, bd, bd, 0.3)
                        print("tarih_oku :", tarih_oku)
                    # print("tarih_oku hex :", tarih_oku.hex())
                else:
                    print("tarih okuma : NACK tekrar denenecek")
                    time.sleep(7)
                    send_serial("/?!\r\n", optik, 300, 300, 0.3)
                    send_serial("\u0006061\r\n", optik, 300, bd, 0.3)
                    get_programming_password_answer1 = send_serial(sifre_hesapla, optik, bd, bd, 0.1)
                    while True:
                        if len(get_programming_password_answer1) == 1:
                            print("sifre_hesapla : ACK")
                            break
                        else:
                            print("sifre_hesapla : NACK")

                            time.sleep(1)
                            break
                    tarih_oku = send_serial(create_obis_tarih_oku, optik, bd, bd, 0.3)
                    print("tarih_oku :", tarih_oku)
            return tarih_oku

        flag = send_serial("/?!\r\n", optik, 300, 300, 0.3)
        print("flag :", flag)

        tail_flag = tailflag()
        head_flag = headflag()
        flag_after_anlyze = head_flag + analyze_buffer_for_meter_id(tail_flag)

        serino = send_serial("\u0006061\r\n", optik, 300, bd, 0.3)
        string_serino = serino.decode('Utf-8')
        string_serino_ac_parantez = string_serino.find("(")
        string_serino_kapa_parantez = string_serino.find(")")
        serino = string_serino[string_serino_ac_parantez + 1: string_serino_kapa_parantez]
        print("0.0.0(" + serino + ")")
        scroll_display("0.0.0(" + serino + ")")
        sifre_hesapla = sifre_hesapla()
        get_programming_password_answer = send_serial(sifre_hesapla, optik, bd, bd, 0.1)
        # print("get_programming_password_answer :", get_programming_password_answer)
        # print(len(get_programming_password_answer))
        while True:
            if len(get_programming_password_answer) == 1:
                print("sifre_hesapla : ACK")
                break
            else:
                print("sifre_hesapla : NACK")
                time.sleep(1)
                break

        def yaz_saati_aktif_obis_okuma():
            create_obis_ileri_saat_aktif = createobiscode(readMode, "96.90.0", "00")
            # print("96.90.0 kodu :", create_obis_ileri_saat_aktif)
            return create_obis_ileri_saat_aktif

        def yaz_saati_oku(x):
            create_obis_ileri_saat_oku_1 = createobiscode(readMode, "96.90." + str(x), "00")
            # print("gönderilecek obis kodu :",create_obis_ileri_saat_oku_1)
            return create_obis_ileri_saat_oku_1

        tarih_oku_obis = tarih_obis_oku()
        yil = parse_yil_oku()
        # ay = parse_ay_oku()
        # gun = parse_gun_oku()
        ileri_geri_aktif = send_serial(yaz_saati_aktif_obis_okuma(), optik, bd, bd, 0.3)
        # print("96.90.0 obis kodu :",ileri_geri_aktif)
        ileri_geri_saat_1 = send_serial(yaz_saati_oku(1), optik, bd, bd, 0.3)

        def tarih_programla(str_ay, str_gun):
            obis_tarih_yaz = createobiscode(writeMode, "0.9.2", (yil + "-" + str_ay + "-" + str_gun))
            tarih_yaz = send_serial(obis_tarih_yaz, optik, bd, bd, 0.3)
            if tarih_yaz == b'\x06':
                print("yıl : " + "20" + yil + " \t " + "ay :", str_ay + " \t " + "gün :", str_gun, "olarak ayarlandı")
            else:
                print("NACK - TARIH PROGRAMLAMA YAPILAMADI")
            return tarih_yaz

        def saat_programla(saat):
            obis_saat_yaz = createobiscode(writeMode, "0.9.1", saat)
            saat_yaz = send_serial(obis_saat_yaz, optik, bd, bd, 0.3)
            if saat_yaz == b'\x06':
                print("Saat ", saat, "yapıldı")
                scroll_display("Saat " + str(saat) + " yapıldı")
                logger2.error("Saat " + str(saat) + " yapıldı")
            return saat_yaz

        def yaz_saati_aktif():
            ileri_geri_aktif_str = ileri_geri_aktif.decode("utf-8")
            ilk_parantez_ileri_saat = ileri_geri_aktif_str.find("(")
            ikinci_parantez_ileri_saat = ileri_geri_aktif_str.find(")")
            parse_yaz_saati_aktif = ileri_geri_aktif_str[ilk_parantez_ileri_saat + 1: ikinci_parantez_ileri_saat]
            # print("96.90.0 :", parse_yaz_saati_aktif)
            return parse_yaz_saati_aktif

        yaz_saati_aktif = yaz_saati_aktif()
        while True:
            # print("96.90.0 obis kodu : ",yaz_saati_aktif)
            if yaz_saati_aktif == "0":
                time.sleep(10)
                programlama_gecisi()
                print("Yaz saati pasif, aktif edilecek")
                obis_yaz_saati_programla = createobiscode(writeMode, "96.90.0", "1")
                yaz_saati_programla = send_serial(obis_yaz_saati_programla, optik, bd, bd, 0.3)
                if yaz_saati_programla == b'\x06':
                    print("Yaz saati aktif edildi")
                    break
            elif yaz_saati_aktif == "1":
                print("96.90.0 obis kodu AKTIF")
                break
            else:
                print("96.90.0 obis kodu okunamadı")

        def yaz_ileri_saati_parse():
            ileri_saat_str = ileri_geri_saat_1.decode("utf-8")
            ilk_virgul_ileri_saat = ileri_saat_str.find(",")
            ikinci_virgul_ileri_saat = ilk_virgul_ileri_saat + 9
            parse_ileri_tarih = ileri_saat_str[ilk_virgul_ileri_saat + 1: ikinci_virgul_ileri_saat]
            yaz_ileri_saati_parse_yil = parse_ileri_tarih[0:2]
            # print("yaz_ileri_saati_parse_yil :", yaz_ileri_saati_parse_yil)
            return yaz_ileri_saati_parse_yil

        yaz_ileri_saati_parse = yaz_ileri_saati_parse()

        def yil_farki():
            print("sayaç yili :", yil)
            print("ilk yaz saati yili :", yaz_ileri_saati_parse)
            a = int(yil)
            b = int(yaz_ileri_saati_parse)
            yillarin_farki = a + 1 - b
            # print("fark :", yillarin_farki)
            return yillarin_farki

        yil_farki = yil_farki()

        ileri_geri_saat = send_serial(yaz_saati_oku(yil_farki), optik, bd, bd, 0.3)

        # print("ileri_geri_saat :",ileri_geri_saat)

        def mart_ayi_parse_gun():
            yaz_saat_yil_str = ileri_geri_saat.decode("utf-8")
            noktali_virgul_geri_saat = yaz_saat_yil_str.find("-")
            yaz_saati_yil = yaz_saat_yil_str[noktali_virgul_geri_saat + 4: noktali_virgul_geri_saat + 6]
            return yaz_saati_yil

        def ekim_ayi_parse_gun():
            yaz_saat_yil_str = ileri_geri_saat.decode("utf-8")
            tire_geri_saat = yaz_saat_yil_str.rfind("-")
            virgul_geri_saat = yaz_saat_yil_str.rfind(",")
            yaz_saati_yil = yaz_saat_yil_str[tire_geri_saat + 1: virgul_geri_saat]
            return yaz_saati_yil

        for j in range(y):
            # print("tarih ayarlama fonk. girdi")
            # yaz_saati_parse_yil_1 = yaz_saati_parse_yil_1()
            # print("96.90.1 obis kodunun yıl değeri :", yaz_saati_parse_yil_1)
            mart_ayi_parse_gun = mart_ayi_parse_gun()
            # print("mart_ayi_parse_gun :", mart_ayi_parse_gun)
            ekim_ayi_parse_gun = ekim_ayi_parse_gun()
            # print("ekim_ayi_parse_gun :", ekim_ayi_parse_gun)
            string_mart_gunu = str(int(mart_ayi_parse_gun) - 1)
            string_ekim_gunu = str(int(ekim_ayi_parse_gun) - 1)
            tarih_programla("03", string_mart_gunu)
            # print("Mart ayının " + string_mart_gunu + " gunune \t" + "20" + yil + " yılına ayarlandı")
            time.sleep(5)
            programlama_gecisi()
            saat_programla("23:59:57")
            time.sleep(5)
            programlama_gecisi()
            saat_programla("00:59:57")
            time.sleep(5)
            programlama_gecisi()
            saat_programla("01:59:57")
            time.sleep(5)
            programlama_gecisi()
            saat_programla("02:59:57")
            time.sleep(5)
            programlama_gecisi()
            saat_oku = send_serial(create_obis_saat_oku, optik, bd, 9600, 0.3)
            # print("Saat :", saat_oku)
            saat_oku_str = saat_oku.decode("utf-8")
            parantez_saat_oku = saat_oku_str.find("(")
            ikinokta_saat_oku = saat_oku_str.find(":")
            parse_saat = saat_oku_str[parantez_saat_oku + 1: ikinokta_saat_oku]
            # print("Saat :", parse_saat)
            if parse_saat == "04":
                print("20" + yil + " - MART AYI ICIN OTOMATIK ILERI SAAT AYARI BASARILI OLDU")
                print("ACK - YAZ SAATI 1 SAAT ILERI ALINMIS")
                scroll_display("20" + yil + "  - MART AYI ICIN OTOMATIK ILERI SAAT AYARI BASARILI OLDU")
                logger2.error("20" + yil + "  - MART AYI ICIN OTOMATIK ILERI SAAT AYARI BASARILI OLDU")
            else:
                print("20" + yil + " NACK - YAZ SAATI AYARLANAMADI")
                scroll_display("20" + yil + "  NACK - YAZ SAATI AYARLANAMADI")
                logger2.error("20" + yil + "  NACK - YAZ SAATI AYARLANAMADI")
                break
            time.sleep(10)
            programlama_gecisi()
            tarih_programla("10", string_ekim_gunu)
            # print("Ekim ayının " + string_ekim_gunu + " gunune \t" + "20" + yil + " yılına ayarlandı")
            time.sleep(5)
            programlama_gecisi()
            saat_programla("23:59:57")
            time.sleep(5)
            programlama_gecisi()
            saat_programla("00:59:57")
            time.sleep(5)
            programlama_gecisi()
            saat_programla("01:59:57")
            time.sleep(5)
            programlama_gecisi()
            saat_programla("02:59:57")
            time.sleep(5)
            programlama_gecisi()
            saat_programla("03:59:57")
            saat_oku = send_serial(create_obis_saat_oku, optik, bd, 9600, 0.3)
            # print("Saat :", saat_oku)
            saat_oku_str = saat_oku.decode("utf-8")
            parantez_saat_oku = saat_oku_str.find("(")
            ikinokta_saat_oku = saat_oku_str.find(":")
            parse_saat = saat_oku_str[parantez_saat_oku + 1: ikinokta_saat_oku]
            # print("Saat :", parse_saat)
            if parse_saat == "03":
                print("20" + yil + " - EKIM AYI ICIN OTOMATIK GERI SAAT AYARI BASARILI OLDU")
                print("ACK - YAZ SAATI 1 SAAT GERI ALINMIS")
                scroll_display("20" + yil + " - EKIM AYI ICIN OTOMATIK GERI SAAT AYARI BASARILI OLDU")
                logger2.error("20" + yil + " - EKIM AYI ICIN OTOMATIK GERI SAAT AYARI BASARILI OLDU")
            else:
                print("NACK - YAZ SAATI AYARLANAMADI")
                scroll_display("20" + yil + "NACK - YAZ SAATI AYARLANAMADI")
                logger2.error("20" + yil + "NACK - YAZ SAATI AYARLANAMADI")
            time.sleep(10)
            programlama_gecisi()
            tarih_programla("12", "31")
            print("20" + yil + " - 31 ARALIK TARIHINE AYARLANDI")
            scroll_display("20" + yil + " - 31 ARALIK TARIHINE AYARLANDI")
            logger2.error("20" + yil + " - 31 ARALIK TARIHINE AYARLANDI")
            time.sleep(10)
            programlama_gecisi()
            saat_programla("23:59:57")
            time.sleep(10)
            print("\n *********************** Yaz saati testi için", j + 1, ". döngü bitti  *********************** \n")
            scroll_display("***************** Yaz saati testi için " + str(j + 1) + ". döngü bitti *******************")
            logger2.error("***************** Yaz saati testi için " + str(j + 1) + ". döngü sonlandı *****************")
            break

    def endeks_kaydi():
        print("Endeks kaydı testi basladı")
        x = int(input("kaç aylık tüketim istersiniz?  :"))
        z = int(input("Bekleme periyodu giriniz (min 10sn)  :"))
        readMode = "R2"
        writeMode = "W2"
        # executeMode = "E2"
        print("BaudRate : ", bd)
        logger2.error("BaudRate : " + str(bd) + " seçildi")
        scroll_display("BaudRate : " + str(bd) + " seçildi")

        optik = serial.Serial(port=select_comport, bytesize=serial.SEVENBITS, parity=serial.PARITY_EVEN,
                              stopbits=serial.STOPBITS_ONE, timeout=1)
        if optik.isOpen():  # Seri port meşgul değilse devam et
            print("Seri port açıldı.")
        else:
            print("Seri port meşgul durumda.")

        def parse_yil_oku():
            tarih_oku_str = tarih_oku_obis.decode("utf-8")
            ac_parantez_yil = tarih_oku_str.find("(")
            ilk_tire_yil = tarih_oku_str.find("-")
            parse_tarih_yil = tarih_oku_str[ac_parantez_yil + 1:ilk_tire_yil]
            # print("parse_tarih_yil :",parse_tarih_yil)
            return parse_tarih_yil

        def parse_ay_oku():
            tarih_oku_str = tarih_oku_obis.decode("utf-8")
            ac_parantez_ay = tarih_oku_str.find("-")
            ilk_tire_ay = tarih_oku_str.rfind("-")
            parse_tarih_ay = tarih_oku_str[ac_parantez_ay + 1:ilk_tire_ay]
            # print("parse_tarih_ay :",parse_tarih_ay)
            return parse_tarih_ay

        def parse_gun_oku():
            tarih_oku_str = tarih_oku_obis.decode("utf-8")
            ac_parantez_gun = tarih_oku_str.rfind("-")
            ilk_tire_gun = tarih_oku_str.find(")")
            parse_tarih_gun = tarih_oku_str[ac_parantez_gun + 1:ilk_tire_gun]
            # print("parse_tarih_gun :",parse_tarih_gun)
            return parse_tarih_gun

        def createobiscode(pm, obis, parameter):
            obiscode = pm + "\u0002" + obis + "(" + parameter + ")" + "\u0003"
            obiscode = "\u0001" + pm + "\u0002" + obis + "(" + parameter + ")" + "\u0003" + \
                       chr(calculatebcc(obiscode)) + "\r\n"
            return obiscode

        def calculatebcc(obis_code):
            bcc = 0
            res = bytes(obis_code, 'utf-8')
            for j in range(len(res)):
                bcc ^= res[j]
            return bcc

        create_obis_tarih_oku = createobiscode(readMode, "0.9.2", "00")

        def analyze_buffer_for_meter_id(buffer):
            retval = buffer
            replacements = {
                #Model dönüşümleri yapıldı
            }

            for key in replacements:
                retval = retval.replace(key, replacements[key])

            for pattern in ["(BM13-R1)", "(BM12-R1)", "(BT10.LP-R1)", "(BT10-R1)"]:
                if pattern in retval:
                    retval = retval.replace(pattern, "-" + pattern)
                    split_loc = retval.index('>') + 1
                    retval = retval[:split_loc] + "BYLN"
                    break
            return retval

        def sifre_hesapla():
            obj = DllDosyasındakiAnaFonksiyon()
            obj.analyzeMeterID(flag_after_anlyze)
            # print("analyzeMeterID :", analyzeMeterID)
            obj.calculateProgrammingPassword(string_serino)
            # print("calculateProgrammingPassword  :",calculateProgrammingPassword)
            get_password = obj.get_password()
            # print("get_password  :",get_password)
            take_get_password_answer = createobiscode("P1", "", str(get_password))
            # print("take_get_password_answer :",take_get_password_answer)
            return take_get_password_answer

        debug = 0

        def send_serial(data, serialport, startbaudrate, baudrate, waittime):
            if debug:
                print("send_serial_1")
            serialport.baudrate = startbaudrate
            # print("data: ", data)
            serialport.write(data.encode())
            time.sleep(waittime)
            if debug:
                print("send_serial_2")
            serialport.baudrate = baudrate
            buffer = read_serial(serialport)
            return buffer

        def read_serial(serialport):
            if debug:
                print("read_serial_1")
            # print(serialport.baudrate)
            return serialport.readline()

        def tailflag():
            t = flag.decode()
            # print(type(t))
            ac_parantez_flag = t.find(">")
            kapa_parantez_flag = t.find(")")
            ham_tail_flag = t[ac_parantez_flag + 1:kapa_parantez_flag + 1]
            # print("tail_flag :", tail_flag)
            return ham_tail_flag

        def headflag():
            h = flag.decode()
            ac_parantez_flag = h.find("/")
            kapa_parantez_flag = h.find(">")
            ham_head_flag = h[ac_parantez_flag: kapa_parantez_flag + 1]
            # print("head_flag :", head_flag)
            return ham_head_flag

        def programlama_gecisi():
            flag2 = send_serial("/?!\r\n", optik, 300, 300, 0.3)
            print(flag2)
            scroll_display(flag2)
            send_serial("\u0006061\r\n", optik, 300, bd, 0.3)
            get_programming_password_answer2 = send_serial(sifre_hesapla, optik, bd, bd, 0.1)
            while True:
                if len(get_programming_password_answer2) == 1:
                    print("sifre_hesapla : ACK")
                    break
                else:
                    print("sifre_hesapla : NACK")
                    time.sleep(1)
                    break

        def tarih_obis_oku():
            tarih_oku = send_serial(create_obis_tarih_oku, optik, bd, bd, 0.3)
            print("tarih_oku :", tarih_oku)
            scroll_display(tarih_oku)
            while True:
                if len(tarih_oku) == 18:
                    tarih_oku_hex = tarih_oku.hex()
                    hex_tarih_okuma_head = tarih_oku_hex[0:14]
                    hex_tarih_okuma_tail = tarih_oku_hex[30:32]
                    if ((hex_tarih_okuma_head == "02302e392e3228") and (hex_tarih_okuma_tail == "29")) \
                            or ((hex_tarih_okuma_head == "41302e392e3228") and (hex_tarih_okuma_tail == "29")) \
                            or ((hex_tarih_okuma_head == "40302e392e3228") and (hex_tarih_okuma_tail == "29")):
                        # print("tarih okuma : ACK ")
                        break
                    else:
                        print("tarih okuma : NACK tekrar denenecek")
                        scroll_display("tarih okuma : NACK tekrar denenecek")
                        time.sleep(7)
                        send_serial("/?!\r\n", optik, 300, 300, 0.3)
                        send_serial("\u0006061\r\n", optik, 300, bd, 0.3)
                        time.sleep(0.16)
                        tarih_oku = send_serial(create_obis_tarih_oku, optik, bd, 9600, 0.3)
                        print("tarih_oku :", tarih_oku)
                        scroll_display(tarih_oku)
                    # print("tarih_oku hex :", tarih_oku.hex())
                else:
                    print("tarih okuma : NACK tekrar denenecek")
                    scroll_display("tarih okuma : NACK tekrar denenecek")
                    time.sleep(7)
                    send_serial("/?!\r\n", optik, 300, 300, 0.3)
                    send_serial("\u0006061\r\n", optik, 300, bd, 0.3)
                    get_programming_password_answer1 = send_serial(sifre_hesapla, optik, bd, bd, 0.1)
                    while True:
                        if len(get_programming_password_answer1) == 1:
                            print("sifre_hesapla : ACK")
                            scroll_display("sifre_hesapla : ACK")
                            break
                        else:
                            print("sifre_hesapla : NACK")
                            scroll_display("sifre_hesapla : NACK")
                            time.sleep(1)
                            break
                    tarih_oku = send_serial(create_obis_tarih_oku, optik, bd, 9600, 0.3)
                    print("tarih_oku :", tarih_oku)
                    scroll_display(tarih_oku)
            return tarih_oku

        flag = send_serial("/?!\r\n", optik, 300, 300, 0.3)
        print("flag :", flag)
        while True:
            if len(flag) == 0:
                time.sleep(1)
                print("COMPORT BAGLANTISINI YENILEYINIZ VEYA OPTIK KAFANIN BAĞLANTISINDAN EMIN OLUNUZ")
            else:
                break
        scroll_display(flag)
        tail_flag = tailflag()
        head_flag = headflag()
        flag_after_anlyze = head_flag + analyze_buffer_for_meter_id(tail_flag)

        serino_oku = send_serial("\u0006061\r\n", optik, 300, bd, 0.3)
        string_serino = serino_oku.decode('Utf-8')
        string_serino_ac_parantez = string_serino.find("(")
        string_serino_kapa_parantez = string_serino.find(")")
        serino = string_serino[string_serino_ac_parantez + 1: string_serino_kapa_parantez]
        print("0.0.0(" + serino + ")")
        scroll_display("0.0.0(" + serino + ")")
        # print("string serino :", string_serino)

        sifre_hesapla = sifre_hesapla()
        get_programming_password_answer = send_serial(sifre_hesapla, optik, bd, bd, 0.1)
        # print("get_programming_password_answer :", get_programming_password_answer)
        # print(len(get_programming_password_answer))
        while True:
            if len(get_programming_password_answer) == 1:
                print("sifre_hesapla : ACK")
                scroll_display("sifre_hesapla : ACK")
                break
            else:
                print("sifre_hesapla : NACK")
                scroll_display("sifre_hesapla : NACK")
                time.sleep(1)
                break

        def saat_programla(saat):
            obis_saat_yaz = createobiscode(writeMode, "0.9.1", saat)
            saat_yaz = send_serial(obis_saat_yaz, optik, bd, bd, 0.3)
            if saat_yaz == b'\x06':
                print("Saat ",saat," yapıldı")
                scroll_display("Saat " + str(saat) + " yapıldı")
                logger2.error("Saat " + str(saat) + " yapıldı")
            return saat_yaz

        def tarih_programla(tarih):
            obis_tarih_yaz = createobiscode(writeMode, "0.9.2", (yil + "-" + ay + tarih))
            tarih_yaz = send_serial(obis_tarih_yaz, optik, bd, bd, 0.3)
            if tarih_yaz == b'\x06':
                print("Tarih",tarih,"ayarlandı")
                scroll_display("Tarih " + tarih + " ayarlandı")
            return tarih_yaz

        for i in range(x):
            print("tarih ayarlama fonk. girdi")
            scroll_display("tarih ayarlama fonk. girdi")
            tarih_oku_obis = tarih_obis_oku()
            yil = parse_yil_oku()
            ay = parse_ay_oku()
            gun = parse_gun_oku()
            if ay == '04' or ay == '06' \
                    or ay == '09' or ay == '11':
                print("ayın son günü 30")
                scroll_display("ayın son günü 30")
                print("parse_tarih_gun", gun)
                scroll_display(gun)
                if gun == '30':
                    print("if ham_gun == '30' yapısına girdi")
                    scroll_display("if ham_gun == '30' yapısına girdi")
                    print("o günün 05.59.57'e gönder")
                    scroll_display("o günün 05.59.57'e gönder")
                    logger2.error("30.günün T1 tarifesine ayarlandı")
                    saat_programla("05:59:57")
                    time.sleep(z)
                    programlama_gecisi()
                    print("o günün 16.59.57'e gönder")
                    scroll_display("o günün 16.59.57'e gönder")
                    logger2.error("30.günün T2 tarifesine ayarlandı")
                    saat_programla("16:59:57")
                    time.sleep(z)
                    programlama_gecisi()
                    print("o günün 21.59.57'e gönder")
                    scroll_display("o günün 21.59.57'e gönder")
                    logger2.error("30.günün T3 tarifesine ayarlandı")
                    saat_programla("21:59:57")
                    time.sleep(z)
                    programlama_gecisi()
                    print("zamanı 23.59.57'e ayarla")
                    scroll_display("zamanı 23.59.57'e ayarla")
                    logger2.error("ay degerinin 30'u gün geçişi için saat 23.59.57 olarak ayarlandı")
                    saat_programla("23:59:57")
                    time.sleep(z)
                else:
                    print("ay degerinin 29'u 23.59.57'e ayarla")
                    scroll_display("ay degerinin 29'u 23.59.57'e ayarla")
                    logger2.error("ay degerinin 29'una ayarlandı")
                    tarih_programla("-29")
                    time.sleep(1)
                    logger2.error("gün geçişi için saat 23.59.57 olarak ayarlandı")
                    saat_programla("23:59:57")
                    time.sleep(z)
                    programlama_gecisi()
                    print("o günün 05.59.57'e gönder")
                    scroll_display("o günün 05.59.57'e gönder")
                    logger2.error("ay degerinin 29'u saat : 05:59:57 yapıldı")
                    saat_programla("05:59:57")
                    time.sleep(z)
                    programlama_gecisi()
                    print("o günün 16.59.57'e gönder")
                    scroll_display("o günün 16.59.57'e gönder")
                    logger2.error("ay degerinin 29'u saat : 16:59:57 yapıldı yapıldı")
                    saat_programla("16:59:57")
                    time.sleep(z)
                    programlama_gecisi()
                    print("o günün 21.59.57'e gönder")
                    scroll_display("o günün 21.59.57'e gönder")
                    logger2.error("ay degerinin 29'u saat : 21:59:57 yapıldı yapıldı")
                    saat_programla("21:59:57")
                    time.sleep(z)
                    programlama_gecisi()
                    print("o günün 23.59.57'e gönder")
                    scroll_display("o günün 23.59.57'e gönder")
                    logger2.error("ay degerinin 29'u gün geçişi için saat 23.59.57 olarak ayarlandı")
                    saat_programla("23:59:57")
                    time.sleep(z)
            elif ay == '01' or ay == '03' \
                    or ay == '05' or ay == '07' \
                    or ay == '08' or ay == '10' or \
                    ay == '12':
                print("ayın son günü 31")
                scroll_display("ayın son günü 31")
                if gun == '31':
                    print("ay degerinin 31'i saat : 05:59:57 programla")
                    scroll_display("ay degerinin 31'i saat : 05:59:57 programla")
                    logger2.error("ay degerinin 31'i saat : 05:59:57 yapıldı")
                    saat_programla("05:59:57")
                    time.sleep(z)
                    programlama_gecisi()
                    print("ay degerinin 31'i saat : 16:59:57 programla")
                    scroll_display("ay degerinin 31'i saat : 16:59:57 programla")
                    logger2.error("ay degerinin 31'i saat : 16:59:57 yapıldı")
                    time.sleep(1)
                    saat_programla("16:59:57")
                    time.sleep(z)
                    programlama_gecisi()
                    print("ay degerinin 31'i saat : 21:59:57 programla")
                    scroll_display("ay degerinin 31'i saat : 21:59:57 programla")
                    logger2.error("ay degerinin 31'i saat : 21:59:57 yapıldı")
                    time.sleep(1)
                    saat_programla("21:59:57")
                    time.sleep(z)
                    programlama_gecisi()
                    print("ay degerinin 31'i gün geçişi için saat 23.59.57 olarak programla")
                    scroll_display("ay degerinin 31'i gün geçişi için saat 23.59.57 olarak programla")
                    logger2.error("ay degerinin 31'i gün geçişi için saat 23.59.57 olarak ayarlandı")
                    time.sleep(1)
                    saat_programla("23:59:57")
                    time.sleep(z)
                else:
                    print("ay degerinin 30'u gün geçişi için saat 23.59.57 olarak programla")
                    scroll_display("ay degerinin 30'u gün geçişi için saat 23.59.57 olarak programlama")
                    logger2.error("ay degerinin 30'u gün geçişi için saat 23.59.57 olarak ayarlandı")
                    tarih_programla("-30")
                    time.sleep(1)
                    saat_programla("23:59:57")
                    time.sleep(z)
                    programlama_gecisi()
                    print("ay degerinin 30'u saat 05.59.57 olarak programlama")
                    scroll_display("ay degerinin 30'u saat 05.59.57 olarak programlama")
                    logger2.error("ay degerinin 30'u saat 05.59.57 olarak ayarlandı")
                    saat_programla("05:59:57")
                    time.sleep(z)
                    programlama_gecisi()
                    print("ay degerinin 30'u saat 16.59.57 olarak programlama")
                    scroll_display("ay degerinin 30'u saat 16.59.57 olarak programlama")
                    logger2.error("ay degerinin 30'u saat 16.59.57 olarak ayarlandı")
                    saat_programla("16:59:57")
                    time.sleep(z)
                    programlama_gecisi()
                    print("ay degerinin 30'u 21.59.57 olarak programlama")
                    scroll_display("ay degerinin 30'u 21.59.57 olarak programlama")
                    logger2.error("ay degerinin 30'u 21.59.57 olarak ayarlandı")
                    saat_programla("21:59:57")
                    time.sleep(z)
                    programlama_gecisi()
                    print("ay degerinin 30'u gün geçişi için saat 23.59.57 olarak programlama")
                    scroll_display("ay degerinin 30'u gün geçişi için saat 23.59.57 olarak programlama")
                    logger2.error("ay degerinin 30'u gün geçişi için saat 23.59.57 olarak ayarlandı")
                    saat_programla("23:59:57")
                    time.sleep(z)
            elif ay == '02':
                if int(yil) % 4 == 0 and int(yil) != 0:
                    print("\nŞubat ayının son günü 29")
                    scroll_display("\nŞubat ayının son günü 29")
                    if gun == '29':
                        print("ay degerinin 29'u saat 05.59.57 olarak programlama")
                        scroll_display("ay degerinin 29'u saat 05.59.57 olarak programlama")
                        logger2.error("ay degerinin 29'u saat 05.59.57 olarak ayarlandı")
                        saat_programla("05:59:57")
                        time.sleep(z)
                        programlama_gecisi()
                        print("ay degerinin 29'u 16.59.57 olarak programlama")
                        scroll_display("ay degerinin 29'u 16.59.57 olarak programlama")
                        logger2.error("ay degerinin 29'u 16.59.57 olarak ayarlandı")
                        saat_programla("16:59:57")
                        time.sleep(z)
                        programlama_gecisi()
                        print("ay degerinin 29'u saat 21.59.57 olarak programlama")
                        scroll_display("ay degerinin 29'u saat 21.59.57 olarak programlama")
                        logger2.error("ay degerinin 29'u saat 21.59.57 olarak ayarlandı")
                        saat_programla("21:59:57")
                        time.sleep(z)
                        programlama_gecisi()
                        print("ay degerinin 29'u gün geçişi için saat 23.59.57 olarak programlama")
                        scroll_display("ay degerinin 29'u gün geçişi için saat 23.59.57 olarak programlama")
                        logger2.error("ay degerinin 29'u gün geçişi için saat 23.59.57 olarak ayarlandı")
                        saat_programla("23:59:57")
                        time.sleep(z)
                    else:
                        print("ay degerinin 28'i gün geçişi için saat 23.59.57 olarak programlama")
                        scroll_display("ay degerinin 28'i gün geçişi için saat 23.59.57 olarak programlama")
                        logger2.error("ay degerinin 28'i gün geçişi için saat 23.59.57 olarak ayarlandı")
                        tarih_programla("-28")
                        time.sleep(1)
                        saat_programla("23:59:57")
                        time.sleep(z)
                        programlama_gecisi()
                        print("o günün 05.59.57'e gönder")
                        scroll_display("o günün 05.59.57'e gönder")
                        logger2.error("ay degerinin 29'u saat 05.59.57 olarak ayarlandı")
                        saat_programla("05:59:57")
                        time.sleep(z)
                        programlama_gecisi()
                        print("o günün 16.59.57'e gönder")
                        scroll_display("o günün 16.59.57'e gönder")
                        logger2.error("ay degerinin 29'u saat 16.59.57 olarak ayarlandı")
                        saat_programla("16:59:57")
                        time.sleep(z)
                        programlama_gecisi()
                        print("o günün 21.59.57'e gönder")
                        scroll_display("o günün 21.59.57'e gönder")
                        logger2.error("ay degerinin 29'u saat 21.59.57 olarak ayarlandı")
                        saat_programla("21:59:57")
                        time.sleep(z)
                        programlama_gecisi()
                        print("o günün 23.59.57'e gönder")
                        scroll_display("o günün 23.59.57'e gönder")
                        logger2.error("ay degerinin 29'u gün geçişi için saat 23.59.57 olarak ayarlandı")
                        saat_programla("23:59:57")
                        time.sleep(z)
                else:
                    print("\nŞubat ayının son günü 28")
                    scroll_display("\nŞubat ayının son günü 28")
                    if gun == '28':
                        print("o ayın o gününün 05.59.57'e gönder")
                        scroll_display("o ayın o gününün 05.59.57'e gönder")
                        logger2.error("ay degerinin 28'i saat 05.59.57 olarak ayarlandı")
                        saat_programla("05:59:57")
                        time.sleep(z)
                        programlama_gecisi()
                        print("o günün 16.59.57'e gönder")
                        scroll_display("o günün 16.59.57'e gönder")
                        logger2.error("ay degerinin 28'i saat 16.59.57 olarak ayarlandı")
                        saat_programla("16:59:57")
                        time.sleep(z)
                        programlama_gecisi()
                        print("o günün 21.59.57'e gönder")
                        scroll_display("o günün 21.59.57'e gönder")
                        logger2.error("ay degerinin 28'i saat 21.59.57 olarak ayarlandı")
                        saat_programla("21:59:57")
                        time.sleep(z)
                        programlama_gecisi()
                        print("o günün 23.59.57'e gönder")
                        scroll_display("o günün 23.59.57'e gönder")
                        logger2.error("ay degerinin 28'i gün geçişi için saat 23.59.57 olarak ayarlandı")
                        saat_programla("23:59:57")
                        time.sleep(z)
                    else:
                        print("ay degerinin 27'si 23.59.57'e ayarla")
                        scroll_display("ay degerinin 27'si 23.59.57'e ayarla")
                        logger2.error("ay degerinin 27'si gün geçişi için saat 23.59.57 olarak ayarlandı")
                        tarih_programla("-27")
                        time.sleep(1)
                        saat_programla("23:59:57")
                        time.sleep(z)
                        programlama_gecisi()
                        print("o günün 05.59.57'e gönder")
                        scroll_display("o günün 05.59.57'e gönder")
                        logger2.error("ay degerinin 28'i saat 05.59.57 olarak ayarlandı")
                        saat_programla("05:59:57")
                        time.sleep(z)
                        programlama_gecisi()
                        print("o günün 16.59.57'e gönder'")
                        scroll_display("o günün 16.59.57'e gönder")
                        logger2.error("ay degerinin 28'i saat 16.59.57 olarak ayarlandı")
                        saat_programla("16:59:57")
                        time.sleep(z)
                        programlama_gecisi()
                        print("o günün 21.59.57'e gönder")
                        scroll_display("o günün 21.59.57'e gönder")
                        logger2.error("ay degerinin 28'i saat 21.59.57 olarak ayarlandı")
                        saat_programla("21:59:57")
                        time.sleep(z)
                        programlama_gecisi()
                        print("o günün 23.59.57'e gönder")
                        scroll_display("o günün 23.59.57'e gönder")
                        logger2.error("ay degerinin 28'i gün geçişi için saat 23.59.57 olarak ayarlandı")
                        saat_programla("23:59:57")
                        time.sleep(z)
            print("\n ********************** Endeks kaydı için", i + 1, ". döngü bitti  ************************ \n")
            scroll_display("**************** Endeks kaydı için " + str(i+1) + ". döngü bitti  ************************")
            logger2.error("***************** Endeks kaydı için " + str(i+1) + ". döngü bitti  ************************")
            if i+1 != x:
                programlama_gecisi()
    B3 = Button(tk1, text="endeks kaydını baslat", bg="blue", command=endeks_kaydi)
    B3.place(x=150, y=0)
    B4 = Button(tk1, text="yaz saati testini baslat", bg="blue", command=yaz_saati_kontrol)
    B4.place(x=150, y=40)
    B5 = Button(tk1, text="çık", bg="red", command=destroy)
    B5.place(x=700, y=0)
    L3 = Label(tk1, text="BaudRate")
    L3.place(x=350, y=0)
    E3 = Entry(tk1, width=10)
    E3.place(x=350, y=25)
    B6 = Button(tk1, text="ayarla", bg="grey", command=baudrate_ayarla)
    B6.place(x=365, y=50)


tk = Tk()
tk.title("TESTER INTERFACE")
tk.geometry("600x450")
tk.iconbitmap(r"Pencerede kullanılacak bit resminin dosya yolu")
resim = ImageTk.PhotoImage(Image.open(r"Pencerede kullanılacak resmin dosya yolu"))
lresim = Label(tk,image=resim)
lresim.place(x=250,y=10)

L1 = Label(tk, text="Kullanıcı adını giriniz")
L1.place(x=75, y=115)
E1 = Entry(tk, width=25)
E1.place(x=50, y=140)
L2 = Label(tk, text="Sifre giriniz")
L2.place(x=95, y=170)
E2 = Entry(tk, width=25, show="*")
E2.place(x=50, y=195)
B1 = Button(tk, text="giriş", bg="green", command=giris)
B1.place(x=120, y=225)
tk.mainloop()