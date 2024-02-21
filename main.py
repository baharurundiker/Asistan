import speech_recognition as sr
from gtts import gTTS
import playsound
import os
from datetime import datetime
import random
import webbrowser

class SesliAsistan:
    def __init__(self):
        self.recognizer = sr.Recognizer()



    def saat_mesaji(self):
        hour = datetime.now().hour
        if hour >= 4 and hour < 12:
            return "Günaydın, size nasıl yardımcı olabilirim?"

        elif hour >= 12 and hour < 17:
            return "İyi günler, size nasıl yardımcı olabilirim?"

        else:
            return "İyi akşamlar, size nasıl yardımcı olabilirim?"
    def dinle(self):
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source)
            print("Sizi dinliyorum...")
            audio = self.recognizer.listen(source)

        try:
            text = self.recognizer.recognize_google(audio, language="tr-TR")
            print("Söylediğiniz: ", text)
            return text.lower()
        except sr.UnknownValueError:
            print("Anlayamadım, tekrar eder misiniz?")
            return ""
        except sr.RequestError:
            print("Bağlantı hatası, lütfen daha sonra tekrar deneyin.")
            return ""

    def cevap_ver(self, soru):
        if "merhaba" in soru:
            return "merhaba!"
        elif "selam" in soru:
            return "Selam! Sana da selam olsun."
        elif "teşekkür ederim" in soru or "teşekkürler" in soru:
            return "Rica ederim."
        elif "görüşürüz" in soru:
            return "Görüşürüz."
        elif "hangi gündeyiz" in soru:
            today = datetime.now().strftime("%A").capitalize()
            if today == "Monday":
                today = "Pazartesi"
            elif today == "Tuesday":
                today = "Salı"
            elif today == "Wednesday":
                today = "Çarşamba"
            elif today == "Thursday":
                today = "Perşembe"
            elif today == "Friday":
                today = "Cuma"
            elif today == "Saturday":
                today = "Cumartesi"
            elif today == "Sunday":
                today = "Pazar"
            return today
        elif "saat" in soru and "kaç" in soru:
            clock = datetime.now().strftime("%H:%M")
            return random.choice(["Saat: " + clock, "Hemen bakıyorum: " + clock])
        elif "google'da ara" in soru:
            self.konus("Ne aramamı istersin?")
            search = self.dinle()
            url = "https://www.google.com/search?q=" + search
            webbrowser.open_new_tab(url)
            return "{} içi Google'da bulabildiklerimi listeliyorum.".format(search)
        elif "tekrar et" in soru:
            self.tekrar_et()
        elif "bugünün tarihi" in soru:
            gunler = {
                "Monday": "Pazartesi",
                "Tuesday": "Salı",
                "Wednesday": "Çarşamba",
                "Thursday": "Perşembe",
                "Friday": "Cuma",
                "Saturday": "Cumartesi",
                "Sunday": "Pazar"
            }
            gun = gunler[datetime.now().strftime("%A")]
            tarih = datetime.now().strftime("%d.%m.%Y")
            return f"Bugün {gun} ve tarih {tarih}"

        else:
            return "Üzgünüm, anlamadım."

    def konus(self, metin):
        tts = gTTS(text=metin, lang="tr", slow=False)
        tts.save("response.mp3")
        playsound.playsound("response.mp3")
        os.remove("response.mp3")

    def tekrar_et(self):
        self.konus("Ne söylememi istersiniz?")
        metin = self.dinle()
        self.konus("Söylediğiniz: " + metin)
        return metin
    def baslat(self):
        print("Sistem aktif.")
        mesaj = self.saat_mesaji()
        print(mesaj)
        while True:
            soru = self.dinle()
            if soru:
                    cevap = self.cevap_ver(soru)
                    print("Cevap:", cevap)
                    self.konus(cevap)
                    if "görüşürüz" in soru:
                        break
if __name__ == "__main__":
    asistan = SesliAsistan()
    asistan.baslat()
