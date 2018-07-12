# import sys,os
# print(sys.path)
# a = os.path.abspath(__file__)
# a = a.split('\\')[0:-3]
# print(a)
# a = '\\'.join(a)
# print(a)
# sys.path.insert(0,a)

import sys,os
import platform
if platform.system() == 'Windows':
    # print(sys.path)
    a = os.path.abspath(__file__)
    a = a.split('\\')[0:-3]
    a = '\\'.join(a)
    sys.path.insert(0, a)
else:
    # print(sys.path)
    a = os.path.abspath(__file__)
    a = a.split('/')[0:-3]
    # print(a)
    a = '/'.join(a)
    # print(a)
    sys.path.insert(0,a)