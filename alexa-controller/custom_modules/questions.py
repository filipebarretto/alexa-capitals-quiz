# -*- coding: utf-8 -*-

import random
import datetime

import six
import boto3
from boto3.dynamodb.conditions import Key, And
from decimal import Decimal
import json
import os


CAPITALS_TABLE = 'CAPITALS_TABLE'
#CAPITALS_TABLE = 'alexa-capitals-quiz-capitals-table-dev'

#boto3.setup_default_session(profile_name='alexa-capitals-quiz')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ[CAPITALS_TABLE])
#table = dynamodb.Table(CAPITALS_TABLE)


def update_question_global_score(country, is_correct):
    print("Updating country score in DynamoDB")
    response = table.update_item(
        Key={
            'country': country
        },
        UpdateExpression="set asked_count = asked_count + :val_a, correct_count = correct_count + :val_c",
        ExpressionAttributeValues={
            ':val_a': Decimal(1),
            ':val_c': Decimal(1 if is_correct else 0)
        },
        ReturnValues="UPDATED_NEW"
    )
    return response

def get_random_country():
    print('Getting random country from DynamoDB')
    scan_filter = {
        'FilterExpression': Key('difficulty').eq("easy")
    }
    response = table.scan(**scan_filter)
    #print(response)
    return random.choice(response['Items'])
    

def get_question():
    print('Getting question')
    random_country = get_random_country()
    print(random_country)
    return {"answer": random_country.get('capital'), "country": random_country.get('country')}
