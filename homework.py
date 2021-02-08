import datetime as dt


class Record:
    def __init__(self, amount, comment, date=None):
        self.amount = amount
        self.comment = comment
        if date:
            self.date = dt.datetime.strptime(date, '%d.%m.%Y').date()
        else:
            self.date = dt.date.today()


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        return sum([record.amount for record in self.records
                    if record.date == dt.date.today()])

    def get_week_stats(self):
        return sum([record.amount for record in self.records
                    if dt.date.today() - dt.timedelta(days=7)
                    <= record.date <= dt.date.today()])


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):
        calories_remained = self.limit - self.get_today_stats()
        if calories_remained > 0:
            return (f"Сегодня можно съесть что-нибудь ещё, но с общей "
                    f"калорийностью не более {calories_remained} кКал")
        else:
            return "Хватит есть!"


class CashCalculator(Calculator):
    USD_RATE = 74.37
    EURO_RATE = 89.59

    def get_today_cash_remained(self, currency):
        cash_remained = self.limit - self.get_today_stats()
        cur = 'руб'
        if currency == 'usd':
            cash_remained /= CashCalculator.USD_RATE
            cur = 'USD'
        elif currency == 'eur':
            cash_remained /= CashCalculator.EURO_RATE
            cur = 'Euro'

        if cash_remained > 0:
            return f"На сегодня осталось {cash_remained:.2f} {cur}"
        elif cash_remained == 0:
            return "Денег нет, держись"
        else:
            debt = abs(cash_remained)
            return f"Денег нет, держись: твой долг - {debt:.2f} {cur}"
