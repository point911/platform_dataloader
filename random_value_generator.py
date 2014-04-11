import random
import string

LE_NAME_PREFIX = "01_IT_"


def generate_random_val(r_type, length):
    if r_type == 'text':
        return ''.join(random.choice(string.ascii_lowercase) for i in range(length))
    elif r_type == 'number':
        return ''.join(random.choice(string.digits) for i in range(length))
    elif r_type == 'mixed':
        text = generate_random_val('text', length / 2)
        nums = generate_random_val('number', length / 2)
        pswd = text + nums
        return ''.join(random.sample(pswd, len(pswd)))
    else:
        raise AssertionError


def get_random(value_name, value_type):
    value = "NO VALUE!"

    if value_name == "idType":
        value = "AVOX"
    elif value_name == "id":
        value = "3215335"
    elif value_name == "city":
        value = "Minsk"
    elif value_name == "addressType":
        value = "LEGAL"
    elif value_name == "country":
        value = "UNITED STATES"
    elif value_name == "line1":
        value = "AV PRESIDENTE JUSCELINO KUBITSCHEK 360"
    elif value_name == "state":
        value = "SPAULO"
    elif value_name == "postalCode":
        value = "04543-000"
    elif value_name == "riskLevel":
        value = random.choice(["low"])
    elif value_name == "tradingStatus":
        value = "ACTIVE"
    elif value_name == "legalEntityName":
        value = LE_NAME_PREFIX + generate_random_val("text", 10)

    return "{0}[{1}]".format(value_type, value)
