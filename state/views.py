from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User,Group
import json

from django.db.models import Q
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
from users import views,templates
import requests
from state import models as models


@csrf_exempt
def get_state(request):
	print("Callll")
	if request.method == 'POST':
		state_data=[]
		country_id=request.POST.get('country_id')
		country_id=json.loads(country_id)
		#print("country_idsddddd",country_id)
		state_list=models.State.objects.filter(country_id__in=country_id).values_list('id', 'state_name','country__country_name')
		for i in state_list:
			case2 = {'id': i[0], 'name': i[1]+' - '+i[2]}
			state_data.append(case2)
			state_data=sorted(state_data, key=itemgetter('name'))
		response=JsonResponse({'status':'success','state_data':state_data})
		return response