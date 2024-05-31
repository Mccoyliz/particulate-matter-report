from unittest import TestCase
from unittest.mock import patch
import requests
from src.particulate_matter_report import ParticulateMatterReport

pm = ParticulateMatterReport('08BEAC0AB11E')


class TestFetchData(TestCase):
    @patch('requests.get')
    def test_fetch_data_success(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {'some': 'data', "num_of_records": 1}
        data = pm.fetch_data('valid_device_id')
        self.assertEqual(data, {'some': 'data', "num_of_records": 1})

    @patch('requests.get')
    def test_fetch_data_network_error(self, mock_get):
        mock_get.side_effect = requests.exceptions.ConnectionError
        with self.assertRaises(requests.exceptions.ConnectionError):
            pm.fetch_data('valid_device_id')


class TestParseData(TestCase):
    def test_parse_data_success(self):
        sample_data = {
            "device_id": "08BEAC0AB11E",
            "source": "history by IIS-NRL",
            "num_of_records": 1,
            'feeds': [{
                'AirBox': [
                    {
                        '2024-05-23T11:32:17Z': {
                            'timestamp': '2024-05-23T11:32:17Z',
                            's_d0': 12.5
                        }
                    }
                ]
            }],
            "version": "2024-05-30T12:44:13Z"
        }
        parsed_data = pm.parse_data(sample_data)
        self.assertEqual(parsed_data, [('2024-05-23T11:32:17Z', 12.5)])

    def test_parse_data_missing_pm25(self):
        sample_data = {
            "device_id": "08BEAC0AB11E",
            "source": "history by IIS-NRL",
            "num_of_records": 1,
            "feeds": [
                {
                    "AirBox": [
                        {
                            "2024-05-23T12:50:05Z": {
                                "timestamp": "2024-05-23T12:50:05Z"
                            }
                        }
                    ]
                }
            ],
            "version": "2024-05-30T12:44:13Z"
        }
        parsed_data = pm.parse_data(sample_data)
        self.assertEqual(parsed_data, [])


class TestEdgeCases(TestCase):
    def test_empty_api_response(self):
        sample_data = {"device_id": "08BEAC0A08AE", "source": "history by IIS-NRL", "num_of_records": 0, "feeds": [], "version": "2024-05-30T14:31:24Z"}
        parsed_data = pm.parse_data(sample_data)
        self.assertEqual(parsed_data, [])

    def test_unexpected_data_format(self):
        sample_data = {'unexpected': 'format'}
        parsed_data = pm.parse_data(sample_data)
        self.assertEqual(parsed_data, [])
