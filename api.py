import json
import requests
from mimesis import Person
from mimesis.random import random

person = Person('ru')


def token(url):
    params = {'grant_type': 'client_credentials'}
    headers = {'Content-Type': 'application/x-www-form-urlencoded',
               'Authorization': 'Basic'}
    token_stand = list(requests.post(url, headers=headers, params=params).json().values())
    header = {'Authorization': 'Bearer ' + token_stand[0],
              'Content-Type': 'application/json'}
    # print(header)
    return header


def api_stand(api, stand):
    if api == 'H':
        print("hy-api")
        url = f""" http://hy-api-front.{stand['url']}.k8s"""
        headers = token(stand['url_token'])
        data = {"birthdate": "1999-12-12",
                "email": person.email(),
                "firstName": person.first_name(),
                "gender": "f",
                "lastName": person.last_name(),
                "middleName": person.name(),
                "notificationConsent": True,
                "personalDataConsent": True,
                "parentNumber": 700952215,
                "phone": person.telephone(),
                "researchConsent": True,
                "townIsoCode": "1000043508170",
                "passportLang": None
                }
        try:
            response = requests.post(url, headers=headers, data=json.dumps(data)).json()
            return response["customer"]["customerID"]
        except:
            print("error hy-api")

    if api == 'O':
        print("ora-api")
        url = f"""http://ora-api-front.{stand['url']}.k8s"""
        headers = token(stand['url_token'])
        data = {
            "birthdate": "2001-12-03T10:15",
            "email": person.email(),
            "firstName": person.first_name(),
            "gender": "f",
            "lastName": person.last_name(),
            "needCreateNotification": True,
            "parentNumber": 700952215,
            "phone": person.telephone(),
            "townIsoCode": "1000043508170"
        }
        try:
            response = requests.post(url, headers=headers, data=json.dumps(data)).json()
            return response["userName"]
        except:
            print('error ora-api')

    if api == 'C':
        print("customer-service")
        url = f"""http://customer-service-front.{stand['url']}.k8s"""
        headers = token(stand['url_token'])
        data = {
            "birthdate": "2000-09-09",
            "email": person.email(),
            "firstName": person.first_name(),
            "gender": "m",
            "lastName": person.last_name(),
            "middleName": person.name(),
            "needCreateNotification": True,
            "parentNumber": 700952215,
            "phone": person.telephone(),
            "researchConSent": 1,
            "sendEmailState": 1,
            "sendSmsState": 1,
            "townIsoCode": "1000043508170",
            "utm": [
                {
                    "key": "SYS_WHERE_CAME_FROM",
                    "value": "mobile-self"
                },
                {
                    "key": "utm_medium",
                    "value": "app2"
                },
                {
                    "key": "utm_source",
                    "value": "Organic"
                }
            ]
        }
        try:
            response = requests.post(url, headers=headers, data=json.dumps(data)).json()
            return response["userName"]
        except:
            print('error')


def api_sms(key, userName, stand):
    url = f"""http://ora-api-front.{stand['url']}.k8s"""
    headers = token(stand['url_token'])
    data = {"key": key,
            "userName": userName}
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        if response.status_code == 200:
            print(key)
            print(stand['url'])
        else:
            print(response.json())
    except:
        print('error response')


def api_customer(setusa, login, stand):
    url = f"""http://hy-api-front.{stand['url']}.k8s{setusa}"""
    headers = token(stand['url_token'])

    data = {"customerID": login,
            "ipAddress": "127.0.0.1"}
    if setusa == 'setusaconsultant':
        data |= {
            "socialSecurityNumber": str(random.randrange(100, 999)) + '-' + str(random.randrange(10, 99)) + '-' + str(
                random.randrange(1000, 9999)),
            "paymentSuccessUrl": "http://test.ru",
            "paymentFailedUrl": "http://test2.ru"}

    try:
        response = requests.post(url, headers=headers, data=json.dumps(data)).json()
        response = response['redirectPaymentURL']
        print(type(response))
    except:
        print("error")
    return response


def main():
    # api_sms('2859', '726463644')
    # print(token('stg'))
    print("22")


if __name__ == "__main__":
    main()
