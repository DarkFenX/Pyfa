import csv
import config

# noinspection PyPackageRequirements
import wx
import wx.lib.agw.hypertreelist

from gui.bitmap_loader import BitmapLoader
from gui.utils.numberFormatter import formatAmount, roundDec
from enum import IntEnum
from gui.builtinItemStatsViews.attributeGrouping import *
from service.const import GuiAttrGroup


class AttributeView(IntEnum):
    NORMAL = 1
    RAW = -1


class ItemParams(wx.Panel):
    def __init__(self, parent, stuff, item, context=None):
        wx.Panel.__init__(self, parent)
        mainSizer = wx.BoxSizer(wx.VERTICAL)

        self.paramList = wx.lib.agw.hypertreelist.HyperTreeList(self, wx.ID_ANY, agwStyle=wx.TR_HIDE_ROOT | wx.TR_NO_LINES | wx.TR_FULL_ROW_HIGHLIGHT | wx.TR_HAS_BUTTONS)
        self.paramList.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW))

        mainSizer.Add(self.paramList, 1, wx.ALL | wx.EXPAND, 0)
        self.SetSizer(mainSizer)

        self.toggleView = AttributeView.NORMAL
        self.stuff = stuff
        self.item = item
        self.attrInfo = {}
        self.attrValues = {}
        self._fetchValues()

        self.paramList.AddColumn("Attribute")
        self.paramList.AddColumn("Current Value")
        if self.stuff is not None:
            self.paramList.AddColumn("Base Value")

        self.paramList.SetMainColumn(0)  # the one with the tree in it...
        self.paramList.SetColumnWidth(0, 300)

        self.m_staticline = wx.StaticLine(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL)
        mainSizer.Add(self.m_staticline, 0, wx.EXPAND)
        bSizer = wx.BoxSizer(wx.HORIZONTAL)

        self.toggleViewBtn = wx.ToggleButton(self, wx.ID_ANY, "Veiw Raw Data", wx.DefaultPosition, wx.DefaultSize,
                                             0)
        bSizer.Add(self.toggleViewBtn, 0, wx.ALIGN_CENTER_VERTICAL)

        self.exportStatsBtn = wx.ToggleButton(self, wx.ID_ANY, "Export Item Stats", wx.DefaultPosition, wx.DefaultSize,
                                              0)
        bSizer.Add(self.exportStatsBtn, 0, wx.ALIGN_CENTER_VERTICAL)

        if stuff is not None:
            self.refreshBtn = wx.Button(self, wx.ID_ANY, "Refresh", wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT)
            bSizer.Add(self.refreshBtn, 0, wx.ALIGN_CENTER_VERTICAL)
            self.refreshBtn.Bind(wx.EVT_BUTTON, self.RefreshValues)

        mainSizer.Add(bSizer, 0, wx.ALIGN_RIGHT)

        self.imageList = wx.ImageList(16, 16)

        self.PopulateList()

        self.toggleViewBtn.Bind(wx.EVT_TOGGLEBUTTON, self.ToggleViewMode)
        self.exportStatsBtn.Bind(wx.EVT_TOGGLEBUTTON, self.ExportItemStats)

    def _fetchValues(self):
        if self.stuff is None:
            self.attrInfo.clear()
            self.attrValues.clear()
            self.attrInfo.update(self.item.attributes)
            self.attrValues.update(self.item.attributes)
        elif self.stuff.item == self.item:
            self.attrInfo.clear()
            self.attrValues.clear()
            self.attrInfo.update(self.stuff.item.attributes)
            self.attrValues.update(self.stuff.itemModifiedAttributes)
        elif self.stuff.charge == self.item:
            self.attrInfo.clear()
            self.attrValues.clear()
            self.attrInfo.update(self.stuff.charge.attributes)
            self.attrValues.update(self.stuff.chargeModifiedAttributes)
        # When item for stats window no longer exists, don't change anything
        else:
            return

    def UpdateList(self):
        self.Freeze()
        self.paramList.DeleteRoot()
        self.PopulateList()
        self.Thaw()
        # self.paramList.resizeLastColumn(100)

    def RefreshValues(self, event):
        self._fetchValues()
        self.UpdateList()
        if event:
            event.Skip()

    def ToggleViewMode(self, event):
        self.toggleView *= -1
        self.UpdateList()
        event.Skip()

    def ExportItemStats(self, event):
        exportFileName = self.item.name + " (" + str(self.item.ID) + ").csv"

        saveFileDialog = wx.FileDialog(self, "Save CSV file", "", exportFileName,
                                       "CSV files (*.csv)|*.csv", wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)

        if saveFileDialog.ShowModal() == wx.ID_CANCEL:
            return  # the user hit cancel...

        with open(saveFileDialog.GetPath(), "w") as exportFile:
            writer = csv.writer(exportFile, delimiter=',')

            writer.writerow(
                    [
                        "ID",
                        "Internal Name",
                        "Friendly Name",
                        "Modified Value",
                        "Base Value",
                    ]
            )

            for attribute in self.attrValues:

                try:
                    attribute_id = self.attrInfo[attribute].ID
                except (KeyError, AttributeError):
                    attribute_id = ''

                try:
                    attribute_name = self.attrInfo[attribute].name
                except (KeyError, AttributeError):
                    attribute_name = attribute

                try:
                    attribute_displayname = self.attrInfo[attribute].displayName
                except (KeyError, AttributeError):
                    attribute_displayname = ''

                try:
                    attribute_value = self.attrInfo[attribute].value
                except (KeyError, AttributeError):
                    attribute_value = ''

                try:
                    attribute_modified_value = self.attrValues[attribute].value
                except (KeyError, AttributeError):
                    attribute_modified_value = self.attrValues[attribute]

                writer.writerow(
                        [
                            attribute_id,
                            attribute_name,
                            attribute_displayname,
                            attribute_modified_value,
                            attribute_value,
                        ]
                )

    def SetupImageList(self):
        self.imageList.RemoveAll()

        self.blank_icon = self.imageList.Add(BitmapLoader.getBitmap("transparent16x16", "gui"))
        self.unknown_icon = self.imageList.Add(BitmapLoader.getBitmap("0", "icons"))

        self.paramList.AssignImageList(self.imageList)

    def AddAttribute(self, parent, attr):
        if attr in self.attrValues and attr not in self.processed_attribs:

            data = self.GetData(attr)
            if data is None:
                return

            attrIcon, attrName, currentVal, baseVal = data
            attr_item = self.paramList.AppendItem(parent, attrName)

            self.paramList.SetItemText(attr_item, currentVal, 1)
            if self.stuff is not None:
                self.paramList.SetItemText(attr_item, baseVal, 2)
            self.paramList.SetItemImage(attr_item, attrIcon, which=wx.TreeItemIcon_Normal)
            self.processed_attribs.add(attr)

    def ExpandOrDelete(self, item):
        if self.paramList.GetChildrenCount(item) == 0:
            self.paramList.Delete(item)
        else:
            self.paramList.Expand(item)

    def PopulateList(self):
        # self.paramList.setResizeColumn(0)
        self.SetupImageList()

        self.processed_attribs = set()
        root = self.paramList.AddRoot("The Root Item")
        misc_parent = root

        # We must first deet4ermine if it's categorey already has defined groupings set for it. Otherwise, we default to just using the fitting group
        order = CategoryGroups.get(self.item.category.categoryName, [GuiAttrGroup.FITTING])
        # start building out the tree
        for data in [AttrGroupDict[o] for o in order]:
            heading = data.get("label")

            header_item = self.paramList.AppendItem(root, heading)
            for attr in data.get("attributes", []):
                # Attribute is a "grouped" attr (eg: damage, sensor strengths, etc). Automatically group these into a child item
                if attr in GroupedAttributes:
                    # find which group it's in
                    for grouping in AttrGroups:
                        if attr in grouping[0]:
                            break

                    # create a child item with the groups label
                    item = self.paramList.AppendItem(header_item, grouping[1])
                    for attr2 in grouping[0]:
                        # add each attribute in the group
                        self.AddAttribute(item, attr2)

                    self.ExpandOrDelete(item)
                    continue

                self.AddAttribute(header_item, attr)

            self.ExpandOrDelete(header_item)

        names = list(self.attrValues.keys())
        names.sort()

        # this will take care of any attributes that weren't collected withe the defined grouping (or all attributes if the item ddidn't have anything defined)
        for name in names:
            if name in GroupedAttributes:
                # find which group it's in
                for grouping in AttrGroups:
                    if name in grouping[0]:
                        break

                # get all attributes in group
                item = self.paramList.AppendItem(root, grouping[1])
                for attr2 in grouping[0]:
                    self.AddAttribute(item, attr2)

                self.ExpandOrDelete(item)
                continue

            self.AddAttribute(root, name)

        self.Layout()

    def GetData(self, attr):
        info = self.attrInfo.get(attr)
        att = self.attrValues[attr]

        # If we're working with a stuff object, we should get the original value from our getBaseAttrValue function,
        # which will return the value with respect to the effective base (with mutators / overrides in place)
        valDefault = getattr(info, "value", None)  # Get default value from attribute
        if self.stuff is not None:
            # if it's a stuff, overwrite default (with fallback to current value)
            valDefault = self.stuff.getBaseAttrValue(attr, valDefault)
        valueDefault = valDefault if valDefault is not None else att

        val = getattr(att, "value", None)
        value = val if val is not None else att

        if self.toggleView == AttributeView.NORMAL and ((attr not in GroupedAttributes and not value) or info is None or not info.published or attr in RequiredSkillAttrs):
            return None

        if info and info.displayName and self.toggleView == AttributeView.NORMAL:
            attrName = info.displayName
        else:
            attrName = attr

        if info and config.debug:
            attrName += " ({})".format(info.ID)

        if info:
            if info.iconID is not None:
                iconFile = info.iconID
                icon = BitmapLoader.getBitmap(iconFile, "icons")

                if icon is None:
                    attrIcon = self.blank_icon
                else:
                    attrIcon = self.imageList.Add(icon)
            else:
                attrIcon = self.unknown_icon
        else:
            attrIcon = self.unknown_icon

        # index = self.paramList.AppendItem(root, attrName)
        # idNameMap[idCount] = attrName
        # self.paramList.SetPyData(index, idCount)
        # idCount += 1

        if self.toggleView == AttributeView.RAW:
            valueUnit = str(value)
        elif info and info.unit:
            valueUnit = self.FormatValue(*info.unit.PreformatValue(value))
        else:
            valueUnit = formatAmount(value, 3, 0, 0)

        if self.toggleView == AttributeView.RAW:
            valueUnitDefault = str(valueDefault)
        elif info and info.unit:
            valueUnitDefault = self.FormatValue(*info.unit.PreformatValue(valueDefault))
        else:
            valueUnitDefault = formatAmount(valueDefault, 3, 0, 0)

        #  todo: attribute that point to another item should load that item's icon.
        return (attrIcon, attrName, valueUnit, valueUnitDefault)

        # self.paramList.SetItemText(index, valueUnit, 1)
        # if self.stuff is not None:
        #     self.paramList.SetItemText(index, valueUnitDefault, 2)
        # self.paramList.SetItemImage(index, attrIcon, which=wx.TreeItemIcon_Normal)

    @staticmethod
    def FormatValue(value, unit, rounding='prec', digits=3):
        """Formats a value / unit combination into a string
        @todo: move this to a more central location, since this is also used in the item mutator panel"""
        if isinstance(value, (int, float)) and rounding == 'prec':
            fvalue = formatAmount(value, digits, 0, 0)
        elif isinstance(value, (int, float)) and rounding == 'dec':
            fvalue = roundDec(value, digits)
        else:
            fvalue = value
        return "%s %s" % (fvalue, unit)


