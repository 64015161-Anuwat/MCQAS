import bcrypt
import environ

env = environ.Env()
environ.Env.read_env()

pepper = env('PEPPER').encode('utf-8')

def hash_password(password):
    # Generate a salt and hash the password
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8') + pepper, salt)
    
    return salt.decode('utf-8'), hashed_password.decode('utf-8')

def verify_password(input_password, stored_salt, stored_hashed_password):
    # Verify the input password against the stored salt and hashed password
    input_password = input_password.encode('utf-8')
    hashed_input_password = bcrypt.hashpw(input_password + pepper, stored_salt.encode()).decode('utf-8')

    return hashed_input_password == stored_hashed_password