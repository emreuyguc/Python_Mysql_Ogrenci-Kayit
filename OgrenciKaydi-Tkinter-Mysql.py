from MySQLdb import * 
from tkinter import *
import tkinter.messagebox

#Emre Utku
#PYTHON 3.52 KUllanildi


class Baglanti():
    def __init__(self,ip,kullanici,sifre,veritabani):
        self.ip= ip
        self.kullanici=kullanici
        self.sifre=sifre
        self.veritabani =veritabani

        #TABLE CREATE
        #DB CREATE ! EKLENCEK
    def Baglan(self):
        try:
            self.baglanti=connect(self.ip,self.kullanici,self.sifre,self.veritabani)
            self.islem=self.baglanti.cursor()
            return 1
        except OperationalError as HataBilgisi:
            HataKodu = HataBilgisi.args[0]
            if HataKodu==1045:
                print("Mysql Giris Bilgileri Yanlis")
                return "g"
            elif HataKodu==1049:
                print("Veritabani Bulunamadi")
                return "db"
            else:
                print("Tanimlanmayan Hata Kodu : ",HataKodu)
                return "n"
            
    def VeritabaniOlustur(self,VeritabaniAdi):
        self.VeritabaniAdi = VeritabaniAdi
        try:
            self.baglanti=connect(self.ip,self.kullanici,self.sifre)
            self.islem=self.baglanti.cursor()
            self.islem.execute("CREATE DATABASE "+self.VeritabaniAdi+";")
        
            return 1
        except OperationalError as HataBilgisi:
            HataKodu = HataBilgisi.args
            print(HataKodu)
            return 0
        
    def tablo_olustur(self,sorgu):
        try:
            self.islem.execute(sorgu)
            print("basariyla olusturuldu!")
            return 1
        except:
             return 0
        self.__out__()
        
    def veri_ekle(self,sorgu):
        try:
            self.islem.execute(sorgu)
            self.baglanti.commit()
            print("basariyla veri eklendi!")
            return 1
        except ProgrammingError as Hata:
            HataKodu= Hata.args[0]
            if HataKodu==1146:
                return "t"
            else:
                return "n"
        self.__out__()
        


    def __out__(self):
        self.baglanti.close()
        
def Baglan():
    global sql
    sql=Baglanti(ipAyari.get(),KullaniciAdiAyari.get(),SifreAyari.get(),VeritabaniAyari.get())
    baglantii=sql.Baglan()
    if baglantii==1:
        AyarPencere.destroy()
        OgrenciKayitPencere.deiconify()
        OgrenciKayitPencere.lift()
        OgrenciKayitPencere.attributes('-topmost', True)
        OgrenciKayitPencere.attributes('-topmost', False)
        
    elif baglantii=="db":
        sor = messagebox.askquestion("Veritabani Hatasi!",
                                  VeritabaniAyari.get()+" adinda veritabani bulunamadi olusturmami istermisin?",
                                  )
        if sor=="yes":
            olustur = sql.VeritabaniOlustur(VeritabaniAyari.get())
            if olustur==1:
                messagebox.showinfo(message="Veritabani Basariyla olusturuldu. Simdi Tekrar Baglanabilirsiniz")
            elif olustur==0:
                messagebox.showinfo(message="Hata Olustu")
            
    elif baglantii=="g":
        messagebox.showinfo(message="Giris Bilgileri Yanlis Lutfen Kullanici ve Sifreyi kontrol edin")
    elif baglantii=="n":
        messagebox.showinfo(message="Bilinmeyen HATA")


    
AnaPencere = Tk()
AnaPencere.withdraw()#deiconify gosterir
AyarPencere = Toplevel(AnaPencere)
AyarPencere.geometry("200x150+500+150")
AyarPencere.resizable(width=FALSE, height=FALSE)
AyarPencere["background"]="sky blue"

ipAyarYazi=Label(AyarPencere,text="Ip:",bg="sky blue").place(x=5,y=5)
ipAyari=Entry(AyarPencere)
ipAyari.insert(0, "127.0.0.1")
ipAyari.place(x=70,y=5)

