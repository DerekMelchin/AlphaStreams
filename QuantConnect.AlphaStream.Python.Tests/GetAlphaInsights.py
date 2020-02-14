import unittest
import sys
from itertools import groupby
from datetime import datetime, timedelta

from test_config import *

sys.path.append('../')

from AlphaStream import AlphaStreamClient


class Insights(unittest.TestCase):
    def setUp(self):
        config = test_config()
        self.client = AlphaStreamClient(config['testing_client_institution_id'], config['testing_client_token'])

    def test_get_insights(self):

        alphaId = "d0fc88b1e6354fe95eb83225a"
        start = 0
        insights = []
        # Fetch all Insights in the Alpha's backtest
        while start < 500:
            insights += self.client.GetAlphaInsights(alphaId, start)
            start += 100

        self.assertEqual(len(insights), 500)

        # check that Insights are in chronological order
        for i in range(len(insights) - 1):
            for j in insights[i+1:]:
                self.assertLessEqual(insights[i].CreatedTime, j.CreatedTime)

        response_ids = [x.Id for x in insights]

        expected_in_sample_ids = read_test_data("InsightTestData.txt")
        # check that response not in-sample IDs == expected not in-sample IDs
        self.assertEqual(len(response_ids), len(expected_in_sample_ids))
        self.assertListEqual(response_ids, expected_in_sample_ids)