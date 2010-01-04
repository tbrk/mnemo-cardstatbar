##############################################################################
#
# cardstatbar.py <timbob@bigpond.com>
#
# Show card statistics in the status bar.
#
# Based on a patch posted to the Mnemosyne development list by Adam Raizen,
# but packaged as a plugin, and with two improvements:
#  * show the easiness value to 2 decimal places.
#  * show all possible choices for `days until next repetition'.
#
# Some options can be added to $HOME/.mnemosyne/config.py:
#   plugin_cardstatbar = {
#	'show_until_next' = False   # disable `days until next repetition'
#   }
#
##############################################################################

from mnemosyne.core import *
from mnemosyne.pyqt_ui.plugin import get_main_widget
from qt import *
import sys

class CardStatBar(Plugin):
    version = "1.0.0"

    def description(self):
	return ("Show card statistics in the status bar. (v" + version + ")")

    def load(self):
	try: self.options = get_config("plugin_cardstatbar")
	except KeyError:
	    self.options = {}
	    set_config("plugin_cardstatbar", {})

	if type(self.options) != type({}):
	    self.options = {}
	
	self.show_until = True
	if self.options.has_key('show_until_next'):
	    self.show_until = self.options['show_until_next']

	self.main_dlg = get_main_widget()
	status_bar = self.main_dlg.statusBar() 

	self.widgets = []
	self.grade     = QLabel("", status_bar)
	self.widgets.append(self.grade)

	self.easiness  = QLabel("", status_bar)
	self.widgets.append(self.easiness)

	self.reps      = QLabel("", status_bar)
	self.widgets.append(self.reps)

	self.lapses    = QLabel("", status_bar)
	self.widgets.append(self.lapses)

	self.sincelast = QLabel("", status_bar)
	self.widgets.append(self.sincelast)

	if self.show_until:
	    self.tillnext  = QLabel("", status_bar)
	    self.widgets.append(self.tillnext)
        
	for w in self.widgets:
	    status_bar.addWidget(w, 0, 0)

	register_function_hook("filter_q", self.set_statbar)

    def unload(self):
	for w in self.widgets:
	    w.parent().removeChild(w)
	    del w

	unregister_function_hook("filter_q", self.set_statbar)

    def forecast(self, item):
	return [process_answer(item, x, True) for x in range(1,6)]

    def set_statbar(self, text, card):
        self.grade.setText(self.main_dlg.trUtf8("Last Grade: ")\
		.append(QString (str(card.grade))))
	self.easiness.setText(self.main_dlg.trUtf8("Easiness: ")\
		.append(QString (str(round(card.easiness, 2)))))
	self.reps.setText(self.main_dlg.trUtf8("Repetitions: ")\
		.append(QString (str(card.acq_reps + card.ret_reps))))
	self.lapses.setText(self.main_dlg.trUtf8("Lapses: ")\
		.append(QString (str(card.lapses))))
	self.sincelast.setText(
		    self.main_dlg.trUtf8("Days since last repetition: ")\
		    .append(QString (str(card.days_since_last_rep()))))
	if self.show_until:
	    self.tillnext.setText(
		    self.main_dlg.trUtf8("Days until next repetition: ")\
		    .append(QString (' / '.join(map(str, self.forecast(card))))))

	return text

p = CardStatBar()
p.load()

