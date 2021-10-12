import unittest
from GetSamplingTargetsRequest import GetSamplingTargetsRequest, SamplingStatisticsDocument
from GetSamplingTargetsResponse import GetSamplingTargetsResponse, SamplingTargetDocument, UnprocessedStatistics


class TestGetSamplingTargetsResponse(unittest.TestCase):
    def setUp(self):
        self.target_doc = SamplingTargetDocument.create(
            12.5, 3, 17, 86, "rule name test")
        self.unprocessed_stat = UnprocessedStatistics.create(
            "test error code", "test message", "test rule name")
        self.targets_response = GetSamplingTargetsResponse.create(
            5, [self.target_doc], [self.unprocessed_stat])

    def test_last_rule_modification(self):
        self.assertEqual(self.targets_response.get_last_rule_modification(), 5)

    def test_target_doc_info(self):
        self.assertEqual(self.targets_response.get_sampling_target_documents()[
                         0].get_fixed_rate(), 12.5)
        self.assertEqual(self.targets_response.get_sampling_target_documents()[
                         0].get_interval(), 3)
        self.assertEqual(self.targets_response.get_sampling_target_documents()[
                         0].get_reservoir_quota(), 17)
        self.assertEqual(self.targets_response.get_sampling_target_documents()[
                         0].get_reservoir_quota_TTL(), 86)
        self.assertEqual(self.targets_response.get_sampling_target_documents()[
                         0].get_rule_name(), "rule name test")

    def test_unprocessed_statistics_info(self):
        self.assertEqual(self.targets_response.get_unprocessed_statistics()[
                         0].get_error_code(), "test error code")
        self.assertEqual(self.targets_response.get_unprocessed_statistics()[
                         0].get_message(), "test message")
        self.assertEqual(self.targets_response.get_unprocessed_statistics()[
                         0].get_rule_name(), "test rule name")


class TestGetSamplingTargetsRequest(unittest.TestCase):
    def setUp(self):
        self.statistic_document = SamplingStatisticsDocument.create(
            5, "test client ID", 6, "test rule name", 700, 850)
        self.targets_request = GetSamplingTargetsRequest.create(
            [self.statistic_document])

    def test_get_statistic_documents_info(self):
        self.assertEqual(self.targets_request.get_statistic_documents()[
                         0].get_borrow_count(), 5)
        self.assertEqual(self.targets_request.get_statistic_documents()[
                         0].get_client_ID(), "test client ID")
        self.assertEqual(self.targets_request.get_statistic_documents()[
                         0].get_request_count(), 6)
        self.assertEqual(self.targets_request.get_statistic_documents()[
                         0].get_rule_name(), "test rule name")
        self.assertEqual(self.targets_request.get_statistic_documents()[
                         0].get_sampled_count(), 700)
        self.assertEqual(self.targets_request.get_statistic_documents()[
                         0].get_timestamp(), 850)


if __name__ == "__main__":
    unittest.main()
