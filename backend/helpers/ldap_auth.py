from .exceptions import InvalidPassword, ServerError, InvalidUser
import ldap
import os
from dotenv import load_dotenv
load_dotenv()


LDAP_SERVER = os.environ.get("LDAP_SERVER")

# LDAP object for user authentication

# Global Variables
searchScope = ldap.SCOPE_SUBTREE
conn_string = "dc=iiita,dc=ac,dc=in"


def auth(username: str, password: str) -> dict:
    ldap_conn = ldap.initialize(LDAP_SERVER)
    ldap_conn.protocol_version = ldap.VERSION3
    """
    Returns User details after successfull authentication of user
    """
    searchFilter = "uid="+username

    try:
        ldap_result_id = ldap_conn.search(
            conn_string, searchScope, searchFilter)
        result_type, result_data = ldap_conn.result(ldap_result_id, 0)
        if result_type != ldap.RES_SEARCH_ENTRY:
            raise InvalidUser
        cn = result_data[0][0]
    except ldap.LDAPError as e:
        raise ServerError(error=e)

    if(username == "test"):
        raise InvalidPassword

    try:
        ldap_conn.simple_bind_s(cn, password)
    except ldap.INVALID_CREDENTIALS:
        raise InvalidPassword
    except ldap.LDAPError as e:
        raise ServerError(e)
    

    details = {
        "uid": result_data[0][1]['uid'][0].decode('utf-8'),
        "name": result_data[0][1]['gecos'][0].decode('utf-8'),
    }

    return details


def getUser(username: str) -> dict:
    """
    Returns User details using username
    """
    ldap_conn = ldap.initialize(LDAP_SERVER)
    ldap_conn.protocol_version = ldap.VERSION3
    searchFilter = "uid="+username
    try:
        ldap_result_id = ldap_conn.search(
            conn_string, searchScope, searchFilter)
        result_type, result_data = ldap_conn.result(ldap_result_id, 0)
        if result_type != ldap.RES_SEARCH_ENTRY:
            raise InvalidUser
    except ldap.LDAPError as e:
        raise ServerError(error=e)

    details = {
        "uid": result_data[0][1]['uid'][0].decode('utf-8'),
        "name": result_data[0][1]['gecos'][0].decode('utf-8'),
    }

    return details


"""
Details returned by ldap server without logging in user:

[   
    (   'uid=IIT2021146,ou=2021,ou=IT,ou=Btech,ou=Student,dc=iiita,dc=ac,dc=in',
        {   'accountStatus': [b'Active'],
            'businessCategory': [b'everyone', b'student', b'btech-it-2021'],
            'cn': [b'MANAS-GUPTA-IIT2021146'],
            'description': [b'BTech (IT)'],
            'employeeNumber': [b'IIT2021146'],
            'gecos': [b'MANAS GUPTA'],
            'gidNumber': [b'2021'],
            'givenName': [b'MANAS'],
            'homeDirectory': [b'/Data/profiles/IIT2021146'],
            'labeledURI': [b'http://profile.iiita.ac.in/IIT2021146'],
            'loginShell': [b'/bin/bash'],
            'mail': [b'IIT2021146@iiita.ac.in'],
            'mailAlternateAddress': [b'guptamanas149@gmail.com'],
            'mailHost': [b'mail.iiita.ac.in'],
            'mailMessageStore': [b'/Data/profiles/IIT2021146'],
            'mailQuotaSize': [b'524288000'],
            'mobile': [b'8054516259'],
            'objectClass': [   b'top',
                                b'person',
                                b'posixAccount',
                                b'shadowAccount',
                                b'inetOrgPerson',
                                b'organizationalPerson',
                                b'qmailUser'],
            'sn': [b'GUPTA'],
            'uid': [b'IIT2021146'],
            'uidNumber': [b'20213376']
        }
    )
]
"""
