# -*- coding: utf8 -*-

import xbmc
import xbmcaddon
import xbmcgui
from OnClickHandler import OnClickHandler
from dialogs.DialogBaseInfo import DialogBaseInfo
from BaseClasses import *
from common import *
try:
    import simplejson
except Exception:
    import json as simplejson

ch = OnClickHandler()
C_LIST_NAVIGATION = 9000
C_LEFTLIST_LOCAL_CATEGORIES = 200104
C_LEFTLIST_CLOUD_CATEGORIES = 300102
C_LIST_LOCAL_MOVIE = 200002
C_LIST_CLOUD_MOVIE = 300001
ADDON = xbmcaddon.Addon()
ADDON_ID = ADDON.getAddonInfo('id')
ADDON_PATH = ADDON.getAddonInfo('path').decode("utf-8")
ADDON_DATA_PATH = xbmc.translatePath("special://profile/addon_data/%s" % ADDON_ID).decode("utf-8")


class WindowHome(WindowXML, DialogBaseInfo):

    def __init__(self, *args, **kwargs):
        super(WindowHome, self).__init__(*args, **kwargs)
        self.isLaunched = False
        self.local_filter = ""
        self.cloud_filter = ""
        self.local_filter_pos = 0
        self.cloud_filter_pos = 0

    def onInit(self):
        self.window = xbmcgui.Window(xbmcgui.getCurrentWindowId())
        if not self.isLaunched:
            self.set_local_movie_categories()
            self.set_local_movie_list()
            self.set_cloud_movie_categories()
            self.set_cloud_movie_list()
            self.isLaunched = True

    def onAction(self, action):
        if (action.getId() == 10 or action.getId() == 92):
            self.setFocus(self.getControl(C_LIST_NAVIGATION))
        else:
            super(WindowHome, self).onAction(action)
            ch.serve_action(action, self.getFocusId(), self)

    def onClick(self, control_id):
        super(WindowHome, self).onClick(control_id)
        ch.serve(control_id, self)

    @check_multiclick
    @ch.action("up", str(C_LEFTLIST_LOCAL_CATEGORIES))
    @ch.action("down", str(C_LEFTLIST_LOCAL_CATEGORIES))
    def refresh_local_movie_list(self):
        xbmc.sleep(500)
        filter_container = self.getControl(C_LEFTLIST_LOCAL_CATEGORIES)
        pos = filter_container.getSelectedPosition()
        if self.local_filter_pos != pos:
            self.local_filter_pos = pos
            item = filter_container.getSelectedItem()
            self.local_filter_up_down(item)

    @check_multiclick
    @ch.action("up", str(C_LEFTLIST_CLOUD_CATEGORIES))
    @ch.action("down", str(C_LEFTLIST_CLOUD_CATEGORIES))
    def refresh_cloud_movie_list(self):
        xbmc.sleep(500)
        filter_container = self.getControl(C_LEFTLIST_CLOUD_CATEGORIES)
        pos = filter_container.getSelectedPosition()
        if self.cloud_filter_pos != pos:
            self.cloud_filter_pos = pos
            item = filter_container.getSelectedItem()
            self.cloud_filter_up_down(item)

    def local_filter_up_down(self, item):
        self.local_filter = item.getProperty("value")
        self.set_local_movie_list(self.local_filter)

    def cloud_filter_up_down(self, item):
        self.cloud_filter = item.getProperty("value")
        self.set_cloud_movie_list(self.cloud_filter)

    def set_local_movie_categories(self):
        data = self.get_local_movie_categories()
        itemValues = data['items'][0]['itemValues']
        items = []
        for value in itemValues:
            item = {"label": value['key'],
                    "value": value['val']}
            items.append(item)
        self.set_container(C_LEFTLIST_LOCAL_CATEGORIES, items, True)

    def set_local_movie_list(self, filter=""):
        data = self.get_local_movie_list(self.local_filter)
        videos = data['videos']
        items = []
        for video in videos:
            item = {"label": video['title'],
                    "icon": video['imgurl'],
                    "vid": video['vid']}
            items.append(item)
        self.set_container(C_LIST_LOCAL_MOVIE, items)

    def set_cloud_movie_categories(self):
        data = self.get_cloud_movie_categories()
        itemValues = data['items'][0]['itemValues']
        items = []
        for value in itemValues:
            item = {"label": value['key'],
                    "value": value['val']}
            items.append(item)
        self.set_container(C_LEFTLIST_CLOUD_CATEGORIES, items)

    def set_cloud_movie_list(self, filter=""):
        data = self.get_cloud_movie_list(self.cloud_filter)
        videos = data['videos']
        items = []
        for video in videos:
            item = {"label": video['title'],
                    "icon": video['imgurl'],
                    "vid": video['vid']}
            items.append(item)
        self.set_container(C_LIST_CLOUD_MOVIE, items)

    def get_local_movie_list(self, strFilter):
        if strFilter == "":
            return self.get_local_movie_list_all()
        elif strFilter == "AREA=美国":
            return self.get_local_movie_list_hollywood()
        elif strFilter == "cataid=211280,157":
            return self.get_local_movie_list_cinema()
        elif strFilter == "AREA=大陆,香港,澳门,台湾":
            return self.get_local_movie_list_chinese()
        elif strFilter == "cataid=101,132,133,134":
            return self.get_local_movie_list_love()
        elif strFilter == "cataid=124":
            return self.get_local_movie_list_comedy()
        elif strFilter == "cataid=125,128":
            return self.get_local_movie_list_crime()
        elif strFilter == "cataid=102,103,129,131":
            return self.get_local_movie_list_scream()
        elif strFilter == "cataid=100,127":
            return self.get_local_movie_list_action()
        elif strFilter == "cataid=104,126":
            return self.get_local_movie_list_fiction()
        elif strFilter == "cataid=130":
            return self.get_local_movie_list_animation()
        elif strFilter == "cataid=75281,211334":
            return self.get_local_movie_list_network()

    def get_cloud_movie_list(self, strFilter):
        if strFilter == "":
            return self.get_cloud_movie_list_all()
        elif strFilter == "AREA=美国":
            return self.get_cloud_movie_list_hollywood()
        elif strFilter == "cataid=211280,157":
            return self.get_cloud_movie_list_cinema()
        elif strFilter == "AREA=大陆,香港,澳门,台湾":
            return self.get_cloud_movie_list_chinese()
        elif strFilter == "cataid=101,132,133,134":
            return self.get_cloud_movie_list_love()
        elif strFilter == "cataid=124":
            return self.get_cloud_movie_list_comedy()
        elif strFilter == "cataid=125,128":
            return self.get_cloud_movie_list_crime()
        elif strFilter == "cataid=102,103,129,131":
            return self.get_cloud_movie_list_scream()
        elif strFilter == "cataid=100,127":
            return self.get_cloud_movie_list_action()
        elif strFilter == "cataid=104,126":
            return self.get_cloud_movie_list_fiction()
        elif strFilter == "cataid=130":
            return self.get_cloud_movie_list_animation()
        elif strFilter == "cataid=75281,211334":
            return self.get_cloud_movie_list_network()

    def get_local_movie_categories(self):
        return get_json_file(ADDON_PATH + "/data/movie_categories.json")

    def get_local_movie_list_all(self):
        return get_json_file(ADDON_PATH + "/data/movie_list_all.json")

    def get_local_movie_list_hollywood(self):
        return get_json_file(ADDON_PATH + "/data/movie_list_hollywood.json")

    def get_local_movie_list_cinema(self):
        return get_json_file(ADDON_PATH + "/data/movie_list_cinema.json")

    def get_local_movie_list_chinese(self):
        return get_json_file(ADDON_PATH + "/data/movie_list_chinese.json")

    def get_local_movie_list_love(self):
        return get_json_file(ADDON_PATH + "/data/movie_list_love.json")

    def get_local_movie_list_comedy(self):
        return get_json_file(ADDON_PATH + "/data/movie_list_comedy.json")

    def get_local_movie_list_crime(self):
        return get_json_file(ADDON_PATH + "/data/movie_list_crime.json")

    def get_local_movie_list_scream(self):
        return get_json_file(ADDON_PATH + "/data/movie_list_scream.json")

    def get_local_movie_list_action(self):
        return get_json_file(ADDON_PATH + "/data/movie_list_action.json")

    def get_local_movie_list_animation(self):
        return get_json_file(ADDON_PATH + "/data/movie_list_animation.json")

    def get_local_movie_list_fiction(self):
        return get_json_file(ADDON_PATH + "/data/movie_list_fiction.json")

    def get_local_movie_list_network(self):
        return get_json_file(ADDON_PATH + "/data/movie_list_network.json")

    def get_cloud_movie_categories(self):
        return get_json_file(ADDON_PATH + "/data/movie_categories.json")

    def get_cloud_movie_list_all(self):
        return get_json_file(ADDON_PATH + "/data/movie_list_all.json")

    def get_cloud_movie_list_hollywood(self):
        return get_json_file(ADDON_PATH + "/data/movie_list_hollywood.json")

    def get_cloud_movie_list_cinema(self):
        return get_json_file(ADDON_PATH + "/data/movie_list_cinema.json")

    def get_cloud_movie_list_chinese(self):
        return get_json_file(ADDON_PATH + "/data/movie_list_chinese.json")

    def get_cloud_movie_list_love(self):
        return get_json_file(ADDON_PATH + "/data/movie_list_love.json")

    def get_cloud_movie_list_comedy(self):
        return get_json_file(ADDON_PATH + "/data/movie_list_comedy.json")

    def get_cloud_movie_list_crime(self):
        return get_json_file(ADDON_PATH + "/data/movie_list_crime.json")

    def get_cloud_movie_list_scream(self):
        return get_json_file(ADDON_PATH + "/data/movie_list_scream.json")

    def get_cloud_movie_list_action(self):
        return get_json_file(ADDON_PATH + "/data/movie_list_action.json")

    def get_cloud_movie_list_animation(self):
        return get_json_file(ADDON_PATH + "/data/movie_list_animation.json")

    def get_cloud_movie_list_fiction(self):
        return get_json_file(ADDON_PATH + "/data/movie_list_fiction.json")

    def get_cloud_movie_list_network(self):
        return get_json_file(ADDON_PATH + "/data/movie_list_network.json")
