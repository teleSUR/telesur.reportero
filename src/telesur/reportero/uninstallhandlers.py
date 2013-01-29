# -*- coding: utf-8 -*-

import logging

from Products.CMFCore.utils import getToolByName

from telesur.reportero.config import PROJECTNAME


logger = logging.getLogger(PROJECTNAME)


def delete_control_panel(portal):
    logger.info("About to remove the control panel 'reportero'")
    controlpanel = getToolByName(portal, 'portal_controlpanel')
    controlpanel.unregisterConfiglet('reportero')
    logger.info("Done.")


def uninstallVarious(context):
    if context.readDataFile('telesur.reportero-uninstall.txt') is None:
        return
    
    portal = context.getSite()
    delete_control_panel(portal)
