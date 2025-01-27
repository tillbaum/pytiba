"""
Copyright (c) 2020 Tillmann Baumeister
Python scripts for Autodesk Revit

"""
#! python3

from Autodesk.Revit import DB, UI
#from Autodesk.Revit.UI import 
from Autodesk.Revit.DB import FilledRegion, FilledRegionType, Line, CurveLoop, ElementId, FilteredElementCollector, Transaction, XYZ
from Autodesk.Revit.UI import IExternalEventHandler, ExternalEvent

from Autodesk.Revit.Exceptions import * #InvalidOperationException, OperationCanceledException
from Autodesk.Revit import Exceptions
from Autodesk.Revit.UI.Selection import ObjectType

import sys
import System 
from System.Collections.Generic import List 
import traceback
from pyrevit import framework
from pyrevit.forms import WPFWindow 
from pyrevit import framework
from pyrevit.framework import System
from pyrevit.framework import Threading
from pyrevit.framework import Interop
from pyrevit.framework import Input
from pyrevit.framework import wpf, Forms, Controls, Media
from pyrevit.framework import CPDialogs
from pyrevit.framework import ComponentModel
from pyrevit import forms

import os.path as op

uidoc = __revit__.ActiveUIDocument 
doc = __revit__.ActiveUIDocument.Document # doc = DocumentManager.Instance.CurrentDBDocument 
uiapp = __revit__ # is the same as uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application 


__doc__ = "ViewFilter Dialog: \nModeless Dialog showing all Filters added to View"
__title__ = "ViewFilter\nPalette"
__author__ = "Tillmann Baumeister"
__persistentengine__ = True


def setViewFilter(): 
    try:
        
        t = Transaction(doc, "Test") 
        t.Start() 
        [doc.ActiveView.SetFilterVisibility(i.item, i.state) for i in response2] 
        t.Commit() 
    except Exceptions.OperationCanceledException: 
        pass
        


# Create a subclass of IExternalEventHandler
class EventHandler(IExternalEventHandler):
    """
    Simple IExternalEventHandler sample
    """

    # __init__ is used to make function from outside of the class to be executed by the handler. \
    # Instructions could be simply written under Execute method only
    def __init__(self, do_this):
        self.do_this = do_this
        #self.type = type
        
    # Execute method run in Revit API environment.
    def Execute(self, uiapp):
        
        try:
            #print "running Execute method of SimpleEventHandler"
            self.do_this()
        except InvalidOperationException:
            # If you don't catch this exeption Revit may crash.
            print "InvalidOperationException catched"
            
    def GetName(self):
        return "simple function executed by an IExternalEventHandler in a Form"


# ha = { "handler" + str(i) : "EventHandler(createobj, typelist[" + str(i) + "][1])" for i in range(len(typelist))}
# for i, j in ha.items():
    # exec( "{} = {}".format(i, j)) #execute 

#response2 = "SomeText"

#handler0 = EventHandler(setViewFilter, response2)

handler1 = EventHandler(setViewFilter) 


ext_event_button_select = ExternalEvent.Create(handler1)  



DEFAULT_CMDSWITCHWND_WIDTH = 600
DEFAULT_SEARCHWND_WIDTH = 600
DEFAULT_SEARCHWND_HEIGHT = 100
DEFAULT_INPUTWINDOW_WIDTH = 300
DEFAULT_INPUTWINDOW_HEIGHT = 600
DEFAULT_RECOGNIZE_ACCESS_KEY = False

WPF_HIDDEN = framework.Windows.Visibility.Hidden
WPF_COLLAPSED = framework.Windows.Visibility.Collapsed
WPF_VISIBLE = framework.Windows.Visibility.Visible


XAML_FILES_DIR = op.dirname(__file__)




