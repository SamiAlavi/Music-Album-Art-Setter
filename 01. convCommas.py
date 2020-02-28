import os

path='Music/'
search_queries=os.listdir(path)
commas=list()
for i in search_queries:
    if i.find(',')!=-1:
        j=i.replace(',',' ')
        os.rename(path+i, path+j)
        with open('commas.txt','a+') as f:
            f.write(i)
            f.write('\n')
