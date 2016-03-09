# -*- coding: utf-8 -*-

##############################################################################
#                        2011 E2OpenPlugins                                  #
#                                                                            #
#  This file is open source software; you can redistribute it and/or modify  #
#     it under the terms of the GNU General Public License version 2 as      #
#               published by the Free Software Foundation.                   #
#                                                                            #
##############################################################################

from Components.VolumeControl import VolumeControl

def getVolumeStatus():
	modernwebif_vctrl = VolumeControl.instance
	return {
		"result": True,
		"message": "Status",
		"current": modernwebif_vctrl.volctrl.getVolume(),
		"ismute": modernwebif_vctrl.volctrl.isMuted()
	}

def setVolumeUp():
	modernwebif_vctrl = VolumeControl.instance
	modernwebif_vctrl.volUp()
	ret = getVolumeStatus()
	ret["message"] = "Volume changed"
	return ret
	
def setVolumeDown():
	modernwebif_vctrl = VolumeControl.instance
	modernwebif_vctrl.volDown()
	ret = getVolumeStatus()
	ret["message"] = "Volume changed"
	return ret

def setVolumeMute():
	modernwebif_vctrl = VolumeControl.instance
	modernwebif_vctrl.volMute()
	ret = getVolumeStatus()
	ret["message"] = "Mute toggled"
	return ret

def setVolume(value):
	modernwebif_vctrl = VolumeControl.instance
	modernwebif_vctrl.volumeDialog.show()
	if value < 0:
		value = 0
	if value > 100:
		value = 100
	modernwebif_vctrl.volctrl.setVolume(value, value)
	modernwebif_vctrl.volSave()
	modernwebif_vctrl.volumeDialog.setValue(value)
	modernwebif_vctrl.hideVolTimer.start(3000, True)
	ret = getVolumeStatus()
	ret["message"] = "Volume set to %i" % value
	return ret
