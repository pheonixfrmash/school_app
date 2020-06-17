from django.shortcuts import render
# dappx/views.py
# -*- coding: utf-8 -*-
from django.shortcuts import render

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User,Group
import json


from django.utils.timezone import get_current_timezone
from datetime import datetime
import dateutil.parser
#from django.utils.encoding import smart_str, smart_unicode
import os
from operator import itemgetter
from datetime import timedelta
import io,csv
from pyfcm import FCMNotification
from django.db.models import Sum
from django.db import transaction
from dashboard import views,templates

# Create your views here.

@login_required
@csrf_exempt
def dashboard(request):
    if request.method == 'POST':
        return render(request, 'dashboard.html')
        
    else:
        username=''
        password=''
        
        return render(request, 'dashboard.html', {"username" : username,"password" : password})