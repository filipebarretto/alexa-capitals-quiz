import boto3
import json

FILE_NAME = '../country-capitals.json'

boto3.setup_default_session(profile_name='alexa-capitals-quiz')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('alexa-capitals-quiz-capitals-table-dev')

def open_json_file(filename):
	with open(filename, 'r') as myfile:
		countries_obj = json.loads(myfile.read())
	return countries_obj


def put_item_in_dynamodb(item):
	response = table.put_item(
       Item={
            'country': item['CountryName'],
            'capital': item['CapitalName'],
			'latitude': item['CapitalLatitude'],
			'longitude': item['CapitalLongitude'],
			'country_code': item['CountryCode'],
			'continent': item['ContinentName']
        }
    )
	return response

if __name__ == '__main__':
	print('Adding countries to DynamoDB')
	print('Opening JSON file')
	countries_obj = open_json_file(FILE_NAME)

	l = []
	print('Putting countries to DynamoDB')
	for country in countries_obj:
		#r = put_item_in_dynamodb(country)
		#print(r)
		#l.append(country['CountryName'])
		l.append({"answer": country['CapitalName'], "country": country['CountryName']})
	print(l)
