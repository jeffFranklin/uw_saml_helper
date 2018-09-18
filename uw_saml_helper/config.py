class DefaultSp(object):
    entity_id = ''
    acs_url = ''
    acs_binding = 'urn:oasis:names:tc:SAML:2.0:bindings:HTTP-POST'
    x509_cert = ''
    private_key = ''

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def to_dict(self):
        data = {
            'strict': True,
            'sp': {
                'entityId': self.entity_id,
                'assertionConsumerService': {
                    'url': self.acs_url,
                    'binding': self.acs_binding
                },
                'x509cert': self.x509_cert,
                'privateKey': self.private_key
            }
        }
        return data


class IdpConfig(object):
    entity_id = ''
    sso_url = ''
    sso_binding = 'urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect'
    x509_cert = ''
    id_attribute = 'urn:oid:1.3.6.1.4.1.5923.1.1.1.6'  # eppn
    attribute_map = {}
    is_two_factor = False

    def to_dict(self):
        data = {
            'strict': True,
            'idp': {
                'entityId': self.entity_id,
                'singleSignOnService': {
                    'url': self.sso_url,
                    'binding': self.sso_binding
                },
                'x509cert': self.x509_cert
            }
        }
        if self.is_two_factor:
            data.update({
                'security': {
                    'requestedAuthnContext': [
                        'urn:oasis:names:tc:SAML:2.0:ac:classes:TimeSyncToken'],
                    'failOnAuthnContextMismatch': True
                }
            })
        return data


class ListAttribute(str):
    """An attribute key whose values should be returned as a list."""


class UwIdp(IdpConfig):
    entity_id = 'urn:mace:incommon:washington.edu'
    sso_url = 'https://idp.u.washington.edu/idp/profile/SAML2/Redirect/SSO'
    x509_cert = '''
        MIID/TCCAuWgAwIBAgIJAMoYJbDt9lKKMA0GCSqGSIb3DQEBBQUAMFwxCzAJBgNV
        BAYTAlVTMQswCQYDVQQIEwJXQTEhMB8GA1UEChMYVW5pdmVyc2l0eSBvZiBXYXNo
        aW5ndG9uMR0wGwYDVQQDExRpZHAudS53YXNoaW5ndG9uLmVkdTAeFw0xMTA0MjYx
        OTEwMzlaFw0yMTA0MjMxOTEwMzlaMFwxCzAJBgNVBAYTAlVTMQswCQYDVQQIEwJX
        QTEhMB8GA1UEChMYVW5pdmVyc2l0eSBvZiBXYXNoaW5ndG9uMR0wGwYDVQQDExRp
        ZHAudS53YXNoaW5ndG9uLmVkdTCCASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoC
        ggEBAMH9G8m68L0Hf9bmf4/7c+ERxgDQrbq50NfSi2YTQWc1veUIPYbZy1agSNuc
        4dwn3RtC0uOQbdNTYUAiVTcYgaYceJVB7syWf9QyGIrglZPMu98c5hWb7vqwvs6d
        3s2Sm7tBib2v6xQDDiZ4KJxpdAvsoPQlmGdgpFfmAsiYrnYFXLTHgbgCc/YhV8lu
        bTakUdI3bMYWfh9dkj+DVGUmt2gLtQUzbuH8EU44vnXgrQYSXNQkmRcyoE3rj4Rh
        hbu/p5D3P+nuOukLYFOLRaNeiiGyTu3P7gtc/dy/UjUrf+pH75UUU7Lb369dGEfZ
        wvVtITXsdyp0pBfun4CP808H9N0CAwEAAaOBwTCBvjAdBgNVHQ4EFgQUP5smx3ZY
        KODMkDglkTbduvLcGYAwgY4GA1UdIwSBhjCBg4AUP5smx3ZYKODMkDglkTbduvLc
        GYChYKReMFwxCzAJBgNVBAYTAlVTMQswCQYDVQQIEwJXQTEhMB8GA1UEChMYVW5p
        dmVyc2l0eSBvZiBXYXNoaW5ndG9uMR0wGwYDVQQDExRpZHAudS53YXNoaW5ndG9u
        LmVkdYIJAMoYJbDt9lKKMAwGA1UdEwQFMAMBAf8wDQYJKoZIhvcNAQEFBQADggEB
        AEo7c2CNHEI+Fvz5DhwumU+WHXqwSOK47MxXwNJVpFQ9GPR2ZGDAq6hzLJLAVWcY
        4kB3ECDkRtysAWSFHm1roOU7xsU9f0C17QokoXfLNC0d7KoivPM6ctl8aRftU5mo
        yFJkkJX3qSExXrl053uxTOQVPms4ypkYv1A/FBZWgSC8eNoYnBnv1Mhy4m8bfeEN
        7qT9rFoxh4cVjMH1Ykq7JWyFXLEB4ifzH4KHyplt5Ryv61eh6J1YPFa2RurVTyGp
        HJZeOLUIBvJu15GzcexuDDXe0kg7sHD6PbK0xzEF/QeXP/hXzMxR9kQXB/IR/b2k
        4ien+EM3eY/ueBcTZ95dgVM='''
    attribute_map = {
        'eppn': 'urn:oid:1.3.6.1.4.1.5923.1.1.1.6',
        'uwnetid': 'urn:oid:0.9.2342.19200300.100.1.1',
        'affiliations': ListAttribute('urn:oid:1.3.6.1.4.1.5923.1.1.1.1'),
        'groups': ListAttribute('urn:oid:1.3.6.1.4.1.5923.1.5.1.1')
    }


