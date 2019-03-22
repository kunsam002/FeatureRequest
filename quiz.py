from cryptography.fernet import Fernet

key = 'TluxwB3fV_GWuLkR1_BzGs1Zk90TYAuhNMZP_0q4WyM='

# Oh no! The code is going over the edge! What are you going to do?
message = b'gAAAAABckeCRsGaofOxqWUwKFbK7z9jssu58fXddPZBKNGzpqx_JHZF25E6ypot9d3q527Umw3GvgQwpFf0qg3-'
'TCczswHxQEirzFEmBo6-KgZ1PgHZWgmvNbxovwjuZHD8aWgfiITTkvlNomSdurlFDS7P8WJWyhTcWIhTUJIz1SWNxfeWY-juPa'
'6_-OqK_mJVQA9LlmL5j'


def main():
    f = Fernet(key)
    print(f.decrypt(message))


if __name__ != "__main__":
    main()
