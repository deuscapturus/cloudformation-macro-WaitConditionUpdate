#!/usr/bin/python3
import json
import hashlib

def recursiveFindReplaceText(obj, text, replace):

    if type(obj) == dict:
        for key, item in obj.items():
            if type(item) == str:
                obj[key] = item.replace(text, replace)
            elif type(item) == list or type(item) == dict:
                recursiveFindReplaceText(item, text, replace)
    elif type(obj) == list:
        for index, item in enumerate(obj):
            if type(item) == str:
                obj[index] = item.replace(text, replace)
            elif type(item) == list or type(item) == dict:
                recursiveFindReplaceText(item, text, replace)
    return obj

def replaceWaitConditionLogicalIds(template, paramHash):

    changes = []
    for logicalId, resource in template['Resources'].items():
        if resource['Type'] in ["AWS::CloudFormation::WaitConditionHandle", "AWS::CloudFormation::WaitCondition"] and not logicalId.endswith(paramHash):
            newId = logicalId+paramHash
            template['Resources'][newId] = template['Resources'].pop(logicalId)
            changes.append((logicalId, newId))

    return template, changes

def handler(event, context):

    template = event["fragment"]

    # Generate hash from a concatenation of the parameters sorted
    updateParameters = event['templateParameterValues']['WaitConditionUpdateParameters']
    updateParameters.sort()

    updateParameterValues = []
    for updateParameter in updateParameters:
        updateParameterValues.append(str(event['templateParameterValues'][updateParameter]))

    paramHash = str(hashlib.md5("".join(updateParameterValues).encode('utf-8')).hexdigest())[:5].upper()

    # Replace the keys in Resources with the one generated
    template, changes = replaceWaitConditionLogicalIds(template, paramHash)

    #Search through template for resources of type
    for change in changes:
        template = recursiveFindReplaceText(template, change[0], change[1])

    return {
        "requestId": event['requestId'],
        "status": "success",
        "fragment": template
    }
