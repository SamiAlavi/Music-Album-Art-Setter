# importing google_images_download module 
from google_images_download import google_images_download
import os

# creating object 
response = google_images_download.googleimagesdownload()  

path='Music/'
search_queries=os.listdir(path)

def downloadimages(query):
    # keywords is the search query 
    # format is the image file format 
    # limit is the number of images to be downloaded 
    # print urs is to print the image file url 
    # size is the image size which can 
    # be specified manually ("large, medium, icon") 
    # aspect ratio denotes the height width ratio 
    # of images to download. ("tall, square, wide, panoramic") 
    arguments = {"keywords": query, 
                 "format": "jpg", 
                 "limit":1, 
                 "print_urls":False, 
                 "size": "large",
                 'silent_mode':True}
    try: 
        response.download(arguments) 
      
    # Handling File NotFound Error     
    except FileNotFoundError:  
        pass  
        
  
# Driver Code 
for query in search_queries:
    try:
        downloadimages(query)
    except:
        with open('errors(downloadArt).txt','a+') as f:
            f.write(query+'\n')
    print() 
