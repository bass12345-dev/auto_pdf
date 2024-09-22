import bcrypt
from src.process.query.query import check_email_query
from flask import request,session


def password_hash(password):
    password1 = password.encode('utf-8')  # Encode the password to bytes
    hashed_password = bcrypt.hashpw(password1, bcrypt.gensalt())
    return hashed_password

def verify_process(email,password):
    response = {}
    hash_password = b'$2b$12$0H1vC0/J0Mb40gLmXrNIy.Yl7FprWxxkFM/RLzk/aChZor.O55lxm'
    if email != '' and password != '':
        
            resp = check_email_query(email)

            if(resp):
                password = password.encode('utf-8') 
                hash_password1 = hash_password.decode('utf-8')

                hashed_password_retrieved = hash_password1.encode('utf-8')
                is_valid = bcrypt.checkpw(password, hashed_password_retrieved)  # Both arguments must be bytes

                if is_valid:
                    set_session(email,resp)
                    response['message']  = 'Success'
                    response['response']  = True
                    
                else:
                    response['message']   = 'Invalid Password'
                    response['response']  = False
            else:
                response['message']   = 'Email Not Found'
                response['response']  = False
            
                 
    else:
        response['message']   = 'Please Fill Up All Fields'
        response['response']  = False

    return response


def set_session(email,resp):
     session['email']   = email
     session['name']    = resp[2]
    #  session['id']      = resp[1]
     