class TgBot:

    def __init__(self) -> None:
        self.language = "en"

    def setup_resolution(self, resolution):
        self.resolution = resolution
        return resolution

    def setup_number(self, number):
        self.number = number
        return number
    
    def setup_lang(self, language):
        if language == "lang_uzb": 
            print("Language", language)
            self.language = "uzb"
            return "O'zbek 🇺🇿"
        elif language == "lang_en":
            print("Language", language)
            self.language = "en"
            return "English 🇬🇧"
        else:
            print("To'g'ri til tanlanmadi")
            return None

    def main(self):
        print('running main function')
