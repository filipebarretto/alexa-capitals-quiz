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
			'continent': item['ContinentName'],
			'difficulty': item['difficulty'],
			'asked_count': 0,
			'correct_count': 0
        }
    )
	return response

if __name__ == '__main__':
	print('Adding countries to DynamoDB')
	print('Opening JSON file')
	countries_obj = open_json_file(FILE_NAME)
	
	countries_list = []
	capitals_list = []
	obj_list = []
	print('Putting countries to DynamoDB')
	for country in countries_obj:
		r = put_item_in_dynamodb(country)
		print(r)
		countries_list.append({"id": country['CountryName'], "name": {"value": country['CountryName']}})
		capitals_list.append({"id": country['CapitalName'], "name": {"value": country['CapitalName']}})
		obj_list.append({"answer": country['CapitalName'], "country": country['CountryName']})
	
	print("\n\n")
	print(json.dumps(countries_list))
	print("\n\n")
	print(json.dumps(capitals_list))
