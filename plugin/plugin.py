# -*- coding: utf-8 -*-

##############################################################################
#                         <<< ModernWebif >>>                                  #
#                                                                            #
#                        2011 E2OpenPlugins                                  #
#                                                                            #
#  This file is open source software; you can redistribute it and/or modify  #
#     it under the terms of the GNU General Public License version 2 as      #
#               published by the Free Software Foundation.                   #
#                                                                            #
##############################################################################
#
#
#
# Authors: meo <lupomeo@hotmail.com>, skaman <sandro@skanetwork.com>
# Graphics: .....

from Screens.Screen import Screen
from Plugins.Plugin import PluginDescriptor
from Screens.MessageBox import MessageBox
from Components.ActionMap import ActionMap
from Components.Label import Label
from Components.ConfigList import ConfigListScreen
from Components.config import config, getConfigListEntry, ConfigSubsection, ConfigInteger, ConfigYesNo, ConfigText, ConfigSelection
from enigma import getDesktop
from controllers.models.info import getInfo

from httpserver import HttpdStart, HttpdStop, HttpdRestart

from __init__ import _

config.ModernWebif = ConfigSubsection()
config.ModernWebif.enabled = ConfigYesNo(default=True)
config.ModernWebif.identifier = ConfigYesNo(default=True)
config.ModernWebif.identifier.custom = ConfigYesNo(default=False)
config.ModernWebif.identifier.text = ConfigText(default = "", fixed_size = False)
config.ModernWebif.port = ConfigInteger(default = 80, limits=(1, 65535) )
config.ModernWebif.streamport = ConfigInteger(default = 8001, limits=(1, 65535) )
config.ModernWebif.auth = ConfigYesNo(default=False)
config.ModernWebif.xbmcservices = ConfigYesNo(default=False)
config.ModernWebif.webcache = ConfigSubsection()
# FIXME: anything better than a ConfigText?
config.ModernWebif.webcache.collapsedmenus = ConfigText(default = "remote", fixed_size = False)
config.ModernWebif.webcache.remotegrabscreenshot = ConfigYesNo(default = True)
config.ModernWebif.webcache.zapstream = ConfigYesNo(default = False)
config.ModernWebif.webcache.epg_desc_search = ConfigYesNo(default = False)
# HTTPS
config.ModernWebif.https_enabled = ConfigYesNo(default=False)
config.ModernWebif.https_port = ConfigInteger(default = 443, limits=(1, 65535) )
config.ModernWebif.https_auth = ConfigYesNo(default=True)
config.ModernWebif.https_clientcert = ConfigYesNo(default=False)
config.ModernWebif.parentalenabled = ConfigYesNo(default=False)
# Use service name for stream
config.ModernWebif.service_name_for_stream = ConfigYesNo(default=True)
# authentication for streaming
config.ModernWebif.auth_for_streaming = ConfigYesNo(default=False)
config.ModernWebif.no_root_access = ConfigYesNo(default=False)
# encoding of EPG data
config.ModernWebif.epg_encoding = ConfigSelection(default = 'utf-8', choices = [ 'utf-8',
										'iso-8859-15',
										'iso-8859-1',
										'iso-8859-2',
										'iso-8859-3',
										'iso-8859-4',
										'iso-8859-5',
										'iso-8859-6',
										'iso-8859-7',
										'iso-8859-8',
										'iso-8859-9',
										'iso-8859-10',
										'iso-8859-16'])
imagedistro = getInfo()['imagedistro']

