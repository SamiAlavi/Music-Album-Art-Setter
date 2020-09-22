import os
from selenium import webdriver
from combined import getAllArts, setArtRunner, getAllLyrics, setLyricsRunner, setAlbum

def setDriver():
    #options to make selenium faster
    prefs = {'profile.default_content_setting_values': {'images': 2, 
            'plugins': 2, 'popups': 2, 'geolocation': 2, 
            'notifications': 2, 'auto_select_certificate': 2, 'fullscreen': 2, 
            'mouselock': 2, 'mixed_script': 2, 'media_stream': 2, 
            'media_stream_mic': 2, 'media_stream_camera': 2, 'protocol_handlers': 2, 
            'ppapi_broker': 2, 'automatic_downloads': 2, 'midi_sysex': 2, 
            'push_messaging': 2, 'ssl_cert_decisions': 2, 'metro_switch_to_desktop': 2, 
            'protected_media_identifier': 2, 'app_banner': 2, 'site_engagement': 2, 
            'durable_storage': 2}}
    options = webdriver.ChromeOptions()    
    options.add_experimental_option("prefs", prefs)
    #options.add_argument('headless') ##remove this to visualize the automation
    driver = webdriver.Chrome('chromedriver.exe',options=options) # Using Chrome to access
    return driver

path='Music/'
files = os.listdir(path)    
audioforms = ['.mp3'] #.mp3 supported
options = ['n','y']

if __name__ == '__main__':
    # options
    flag1 = input('Find album arts? (n/Y) ').lower()
    while flag1 not in options:
        flag1 = input('Find album arts? (n/Y) ').lower()
    
    flag2 = input('Find music lyrics? (N/y) ').lower()
    while flag2 not in options:
        flag2 = input('Find music lyrics? (N/y) ').lower()

    flag3 = input('Rename album names? (N/y) ').lower()
    while flag3 not in options:
        flag3 = input('Rename album names? (N/y) ').lower()
        
    driver = setDriver()
    print('Total files:',len(files)-1)
    
    if flag1=='y':
        getAllArts(driver,files,audioforms) #getAllArts called
        setArtRunner(path,files,audioforms) #setArtRunner called
        pass
    
    if flag2=='y':
        getAllLyrics(driver,files,audioforms) #getAllLyrics called
        setLyricsRunner(path,files,audioforms) #setLyricsRunner called
    driver.quit()

    if flag3=='y':
        setAlbum(path,files,audioforms) #setAlbum called
        pass
