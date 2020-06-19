import wx
import config
import os
from logbook import Logger
pyfalog = Logger(__name__)

class PyfaApp(wx.App):
    def OnInit(self):
        """
        Do application initialization work, e.g. define application globals.
        """

        # Name for my application.
        self.appName = "pyfa"

        #------------

        # # Simplified init method.
        # self.DoConfig()
        # self.Init() # InspectionMixin
        # # work around for Python stealing "_".
        # sys.displayhook = _displayHook
        #
        # #------------


        # Return locale folder.
        localeDir = os.path.join(config.pyfaPath, "locale")

        # Set language stuff and update to last used language.
        self.locale = None
        wx.Locale.AddCatalogLookupPathPrefix(localeDir)
        # Set language stuff and update to last used language.
        self.UpdateLanguage(config.language)

        return True

    #-----------------------------------------------------------------------

    def UpdateLanguage(self, lang = "en_US"):
        """
        Update the language to the requested one.

        Make *sure* any existing locale is deleted before the new
        one is created. The old C++ object needs to be deleted
        before the new one is created, and if we just assign a new
        instance to the old Python variable, the old C++ locale will
        not be destroyed soon enough, likely causing a crash.

        :param string `lang`: one of the supported language codes.
        """

        # Language domain.
        langDomain = "lang"

        # Languages you want to support.
        supLang = {
            "en_US": wx.LANGUAGE_ENGLISH,
            "zh_CN": wx.LANGUAGE_CHINESE_SIMPLIFIED,
            "de": wx.LANGUAGE_GERMAN
        }

        # If an unsupported language is requested default to English.
        if lang in supLang:
            selLang = supLang[lang]
        else:
            selLang = wx.LANGUAGE_ENGLISH

        if self.locale:
            assert sys.getrefcount(self.locale) <= 2
            del self.locale

        # Create a locale object for this language.
        pyfalog.debug("Setting language to: " + lang)
        self.locale = wx.Locale(selLang)
        if self.locale.IsOk():
            success = self.locale.AddCatalog(langDomain, selLang)
            if not success:
                print("Langauage catalog not successfully loaded")

        else:
            self.locale = None