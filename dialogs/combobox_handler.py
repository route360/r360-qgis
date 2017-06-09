# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from ggapi import helpers, logging

class Combobox_handler(object):
    def __init__(self, layer_combobox, layer_label, id_combobox, id_label, layer_list, dlg, bar):
        try:
            self.layer_combobox = layer_combobox
            self.layer_label = layer_label
            self.id_combobox = id_combobox
            self.id_label = id_label
            self.layer_list = layer_list
            self.dlg = dlg
            self.bar = bar
            for layer in layer_list:
                self.layer_combobox.addItem(layer.name())
            self.update_id_box()
            self.layer_combobox.currentIndexChanged.connect(self.update_id_box)
        except:
            self.bar.pushWarning("Warning", u"No point layer.")

    def update_id_box(self):
        self.id_combobox.clear()
        layer = self.get_layer()
        for f in layer.pendingFields():
            self.id_combobox.addItem(f.name())

    def get_layer(self):
        return self.layer_list[self.layer_combobox.currentIndex()]

    def get_id(self):
        return self.id_combobox.currentIndex()

    def check_id_column(self):
        layer = self.get_layer()
        value_set = set()
        for feature in layer.getFeatures():
            attr_list = feature.attributes()
            attr = attr_list[self.get_id()]
            if type(attr) is QPyNullVariant:
                raise Exception(u"The ID column contains NULL values.")
                break
            if attr in value_set:
                raise Exception(u"The ID column contains non unique values.")
                break
            value_set.add(attr)

    def setEnabled(self, bool):
        self.layer_combobox.setEnabled(bool)
        self.layer_label.setEnabled(bool)
        self.id_combobox.setEnabled(bool)
        self.id_label.setEnabled(bool)