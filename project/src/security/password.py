from passlib.context import CryptContext

'''
Exporting our password checker to this area means that everyone can
import this global symbol into their code as needed, and we're able to
update the hash function we use with very little headache. Overall,
it's way better than doing it manually.
@author: npcompletenate
'''
pwd_context = CryptContext(schemes=['pbkdf2_sha256'], deprecated="auto")