class ModernWebifConfig(Screen, ConfigListScreen):
	skin = """
	<screen position="center,center" size="700,340" title="ModernWebif Configuration">
		<widget name="lab1" position="10,30" halign="center" size="680,60" zPosition="1" font="Regular;24" valign="top" transparent="1" />
		<widget name="config" position="10,100" size="680,180" scrollbarMode="showOnDemand" />
		<ePixmap position="140,290" size="140,40" pixmap="skin_default/buttons/red.png" alphatest="on" />
		<widget name="key_red" position="140,290" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="red" transparent="1" />
		<ePixmap position="420,290" size="140,40" pixmap="skin_default/buttons/green.png" alphatest="on" zPosition="1" />
		<widget name="key_green" position="420,290" zPosition="2" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="green" transparent="1" />
	</screen>"""

	def __init__(self, session):
		self.skin = ModernWebifConfig.skin
		Screen.__init__(self, session)

		self.list = []
		ConfigListScreen.__init__(self, self.list)
		self["key_red"] = Label(_("Cancel"))
		self["key_green"] = Label(_("Save"))
		self["lab1"] = Label(_("ModernWebif url: http://yourip:port"))

		self["actions"] = ActionMap(["WizardActions", "ColorActions"],
		{
			"red": self.keyCancel,
			"back": self.keyCancel,
			"green": self.keySave,

		}, -2)
		self.runSetup()
		self.onLayoutFinish.append(self.setWindowTitle)

	def runSetup(self):
		self.list = []
		self.list.append(getConfigListEntry(_("ModernWebInterface Enabled"), config.ModernWebif.enabled))
		if config.ModernWebif.enabled.value:
			self.list.append(getConfigListEntry(_("Show box name in header"), config.ModernWebif.identifier))
			if config.ModernWebif.identifier.value:
				self.list.append(getConfigListEntry(_("Use custom box name"), config.ModernWebif.identifier.custom))
				if config.ModernWebif.identifier.custom.value:
					self.list.append(getConfigListEntry(_("Custom box name"), config.ModernWebif.identifier.text))
			self.list.append(getConfigListEntry(_("HTTP port"), config.ModernWebif.port))
			self.list.append(getConfigListEntry(_("Enable HTTP Authentication"), config.ModernWebif.auth))
			self.list.append(getConfigListEntry(_("Enable HTTPS"), config.ModernWebif.https_enabled))
			if config.ModernWebif.https_enabled.value:
				self.list.append(getConfigListEntry(_("HTTPS port"), config.ModernWebif.https_port))
				self.list.append(getConfigListEntry(_("Enable HTTPS Authentication"), config.ModernWebif.https_auth))
				self.list.append(getConfigListEntry(_("Require client cert for HTTPS"), config.ModernWebif.https_clientcert))
			if config.ModernWebif.auth.value:
				self.list.append(getConfigListEntry(_("Enable Authentication for streaming"), config.ModernWebif.auth_for_streaming))
				self.list.append(getConfigListEntry(_("Disable access for user root"), config.ModernWebif.no_root_access))
			self.list.append(getConfigListEntry(_("Smart services renaming for XBMC"), config.ModernWebif.xbmcservices))
			self.list.append(getConfigListEntry(_("Enable Parental Control"), config.ModernWebif.parentalenabled))
			self.list.append(getConfigListEntry(_("Add service name to stream information"), config.ModernWebif.service_name_for_stream))
			if imagedistro in ("VTi-Team Image"):
				self.list.append(getConfigListEntry(_("Character encoding for EPG data"), config.ModernWebif.epg_encoding))

		self["config"].list = self.list
		self["config"].l.setList(self.list)

	def setWindowTitle(self):
		self.setTitle(_("ModernWebif Configuration"))

	def keyLeft(self):
		ConfigListScreen.keyLeft(self)
		self.runSetup()

	def keyRight(self):
		ConfigListScreen.keyRight(self)
		self.runSetup()

	def keySave(self):
		for x in self["config"].list:
			x[1].save()

		if not config.ModernWebif.auth.value == True:
			config.ModernWebif.auth_for_streaming.value = False
			config.ModernWebif.auth_for_streaming.save()

		if not config.ModernWebif.https_enabled.value == True:
			config.ModernWebif.https_clientcert.value = False
			config.ModernWebif.https_clientcert.save()

		if config.ModernWebif.enabled.value == True:
			HttpdRestart(global_session)
		else:
			HttpdStop(global_session)
		self.close()

	def keyCancel(self):
		for x in self["config"].list:
			x[1].cancel()
		self.close()

def confplug(session, **kwargs):
		session.open(ModernWebifConfig)

def IfUpIfDown(reason, **kwargs):
	if reason is True:
		HttpdStart(global_session)
	else:
		HttpdStop(global_session)

def startSession(reason, session):
	global global_session
	global_session = session

def main_menu(menuid, **kwargs):
	if menuid == "network":
		return [("ModernWebif", confplug, "ModernWebif", 45)]
	else:
		return []

def Plugins(**kwargs):
	result = [
		PluginDescriptor(where=[PluginDescriptor.WHERE_SESSIONSTART], fnc=startSession),
		PluginDescriptor(where=[PluginDescriptor.WHERE_NETWORKCONFIG_READ], fnc=IfUpIfDown),
		]
	screenwidth = getDesktop(0).size().width()
	if imagedistro in ("openatv"):
		result.append(PluginDescriptor(name="ModernWebif", description=_("ModernWebif Configuration"), where = PluginDescriptor.WHERE_MENU, fnc = main_menu))
	if screenwidth and screenwidth == 1920:
		result.append(PluginDescriptor(name="ModernWebif", description=_("ModernWebif Configuration"), icon="modernwebifhd.png", where=[PluginDescriptor.WHERE_PLUGINMENU], fnc=confplug))
	else:
		result.append(PluginDescriptor(name="ModernWebif", description=_("ModernWebif Configuration"), icon="modernwebif.png", where=[PluginDescriptor.WHERE_PLUGINMENU], fnc=confplug))
	return result
