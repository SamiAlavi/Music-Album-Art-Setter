from requests import get
from stagger import read_tag
from selenium import webdriver

def setArt(song, art):
    mp3=read_tag(song)
    mp3.picture=art
    mp3.write()

def setArtRunner(path,files,audioforms):
    for filename in files:
        for formats in audioforms:
            if checkformat(filename, formats):
                try:
                    setArt(path+filename,'downloads/'+filename+'.jpg')
                except:
                    with open('errors(setArt).txt','a+') as f:
                        f.write(filename+'\n')
                break


def saveImage(iname,link):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    img_data = get(link, headers=headers).content
    with open('downloads/'+iname+'.jpg', 'wb') as f:
        f.write(img_data)

def downloadImage(driver,url,query):
    q=query[:-4].replace(' ','+')+'&size=large'
    xpath='/html/body/div[1]/div/main/div[2]/div/a[1]/img'
    driver.get(url+q)

    link = driver.find_element_by_xpath(xpath).get_attribute("src")
    #print(link)
    saveImage(query,link)

def checkformat(query, formats):
    return query.lower().endswith(formats)

def getAllArts(search_queries, audioforms):
    options = webdriver.ChromeOptions()
    options.add_argument('headless') ##remove this to visualize the automation
    
    driver = webdriver.Chrome('chromedriver.exe',chrome_options=options) # Using Chrome to access
    url='https://www.ecosia.org/images?q='
    for query in search_queries:
        for formats in audioforms:
            if checkformat(query, formats):
                print(query)
                try:
                    downloadImage(driver,url,query)
                except:
                    with open('.errors(downloadImage).txt','a+') as f:
                        f.write(query+'\n')
                break
    driver.quit()

def setAlbum(path,music,audioforms):
    with open("##COUNT.txt", "r") as f:
        count=int(f.read())
    
    for i in music:
        for formats in audioforms:
            if checkformat(i, formats):
                count+=1
                mp3=read_tag(path+i)
                mp3.album=str(count)
                mp3.write()
                break
        
    with open("##COUNT.txt", "w") as f:
        f.write(str(count))