class TemplateUserInputWindowModeless(WPFWindow):
    """Base class for pyRevit user input standard forms.

    Args:
        context (any): window context element(s)
        title (str): window title
        width (int): window width
        height (int): window height
        **kwargs: other arguments to be passed to :func:`_setup`
    """
    response2 = "SomeText"
    xaml_source = 'BaseWindow.xaml'

    def __init__(self, context, title, width, height, **kwargs):
        """Initialize user input window."""
        WPFWindow.__init__(self,
                           op.join(XAML_FILES_DIR, self.xaml_source),
                           handle_esc=True)
        self.Title = title or 'pyRevit' 
        self.Width = width 
        self.Height = height 

        self._context = context
        self.response = None

        # parent window?
        owner = kwargs.get('owner', None) 
        if owner: 
            # set wpf windows directly 
            self.Owner = owner 
            self.WindowStartupLocation = framework.Windows.WindowStartupLocation.CenterOwner 

        self._setup(**kwargs)

    def _setup(self, **kwargs):
        """Private method to be overriden by subclasses for window setup."""
        pass

    @classmethod
    def show(cls, context,          #pylint: disable=W0221
             title='View Filter',
             width=DEFAULT_INPUTWINDOW_WIDTH,
             height=DEFAULT_INPUTWINDOW_HEIGHT, **kwargs):

        """Show user input window.

        Args:
            context (any): window context element(s)
            title (str): window title
            width (int): window width
            height (int): window height
            **kwargs (any): other arguments to be passed to window
        """
        dlg = cls(context, title, width, height, **kwargs)
        dlg.Show()
        return dlg.response 




