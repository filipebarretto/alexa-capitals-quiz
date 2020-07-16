import sys
import pytest

sys.path.insert(1, '../alexa-controller/')
from custom_modules import util, data, questions

supported_languages = ["en-US", "pt-BR"]

countries_list = ['Somaliland', 'South Georgia and South Sandwich Islands', 'French Southern and Antarctic Lands', 'Palestine', 'Aland Islands', 'Nauru', 'Saint Martin', 'Tokelau', 'Western Sahara', 'Afghanistan', 'Albania', 'Algeria', 'American Samoa', 'Andorra', 'Angola', 'Anguilla', 'Antigua and Barbuda', 'Argentina', 'Armenia', 'Aruba', 'Australia', 'Austria', 'Azerbaijan', 'Bahamas', 'Bahrain', 'Bangladesh', 'Barbados', 'Belarus', 'Belgium', 'Belize', 'Benin', 'Bermuda', 'Bhutan', 'Bolivia', 'Bosnia and Herzegovina', 'Botswana', 'Brazil', 'British Virgin Islands', 'Brunei Darussalam', 'Bulgaria', 'Burkina Faso', 'Myanmar', 'Burundi', 'Cambodia', 'Cameroon', 'Canada', 'Cape Verde', 'Cayman Islands', 'Central African Republic', 'Chad', 'Chile', 'China', 'Christmas Island', 'Cocos Islands', 'Colombia', 'Comoros', 'Democratic Republic of the Congo', 'Republic of Congo', 'Cook Islands', 'Costa Rica', "Cote d'Ivoire", 'Croatia', 'Cuba', 'CuraÃ§ao', 'Cyprus', 'Czech Republic', 'Denmark', 'Djibouti', 'Dominica', 'Dominican Republic', 'Ecuador', 'Egypt', 'El Salvador', 'Equatorial Guinea', 'Eritrea', 'Estonia', 'Ethiopia', 'Falkland Islands', 'Faroe Islands', 'Fiji', 'Finland', 'France', 'French Polynesia', 'Gabon', 'The Gambia', 'Georgia', 'Germany', 'Ghana', 'Gibraltar', 'Greece', 'Greenland', 'Grenada', 'Guam', 'Guatemala', 'Guernsey', 'Guinea', 'Guinea-Bissau', 'Guyana', 'Haiti', 'Vatican City', 'Honduras', 'Hungary', 'Iceland', 'India', 'Indonesia', 'Iran', 'Iraq', 'Ireland', 'Isle of Man', 'Israel', 'Italy', 'Jamaica', 'Japan', 'Jersey', 'Jordan', 'Kazakhstan', 'Kenya', 'Kiribati', 'North Korea', 'South Korea', 'Kosovo', 'Kuwait', 'Kyrgyzstan', 'Laos', 'Latvia', 'Lebanon', 'Lesotho', 'Liberia', 'Libya', 'Liechtenstein', 'Lithuania', 'Luxembourg', 'Macedonia', 'Madagascar', 'Malawi', 'Malaysia', 'Maldives', 'Mali', 'Malta', 'Marshall Islands', 'Mauritania', 'Mauritius', 'Mexico', 'Federated States of Micronesia', 'Moldova', 'Monaco', 'Mongolia', 'Montenegro', 'Montserrat', 'Morocco', 'Mozambique', 'Namibia', 'Nepal', 'Netherlands', 'New Caledonia', 'New Zealand', 'Nicaragua', 'Niger', 'Nigeria', 'Niue', 'Norfolk Island', 'Northern Mariana Islands', 'Norway', 'Oman', 'Pakistan', 'Palau', 'Panama', 'Papua New Guinea', 'Paraguay', 'Peru', 'Philippines', 'Pitcairn Islands', 'Poland', 'Portugal', 'Puerto Rico', 'Qatar', 'Romania', 'Russia', 'Rwanda', 'Saint Barthelemy', 'Saint Helena', 'Saint Kitts and Nevis', 'Saint Lucia', 'Saint Pierre and Miquelon', 'Saint Vincent and the Grenadines', 'Samoa', 'San Marino', 'Sao Tome and Principe', 'Saudi Arabia', 'Senegal', 'Serbia', 'Seychelles', 'Sierra Leone', 'Singapore', 'Sint Maarten', 'Slovakia', 'Slovenia', 'Solomon Islands', 'Somalia', 'South Africa', 'South Sudan', 'Spain', 'Sri Lanka', 'Sudan', 'Suriname', 'Svalbard', 'Swaziland', 'Sweden', 'Switzerland', 'Syria', 'Taiwan', 'Tajikistan', 'Tanzania', 'Thailand', 'Timor-Leste', 'Togo', 'Tonga', 'Trinidad and Tobago', 'Tunisia', 'Turkey', 'Turkmenistan', 'Turks and Caicos Islands', 'Tuvalu', 'Uganda', 'Ukraine', 'United Arab Emirates', 'United Kingdom', 'United States', 'Uruguay', 'Uzbekistan', 'Vanuatu', 'Venezuela', 'Vietnam', 'US Virgin Islands', 'Wallis and Futuna', 'Yemen', 'Zambia', 'Zimbabwe', 'US Minor Outlying Islands', 'Antarctica', 'Northern Cyprus', 'Hong Kong', 'Heard Island and McDonald Islands', 'British Indian Ocean Territory', 'Macau']

