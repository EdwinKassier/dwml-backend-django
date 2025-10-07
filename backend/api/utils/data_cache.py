import sqlite3
from datetime import datetime, timedelta
from dateutil import parser

from api.models.portfolio import Results, LOGGING
from api.models.portfolio import ResultsSerializer, LOGGINGSerializer
from api.models.market_data import OpeningAverage
from api.models.market_data import OpeningAverageSerializer


class DataCache:

    def __init__(self, coin_symbol, investment):
        self.coin_symbol = str(coin_symbol)
        self.investment = int(investment)

    # Check if there exists a freshly cached result for the current query
    def check_if_valid_final_result_exists(self):

        existing_result_raw = (
            Results.objects.get(SYMBOL=self.coin_symbol, INVESTMENT=self.investment)
            if Results.objects.filter(
                SYMBOL=self.coin_symbol, INVESTMENT=self.investment
            ).exists()
            else ""
        )

        if existing_result_raw != "":
            # There exists a historical cache for this query
            serializer = ResultsSerializer(existing_result_raw, many=False)

            print(serializer)
            return True

        else:
            # There doesn\'t exist a valid historical query
            return False

    # Get cached result for the current query
    def get_valid_final_result(self):

        existing_result_raw = (
            Results.objects.get(SYMBOL=self.coin_symbol, INVESTMENT=self.investment)
            if Results.objects.filter(
                SYMBOL=self.coin_symbol, INVESTMENT=self.investment
            ).exists()
            else ""
        )

        if existing_result_raw != "":

            serializer = ResultsSerializer(existing_result_raw, many=False)

            print(serializer.data)
            return serializer.data
        else:
            # There doesn\'t exist a valid historical query
            return {}

    # Check if we have already stored a cached version of the opening price data for the symbol
    def check_if_historical_cache_exists(self):

        existing_result_raw = (
            OpeningAverage.objects.get(SYMBOL=self.coin_symbol)
            if OpeningAverage.objects.filter(SYMBOL=self.coin_symbol).exists()
            else ""
        )

        query = f"SELECT * from OpeningAverage WHERE SYMBOL = '{self.coin_symbol}'"

        if existing_result_raw != "":
            print(f"There exists a historical cache for this query {query}")
            return True
        else:
            print(f"There doesn't exist a valid historical query {query}")
            return False

    # Get cached version of the opening price data for the symbol
    def get_historical_cache(self):

        existing_result_raw = (
            OpeningAverage.objects.get(SYMBOL=self.coin_symbol)
            if OpeningAverage.objects.filter(SYMBOL=self.coin_symbol).exists()
            else ""
        )

        query = f"SELECT * from OpeningAverage WHERE SYMBOL = '{self.coin_symbol}'"

        if existing_result_raw != "":
            serializer = OpeningAverageSerializer(existing_result_raw, many=False)

            print(serializer.data)
            return serializer.data
        else:
            return {}

    # Insert current query into the logging table
    def insert_into_logging(self):

        combined_results = {
            "SYMBOL": self.coin_symbol,
            "INVESTMENT": self.investment,
            "GENERATIONDATE": datetime.now().isoformat(),
        }
        try:

            logging_item = LOGGING(
                SYMBOL=self.coin_symbol,
                INVESTMENT=self.investment,
                GENERATIONDATE=datetime.now().isoformat(),
            )

            logging_item.save()
        except Exception as e:
            print(e)

    # Insert final result from a query into the results table
    def insert_into_result(self, result):

        QUERY = f"{self.coin_symbol}-{self.investment}"

        try:
            result_item = Results(
                NUMBERCOINS=result["NUMBERCOINS"],
                PROFIT=result["PROFIT"],
                GROWTHFACTOR=result["GROWTHFACTOR"],
                LAMBOS=result["LAMBOS"],
                INVESTMENT=self.investment,
                SYMBOL=self.coin_symbol,
                GENERATIONDATE=datetime.now().isoformat(),
            )

            result_item.save()
        except Exception as e:
            print(e)

    # Insert final result from data collector into the db
    def insert_into_opening_average(self, result):

        combined_results = {**result, "SYMBOL": self.coin_symbol}

        try:
            opening_average_item = OpeningAverage(
                SYMBOL=self.coin_symbol,
                AVERAGE=result["AVERAGE"],
                GENERATIONDATE=datetime.now().isoformat(),
            )

            opening_average_item.save()
        except Exception as e:
            print(e)

    # Check if queried table exists
    def check_table_exists(self, table_name):
        # Create cursor
        cur = self.connection.cursor()

        # get the count of tables with the given table name
        cur.execute(
            f""" SELECT count(name) FROM sqlite_master WHERE type='table' AND name='{table_name}' """
        )

        if cur.fetchone()[0] == 1:
            print(f"The {table_name} Table exists")
            return True
        else:
            print(f"The {table_name} Table does not exist")
            return False