KullaniciAdiYazi=Label(AyarPencere,text="Kullanici:",bg="sky blue").place(x=5,y=30)
KullaniciAdiAyari=Entry(AyarPencere)
KullaniciAdiAyari.insert(0, "root")
KullaniciAdiAyari.place(x=70,y=30)

SifreYazi=Label(AyarPencere,text="Sifre:",bg="sky blue").place(x=5,y=60)
SifreAyari=Entry(AyarPencere)
SifreAyari.place(x=70,y=60)

VeritabaniAyarYazi=Label(AyarPencere,text="Veritabani:",bg="sky blue").place(x=5,y=90)

VeritabaniAyari=Entry(AyarPencere)
VeritabaniAyari.insert(0, "Okul")
VeritabaniAyari.place(x=70,y=90)

BaglanDugme = Button(AyarPencere,text="     Baglan     ",command=Baglan).place(x=70,y=120)


#########################################3

def OgrenciKaydet():
    sorgum=(" insert into ogrenciler(Ad,Soyad,Telefon,Adres,Dt) values (\'"+AdGiris.get()+"\',\'"+SoyadGiris.get()+"\',\'"+TelefonGiris.get()+"\',\'"+AdresGiris.get()+"\',\'"+DtGiris.get()+"\')")
    eklee=sql.veri_ekle(sorgum)
    if eklee=="t":
        sor=messagebox.askquestion(message="Ogrenciler Tablosu Bulunamadi olusturulsunmu ?")
        if sor=="yes":
            try:
                ols=sql.tablo_olustur("CREATE TABLE ogrenciler ( \
    siraNo int NOT NULL AUTO_INCREMENT PRIMARY KEY, \
    Ad varchar(255), \
    Soyad varchar(255), \
    Adres varchar(255), \
    Telefon varchar(255),\
    Dt varchar(255)\
    );")
                if ols==1:
                    messagebox.showinfo(message="Tablo olusturuldu tekrar veri girebilirisiniz.")
                else:
                    messagebox.showinfo(message="Bilinmeyen HATA")
            except:
                messagebox.showinfo(message="Bilinmeyen HATA")
    elif eklee=="n":
        messagebox.showinfo(message="Bilinmeyen HATA")
        
    elif eklee==1:
        messagebox.showinfo(message="Veri Eklendi !")
        
OgrenciKayitPencere = Toplevel(AnaPencere)
OgrenciKayitPencere.withdraw()
OgrenciKayitPencere.geometry("+500+150")
OgrenciKayitPencere["background"]="sky blue"
OgrenciKayitPencere.resizable(width=FALSE, height=FALSE)
    
adYazi=Label(OgrenciKayitPencere,text="Adi:",font=16,bg="sky blue").grid(row=0,column=0,sticky="w")
AdGiris=Entry(OgrenciKayitPencere)
AdGiris.grid(row=0,column=1)

SoyadYazi=Label(OgrenciKayitPencere,text="Soyadi:",font=16,bg="sky blue").grid(row=1,column=0,sticky="w")
SoyadGiris=Entry(OgrenciKayitPencere)
SoyadGiris.grid(row=1,column=1)

TelefonYazi=Label(OgrenciKayitPencere,text="Telefon:",font=16,bg="sky blue").grid(row=2,column=0,sticky="w")
TelefonGiris=Entry(OgrenciKayitPencere)
TelefonGiris.grid(row=2,column=1)

AdresYazi=Label(OgrenciKayitPencere,text="Adres:",font=16,bg="sky blue").grid(row=3,column=0,sticky="w")
AdresGiris=Entry(OgrenciKayitPencere)
AdresGiris.grid(row=3,column=1)

DogumTarihYazi=Label(OgrenciKayitPencere,text="Dogum Tarihi(gg-aa-yyyy):",bg="sky blue").grid(row=4,column=0,sticky="w")
DtGiris=Entry(OgrenciKayitPencere)
DtGiris.grid(row=4,column=1)

Kaydet = Button(OgrenciKayitPencere,text="OGRENCİ KAYDET",command=OgrenciKaydet).grid(row=5,columnspan = 2)



AnaPencere.mainloop()