class SelectFromList(TemplateUserInputWindowModeless):
    """Standard form to select from a list of items.

    Any object can be passed in a list to the ``context`` argument. This class
    wraps the objects passed to context, in :obj:`TemplateListItem`.
    This class provides the necessary mechanism to make this form work both
    for selecting items from a list, and from a list of checkboxes. See the
    list of arguments below for additional options and features.

    Args: 
        context (list[str] or dict[list[str]]):
            list of items to be selected from
            OR
            dict of list of items to be selected from.
            use dict when input items need to be grouped
            e.g. List of sheets grouped by sheet set.
        title (str, optional): window title. see super class for defaults.
        width (int, optional): window width. see super class for defaults.
        height (int, optional): window height. see super class for defaults.
        button_name (str, optional):
            name of select button. defaults to 'Select'
        name_attr (str, optional):
            object attribute that should be read as item name.
        multiselect (bool, optional):
            allow multi-selection (uses check boxes). defaults to False
        return_all (bool, optional):
            return all items. This is handly when some input items have states
            and the script needs to check the state changes on all items.
            This options works in multiselect mode only. defaults to False
        filterfunc (function):
            filter function to be applied to context items.
        group_selector_title (str):
            title for list group selector. defaults to 'List Group'
        default_group (str): name of defautl group to be selected



    Example:
        >>> from pyrevit import forms
        >>> items = ['item1', 'item2', 'item3']
        >>> forms.SelectFromList.show(items, button_name='Select Item')
        >>> ['item1']

        >>> from pyrevit import forms
        >>> ops = [viewsheet1, viewsheet2, viewsheet3]
        >>> res = forms.SelectFromList.show(ops,
        ...                                 multiselect=False,
        ...                                 name_attr='Name',
        ...                                 button_name='Select Sheet')


        >>> from pyrevit import forms
        >>> ops = {'Sheet Set A': [viewsheet1, viewsheet2, viewsheet3],
        ...        'Sheet Set B': [viewsheet4, viewsheet5, viewsheet6]}
        >>> res = forms.SelectFromList.show(ops,
        ...                                 multiselect=True,
        ...                                 name_attr='Name',
        ...                                 group_selector_title='Sheet Sets',
        ...                                 button_name='Select Sheets')


        This module also provides a wrapper base class :obj:`TemplateListItem`
        for when the checkbox option is wrapping another element,
        e.g. a Revit ViewSheet. Derive from this base class and define the
        name property to customize how the checkbox is named on the dialog.

        >>> from pyrevit import forms
        >>> class MyOption(forms.TemplateListItem):
        ...    @property
        ...    def name(self):
        ...        return '{} - {}{}'.format(self.item.SheetNumber,
        ...                                  self.item.SheetNumber)

        >>> ops = [MyOption('op1'), MyOption('op2', True), MyOption('op3')] 
        >>> res = forms.SelectFromList.show(ops, 
        ...                                 multiselect=True, 
        ...                                 button_name='Select Item') 
        >>> [bool(x) for x in res]  # or [x.state for x in res] 
        [True, False, True] 
    """
    
    xaml_source = 'SelectFromList2.xaml' 

    @property
    def use_regex(self):
        return self.regexToggle_b.IsChecked 

    def _setup(self, **kwargs):
        # custom button name?
        button_name = kwargs.get('button_name', 'Select')
        if button_name:
            self.select_b.Content = button_name

        # attribute to use as name?
        self._nameattr = kwargs.get('name_attr', None)

        # multiselect?
        if kwargs.get('multiselect', False):
            self.multiselect = True
            self.list_lb.SelectionMode = Controls.SelectionMode.Extended
            self.show_element(self.checkboxbuttons_g) 
        else:
            self.multiselect = False 
            self.list_lb.SelectionMode = Controls.SelectionMode.Single 
            self.hide_element(self.checkboxbuttons_g) 

        # return checked items only?
        self.return_all = kwargs.get('return_all', False) 

        # filter function?
        self.filter_func = kwargs.get('filterfunc', None)

        # context group title?
        self.ctx_groups_title = \
            kwargs.get('group_selector_title', 'List Group')
        self.ctx_groups_title_tb.Text = self.ctx_groups_title

        self.ctx_groups_active = kwargs.get('default_group', None) 

        # check for custom templates
        items_panel_template = kwargs.get('items_panel_template', None) 
        if items_panel_template: 
            self.Resources["ItemsPanelTemplate"] = items_panel_template 

        item_container_template = kwargs.get('item_container_template', None) 
        if item_container_template: 
            self.Resources["ItemContainerTemplate"] = item_container_template 

        item_template = kwargs.get('item_template', None) 
        if item_template: 
            self.Resources["ItemTemplate"] = \
                item_template  

        # nicely wrap and prepare context for presentation, then present
        self._prepare_context()  

        # list options now 
        self._list_options()  

        # setup search and filter fields 
        self.hide_element(self.clrsearch_b)  
        self.clear_search(None, None)   
        
    def _prepare_context_items(self, ctx_items): 
        new_ctx = []
        # filter context if necessary
        if self.filter_func:
            ctx_items = filter(self.filter_func, ctx_items)

        for item in ctx_items:
            if TemplateListItem.is_checkbox(item):
                item.checkable = self.multiselect
                new_ctx.append(item)
            else:
                new_ctx.append(
                    TemplateListItem(item,
                                     checkable=self.multiselect,
                                     name_attr=self._nameattr)
                                )
        return new_ctx


    def _prepare_context(self):
        if isinstance(self._context, dict) and self._context.keys():
            self._update_ctx_groups(sorted(self._context.keys()))
            new_ctx = {}
            for ctx_grp, ctx_items in self._context.items():
                new_ctx[ctx_grp] = self._prepare_context_items(ctx_items)
        else:
            new_ctx = self._prepare_context_items(self._context)

        self._context = new_ctx


    def _update_ctx_groups(self, ctx_group_names):
        self.show_element(self.ctx_groups_dock)
        self.ctx_groups_selector_cb.ItemsSource = ctx_group_names
        if self.ctx_groups_active in ctx_group_names:
            self.ctx_groups_selector_cb.SelectedIndex = \
                ctx_group_names.index(self.ctx_groups_active)
        else:
            self.ctx_groups_selector_cb.SelectedIndex = 0   


    def _get_active_ctx_group(self):
        return self.ctx_groups_selector_cb.SelectedItem

    def _get_active_ctx(self): #get_active_context
        if isinstance(self._context, dict):
            return self._context[self._get_active_ctx_group()]
        else:
            return self._context

    def _list_options(self, option_filter=None): 
        if option_filter:
            self.checkall_b.Content = 'Check'
            self.uncheckall_b.Content = 'Uncheck'
            self.toggleall_b.Content = 'UPDATE'
            # get a match score for every item and sort high to low
            fuzzy_matches = sorted(
                [(x, coreutils.fuzzy_search_ratio(
                      target_string=x.name,
                      sfilter=option_filter,
                      regex=self.use_regex))
                 for x in self._get_active_ctx()],
                key=lambda x: x[1], reverse=True)

            # filter out any match with score less than 80
            self.list_lb.ItemsSource = \
                [x[0] for x in fuzzy_matches if x[1] >= 80]
        else:
            self.checkall_b.Content = 'Check All'
            self.uncheckall_b.Content = 'Uncheck All'
            self.toggleall_b.Content = 'UPDATE'
            self.list_lb.ItemsSource = [x for x in self._get_active_ctx()]


    @staticmethod
    def _unwrap_options(options):
        unwrapped = []
        for optn in options:
            if isinstance(optn, TemplateListItem):
                unwrapped.append(optn.unwrap())
            else:
                unwrapped.append(optn)
        return unwrapped 

    def _get_options(self):
        if self.multiselect:
            if self.return_all:
                return [x for x in self._get_active_ctx()]
            else:
                return self._unwrap_options(
                    [x for x in self._get_active_ctx()
                     if x.state or x in self.list_lb.SelectedItems])
        else:
            return self._unwrap_options([self.list_lb.SelectedItem])[0]


    def _set_states(self, state=True, flip=False, selected=False): 
        all_items = self.list_lb.ItemsSource 
        if selected: 
            current_list = self.list_lb.SelectedItems 
        else: 
            current_list = self.list_lb.ItemsSource 
        for checkbox in current_list: 
            if flip: 
                checkbox.state = not checkbox.state 
            else: 
                checkbox.state = state

        # push list view to redraw 
        self.list_lb.ItemsSource = None 
        self.list_lb.ItemsSource = all_items 
        global  response2
        response2 = self._get_options() 
       
        # forms.alert(str(response2), ok=True) 
        ext_event_button_select.Raise() 


    def updateview(self, sender, args):    #pylint: disable=W0613
        """Handle toggle all button to toggle state of all check boxes."""
        self._context =  sorted([option(x) for x in doc.ActiveView.GetFilters()], key= lambda x: x.name) 
        self.list_lb.ItemsSource = [x for x in self._get_active_ctx()]

    def check_all(self, sender, args):    #pylint: disable=W0613
        """Handle check all button to mark all check boxes as checked."""
        self._set_states(state=True)

    def uncheck_all(self, sender, args):    #pylint: disable=W0613
        """Handle uncheck all button to mark all check boxes as un-checked."""
        self._set_states(state=False) 

    def check_selected(self, sender, args):    #pylint: disable=W0613
        """Mark selected checkboxes as checked."""
        self._set_states(state=True, selected=True) 

    def uncheck_selected(self, sender, args):    #pylint: disable=W0613
        """Mark selected checkboxes as unchecked."""
        self._set_states(state=False, selected=True) 

    def button_select(self, sender, args):    #pylint: disable=W0613
        """Handle select button click."""
        # self.response = self._get_options()   
        global  response2
        response2 = self._get_options() 
       
        # forms.alert(str(response2), ok=True) 
        ext_event_button_select.Raise() 
        
        #self.Close() 

    # def search_txt_changed(self, sender, args):    #pylint: disable=W0613
        # """Handle text change in search box."""
        # if self.search_tb.Text == '':
            # self.hide_element(self.clrsearch_b)
        # else:
            # self.show_element(self.clrsearch_b)

        # self._list_options(option_filter=self.search_tb.Text)

    # def toggle_regex(self, sender, args):
        # self.regexToggle_b.Content = \
            # self.Resources['regexIcon'] if self.use_regex \
                # else self.Resources['filterIcon']
        # self.search_txt_changed(sender, args)
        # self.search_tb.Focus()

    def clear_search(self, sender, args):    #pylint: disable=W0613
        """Clear search box."""
        self.search_tb.Text = ' '
        self.search_tb.Clear() 
        self.search_tb.Focus() 
    


from pyrevit.forms import TemplateListItem    


class option(TemplateListItem): 
    """Sheet wrapper for :func:`select_sheets`.""" 
    def __init__(self, textnotetype): 
        super(option, self).__init__(textnotetype) 
        self.state = True if doc.ActiveView.GetFilterVisibility(self.item) else False

    
    @property
    def name(self):
        """Sheet name.""" 
        return '{:<40s} '.format(doc.GetElement(self.item).Name)
    


test= [(i, doc.GetElement(i).Name, doc.ActiveView.GetFilterVisibility(i)) for i in doc.ActiveView.GetFilters()] 
filter_dict = {doc.GetElement(i).Name: i for i in doc.ActiveView.GetFilters()} 


filter = doc.ActiveView.GetFilters() 

ops = [option(x) for x in filter] 


res = SelectFromList.show(sorted([option(x) for x in doc.ActiveView.GetFilters()], key= lambda x: x.name), 
                               multiselect=True,  
                               return_all = True, 
                               group_selector_title='Filter of View',
                               button_name='Set ViewFilter') 


# print res
# print response2
# for i in res: 
    # print i.state 
    # print i.name 

# handler0 = EventHandler(setViewFilter)


# ext_event_button_select = ExternalEvent.Create(handler0)
   