class UwIdpTwoFactor(UwIdp):
    is_two_factor = True


class CascadiaStudentIdp(IdpConfig):
    entity_id = 'https://idp.cascadia.edu/idp/shibboleth'
    sso_url = 'https://idp.student.cascadia.edu/idp/profile/Shibboleth/SSO'
    id_attribute = 'urn:mace:washington.edu:dir:attribute-def:stu-validationID'
    x509_cert = '''
        MIIDTDCCAjSgAwIBAgIVAKF/idZbWozYUUVYSAZqNtoPhTTpMA0GCSqGSIb3DQEB
        BQUAMCMxITAfBgNVBAMTGGlkcC5zdHVkZW50LmNhc2NhZGlhLmVkdTAeFw0wOTA3
        MTcxNzM0NDZaFw0yOTA3MTcxNzM0NDZaMCMxITAfBgNVBAMTGGlkcC5zdHVkZW50
        LmNhc2NhZGlhLmVkdTCCASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEBAKsC
        6uf6XGhfUYhypRK7BNXr9df4phb1pAISvXXGvICQB/iABP40fbMgk1+RVwjTVXj2
        40JBlmYiHZ69Gcwv6GyIhbouNTb46k5Pp/bmU3K0oqwWHjbE68CyHS5IxRPImAlR
        OeTFI4LFNvnNvZPb7uRhYAg1EgmJXjwscUqssNCmXozesHwM7vEjv/6jfeQ2RLB3
        q2QVVuMEcFYh21+lNY07HmKkxBFSifHu2qKyVpLK7CWd8Qsj7v6cy/ixEc9VJdBJ
        ptridTi2zcv33E4hZGrCvwWjdwPt/evOGOY7umUzOokbT6tqPFTUAmdlEeJKAdyv
        FXVki+85jyJm0xg3FkkCAwEAAaN3MHUwVAYDVR0RBE0wS4IYaWRwLnN0dWRlbnQu
        Y2FzY2FkaWEuZWR1hi9odHRwczovL2lkcC5zdHVkZW50LmNhc2NhZGlhLmVkdS9p
        ZHAvc2hpYmJvbGV0aDAdBgNVHQ4EFgQUtK4D0urHY0BSPPxibiQcjWlp0YkwDQYJ
        KoZIhvcNAQEFBQADggEBAGzAU57okBkfeaRUC1lnOXbjNfX/+XRTBY6dWLhlwxmK
        zJ4yosaCHD6XsXuDwlVOeu0Ms38tvTakGlmLiJ644PKJVfrQeVRY22EKEJnpHMl5
        mIKsRFjSA6we3sot0f/APiMqisieSLJHnd4Q7XXzt5ybBRSbDneEf0ukO+gqGHY2
        TlwHPe9Z73h1R5sQdLlSAUDH/UKm+5uWb0K+o7STppImd0Fs+fEInSIzZk7YpAG3
        v1S5a9uxu9q/jtCa5N49Dgu8H6p9dtqlVtU+v0ZQREpaLSxThI0gXMeDLhHKn+Oh
        4evvj1ikdsX7XBiSpTNiUGMF0D7ZllSqTk+E+/Cyo5Q='''


