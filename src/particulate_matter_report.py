import logging
import sqlite3
import requests

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    handlers=[logging.FileHandler('app.log'),
                              logging.StreamHandler()])


class ParticulateMatterReport:
    """A class for ingesting and analysing PM2.5 data."""

    def __init__(self, device_id):
        self.THRESHOLD = 30
        self.API_URL = "https://pm25.lass-net.org/API-1.0.0"
        self.device_id = device_id
        self.logger = logging.getLogger(f"Particulate Matter Report for device: {self.device_id}")

    def fetch_data(self, device_id: str):
        """ Function to fetch data from the API"""
        response = requests.get(f"{self.API_URL}/device/{device_id}/history/")
        response.raise_for_status()  # Raise an exception for HTTP errors
        if response.json()["num_of_records"] == 0:
            raise Exception(f"Zero Records in history for device id: {device_id}")

        return response.json()

    @staticmethod
    def parse_data(data: dict) -> list:
        """Returns parsed list of timestamps and PM2.5 values from the API response."""
        parsed_data = []

        feeds = data.get('feeds', {})

        for feed in feeds:
            airbox_data = feed.get('AirBox', [])

            for record in airbox_data:
                for timestamp, values in record.items():
                    pm25 = values.get('s_d0')
                    if pm25 is not None:
                        parsed_data.append((timestamp, pm25))

        return parsed_data

    def save_data_to_db(self, data, db_path='pm25_data.db') -> None:
        """ Function to save data into SQLite database"""
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS pm25_data
                     (timestamp TEXT PRIMARY KEY, pm25 REAL)''')

        # Insert data into the table
        for entry in data:
            cursor.execute('INSERT OR IGNORE INTO pm25_data (timestamp, pm25) VALUES (?, ?)', entry)

        conn.commit()
        conn.close()

    def analyse_data(self, db_path='pm25_data.db'):
        """Function to analyse the data"""
        conn = sqlite3.connect(db_path)
        c = conn.cursor()

        # Fetch data from the database
        c.execute('SELECT timestamp, pm25 FROM pm25_data')
        rows = c.fetchall()

        # Detect periods where PM2.5 goes above the threshold
        above_threshold = [row[0] for row in rows if row[1] > self.THRESHOLD]

        # Calculate daily stats
        daily_stats = {}
        for row in rows:
            date = row[0][:10]  # Extract the date part
            pm25 = row[1]
            if date not in daily_stats:
                daily_stats[date] = {'max': pm25, 'min': pm25, 'sum': pm25, 'count': 1}
            else:
                daily_stats[date]['max'] = max(daily_stats[date]['max'], pm25)
                daily_stats[date]['min'] = min(daily_stats[date]['min'], pm25)
                daily_stats[date]['sum'] += pm25
                daily_stats[date]['count'] += 1

        for date in daily_stats:
            daily_stats[date]['avg'] = daily_stats[date]['sum'] / daily_stats[date]['count']

        conn.close()
        return above_threshold, daily_stats

    def generate_report(self, above_threshold, daily_stats) -> None:
        """Function to generate a report based on sensor data"""
        self.logger.info(f"Periods where PM2.5 level went above the threshold of 30: {above_threshold}")

        self.logger.info("\nDaily PM2.5 statistics:")
        for date, stats in daily_stats.items():
            self.logger.info(f"Date: {date}, Max: {stats['max']}, Min: {stats['min']}, Avg: {stats['avg']}")

    def fetch_device_ids(self) -> list:
        """Fetches ids for devices in the airbox project that have returned measurements in the last 2 hours"""

        response = requests.get(f"{self.API_URL}/project/airbox/latest/")
        response.raise_for_status()
        devices = response.json()['feeds']
        device_ids = [device['device_id'] for device in devices]
        return device_ids

    def run_report(self) -> None:
        """Read the data for a device, saves the data into local persistent storage and generates a report"""
        try:
            data = self.fetch_data(self.device_id)
        except Exception(f"Zero Records in history for device id: {self.device_id}"):
            return
        data = self.parse_data(data)

        self.save_data_to_db(data)
        above_threshold, daily_stats = self.analyse_data()
        self.generate_report(above_threshold, daily_stats)
