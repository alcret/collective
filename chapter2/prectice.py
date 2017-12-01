#coding=utf-8
from recommendations import critics
print critics['Lisa Rose']['Lady in the Water']

dict={"name":"python","english":33,"math":35}

print "##for in "
for i in dict:
        print "dict[%s]=" % i,dict[i]