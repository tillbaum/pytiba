

import pyrevit
from pyrevit import forms


def warn(): 
    return forms.alert("Script is executed", ok=True)



exec( "warn()")