questions_list = [{'answer': 'Hargeisa', 'country': 'Somaliland'}, {'answer': 'King Edward Point', 'country': 'South Georgia and South Sandwich Islands'}, {'answer': 'Port-aux-FranÃ§ais', 'country': 'French Southern and Antarctic Lands'}, {'answer': 'Jerusalem', 'country': 'Palestine'}, {'answer': 'Mariehamn', 'country': 'Aland Islands'}, {'answer': 'Yaren', 'country': 'Nauru'}, {'answer': 'Marigot', 'country': 'Saint Martin'}, {'answer': 'Atafu', 'country': 'Tokelau'}, {'answer': 'El-AaiÃºn', 'country': 'Western Sahara'}, {'answer': 'Kabul', 'country': 'Afghanistan'}, {'answer': 'Tirana', 'country': 'Albania'}, {'answer': 'Algiers', 'country': 'Algeria'}, {'answer': 'Pago Pago', 'country': 'American Samoa'}, {'answer': 'Andorra la Vella', 'country': 'Andorra'}, {'answer': 'Luanda', 'country': 'Angola'}, {'answer': 'The Valley', 'country': 'Anguilla'}, {'answer': "Saint John's", 'country': 'Antigua and Barbuda'}, {'answer': 'Buenos Aires', 'country': 'Argentina'}, {'answer': 'Yerevan', 'country': 'Armenia'}, {'answer': 'Oranjestad', 'country': 'Aruba'}, {'answer': 'Canberra', 'country': 'Australia'}, {'answer': 'Vienna', 'country': 'Austria'}, {'answer': 'Baku', 'country': 'Azerbaijan'}, {'answer': 'Nassau', 'country': 'Bahamas'}, {'answer': 'Manama', 'country': 'Bahrain'}, {'answer': 'Dhaka', 'country': 'Bangladesh'}, {'answer': 'Bridgetown', 'country': 'Barbados'}, {'answer': 'Minsk', 'country': 'Belarus'}, {'answer': 'Brussels', 'country': 'Belgium'}, {'answer': 'Belmopan', 'country': 'Belize'}, {'answer': 'Porto-Novo', 'country': 'Benin'}, {'answer': 'Hamilton', 'country': 'Bermuda'}, {'answer': 'Thimphu', 'country': 'Bhutan'}, {'answer': 'La Paz', 'country': 'Bolivia'}, {'answer': 'Sarajevo', 'country': 'Bosnia and Herzegovina'}, {'answer': 'Gaborone', 'country': 'Botswana'}, {'answer': 'Brasilia', 'country': 'Brazil'}, {'answer': 'Road Town', 'country': 'British Virgin Islands'}, {'answer': 'Bandar Seri Begawan', 'country': 'Brunei Darussalam'}, {'answer': 'Sofia', 'country': 'Bulgaria'}, {'answer': 'Ouagadougou', 'country': 'Burkina Faso'}, {'answer': 'Rangoon', 'country': 'Myanmar'}, {'answer': 'Bujumbura', 'country': 'Burundi'}, {'answer': 'Phnom Penh', 'country': 'Cambodia'}, {'answer': 'Yaounde', 'country': 'Cameroon'}, {'answer': 'Ottawa', 'country': 'Canada'}, {'answer': 'Praia', 'country': 'Cape Verde'}, {'answer': 'George Town', 'country': 'Cayman Islands'}, {'answer': 'Bangui', 'country': 'Central African Republic'}, {'answer': "N'Djamena", 'country': 'Chad'}, {'answer': 'Santiago', 'country': 'Chile'}, {'answer': 'Beijing', 'country': 'China'}, {'answer': 'The Settlement', 'country': 'Christmas Island'}, {'answer': 'West Island', 'country': 'Cocos Islands'}, {'answer': 'Bogota', 'country': 'Colombia'}, {'answer': 'Moroni', 'country': 'Comoros'}, {'answer': 'Kinshasa', 'country': 'Democratic Republic of the Congo'}, {'answer': 'Brazzaville', 'country': 'Republic of Congo'}, {'answer': 'Avarua', 'country': 'Cook Islands'}, {'answer': 'San Jose', 'country': 'Costa Rica'}, {'answer': 'Yamoussoukro', 'country': "Cote d'Ivoire"}, {'answer': 'Zagreb', 'country': 'Croatia'}, {'answer': 'Havana', 'country': 'Cuba'}, {'answer': 'Willemstad', 'country': 'CuraÃ§ao'}, {'answer': 'Nicosia', 'country': 'Cyprus'}, {'answer': 'Prague', 'country': 'Czech Republic'}, {'answer': 'Copenhagen', 'country': 'Denmark'}, {'answer': 'Djibouti', 'country': 'Djibouti'}, {'answer': 'Roseau', 'country': 'Dominica'}, {'answer': 'Santo Domingo', 'country': 'Dominican Republic'}, {'answer': 'Quito', 'country': 'Ecuador'}, {'answer': 'Cairo', 'country': 'Egypt'}, {'answer': 'San Salvador', 'country': 'El Salvador'}, {'answer': 'Malabo', 'country': 'Equatorial Guinea'}, {'answer': 'Asmara', 'country': 'Eritrea'}, {'answer': 'Tallinn', 'country': 'Estonia'}, {'answer': 'Addis Ababa', 'country': 'Ethiopia'}, {'answer': 'Stanley', 'country': 'Falkland Islands'}, {'answer': 'Torshavn', 'country': 'Faroe Islands'}, {'answer': 'Suva', 'country': 'Fiji'}, {'answer': 'Helsinki', 'country': 'Finland'}, {'answer': 'Paris', 'country': 'France'}, {'answer': 'Papeete', 'country': 'French Polynesia'}, {'answer': 'Libreville', 'country': 'Gabon'}, {'answer': 'Banjul', 'country': 'The Gambia'}, {'answer': 'Tbilisi', 'country': 'Georgia'}, {'answer': 'Berlin', 'country': 'Germany'}, {'answer': 'Accra', 'country': 'Ghana'}, {'answer': 'Gibraltar', 'country': 'Gibraltar'}, {'answer': 'Athens', 'country': 'Greece'}, {'answer': 'Nuuk', 'country': 'Greenland'}, {'answer': "Saint George's", 'country': 'Grenada'}, {'answer': 'Hagatna', 'country': 'Guam'}, {'answer': 'Guatemala City', 'country': 'Guatemala'}, {'answer': 'Saint Peter Port', 'country': 'Guernsey'}, {'answer': 'Conakry', 'country': 'Guinea'}, {'answer': 'Bissau', 'country': 'Guinea-Bissau'}, {'answer': 'Georgetown', 'country': 'Guyana'}, {'answer': 'Port-au-Prince', 'country': 'Haiti'}, {'answer': 'Vatican City', 'country': 'Vatican City'}, {'answer': 'Tegucigalpa', 'country': 'Honduras'}, {'answer': 'Budapest', 'country': 'Hungary'}, {'answer': 'Reykjavik', 'country': 'Iceland'}, {'answer': 'New Delhi', 'country': 'India'}, {'answer': 'Jakarta', 'country': 'Indonesia'}, {'answer': 'Tehran', 'country': 'Iran'}, {'answer': 'Baghdad', 'country': 'Iraq'}, {'answer': 'Dublin', 'country': 'Ireland'}, {'answer': 'Douglas', 'country': 'Isle of Man'}, {'answer': 'Jerusalem', 'country': 'Israel'}, {'answer': 'Rome', 'country': 'Italy'}, {'answer': 'Kingston', 'country': 'Jamaica'}, {'answer': 'Tokyo', 'country': 'Japan'}, {'answer': 'Saint Helier', 'country': 'Jersey'}, {'answer': 'Amman', 'country': 'Jordan'}, {'answer': 'Astana', 'country': 'Kazakhstan'}, {'answer': 'Nairobi', 'country': 'Kenya'}, {'answer': 'Tarawa', 'country': 'Kiribati'}, {'answer': 'Pyongyang', 'country': 'North Korea'}, {'answer': 'Seoul', 'country': 'South Korea'}, {'answer': 'Pristina', 'country': 'Kosovo'}, {'answer': 'Kuwait City', 'country': 'Kuwait'}, {'answer': 'Bishkek', 'country': 'Kyrgyzstan'}, {'answer': 'Vientiane', 'country': 'Laos'}, {'answer': 'Riga', 'country': 'Latvia'}, {'answer': 'Beirut', 'country': 'Lebanon'}, {'answer': 'Maseru', 'country': 'Lesotho'}, {'answer': 'Monrovia', 'country': 'Liberia'}, {'answer': 'Tripoli', 'country': 'Libya'}, {'answer': 'Vaduz', 'country': 'Liechtenstein'}, {'answer': 'Vilnius', 'country': 'Lithuania'}, {'answer': 'Luxembourg', 'country': 'Luxembourg'}, {'answer': 'Skopje', 'country': 'Macedonia'}, {'answer': 'Antananarivo', 'country': 'Madagascar'}, {'answer': 'Lilongwe', 'country': 'Malawi'}, {'answer': 'Kuala Lumpur', 'country': 'Malaysia'}, {'answer': 'Male', 'country': 'Maldives'}, {'answer': 'Bamako', 'country': 'Mali'}, {'answer': 'Valletta', 'country': 'Malta'}, {'answer': 'Majuro', 'country': 'Marshall Islands'}, {'answer': 'Nouakchott', 'country': 'Mauritania'}, {'answer': 'Port Louis', 'country': 'Mauritius'}, {'answer': 'Mexico City', 'country': 'Mexico'}, {'answer': 'Palikir', 'country': 'Federated States of Micronesia'}, {'answer': 'Chisinau', 'country': 'Moldova'}, {'answer': 'Monaco', 'country': 'Monaco'}, {'answer': 'Ulaanbaatar', 'country': 'Mongolia'}, {'answer': 'Podgorica', 'country': 'Montenegro'}, {'answer': 'Plymouth', 'country': 'Montserrat'}, {'answer': 'Rabat', 'country': 'Morocco'}, {'answer': 'Maputo', 'country': 'Mozambique'}, {'answer': 'Windhoek', 'country': 'Namibia'}, {'answer': 'Kathmandu', 'country': 'Nepal'}, {'answer': 'Amsterdam', 'country': 'Netherlands'}, {'answer': 'Noumea', 'country': 'New Caledonia'}, {'answer': 'Wellington', 'country': 'New Zealand'}, {'answer': 'Managua', 'country': 'Nicaragua'}, {'answer': 'Niamey', 'country': 'Niger'}, {'answer': 'Abuja', 'country': 'Nigeria'}, {'answer': 'Alofi', 'country': 'Niue'}, {'answer': 'Kingston', 'country': 'Norfolk Island'}, {'answer': 'Saipan', 'country': 'Northern Mariana Islands'}, {'answer': 'Oslo', 'country': 'Norway'}, {'answer': 'Muscat', 'country': 'Oman'}, {'answer': 'Islamabad', 'country': 'Pakistan'}, {'answer': 'Melekeok', 'country': 'Palau'}, {'answer': 'Panama City', 'country': 'Panama'}, {'answer': 'Port Moresby', 'country': 'Papua New Guinea'}, {'answer': 'Asuncion', 'country': 'Paraguay'}, {'answer': 'Lima', 'country': 'Peru'}, {'answer': 'Manila', 'country': 'Philippines'}, {'answer': 'Adamstown', 'country': 'Pitcairn Islands'}, {'answer': 'Warsaw', 'country': 'Poland'}, {'answer': 'Lisbon', 'country': 'Portugal'}, {'answer': 'San Juan', 'country': 'Puerto Rico'}, {'answer': 'Doha', 'country': 'Qatar'}, {'answer': 'Bucharest', 'country': 'Romania'}, {'answer': 'Moscow', 'country': 'Russia'}, {'answer': 'Kigali', 'country': 'Rwanda'}, {'answer': 'Gustavia', 'country': 'Saint Barthelemy'}, {'answer': 'Jamestown', 'country': 'Saint Helena'}, {'answer': 'Basseterre', 'country': 'Saint Kitts and Nevis'}, {'answer': 'Castries', 'country': 'Saint Lucia'}, {'answer': 'Saint-Pierre', 'country': 'Saint Pierre and Miquelon'}, {'answer': 'Kingstown', 'country': 'Saint Vincent and the Grenadines'}, {'answer': 'Apia', 'country': 'Samoa'}, {'answer': 'San Marino', 'country': 'San Marino'}, {'answer': 'Sao Tome', 'country': 'Sao Tome and Principe'}, {'answer': 'Riyadh', 'country': 'Saudi Arabia'}, {'answer': 'Dakar', 'country': 'Senegal'}, {'answer': 'Belgrade', 'country': 'Serbia'}, {'answer': 'Victoria', 'country': 'Seychelles'}, {'answer': 'Freetown', 'country': 'Sierra Leone'}, {'answer': 'Singapore', 'country': 'Singapore'}, {'answer': 'Philipsburg', 'country': 'Sint Maarten'}, {'answer': 'Bratislava', 'country': 'Slovakia'}, {'answer': 'Ljubljana', 'country': 'Slovenia'}, {'answer': 'Honiara', 'country': 'Solomon Islands'}, {'answer': 'Mogadishu', 'country': 'Somalia'}, {'answer': 'Pretoria', 'country': 'South Africa'}, {'answer': 'Juba', 'country': 'South Sudan'}, {'answer': 'Madrid', 'country': 'Spain'}, {'answer': 'Colombo', 'country': 'Sri Lanka'}, {'answer': 'Khartoum', 'country': 'Sudan'}, {'answer': 'Paramaribo', 'country': 'Suriname'}, {'answer': 'Longyearbyen', 'country': 'Svalbard'}, {'answer': 'Mbabane', 'country': 'Swaziland'}, {'answer': 'Stockholm', 'country': 'Sweden'}, {'answer': 'Bern', 'country': 'Switzerland'}, {'answer': 'Damascus', 'country': 'Syria'}, {'answer': 'Taipei', 'country': 'Taiwan'}, {'answer': 'Dushanbe', 'country': 'Tajikistan'}, {'answer': 'Dar es Salaam', 'country': 'Tanzania'}, {'answer': 'Bangkok', 'country': 'Thailand'}, {'answer': 'Dili', 'country': 'Timor-Leste'}, {'answer': 'Lome', 'country': 'Togo'}, {'answer': "Nuku'alofa", 'country': 'Tonga'}, {'answer': 'Port of Spain', 'country': 'Trinidad and Tobago'}, {'answer': 'Tunis', 'country': 'Tunisia'}, {'answer': 'Ankara', 'country': 'Turkey'}, {'answer': 'Ashgabat', 'country': 'Turkmenistan'}, {'answer': 'Grand Turk', 'country': 'Turks and Caicos Islands'}, {'answer': 'Funafuti', 'country': 'Tuvalu'}, {'answer': 'Kampala', 'country': 'Uganda'}, {'answer': 'Kyiv', 'country': 'Ukraine'}, {'answer': 'Abu Dhabi', 'country': 'United Arab Emirates'}, {'answer': 'London', 'country': 'United Kingdom'}, {'answer': 'Washington', 'country': 'United States'}, {'answer': 'Montevideo', 'country': 'Uruguay'}, {'answer': 'Tashkent', 'country': 'Uzbekistan'}, {'answer': 'Port-Vila', 'country': 'Vanuatu'}, {'answer': 'Caracas', 'country': 'Venezuela'}, {'answer': 'Hanoi', 'country': 'Vietnam'}, {'answer': 'Charlotte Amalie', 'country': 'US Virgin Islands'}, {'answer': 'Mata-Utu', 'country': 'Wallis and Futuna'}, {'answer': 'Sanaa', 'country': 'Yemen'}, {'answer': 'Lusaka', 'country': 'Zambia'}, {'answer': 'Harare', 'country': 'Zimbabwe'}, {'answer': 'Washington', 'country': 'US Minor Outlying Islands'}, {'answer': 'N/A', 'country': 'Antarctica'}, {'answer': 'North Nicosia', 'country': 'Northern Cyprus'}, {'answer': 'N/A', 'country': 'Hong Kong'}, {'answer': 'N/A', 'country': 'Heard Island and McDonald Islands'}, {'answer': 'Diego Garcia', 'country': 'British Indian Ocean Territory'}, {'answer': 'N/A', 'country': 'Macau'}]



def test_get_random_country():
    assert questions.get_random_country()['country'] in countries_list

def test_get_question():
    assert questions.get_question() in questions_list
            