class CascadiaEmployeeIdp(CascadiaStudentIdp):
    sso_url = 'https://idp.employee.cascadia.edu/idp/profile/Shibboleth/SSO'
    id_attribute = 'urn:mace:washington.edu:dir:attribute-def:emp-validationID'


class CollegenetIdp(IdpConfig):
    entity_id = 'https://shibboleth-idp.collegenet.com/idp/shibboleth'
    sso_url = ('https://shibboleth-idp.collegenet.com'
               '/idp/profile/SAML2/Redirect/SSO')
    id_attribute = 'urn:oid:1.3.6.1.4.1.5923.1.1.1.10'  # persistent id
    x509_cert = '''
        MIIDYDCCAkigAwIBAgIUE7bIe4hwDfwhSM8wn4E8Rza/AdEwDQYJKoZIhvcNAQEF
        BQAwKDEmMCQGA1UEAxMdc2hpYmJvbGV0aC1pZHAuY29sbGVnZW5ldC5jb20wHhcN
        MTAwMjExMjMxNTMyWhcNMzAwMjExMjMxNTMyWjAoMSYwJAYDVQQDEx1zaGliYm9s
        ZXRoLWlkcC5jb2xsZWdlbmV0LmNvbTCCASIwDQYJKoZIhvcNAQEBBQADggEPADCC
        AQoCggEBAIFEn4f9ObsbquJlOPvIazrYJ+cltWyFL5My6Sci6K1L/xTfRNAtGA3U
        DQL3wOALSFtfddl/ULTfQYU2/AZKFj7BwA72lou6G9SUco5QchHUoaiCxnOs1LQ8
        kP2rA5nsxwfJrYnGULx1+c7qKmatN+OftKL96LD6g2rBw794FZd7j29ptrqOv97B
        gzVaH5od8ZMvegsKzpuYf0cOklD0dRJEW0ppb79JLJvSrWVX6K9oAvOXJx7+nHwK
        BGqETOU4nhXXJOgyVqib7d3mCg7YWyJXl1tLnTLZrHLi7bVk2BKUZO2yT62SsBy3
        MkThcDHokvyvwo/GUmF2dnJaYj59afUCAwEAAaOBgTB/MF4GA1UdEQRXMFWCHXNo
        aWJib2xldGgtaWRwLmNvbGxlZ2VuZXQuY29thjRodHRwczovL3NoaWJib2xldGgt
        aWRwLmNvbGxlZ2VuZXQuY29tL2lkcC9zaGliYm9sZXRoMB0GA1UdDgQWBBRf5n4e
        0WSw5ow5doI1M71y7rzfGjANBgkqhkiG9w0BAQUFAAOCAQEAGlTRbPUU9d5ond5O
        O3efuPRoIMCurUo6xaTD39rnr5m94Cr55n3dOwCnvjn0IMQvvvqGBJRD92i0VvZI
        4r63QtU5ZqSeAiNG5FFCA89jnR6P0nZqXV3R3mRaRHDM2apD9pNz2PUtFdktw5AB
        cURaOv4usFw8sWMQg0oM3rHC5VbTCCoQbmiRGiMCIqSEJbZ02JG+lUhrv1jp9xNj
        PjDjvSkxTTH3Mo4Lt7jVww76pgWRDa8L0eZ4sOREQVqMXEMcB3JNy7fFimunvxgw
        fIJN0Yk9uqeMFBoZiL8r0itI9BTt4gk2sYDbNnG6/pqoPS9mwmiM22XEeTeG1x3a
        WWeBDw=='''


