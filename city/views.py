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
from city import models as models


@csrf_exempt
def get_city(request):
	
	if request.method == 'POST':
		city_data=[]
		state_id=request.POST.get('state_id')
		state_id=json.loads(state_id)
		city_list=models.City.objects.filter(state_id__in=state_id).values_list('id', 'city_name','state__state_name')
		for i in city_list:
			case2 = {'id': i[0], 'name': i[1]+' - '+i[2]}
			city_data.append(case2)
			city_data=sorted(city_data, key=itemgetter('name'))
		response=JsonResponse({'status':'success','city_data':city_data})
		return response