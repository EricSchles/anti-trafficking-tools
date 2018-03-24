import os
import pickle
from collections import defaultdict
import usaddress
from geopy.geocoders import Nominatim, GoogleV3


def format_post_type(post_type):
    if post_type.lower() == "st.":
        return "Street"
    elif post_type.lower() in ["ct.", 'crt.']:
        return "Court"
    else:
        return post_type


def format_address(addr_components):
    dicter = defaultdict(str)
    for component, label in addr_components:
        dicter[label] += " {}".format(component)
    label_order = [
        "AddressNumber",
        "Street Name",
        "StreetNamePostType",
        "PlaceName",
        "StateName",
        "ZipCode"
    ]
    dicter["StreetNamePostType"] = format_post_type(dicter["StreetNamePostType"])
    result_addr = "".join([dicter[label] for label in label_order])
    return result_addr


# def format_address(addr):
#     addr_components = usaddress.parse(addr)
#     dicter = {}
#     for component in addr_components:
#         if not component[1] in dicter.keys():
#             dicter[component[1]] = component[0]
#         else:
#             dicter[component[1]] += " "+component[0]
#     result_addr = dicter["AddressNumber"] + " " + dicter["StreetName"]
#     result_addr += " " + format_streetname_post_type(dicter["StreetNamePostType"])
#     result_addr += " " + dicter["PlaceName"] + " " + dicter["StateName"] + " "+ dicter["ZipCode"]
#     return result_addr


def address_is_complete(text):
    for component, label in usaddress.parse(text):
        if label == "IntersectionSeparator" or "CornerOf":
            return "cross street"
    return "complete"


# def get_streetnames(text):
#     streetnames = []
#     parsed_text = usaddress.parse(text)
#     for index, elem in enumerate(parsed_text):
#         if elem[1] == "StreetName" and parsed_text[index+1][1]["StreetNamePostType"] :
#             streetnames.append(elem[0] + parsed_text[index+1][0])
#         elif elem[1] not in ["StreetNamePostType", "IntersectionSeparator", "CornerOf"]:
#             streetnames.append(elem[0])
#     return streetnames

def get_streetnames(text):
    add_parsed = usaddress.parse(text)
    streetnames = []
    prev_comp, prev_label = None, None
    for ind, (component, label) in enumerate(add_parsed):
        if label == "StreetNamePostType" and prev_label == "StreetName":
            streetnames.append("{0} {1}".format(prev_comp, component))
        elif label not in ["StreetNamePostType", "IntersectionSeparator", "CornerOf"]:
            streetnames.append(label)
        prev_comp, prev_label = component, label
    return streetnames


def get_lat_long(text, city):
    location = None
    text = clean_location_string(text)
    try:
        formatted_text = format_address(text)
        nominatim_encoder = Nominatim()
        location = nominatim_encoder.geocode(formatted_text)
    except:
        #for local:
        google_api_key = pickle.load(open("google_geocoder_api.creds","rb"))
        #for server:
        #google_api_key = os.getenv("GOOGLE_GEOCODER_API")
        google_encoder = GoogleV3(google_api_key)
        address_type = address_is_complete(text)
        if address_type == "complete":
            location = google_encoder.geocode(text)
        elif address_type == "cross street":
            location = google_encoder.geocode(' and '.join(get_streetnames(text)) + city)
    if location:
        return location.latitude, location.longitude

def clean_location_string(text):
    replace_pairs = [
        ("&"," "),
        ("\r"," "),
        ("\n"," "),
        ("Location:",""),
        ("•","")
    ]
    for old_char, new_char in replace_pairs:
        text = text.replace(old_char, new_char)
    return text.strip()

def strip_post_id(text):
    return text.split(": ")[1].split(" ")[0]
