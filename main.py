import datetime as dt


class Record:
    def __init__(self, amount, comment, date=''):
        self.amount = amount

        # Условие логичнее сделать наоборот 
        # dt.datetime.strptime(date, '%d.%m.%Y').date() if date else ...
        self.date = (
            dt.datetime.now().date() if
            not
            date else dt.datetime.strptime(date, '%d.%m.%Y').date())
        self.comment = comment


class Calculator:
    def __init__(self, limit):
        self.limit = limit

        # Тут так же можно добавить типизацию, например
        # self.records: List[Record] = []
        self.records = []

    def add_record(self, record):
        # Тут и далее нет типизации, что такое record? в чём измеряется amount у Record?
        # Например, def add_record(self, record: Record) -> None:
        # Тут и далее нет докстрингов к функциям
        self.records.append(record)

    def get_today_stats(self):
        today_stats = 0
        for Record in self.records:
            if Record.date == dt.datetime.now().date():
                today_stats = today_stats + Record.amount
                # Лучше: today_stats += Record.amount
        return today_stats

    def get_week_stats(self):
        week_stats = 0
        today = dt.datetime.now().date()

        for record in self.records:

            # today - record.date).days можно вынести в отдельную переменную
            # Потом проверить входит ли она в диапазон 0 <= days < 7 одним условием
            if (
                (today - record.date).days < 7 and
                (today - record.date).days >= 0
            ):
                week_stats += record.amount
        return week_stats


class CaloriesCalculator(Calculator):
    # Комментарий к функции должен быть в докстринге
    def get_calories_remained(self):  # Получает остаток калорий на сегодня

        # Что такое X?  Название переменной должно быть осмысленным 
        x = self.limit - self.get_today_stats()
        if x > 0:
            # Бэкслеши для переносов не применяются.
            return f'Сегодня можно съесть что-нибудь' \
                   f' ещё, но с общей калорийностью не более {x} кКал'
        else:
            # Просто return 'Хватит есть!'
            return('Хватит есть!')


class CashCalculator(Calculator):

    # Лишнее приведение типов
    USD_RATE = float(60)  # Курс доллар США.
    EURO_RATE = float(70)  # Курс Евро.

    def get_today_cash_remained(self, currency,
                                USD_RATE=USD_RATE, EURO_RATE=EURO_RATE):
        # Нет смысла в переменных USD_RATE, EURO_RATE, курсы можно достать через экземпляр self.USD_RATE
        currency_type = currency
        cash_remained = self.limit - self.get_today_stats()

        # Вынести в отдельную функцию
        # Почему в одном случае проверка идёт currency, в других currency_type?
        # Нет описание зачем эта часть кода нужна.
        # А если я введу currency которое не подходит ни под одно из условий? 
        # Нужно предложить пользователю в каком формате выводить валюту "rub", "usd" или "eur"
        # и вызывать ошибку, в случае несоответствия
        # + лучше где то указать, что по умолчанию amount хранится в рублях
        if currency == 'usd':
            cash_remained /= USD_RATE
            currency_type = 'USD'
        elif currency_type == 'eur':
            cash_remained /= EURO_RATE
            currency_type = 'Euro'
        elif currency_type == 'rub':
            cash_remained == 1.00
            currency_type = 'руб'
        if cash_remained > 0:
            return (
                # В f-строках применяется только подстановка переменных и нет логических или
                # арифметических операций, вызовов функций и подобной динамики.
                f'На сегодня осталось {round(cash_remained, 2)} '
                f'{currency_type}'
            )
        elif cash_remained == 0:
            return 'Денег нет, держись'
        elif cash_remained < 0:
            # Бэкслеши для переносов не применяются.
            return 'Денег нет, держись:' \
                   ' твой долг - {0:.2f} {1}'.format(-cash_remained,
                                                     currency_type)

    # Этот код лишний, метод и так подтянется из класса-родителя
    def get_week_stats(self):
        super().get_week_stats()


# Добавить конструкцию if __name__ == ‘__main__’, где реализовать сценарий использования
