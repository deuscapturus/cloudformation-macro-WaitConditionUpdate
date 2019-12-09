import unittest
import json
from main import *

class MainTest(unittest.TestCase):

    def test_recursiveFindReplaceText(self):
        obj = {"key":[{"key":["this"]},"this",{"key":[{"key":"this"}]}]}
        output = recursiveFindReplaceText(obj, "this", "that")
        self.assertEqual(output,{"key":[{"key":["that"]},"that",{"key":[{"key":"that"}]}]})

    def test_replaceWaitConditionLogicalIds(self):
        template = {
            "Resources": {
                "ServiceWaitHandle": {
                    "Type": "AWS::CloudFormation::WaitConditionHandle"
                },
                "ServiceWaitCondition": {
                    "Type": "AWS::CloudFormation::WaitCondition"
                }
            }
        }
        newTemplate, changes = replaceWaitConditionLogicalIds(template, "HOHOH")
        self.assertEqual(changes,[("ServiceWaitHandle","ServiceWaitHandleHOHOH"),("ServiceWaitCondition","ServiceWaitConditionHOHOH")])
        self.assertEqual(newTemplate, {"Resources": {"ServiceWaitHandleHOHOH": {"Type": "AWS::CloudFormation::WaitConditionHandle"}, "ServiceWaitConditionHOHOH": {"Type": "AWS::CloudFormation::WaitCondition"}}})

    def test_handler(self):
        with open('./event.json') as eventJson:
            event = json.load(eventJson)
            output = handler(event, {})
            self.assertIn("ServiceWaitHandle85C7F", output['fragment']['Resources'])
