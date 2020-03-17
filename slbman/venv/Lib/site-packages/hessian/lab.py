'''
Created on Oct 22, 2009

@author: petr
'''

class E(Exception):
    pass

if __name__ == '__main__':
    try:
        raise Exception(2)
    except Exception as e:
        print e.args 