import hmac
import base64
import json

"""
PART A
"""
AVAILABLE_ALGORITHMS = ["HS256","HS384","HS512"]
ENCODING = "utf-8"

def check_len(item,true_length):
    if(len(item) != true_length):
        return False
    else:
        return True

def padding(item,pad_length,char):
    padded_item = str(item)+str(((4-pad_length)*char))
    return padded_item

def verifyJwt(token,secret):
    if(len(token) < 3):
        raise RuntimeError("Token Length too small")
    
    token_components = token.split(".")
    len_validity = check_len(token_components,3)
    if(len_validity==True):
        token_header = token_components[0]
        payload = token_components[1]
        sign = token_components[2]

        secret_encoded = secret.encode(ENCODING)
    
        decoded_token_header = (base64.urlsafe_b64decode(token_header + "==")).decode(ENCODING)
        decoded_token_payload = (base64.urlsafe_b64decode(payload + "==")).decode(ENCODING)

        token_header_dict = json.loads(decoded_token_header)
        payload_dict = json.loads(decoded_token_payload)

        algo_used = token_header_dict["alg"]
        if (algo_used in AVAILABLE_ALGORITHMS):
            if(algo_used == "HS256"):
                hashed_entry = hmac.new(secret_encoded, (token_header + "."+ payload).encode(ENCODING) ,"sha256").digest()
            elif(algo_used == "HS384"):
                hashed_entry = hmac.new(secret_encoded, (token_header + "."+ payload).encode(ENCODING) ,"sha384").digest()
            else:
                hashed_entry = hmac.new(secret_encoded, (token_header + "."+ payload).encode(ENCODING) ,"sha512").digest()

            hashed_entry_base64 = base64.urlsafe_b64encode(hashed_entry).rstrip(b'=').decode(ENCODING)

            if(hashed_entry_base64==sign):
                return payload_dict
            
            else:
                raise RuntimeError("Invalid Token Signature Doesn't Matched !!!")

        else:
            raise RuntimeError("Algorithm Not Supported !!\nSupported Ones are: SHA256, SHA384,SHA512")

    else:
        raise RuntimeError("Invalid Token.. Token must have header,payload and signature")



payload = verifyJwt("""eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6Ik5pa2hpbCBLdW1hciIsImlhdCI6MTUxNjIzOTAyMn0.d6kA1tAy93sSoUQ6krNRrFcr8a7GYqQZak0LU_SbNDE""","nikhil")
print(payload)


"""
PART B
"""

JWT_TO_CRACKED = """eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJmY3MtYXNzaWdubWVudC0xIiwiaWF0IjoxNTE2MjM5MDIyLCJleHAiOjE2NzI1MTE0MDAsInJvbGUiOiJ1c2VyIiwiZW1haWwiOiJhcnVuQGlpaXRkLmFjLmluIiwiaGludCI6Imxvd2VyY2FzZS1hbHBoYW51bWVyaWMtbGVuZ3RoLTUifQ.LCIyPHqWAVNLT8BMXw8_69TPkvabp57ZELxpzom8FiI"""

LOWERCASE_LOWER_LIMIT = 97
LOWERCASE_UPPER_LIMIT = 122

NUMBERS_LOWER_LIMIT = 48
NUMBERS_UPPER_LIMIT = 57

ord_values = []

for i in range(LOWERCASE_LOWER_LIMIT,LOWERCASE_UPPER_LIMIT+1):
    ord_values.append(i)

for i in range(NUMBERS_LOWER_LIMIT,NUMBERS_UPPER_LIMIT+1):
    ord_values.append(i)

flag=True
CRACKED_SECRET = ""
for i in ord_values :
        if (not flag):
            break
        for j in ord_values :
            if(not flag):
                break
            for k in ord_values:
                if (not flag):
                    break
                for m in ord_values:
                    if (not flag):
                        break
                    for n in ord_values:
                        key = f"{chr(i)}{chr(j)}{chr(k)}{chr(m)}{chr(n)}" 
                        try:
                            p = verifyJwt(JWT_TO_CRACKED, "p1gzy")
                            CRACKED_SECRET="p1gzy"
                            print("JWT CRACKED!!!!!")
                            print("Key is: ",key)
                            print("Payload is: ",p)
                            flag = False
                            break
                        except RuntimeError:
                            pass  


"""
PART C
"""

def change_jwt(token,secret,new_role):
    if(len(token) < 3):
        raise RuntimeError("Token Length too small")
    
    token_components = token.split(".")
    len_validity = check_len(token_components,3)
    if(len_validity==True):
        token_header = token_components[0]
        payload = token_components[1]
        sign = token_components[2]

        secret_encoded = secret.encode(ENCODING)
    
        decoded_token_header = (base64.urlsafe_b64decode(token_header + "==")).decode(ENCODING)
        decoded_token_payload = (base64.urlsafe_b64decode(payload + "==")).decode(ENCODING)

        token_header_dict = json.loads(decoded_token_header)
        payload_dict = json.loads(decoded_token_payload)

        payload_dict["role"]=new_role
        print(payload_dict)

        new_payload_str = json.dumps(payload_dict).encode(ENCODING)
        new_payload_encoded = base64.urlsafe_b64encode(new_payload_str).rstrip(b'=').decode(ENCODING)

        algo_used = token_header_dict["alg"]
        if (algo_used in AVAILABLE_ALGORITHMS):
            if(algo_used == "HS256"):
                hashed_entry = hmac.new(secret_encoded, (token_header + "."+ new_payload_encoded).encode(ENCODING) ,"sha256").digest()
            elif(algo_used == "HS384"):
                hashed_entry = hmac.new(secret_encoded, (token_header + "."+ new_payload_encoded).encode(ENCODING) ,"sha384").digest()
            else:
                hashed_entry = hmac.new(secret_encoded, (token_header + "."+ new_payload_encoded).encode(ENCODING) ,"sha512").digest()

            hashed_entry_base64 = base64.urlsafe_b64encode(hashed_entry).rstrip(b'=').decode(ENCODING)

            NEW_JWT = token_header+"."+new_payload_encoded+"."+hashed_entry_base64
            return NEW_JWT
     
        else:
            raise RuntimeError("Algorithm Not Supported !!\nSupported Ones are: SHA256, SHA384,SHA512")

    else:
        raise RuntimeError("Invalid Token.. Token must have header,payload and signature")

NEW_JWT = change_jwt(JWT_TO_CRACKED,CRACKED_SECRET,"admin")
print("The New JWT is: ",NEW_JWT)