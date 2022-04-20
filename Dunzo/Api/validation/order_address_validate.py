from rest_framework.response import Response
from ZapioApi.api_packages import *


def validate_address_update(data):
    err_message = {}
    err_message["City"] = \
        only_required(data['address']['city'], "City")

    err_message["state"] = \
        only_required(data['address']['state'], "state")
    err_message["latitude"] = \
        only_required(data['address']['latitude'], "latitude")
    err_message["longitude"] = \
        only_required(data['address']['longitude'], "longitude")
    err_message["address"] = \
        only_required(data['address']['address'], "Address")
    err_message["landmark"] = \
        only_required(data['address']['landmark'], "Landmark")
    err_message["pincode"] = \
        validation_master_anything(data['address']["pincode"], "Pincode", contact_re, 6)
    if any(err_message.values()) == True:
        err = {
            "success": False,
            "error": err_message,
            "message": "Please correct listed errors!!"
        }
        return Response(err)
    else:
        return None



def validate_address(order_address):
    data = order_address
    err_message = {}
    if "city" in data.address:
        err_message["City"] = \
        only_required(data.address['city'], "City")
    else:
        err_message["City"] = "City is not provided in address!!"

    if "state" in data.address:
        err_message["state"] = \
            only_required(data.address['state'], "state")
    else:
        err_message["state"] = "State is not provided in address!!"

    # err_message["country"] = \
    #     only_required(data.address['country'], "country")
    if "latitude" in data.address:
        err_message["latitude"] = \
            only_required(data.address['latitude'], "latitude")
    else:
        err_message["latitude"] = "Latitude is required in address!!"
    if "longitude" in data.address:
        err_message["longitude"] = \
        only_required(data.address['longitude'], "longitude")
    else:
        err_message["longitude"] = "Longitude is required in address!!"
    if "address" in data.address:
        err_message["address"] = \
            only_required(data.address['address'], "address")
    else:
        err_message["address"] = "Address is not provided!!"
    if 'landmark' in data.address:
        err_message["landmark"] = \
            only_required(data.address['landmark'], "landmark")
    else:
        pass
    if "pincode" in data.address:
        err_message["pincode"] = \
        only_required(data.address['pincode'], "pincode")
    else:
        err_message["pincode"] = "Pincode is not provided in address!!"
    if any(err_message.values()) == True:
        err = {
            "success": False,
            "error": err_message,
            "message": "Please correct listed errors!!"
        }
        return Response(err)
    else:
        return None


def validate_customer_details(order_customer):
    data = order_customer
    err_message = {}
    if "name" in data.customer:
        err_message["name"] = \
        only_required(data.customer['name'], "Name")
    else:
        err_message["name"] = "Customer name is not provided!!"
    if "mobile_number" in data.customer:
        err_message["mobile_number"] = \
        only_required(data.customer["mobile_number"], "mobile_number")
    else:
        err_message["mobile_number"] = "Customer mobile is not provided!!"
    if any(err_message.values()) == True:
        err = {
            "success": False,
            "error": err_message,
            "message": "Please correct listed errors!!"
        }
        return Response(err)
    else:
        return None

def validate_customer_details_update(data):
    err_message = {}
    err_message["name"] = \
        only_required(data['customer']['name'], "name")
    err_message["mobile_number"] = \
        validation_master_anything(data['customer']["mobile_number"], "Mobile Number", contact_re, 10)
    if any(err_message.values()) == True:
        err = {
            "success": False,
            "error": err_message,
            "message": "Please correct listed errors!!"
        }
        return Response(err)
    else:
        return None