if __name__ == "__main__":

    import eos.db
    # need to set up some paths, since bitmap loader requires config to have things
    # Should probably change that so that it's not dependant on config
    import os
    os.chdir('..')
    import config
    config.defPaths(None)
    config.debug = True
    class Frame(wx.Frame):
        def __init__(self, ):
            # item = eos.db.getItem(23773)  # Ragnarok
            item = eos.db.getItem(23061)  # Einherji I
            #item = eos.db.getItem(24483)  # Nidhoggur
            #item = eos.db.getItem(587)    # Rifter
            #item = eos.db.getItem(2486)   # Warrior I
            #item = eos.db.getItem(526)    # Stasis Webifier I
            item = eos.db.getItem(486)  # 200mm AutoCannon I
            #item = eos.db.getItem(200)  # Phased Plasma L
            super().__init__(None, title="Test Attribute Window | {} - {}".format(item.ID, item.name), size=(1000, 500))

            if 'wxMSW' in wx.PlatformInfo:
                color = wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNFACE)
                self.SetBackgroundColour(color)

            main_sizer = wx.BoxSizer(wx.HORIZONTAL)

            panel = ItemParams(self, None, item)

            main_sizer.Add(panel, 1, wx.EXPAND | wx.ALL, 2)

            self.SetSizer(main_sizer)

    app = wx.App(redirect=False)   # Error messages go to popup window
    top = Frame()
    top.Show()
    app.MainLoop()
