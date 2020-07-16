# -*- coding: utf-8 -*-

import random
import datetime

import six
import boto3
import json
import os


CAPITALS_TABLE = 'CAPITALS_TABLE'
#CAPITALS_TABLE = 'alexa-capitals-quiz-capitals-table-dev'

#boto3.setup_default_session(profile_name='alexa-capitals-quiz')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ[CAPITALS_TABLE])
#table = dynamodb.Table(CAPITALS_TABLE)


def get_random_country():
    print('Getting random country from DynamoDB')
    response = table.scan()
    #print(response)
    return random.choice(response['Items'])
    

def get_question():
    print('Getting question')
    random_country = get_random_country()
    print(random_country)
    return {"answer": random_country.get('capital'), "country": random_country.get('country')}
