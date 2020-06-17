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
from class_master import models as models


@csrf_exempt
def get_class(request):
	#print("Callllcvcvvvvvvvvvvvv")
	if request.method == 'POST':
		class_data=[]
		school_id=request.POST.get('school_id')
		#print("school_iddsddddd",school_id)
		school_id=json.loads(school_id)
		
		state_list=models.school_class_mapping.objects.filter(school_id__in=school_id).values_list('id', 'class_id__class_name','school_id__school_name','school_id')
		for i in state_list:
			#case2 = {'id': i[0], 'name': i[1]}
			case2 = {'id': str(i[0])+'_'+str(i[3]), 'name': i[1]+' - '+i[2]}
			#print("case2case2case2",case2)
			class_data.append(case2)
			class_data=sorted(class_data, key=itemgetter('name'))
		response=JsonResponse({'status':'success','class_data':class_data})
		return response
		