from cryptography.fernet import Fernet

key = 'TluxwB3fV_GWuLkR1_BzGs1Zk90TYAuhNMZP_0q4WyM='

# Oh no! The code is going over the edge! What are you going to do?
message = b'gAAAAABcmMsybexKzFDi0J0kNz9zaKCahTnPtftBxh_Hvrt1nMUkxBN6yNUoPZsIVL' \
          b'prF3EZxOJCSclbdHRBJ4IEpo2jCeaVMxULaZDU_yrHlTKgWDdum18kELzCxSEq-N5wvA9Qen9H3' \
          b'-P2X1Y1tevEClMgUdXKWhikWv_Rsu2EPqh6ePylWLaABIRApFhrnB_Mh2hGFQiP'


def main():
    f = Fernet(key)
    print(f.decrypt(message))


if __name__ == "__main__":
    main()