class FredHutchIdp(IdpConfig):
    entity_id = 'https://shib.fhcrc.org/idp/shibboleth'
    sso_url = 'https://shib.fhcrc.org/idp/profile/SAML2/Redirect/SSO'
    x509_cert = '''
        MIIDIzCCAgugAwIBAgIUYqaDH2PjPdZ38g8PPuq3hjmdVQswDQYJKoZIhvcNAQEF
        BQAwGTEXMBUGA1UEAxMOc2hpYi5maGNyYy5vcmcwHhcNMTEwMjIzMjMzNDEwWhcN
        MzEwMjIzMjMzNDEwWjAZMRcwFQYDVQQDEw5zaGliLmZoY3JjLm9yZzCCASIwDQYJ
        KoZIhvcNAQEBBQADggEPADCCAQoCggEBAJDWhNtMACDyyVwdEn7ZTt4teMurPpIQ
        0QAnJB8A/VBo15/kkGQl6GKnjVT0yuXM9iRurwwbDh1nwhIaDX1kVqBCBueu4wh1
        cceN1U+w5mhhWr37jc6hvml9vf/m/2GJcXyOEeneNOf5yo3Lvia4ueoW0qLAbsTr
        36fYe8M1pa0AAudhpqUXDWdlXTfZdkPomufVVef6YpEVpJXxKezaF5BAYeyjAJ+k
        vrIxZXIxghjoFDHkTdf536YAxj23HHp0aUciL2r+QgGhho9i6LRAnMFce5HESL/G
        lIwHJLgvDgozCyw42kEPjQCwU7qBfnY33nmjBHLhw34sFZ1ElMOGbWMCAwEAAaNj
        MGEwQAYDVR0RBDkwN4IOc2hpYi5maGNyYy5vcmeGJWh0dHBzOi8vc2hpYi5maGNy
        Yy5vcmcvaWRwL3NoaWJib2xldGgwHQYDVR0OBBYEFH2yMS2n85KB2MuYt1flMZt4
        rhJLMA0GCSqGSIb3DQEBBQUAA4IBAQAK8eF4qh4l1cMY3X9v3+TN2+Ld+CkowKp/
        ALkr81YRVui4tbMOZ7yQs5WdEY3J4QJrDtQ2tsComdAWb0JIpRwJLHnj1cO3bAel
        jJr8GY4oXUUPGAJpRi5Ly6UKTQKEAHvBdsq6JQQqRLYN5yO1f2lr+QHnizs8rS5a
        +3dB0vs3YxYy1OqKzBLaCH13QkZClNBl87/62OLpnpEm6tAOSiWsD/4unPe2kOW5
        19aqTzwjsV2Am2OINyXSKUK1yA6B5nv9LUzO2ESIH9A06DOYlXWch6u7a0b+3URk
        //e64IUXSJ1NqLsVrX68mC2ysMMojbRiOdmV9mPUcpizb0devpvc'''


class SccaIdp(IdpConfig):
    entity_id = 'https://shib.seattlecca.org/idp/shibboleth'
    sso_url = 'https://shib.seattlecca.org/idp/profile/SAML2/Redirect/SSO'
    x509_cert = '''
        MIIDNzCCAh+gAwIBAgIUbcFgoLeGDb4Ai/Ll8QDjXOQ4GF4wDQYJKoZIhvcNAQEF
        BQAwHjEcMBoGA1UEAxMTc2hpYi5zZWF0dGxlY2NhLm9yZzAeFw0xMDEyMjkyMzUz
        MDBaFw0zMDEyMjkyMzUzMDBaMB4xHDAaBgNVBAMTE3NoaWIuc2VhdHRsZWNjYS5v
        cmcwggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIBAQCEW0aj4zjtHes50H9y
        S0I+Nom/r/mBjjf24UMSbY3N/f2Pz/J+lH+rRyDIhWGOovyvu3GoIGEFz3o28F4e
        KXGDoexlZ3wm3/uz1OnTZqI2RNS6Q8RBTDhf5f+VTz2zaSNsi1Mnsg701/GFybLO
        GyQr0ShdwcWK3YVGLt5BQ/STGdv1/rCkJqdv/x3eE51yveZnkpbGlI+l4DnickmH
        GJzRCcpWvHHsANotdjBl4xu/uWGs4q9BXHEXSJtd5cY7xWvcVy7PUMzrrNOniMzl
        sDMESjdi3nMFOrzZQ9obvBj+TXD5S3+ZdCCMZepbjkaWbP1nAzU5i+KdP5X8ltFz
        0cX9AgMBAAGjbTBrMEoGA1UdEQRDMEGCE3NoaWIuc2VhdHRsZWNjYS5vcmeGKmh0
        dHBzOi8vc2hpYi5zZWF0dGxlY2NhLm9yZy9pZHAvc2hpYmJvbGV0aDAdBgNVHQ4E
        FgQUeHpCU4lXvT+TIYwAfcxr/TRgC+kwDQYJKoZIhvcNAQEFBQADggEBADEKJkMr
        JpNF72v8dP1fpyvFdIiypBiQtVlQddM3UkWeKGJdNEh4VcPcMvt75JiJKExZi7sD
        1GzuW1e5tFIOHdBuFFJ3+dhNuJHCRi+J8WM09s7gcU0usrJMmcg4/oaqrZCDUsFK
        Qd/Qy5EpAVO2W64pCekjmU8GU3pKQ+pVJy09U0b7JDnRW1MSXrN6XDb1ZmVbDgcZ
        Nptlvp+WBbg4k1u+7kpCd7dY5DmBe5U+57Ha8Gzrwx+HPxQqEbuT8mtvu1sEqAqJ
        VWCU3vLq2NMiSWevER9gA5g3kl0cwFfSSIFaUPLA5lnm6LUBOrDgK/50gWfYyidH
        z8rWDouRlgPxFA0='''


