import urllib,urllib2, sys, xbmcplugin ,xbmcgui, xbmcaddon, xbmc, os, json, re
import common,xbmcvfs,zipfile,downloader,extract
import GoDev
from datetime import datetime, timedelta
import base64, time

AddonID = 'plugin.video.ottalpha'
Addon = xbmcaddon.Addon(AddonID)
ADDON = xbmcaddon.Addon(id='plugin.video.ottalpha')

Username=xbmcplugin.getSetting(int(sys.argv[1]), 'Username')
Password=xbmcplugin.getSetting(int(sys.argv[1]), 'Password')
ServerURL = "http://otttv.gq:2095/get.php?username=%s&password=%s&type=m3u&output=hls"%(Username,Password,)
AccLink = "http://otttv.gq:2095/panel_api.php?username=%s&password=%s"%(Username,Password,)
addonDir = Addon.getAddonInfo('path').decode("utf-8")
Images=xbmc.translatePath(os.path.join('special://home','addons',AddonID,'resources/'));
addon_data_dir = os.path.join(xbmc.translatePath("special://userdata/addon_data" ).decode("utf-8"), AddonID)
if not os.path.exists(addon_data_dir):
    os.makedirs(addon_data_dir)
def OPEN_URL(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    return link
def Open_URL(AccLink):
        req = urllib2.Request(url)
        #req.add_header('User-Agent' , "Magic Browser")
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:11.0) Gecko/20100101 Firefox/11.0')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        return link		
def MainMenu():
        AddDir('My Account',AccLink,1,Images + 'MyAcc.png')
        AddDir('Live TV','url',2,Images + 'Live TV.png')
        AddDir('Movies (Coming Soon)','Movies',8,Images + 'movies.png')
        AddDir('TVShows (Coming Soon)','Movies',9,Images + 'tvshows.png')
        AddDir('Extras','Extras',5,Images + 'extras.png')
        AddDir('Clear Cache','Clear Cache',7,Images + 'cache.png')
        AddDir('Settings','settings',4,Images + 'settings.png')
def LiveTv(url):
    list = common.m3u2list(ServerURL)
    for channel in list:
        name = common.GetEncodeString(channel["display_name"])
        AddDir(name ,channel["url"], 3, iconimage, isFolder=False)
def MyAccDetails(url):
        link = Open_URL(url)
        match=re.compile('"username":"(.+?)"').findall(link)
        match1=re.compile('"status":"(.+?)"').findall(link)
        match2=re.compile('"exp_date":"(.+?)"').findall(link) 	
        match4=re.compile('"created_at":"(.+?)"').findall(link)
        match6=re.compile('"is_trial":"1"').findall(link)
        for url in match:
                AddAccInfo('My Account Information','','',Images +'MyAcc.png')
                AddAccInfo('Username:  %s'%(url),'','',Images + 'MyAcc.png')
        for url in match1:
                AddAccInfo('Status:  %s'%(url),'','',Images + 'MyAcc.png')
        for url in match4:
                dt = datetime.fromtimestamp(float(match4[0]))
                dt.strftime('%Y-%m-%d %H:%M:%S')
                AddAccInfo('Created:  %s'%(dt),'','',Images +'MyAcc.png')
        for url in match2:
                dt = datetime.fromtimestamp(float(match2[0]))
                dt.strftime('%Y-%m-%d %H:%M:%S')
                AddAccInfo('Expires:  %s'%(dt),'','',Images +'MyAcc.png')
        for url in match6:
                AddAccInfo('Trial: Yes','','',Images +'MyAcc.png')
	     
def PlayUrl(name, url, iconimage=None):
        _NAME_=name
        list = common.m3u2list(ServerURL)
        for channel in list:
            name = common.GetEncodeString(channel["display_name"])
            stream=channel["url"]
            if _NAME_ in name:
                listitem = xbmcgui.ListItem(path=stream, thumbnailImage=iconimage)
                listitem.setInfo(type="Video", infoLabels={ "Title": name })
                xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem)				
def AddAccInfo(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)				
def AddDir(name, url, mode, iconimage, description="", isFolder=True, background=None):
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&description="+urllib.quote_plus(description)
    a=sys.argv[0]+"?url=None&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&description="+urllib.quote_plus(description)
    print name.replace('-[US]','').replace('-[EU]','').replace('[COLOR yellow]','').replace('[/COLOR]','').replace(' (G)','')+'='+a
    liz = xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
    liz.setInfo(type="Video", infoLabels={ "Title": name, "Plot": description})
    liz.setProperty('IsPlayable', 'true')
    xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=isFolder)
def Get_Params():
    param = []
    paramstring = sys.argv[2]
    if len(paramstring) >= 2:
        params = sys.argv[2]
        cleanedparams = params.replace('?','')
        if (params[len(params)-1] == '/'):
            params = params[0:len(params)-2]
        pairsofparams = cleanedparams.split('&')
        param = {}
        for i in range(len(pairsofparams)):
            splitparams = {}
            splitparams = pairsofparams[i].split('=')
            if (len(splitparams)) == 2:
                param[splitparams[0].lower()] = splitparams[1]
    return param
def OpenSettings():
    ADDON.openSettings()
    MainMenu()	
def Clear_Cache():
    choice = xbmcgui.Dialog().yesno('Clear your Cache?', 'If you still cant see your account after ok button is clicked your details are incorrect', nolabel='Cancel',yeslabel='Delete')
    if choice == 1:
        GoDev.Wipe_Cache()


		


params=Get_Params()
url=None
name=None
mode=None
iconimage=None
description=None

try:url = urllib.unquote_plus(params["url"])
except:pass
try:name = urllib.unquote_plus(params["name"])
except:pass
try:iconimage = urllib.unquote_plus(params["iconimage"])
except:pass
try:mode = int(params["mode"])
except:pass
try:description = urllib.unquote_plus(params["description"])
except:pass

if mode == 7:
	Clear_Cache()
elif mode == 8:
	Movies()
elif mode == 9:
	TVShows()
elif mode == 1:
    MyAccDetails(url)
elif mode == 2:
    LiveTv(url)
elif mode == 3:
    PlayUrl(name, url, iconimage)
elif mode == 4:
	OpenSettings()
elif mode == 5:
	ExtraMenu()
elif mode == 6:
	wizard2(name,url,description)
