#Importing Libraries & Packages
import pandas as pd
from django.http import HttpResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny

#Import the Diabetes Dataset
from sklearn.datasets import load_diabetes
import subprocess
import json

global edb_sub_prs
edb_sub_prs = None

# Create your views here.

@api_view(['GET'])
@permission_classes([AllowAny])
def show_dashboard(request):

    df = pd.read_csv('acmec_admin_master1.csv')
    target = 'is_member'
    p_type = 'classification'

    global edb_sub_prs
    if edb_sub_prs is not None:
        edb_sub_prs.terminate()
    edb_sub_prs = edb_sub_process(df, target, p_type)

    return HttpResponse('dashboard started')

def edb_sub_process(df, target, p_type):
    edb = subprocess.Popen(['python', 'dashboard.py', json.dumps(df.to_dict()), target, p_type])
    return edb

def stop_dashboard(request):
    if edb_sub_prs is not None:
        edb_sub_prs.terminate()
        return HttpResponse('dashboard stoped')
    else:
        return HttpResponse('no subprocess to stop')