class TestIdp(IdpConfig):
    entity_id = 'https://thor-idp.cac.washington.edu/idp/shibboleth'
    sso_url = ('https://thor-idp.cac.washington.edu'
               '/idp/profile/SAML2/Redirect/SSO')
    x509_cert = '''
        MIIDVzCCAj+gAwIBAgIUedVWX+JQX04XEack4w0QDiIDGlQwDQYJKoZIhvcNAQEL
        BQAwJjEkMCIGA1UEAwwbdGhvci1pZHAuY2FjLndhc2hpbmd0b24uZWR1MB4XDTE4
        MDEwMzE2MDY0MFoXDTM4MDEwMzE2MDY0MFowJjEkMCIGA1UEAwwbdGhvci1pZHAu
        Y2FjLndhc2hpbmd0b24uZWR1MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKC
        AQEAnTQHW/mvtzJc4MVCt7xa/sOWvvsi19MHf6yPMSXOASILNEmXwqBsmjogVQnK
        urjk9sO4tPSWpRFG3vlk5CjFHUHLZlzY6g+h0qcqE6Rh833rqi9IywY9T5wM5ssH
        BbvAbVvGK53oe31DoNn99Ig+PuW3k9QkzF71zGLCSZtSsYNWaErNx5qVX8C+VITM
        gli5SOmKEJXJuOcCwUl1PjxPez/v+9z5WijFhMbYKPxvfwu2HAr+WwMjHucbm/k3
        au2YLwUo9jt+TLZtxhkQKlXilVYZ8rJeFQ1XenqV6+nlH6nPQ92L1thGR4yx3LfM
        85JR1hScRvOAtDultWgZ4xZCYQIDAQABo30wezAdBgNVHQ4EFgQUkFx2WA1kCtdB
        pbcHqTvNWBR8HVQwWgYDVR0RBFMwUYIbdGhvci1pZHAuY2FjLndhc2hpbmd0b24u
        ZWR1hjJodHRwczovL3Rob3ItaWRwLmNhYy53YXNoaW5ndG9uLmVkdS9pZHAvc2hp
        YmJvbGV0aDANBgkqhkiG9w0BAQsFAAOCAQEAcWf5OeoRmz05/itP4GaUL+uJzO4f
        o3bFvU1QwETMm8Lkukh0sdsyDs6cVwgp8Pt738isj52+jwPSzEl+4Iirh8t7c84o
        J4Yj4lhvDXEb7wPPR1/3xWSaMPFFqNHpqqDp5x1Wq7h7MYc/Pq8ApNTISvtnKar8
        vPEek8lr1WxNQfLgaSUyb3uHOCAaQQnLCQzfQGSpqwcn3OsLxfFP5a0jdcXGNPwg
        Ul/zCgXGtpqj0pgaGKncgEwAX/CItsqUmnia58mMAzUQfbEtawSBw8QztBh1uJ/J
        szamvpcczUDLghpfj8byPjyTBIWAeJFVfmOJRsob+NcspvuZXMcKd8o+RQ=='''
