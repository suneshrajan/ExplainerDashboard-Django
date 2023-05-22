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
        
    #Import the Diabetes Dataset
    data= load_diabetes()
    
    #create a DataFrame from the dataset
    x=pd.DataFrame(data.data,columns=data.feature_names)
    y=pd.DataFrame(data.target,columns=["target"])

    data = pd.read_csv('acmec_admin_master1.csv')
    df = data.copy()

    x=df.drop(columns=['category_id'])
    y=data[['category_id']]

    global edb_sub_prs
    if edb_sub_prs is not None:
        edb_sub_prs.terminate()
    edb_sub_prs = edb_sub_process(x, y)

    return HttpResponse('dashboard started')

def edb_sub_process(x, y):
    edb = subprocess.Popen(['python', 'dashboard.py', json.dumps(x.to_dict()), json.dumps(y.to_dict())])
    return edb

def stop_dashboard(request):
    if edb_sub_prs is not None:
        edb_sub_prs.terminate()
        return HttpResponse('dashboard stoped')
    else:
        return HttpResponse('no subprocess to stop')