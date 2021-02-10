import datetime as dt
from typing import Dict, Union


class Record:
    def __init__(self,
                 amount: Union[int, float],
                 comment: str,
                 date: str = None) -> None:
        self.amount = amount
        self.comment = comment
        if date is None:
            self.date = dt.date.today()
        else:
            self.date = dt.datetime.strptime(date, '%d.%m.%Y').date()


class Calculator:
    def __init__(self, limit: float) -> None:
        self.limit = limit
        self.records = []

    def add_record(self, record: Record) -> None:
        """Add record to record list."""
        self.records.append(record)

    def get_today_stats(self) -> float:
        """Return overall amount for current day."""
        today = dt.date.today()
        return sum([record.amount for record in self.records
                    if record.date == today])

    def get_week_stats(self) -> float:
        """Return overall amount for last week."""
        today = dt.date.today()
        week_ago = today - dt.timedelta(weeks=1)
        return sum([record.amount for record in self.records
                    if week_ago < record.date <= today])


class CaloriesCalculator(Calculator):
    def get_calories_remained(self) -> str:
        """Tell whether one could eat something more for today."""
        calories_remained = self.limit - self.get_today_stats()
        if calories_remained > 0:
            return (f"Сегодня можно съесть что-нибудь ещё, но с общей "
                    f"калорийностью не более {calories_remained} кКал")
        return "Хватит есть!"


class CashCalculator(Calculator):
    RUB_RATE = 1.0
    USD_RATE = 74.37
    EURO_RATE = 89.59

    def get_currences(self) -> Dict:
        """Return currency names and up to date rates."""
        return {
            'rub': {
                'name': 'руб',
                'rate': self.RUB_RATE
            },
            'usd': {
                'name': 'USD',
                'rate': self.USD_RATE
            },
            'eur': {
                'name': 'Euro',
                'rate': self.EURO_RATE
            }
        }

    def get_today_cash_remained(self, currency: str = 'rub') -> str:
        """Tell whether one could spend more money today."""
        cash_remained = self.limit - self.get_today_stats()
        currences = self.get_currences()

        if cash_remained == 0:
            return "Денег нет, держись"
        elif cash_remained > 0:
            cash_remained /= currences[currency]['rate']
            return (f"На сегодня осталось "
                    f"{cash_remained:.2f} {currences[currency]['name']}")
        else:
            debt = abs(cash_remained) / currences[currency]['rate']
            return (f"Денег нет, держись: твой долг - "
                    f"{debt:.2f} {currences[currency]['name']}")
