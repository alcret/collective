import pydelicious
from urllib import urlencode
from urllib2 import urlopen
    # import get_userposts,get_popular,get_urlposts
pydelicious.get_popular(tag = "programming")
# pydelicious.get_userposts('dorsia')



# def initializeUserDict(tag,count=5):
#     user_dict={}
#     for p1 in get_popular(tag=tag)[0:count]:
#         for p2 in get_urlposts(p1['href']):
#             user = p2['user']
#             user_dict[user] = {}
#     return user_dict
