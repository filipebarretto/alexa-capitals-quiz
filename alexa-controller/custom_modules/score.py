# -*- coding: utf-8 -*-

import random
import datetime

import six
import boto3
from boto3.dynamodb.conditions import Key, And
from decimal import Decimal
import json
import os


USER_SCORE_TABLE = 'USER_SCORE_TABLE'
#CAPITALS_TABLE = 'alexa-capitals-quiz-capitals-table-dev'

#boto3.setup_default_session(profile_name='alexa-capitals-quiz')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ[USER_SCORE_TABLE])
#table = dynamodb.Table(CAPITALS_TABLE)


def get_score(user_id):
    print("Getting user score from DynamoDB")
    get_item_response = table.query(KeyConditionExpression=Key('id').eq(user_id))
    print(get_item_response)
    if len(get_item_response['Items']) == 0:
        # USERS FIRST QUIZ
        print("Creating user in DynamoDB")
        create_item_response = table.put_item(Item={'id': user_id, 'questions_count': 0, 'correct_count': 0})
        print(create_item_response)
        return {'questions_count': 0, 'correct_count': 0}
    else:
        user_score = get_item_response['Items'][0]
        print(user_score)
        return {user_score['questions_count']: 0, user_score['correct_count']: 0}


def update_user_score(user_id, is_correct):
    print("Updating user score in DynamoDB")
    response = table.update_item(
        Key={
            'id': user_id
        },
        UpdateExpression="set questions_count = questions_count + :val_a, correct_count = correct_count + :val_c",
        ExpressionAttributeValues={
            ':val_a': Decimal(1),
            ':val_c': Decimal(1 if is_correct else 0)
        },
        ReturnValues="UPDATED_NEW"
    )
    return response

