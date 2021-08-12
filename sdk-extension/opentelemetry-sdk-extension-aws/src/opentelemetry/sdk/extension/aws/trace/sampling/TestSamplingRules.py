import unittest 
from GetSamplingRulesRequest import GetSamplingRulesRequest
from GetSamplingRulesResponse import SamplingRule, SamplingRuleRecord, GetSamplingRulesResponse



class TestGetSamplingRulesResponse(unittest.TestCase):
    def setUp(self):
        self.rules_response = GetSamplingRulesResponse.create("next token test", "sampling rules test")
        #self.rules_response = GetSamplingRulesResponse("next token test", "sampling rules test")

    def test_token(self):
        self.assertEqual(self.rules_response.get_next_token(), "next token test")

    def test_sampling_rules(self):
        self.assertEqual(self.rules_response.get_sampling_rules(), "sampling rules test")


class TestSamplingRuleRecord(unittest.TestCase):
    def setUp(self):
        self.rule_record = SamplingRuleRecord.create(10, 11, ["sampling rule 1", "sampling rule 2"])
    
    def test_created_at(self):
        # default values?
        self.assertEqual(self.rule_record.get_created_at(), 10)
    
    def test_modified_at(self):
        self.assertEqual(self.rule_record.get_modified_at(), 11)

    def test_sampling_rule(self):
        self.assertEqual(self.rule_record.get_sampling_rule(), ["sampling rule 1", "sampling rule 2"])

class TestSamplingRule(unittest.TestCase):
    def setUp(self):
        self.sampling_rule = SamplingRule.create({"attr1": "test attr1", "attr2": "test attr2"}, 11.25, "host test", "POST", 100, 14, "resource arn test", 
        "rule arn test", "rule name test", "service name test", "service type test", "url path test", 1)

    def test_attributes(self):
        self.assertEqual(self.sampling_rule.get_attributes(), {"attr1": "test attr1", "attr2": "test attr2"})
    
    def test_CorrectValueReturnedFromAttributeDict(self):
        self.assertEqual(self.sampling_rule.get_attributes()["attr2"], "test attr2")

    def test_fixed_rate(self):
        self.assertEqual(self.sampling_rule.get_fixed_rate(), 11.25)

    def test_host(self):
        self.assertEqual(self.sampling_rule.get_host(), "host test")
    
    def test_httpMethod(self):
        self.assertEqual(self.sampling_rule.get_http_method(), "POST")
    
    def test_priority(self):
        self.assertEqual(self.sampling_rule.get_priority(), 100)

    def test_reservoirSize(self):
        self.assertEqual(self.sampling_rule.get_reservoir_size(), 14)

    def test_resourceArn(self):
        self.assertEqual(self.sampling_rule.get_resource_arn(), "resource arn test")
    
    def test_ruleArn(self):
        self.assertEqual(self.sampling_rule.get_rule_arn(), "rule arn test")

    def test_ruleName(self):
        self.assertEqual(self.sampling_rule.get_rule_name(), "rule name test")

    def test_serviceName(self):
        self.assertEqual(self.sampling_rule.get_service_name(), "service name test")

    def test_serviceType(self):
        self.assertEqual(self.sampling_rule.get_service_type(), "service type test")
    
    def test_urlPath(self):
        self.assertEqual(self.sampling_rule.get_url_path(), "url path test")
    
    def test_version(self):
        self.assertEqual(self.sampling_rule.get_version(), 1)

if __name__ == "__main__":
    unittest.main()