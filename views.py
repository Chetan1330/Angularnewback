from operator import index
from statistics import mode
from requests.api import request
import yfinance as yf
from datetime import datetime
from datetime import datetime as dt
from dateutil.relativedelta import relativedelta
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers, status
from django.shortcuts import render
import pandas as pd
from pandas.tseries.offsets import BDay
from datetime import date,timedelta
import seaborn as sn
import matplotlib.pyplot as plt
import numpy as np
#from scipy import stats
import math
from django.http import JsonResponse
import json
from .models import CustomUser, SecondStock,FirstStock,Scenario,ScenarioUser,ScenarioSolution
from .serilizers import SecondStockSerializer, SecondStockSerializer2,FirstStockSerializer,FirstStockSerializer2,UserSerializer,SolutionSerializer
#import stripe
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from  rest_framework import status
from rest_framework.decorators import api_view

@api_view(['POST'])
def registerUser(request):
    data = request.data

    print(data, 'data')

    try:
        user, created = CustomUser.objects.get_or_create(
            user_id=data['id'],
            first_name=data['name'],
            username=data['name'],
            email=data['email'],
            picture=data['picture']
        )
        return Response("Successfully add!")
    except:
        message = {'detail': 'User with this email already exists'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
# This is your test secret API key.

@csrf_exempt
def create_checkout_session(request):
    if request.method=="POST":
        try:
            checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                    'price': 'price_1K6T4QAycbtKpV299EI4d61w',
                    'quantity': 3,
                },
            ],
            mode='payment',
            success_url=YOUR_DOMAIN + '?success=true',
            cancel_url=YOUR_DOMAIN + '?canceled=true',
        )
       
        except Exception as e:
            print("eeeeee",e)
            return JsonResponse(e)
        return redirect(checkout_session.url, code=303)

#request.tutorial.title
class user(APIView):
    def get(self,request,id):
        uploaddic = {}

        ScenarioName=[]
        ModelLinks=[]
        LinktoDataset=[]
        Description=[]

        userexist = ScenarioUser.objects.filter(user_id=id)
        if userexist:
            # serializer=UserSerializer(data=request.data)
            # print("Serializer:",serializer)
            # if serializer.is_valid():
            #     serializer.save(response_data=uploaddic)
            #     # serializer.save(response_data={"PreviousInv": perc_Invs, "PercentageAR": perc_returns, "StockNames": stockNames, "PercentARlistT": PercentAR_t, "SP500listt": SP500_t, "W5000listt": W5000_t, "corrlist": corrlist, "dailyreturnportf": list(daily_returns_portf), "fullloc1": list(full.iloc[1]), "fullloc0": list(full.iloc[0]), "full1loc1": list(full1.iloc[1]), "full1loc0": list(full1.iloc[0])})
            #     print("Nice to Add Second!")
            #     # return Response(stockInfoDic)
            #     return Response(uploaddic)
            
            # else:
            #     print('errors:  ',serializer.errors)

            userobj=ScenarioUser.objects.get(user_id=id)
            scenarioobj = userobj.Scenario.all()
            
            # print("Scenarioobj:",scenarioobj['response_data'][''])
            if scenarioobj:
                for i in scenarioobj:
                    print("I is",str(i.response_data['ScenarioName']).split("['")[1].split("']")[0])
                    ScenarioName.append(str(i.response_data['ScenarioName']).split("['")[1].split("']")[0])
                    ModelLinks.append(str(i.response_data['ModelLinks']).split("['")[1].split("']")[0])
                    LinktoDataset.append(str(i.response_data['LinktoDataset']).split("['")[1].split("']")[0])
                    Description.append(str(i.response_data['Description']).split("['")[1].split("']")[0])

            print("ScenarioName",ScenarioName)
            uploaddic['ScenarioName'] = ScenarioName
            uploaddic['ModelLinks'] = ModelLinks
            uploaddic['LinktoDataset'] = LinktoDataset
            uploaddic['Description'] = Description
            # print("User exist",scenarioobj)
            print("uploaddic",uploaddic)
            return Response(uploaddic)
            # return Response("Successfully Get!")
        else:
            print("User not exist.... Created new")
        return Response(uploaddic)
    
    def post(self, request):
        userexist = ScenarioUser.objects.filter(user_id=request.data['Userid'])
        if userexist:
            uploaddic = {}

            ScenarioName=''
            ModelLinks=''
            LinktoDataset=''
            Description=''

            if request.data is not None:
                ScenarioName= request.data['ScenarioName'],
                ModelLinks= request.data['ModelLinks'],
                LinktoDataset= request.data['LinktoDataset'],
                Description= request.data['Description'],
                

            uploaddic['ScenarioName'] = ScenarioName
            uploaddic['ModelLinks'] = ModelLinks
            uploaddic['LinktoDataset'] = LinktoDataset
            uploaddic['Description'] = Description


            user=ScenarioUser.objects.get(user_id=request.data['Userid'])
            request.data['user'] = user.id
            # serializer=FirstStockSerializer(data=request.data)
            serializer=UserSerializer(data=request.data)
            print("Serializer:",serializer)
            if serializer.is_valid():
                serializer.save(response_data=uploaddic)
                # serializer.save(response_data={"PreviousInv": perc_Invs, "PercentageAR": perc_returns, "StockNames": stockNames, "PercentARlistT": PercentAR_t, "SP500listt": SP500_t, "W5000listt": W5000_t, "corrlist": corrlist, "dailyreturnportf": list(daily_returns_portf), "fullloc1": list(full.iloc[1]), "fullloc0": list(full.iloc[0]), "full1loc1": list(full1.iloc[1]), "full1loc0": list(full1.iloc[0])})
                print("Nice to Add Second!")
                # return Response(stockInfoDic)
                return Response(uploaddic)
            
            else:
                print('errors:  ',serializer.errors)
                # return Response(serializer.errors)

            # userobj=CustomUser.objects.get(user_id=request.data['Userid'])
            # scenarioobj = Scenario.objects.create(
            #     user=userobj,
            #     ScenarioName= request.data['ScenarioName'],
            #     ModelLinks= request.data['ModelLinks'],
            #     LinktoDataset= request.data['LinktoDataset'],
            #     Description= request.data['Description'],
            # )
            # print("User exist")
        else:
            # try:
            #     user, created = CustomUser.objects.get_or_create(
            #         user_id=request.data['Userid'],
            #         email=request.data['emailid'],
            #     )
            #     return Response("Successfully add!")
            # except:
            #     message = {'detail': 'User with this email already exists'}
            #     return Response("Unable to create User")
                # return Response(message, status=status.HTTP_400_BAD_REQUEST)
            # CustomUser.objec
            print("User ID:",request.data['Userid'])
            createuser = ScenarioUser.objects.create(user_id=request.data['Userid'])
            createuser.save()

            uploaddic = {}

            ScenarioName=''
            ModelLinks=''
            LinktoDataset=''
            Description=''

            if request.data is not None:
                ScenarioName= request.data['ScenarioName'],
                ModelLinks= request.data['ModelLinks'],
                LinktoDataset= request.data['LinktoDataset'],
                Description= request.data['Description'],
                

            uploaddic['ScenarioName'] = ScenarioName
            uploaddic['ModelLinks'] = ModelLinks
            uploaddic['LinktoDataset'] = LinktoDataset
            uploaddic['Description'] = Description


            # user=ScenarioUser.objects.get(user_id=request.data['Userid']) 
            request.data['user'] = createuser.id
            # serializer=FirstStockSerializer(data=request.data)
            serializer=UserSerializer(data=request.data)
            print("Serializer:",serializer)
            if serializer.is_valid():
                serializer.save(response_data=uploaddic)
                # serializer.save(response_data={"PreviousInv": perc_Invs, "PercentageAR": perc_returns, "StockNames": stockNames, "PercentARlistT": PercentAR_t, "SP500listt": SP500_t, "W5000listt": W5000_t, "corrlist": corrlist, "dailyreturnportf": list(daily_returns_portf), "fullloc1": list(full.iloc[1]), "fullloc0": list(full.iloc[0]), "full1loc1": list(full1.iloc[1]), "full1loc0": list(full1.iloc[0])})
                print("Nice to Add Second!")
                # return Response(stockInfoDic)
                return Response(uploaddic)
            
            else:
                print('errors:  ',serializer.errors)

            print("User not exist.... Created new")
            return Response("Successfully add!")
            
        print("Received Post request:",request.data['Userid']) 
        return Response("Successfully add!")
          


class solution(APIView):
    def get(self,request,id):
        uploaddic = {}

        SolutionName=[]
        ModelLinks=[]
        LinktoDataset=[]
        Description=[]

        userexist = ScenarioUser.objects.filter(user_id=id)
        if userexist:
            userobj=ScenarioUser.objects.get(user_id=id)
            scenarioobj = userobj.scenariosolution.all()
            
            # print("Scenarioobj:",scenarioobj['response_data'][''])
            if scenarioobj:
                for i in scenarioobj:
                    # print("Solution is:",str(i.SolutionName))
                    SolutionName.append(i.SolutionName)
                    # ModelLinks.append(str(i.response_data['ModelLinks']).split("['")[1].split("']")[0])
                    # LinktoDataset.append(str(i.response_data['LinktoDataset']).split("['")[1].split("']")[0])
                    # Description.append(str(i.response_data['Description']).split("['")[1].split("']")[0])

            print("SolutionName",SolutionName)
            uploaddic['SolutionName'] = SolutionName
            # uploaddic['ModelLinks'] = ModelLinks
            # uploaddic['LinktoDataset'] = LinktoDataset
            # uploaddic['Description'] = Description
            # # print("User exist",scenarioobj)
            # print("uploaddic",uploaddic)
            return Response(uploaddic)

            # return Response("Successfully Get!")
        else:
            print("User not exist.... Created new")
            return Response("User not exist.... Created new")
        # return Response(uploaddic)
        # return Response("User not exist.... Created new")
    
    def post(self, request):
        if request.data is not None:
            # trainingdata=request.data['TrainnigDatafile']
            # serializer=SolutionSerializer(data=request.data)
            userexist = ScenarioUser.objects.get(user_id=request.data['Userid'])
            fileupload = ScenarioSolution.objects.create(
                user=userexist,
                ScenarioName=request.data['SelectScenario'],
                SolutionName=request.data['NameSolution'],
                SolutionDescription=request.data['DescriptionSolution'],
                TrainingFile=request.data['TrainingFile'],
                TestFile=request.data['TesdtataFile'],
                FactsheetFile=request.data['FactsheetFile'],
                ModelFile=request.data['ModelFile'],
                Targetcolumn=request.data['Targetcolumn']
            )
            fileupload.save()
            # for i in request.FILES.get['TrainnigDatafile']:
            #     print("File i:",i)
            print("Received request.data request:",request.data)
            # print("Received Post request:",request.data['Userid'])
            # print("Received SelectScenario request:",request.data['SelectScenario'])
            # print("Received TrainnigDatafile request:",request.data['TrainnigDatafile'])
            # print("Type of file:",type(request.data['file']))
        return Response("Successfully add!")

class analyze(APIView):
    def get(self,request,id):
        
        print("User not exist.... Created new")
        # return Response(uploaddic)
    
    def post(self, request):
        print("POST analyze request.data request:",request.data)
        return Response("Successfully add!")


class dataList1(APIView):
    def get(self,request,id):
        stockInfoDic={}
        indexDic={}

        ################# User data ####################
        # stockNames=['GME','AAPL','AMC']
        # indices=['^GSPC','^W5000']
        # quantitiesPurchased=[15, 2, 10]
        # # prchsdDts=['2020-02-19','2021-12-17','2022-01-12','2035-02-21']
        # prchsdDts= []
        ################################################

        stockNames=['AMZN','TSLA','PYPL','BABA']
        indices=['^GSPC','^W5000']
        quantitiesPurchased=[1,2,3,1]
        prchsdDts=[]
        uploadDict = {}
        # print("stocknames before",stockNames)
        user=CustomUser.objects.get(user_id=id)
        print('User Get=====>',user)
        stock_data=FirstStock.objects.filter(user=user).order_by('-id')[:1]
        print("User stock:",stock_data)
        serializer =FirstStockSerializer2(stock_data,many=True)
        # print("Serializer data:",serializer.data)
        # serializer = FirstStockSerializer(stock_data,many=True)

        corrlist = []
        dailyreturnsportf = []
        PreviousInv = []
        PercentageAR = []
        PercentAR_t = []
        SP500listt = []
        W5000listt = []

        TotalInvestment = []
        TotalReturn = []
        
        FullLoc1 = []
        FullLoc0 = []
        Full1Loc1 = []
        Full1Loc0 = []
        if stock_data is not None:
            for i in stock_data:
                # print("response Data:",i.response_data['PreviousInv'])
                stockNames = i.form_data['stockNames']
                # prchsdDts = i.form_data['purchaseDate']
                # print("prchsdDts:",i.form_data['purchaseDate'])
                quantitiesPurchased = i.form_data['quantitiesPurchased']
                for j in  i.form_data['purchaseDate']:
                    prchsdDts.append(dt.strptime(j, "%d/%m/%Y").strftime("%Y-%m-%d"))


                corrlist = i.response_data['corrlist']
                dailyreturnsportf = i.response_data['dailyreturnsportf']
                PreviousInv = i.response_data['PrevInvestments']
                PercentageAR = i.response_data['PercentageAR']

                TotalInvestment = int(i.response_data['TotalInvestment'])
                TotalReturn = int(i.response_data['TotalReturn'])

                PercentAR_t = i.response_data['PercentARlistt']
                SP500listt = i.response_data['SP500listt']
                W5000listt = i.response_data['W5000listt']

                FullLoc1 = i.response_data['FullLoc1']
                FullLoc0 = i.response_data['FullLoc0']
                Full1Loc1 = i.response_data['Full1Loc1']
                Full1Loc0 = i.response_data['Full1Loc0']
                
        # #             # print("Dates:", dt.strptime(j, "%d/%m/%Y").strftime("%Y-%m-%d"))
        # #         # print("Stock Data:",i.form_data['stockNames'])
        # # # print("Serializer Data:",serializer.data)
        print("stocknames after",stockNames)
        uploadDict['stockNames'] = stockNames
        uploadDict['quantitiesPurchased'] = quantitiesPurchased
        uploadDict['prchsdDts'] = prchsdDts
        uploadDict['corrlist'] = corrlist
        uploadDict['dailyreturnsportf'] = dailyreturnsportf
        uploadDict['PreviousInv'] = PreviousInv
        uploadDict['PercentageAR'] = PercentageAR
        uploadDict['PercentAR_t'] = PercentAR_t
        uploadDict['SP500listt'] = SP500listt
        uploadDict['W5000listt'] = W5000listt
        uploadDict['FullLoc1'] = FullLoc1
        uploadDict['FullLoc0'] = FullLoc0
        uploadDict['Full1Loc1'] = Full1Loc1
        uploadDict['Full1Loc0'] = Full1Loc0
        uploadDict['TotalInvestment'] = TotalInvestment
        uploadDict['TotalReturn'] = TotalReturn
        
        
        print("Correlation:",corrlist)
        return Response(uploadDict)

    def post(self, request):
        # serializer = DataSerializer(data=request.data,many=False)
        print('successfull id is:',request.data['user'])
        stockInfoDic = {}
        indexDic={}
        print(request.data)
        uploaddic = {}
        # stockNames=request.data['form_data']['stockNames']
        # quantitiesPurchased=request.data['form_data']["quantitiesPurchased"]
        # prchsdDts= dt.strptime(request.data['form_data']["purchaseDate"], "%d/%m/%Y").strftime("%Y-%m-%d")
        stockNames=[]
        indices=['^GSPC','^W5000']
        quantitiesPurchased=[]
        prchsdDts=[]
        lst = []
        # print("stocknames before",stockNames)
        user=CustomUser.objects.get(user_id=request.data['user'])
        print('User=====>',user)
        stock_data=FirstStock.objects.filter(user=user).order_by('-id')[:1]
        serializer =FirstStockSerializer2(stock_data,many=True)
        # serializer = FirstStockSerializer(stock_data,many=True)
        if request.data is not None:
            for i, j, k in zip(request.data['form_data']['stockNames'], request.data['form_data']['purchaseDate'], request.data['form_data']['quantitiesPurchased']):
                print("DATA:",i, j, k)
                stockNames.append(i)
                prchsdDts.append(dt.strptime(j, "%d/%m/%Y").strftime("%Y-%m-%d"))
                quantitiesPurchased.append(k)
                # stockNames = i.form_data
                # # print("Stock Data:",i.form_data)
                # stockNames = i.form_data['stockNames']
                # # prchsdDts = i.form_data['purchaseDate']
                # # print("prchsdDts:",i.form_data['purchaseDate'])
                # quantitiesPurchased = i.form_data['quantitiesPurchased']
                # for j in  i.form_data['purchaseDate']:
                #     prchsdDts.append(dt.strptime(j, "%d/%m/%Y").strftime("%Y-%m-%d"))
        #             # print("Dates:", dt.strptime(j, "%d/%m/%Y").strftime("%Y-%m-%d"))
        #         # print("Stock Data:",i.form_data['stockNames'])
        # # print("Serializer Data:",serializer.data)
        print("stocknames after",stockNames)
        uploaddic['stockNames'] = stockNames

        print("Quantities:",quantitiesPurchased)
        uploaddic['Quantities'] = quantitiesPurchased

        print("Dates are:",prchsdDts)
        uploaddic['prchsdDts'] = prchsdDts

        if len(stockNames) != len(quantitiesPurchased) or len(stockNames) != len(prchsdDts):
            return "error, incompatible number of variables input!"

        for p in range(len(prchsdDts)):
            if dt.strptime(prchsdDts[p],"%Y-%m-%d").weekday() == 5 or dt.strptime(prchsdDts[p],"%Y-%m-%d").weekday() == 6:
                prchsdDts[p]=(dt.strptime(prchsdDts[p],"%Y-%m-%d")-BDay(1)).strftime("%Y-%m-%d")
            else:
                pass

        ########## last 2 graphs corr_matrix   daily_returns_portf  ################
        Min_date=min(prchsdDts)
        Max_date=dt.today()
                # qnttsPrchsd = list(map(lambda x: int(x), quantitiesPurchased))
        qnttsPrchsd = [int(x) for x in quantitiesPurchased]

        stocksDF = yf.download(tickers = stockNames,start=Min_date,end=Max_date)['Close']
        portf=stocksDF.sum(axis=1)
        daily_returns_portf=portf.pct_change(1)*100
        daily_returns = stocksDF.pct_change(1)
        corr_matrix=daily_returns.corr()

        # print("corr_matrix",corr_matrix)
        corrlist = []
        for i in corr_matrix:
            print("corr_matrix",list(corr_matrix[i]))
            corrlist.append(list(corr_matrix[i]))
        print("corrlist:",corrlist)
        uploaddic['corrlist'] = corrlist
        # print("corr_matrix",list(corr_matrix['AAPL']))
        # print("corr_matrix",list(corr_matrix['AMC']))
        # print("corr_matrix",list(corr_matrix['GME']))

        uploaddic['dailyreturnsportf'] = list(daily_returns_portf)[1:]
        # print("daily_returns_portf",list(daily_returns_portf))
        
        # # Min_date=min(prchsdDts)
        # # Max_date=dt.today()
        # #             # qnttsPrchsd = list(map(lambda x: int(x), quantitiesPurchased))
        # # qnttsPrchsd = [int(x) for x in quantitiesPurchased]

        # # stocksDF = yf.download(tickers = stockNames,start=Min_date,end=Max_date)['Close']
        # # if stocksDF.empty:
        # #     return "Error! no market data available for today"

        # # daily_returns = stocksDF.pct_change(1)
        

        for SN, PD, QP in zip(stockNames, prchsdDts, quantitiesPurchased):

            Min_date=min(prchsdDts)
            Max_date=dt.today()
                    # qnttsPrchsd = list(map(lambda x: int(x), quantitiesPurchased))
            qnttsPrchsd = [int(x) for x in quantitiesPurchased]

            stocksDF = yf.download(tickers = stockNames,start=Min_date,end=Max_date)['Close']
            
            if stocksDF.empty:
                return "Error! no market data available for today"

            daily_returns = stocksDF[SN].pct_change(1)
            standard_deviation=np.std(daily_returns)*100

            stock = yf.Ticker(SN)
            PD_=dt.strptime(PD,"%Y-%m-%d").strftime("%Y-%m-%d")
            # retrieving stock information for purchaseDate
            df_stock = stock.history(start=PD_,
                end=dt.strptime(PD_,"%Y-%m-%d") + timedelta(days=1))
                    #print(df, PD, type(PD))    

            stockValuePD = df_stock.loc[PD_,"Close"]
                        # print("stockvaluePD",stockValuePD, stockValuePD.corr())
                        # return Response("Hello")

            FSV0 = stockValuePD * QP

            try:               
                present_date = dt.today()-BDay(1)
                #print('Present date: ', present_date)
                stockValueToday = stocksDF[SN].loc[present_date.strftime("%Y-%m-%d")]
                #print('stockvalueToday',stockValueToday)
            
            #except KeyError:
            #    return "errMessage Error! no market data available for today"
            except Exception as ex:
                template = "An exception of type {0} occurred. Arguments:\n{1!r}"
                message = template.format(type(ex).__name__, ex.args)
                return message
                print("Usman")
                
                    # calculating FSV1
            FSV1 = stockValueToday * QP

                    # claculating stock return
            R = FSV1-FSV0

                    # calculation of percentage return
            percentAR = (R/FSV0)*100


            stockInfoDic[SN] = {"FSV0": FSV0, "FSV1": FSV1, "StockName": SN,"PurchaseDate":PD,
                    "PercentAR": percentAR, "R": R,"StandardDev":standard_deviation}
            
            TotalInvestment = 0
            for x in stockInfoDic.values():
                TotalInvestment = TotalInvestment+x["FSV0"]
                x['perc_Inv']=100*x['FSV0']/TotalInvestment

        
            ###########  4th Bar graph  ####################
            TotalInvestment = 0
            TotalReturn=0
            for x in stockInfoDic.values():
                TotalInvestment = TotalInvestment+x["FSV0"]
                TotalReturn = TotalReturn+x["R"]
                # Calculation of percentage return compared to total investment
            for x in stockInfoDic.values():
                PR = (x["FSV0"]/TotalInvestment)*100
                x["prTotalI"] = PR

            for x in stockInfoDic.values():

                indicesDic={}    
                for i in indices:
                    indexDF = yf.download(tickers = indices,start=Min_date,end=Max_date)['Close']
                    index = yf.Ticker(i)

                    df_index = index.history(start=x['PurchaseDate'],end=dt.strptime(x['PurchaseDate'],"%Y-%m-%d") + timedelta(days=1))
                    FSV0_index = df_index.loc[x['PurchaseDate'],"Close"]

                    FSV1_index = indexDF[i].loc[present_date.strftime("%Y-%m-%d")]

                    R_index = FSV1_index-FSV0_index

                    percentAR_index = (R_index/FSV0_index)*100

                    indicesDic[i]=percentAR_index

                x['SP500']=indicesDic['^GSPC']
                x['W5000']=indicesDic['^W5000']

        print("TotalInvestment is:",TotalInvestment)
        uploaddic['TotalInvestment'] = TotalInvestment
        print("TotalReturn is:",TotalReturn)
        uploaddic['TotalReturn'] = TotalReturn
        perc_Invs=[]

        for i in stockInfoDic.keys():
            perc_Invs.append(stockInfoDic[i]['perc_Inv'])

        perc_returns=[]

        for i in stockInfoDic.keys():
            perc_returns.append(stockInfoDic[i]['PercentAR'])

        
        print("PrevInvestments:",perc_Invs)
        uploaddic['PrevInvestments'] = perc_Invs

        print("PercentageAR:",perc_returns)
        uploaddic['PercentageAR'] = perc_returns

        # print("stock Names:", stockNames)
        # uploaddic['perc_returns'] = perc_returns

        x = np.arange(len(stockNames))  # the label locations
        width = 0.25  # the width of the bars
        #fig, ax = plt.subplots()

        PercentAR_list=[]
        SP500_list=[]
        W5000_list=[]

        for i in stockInfoDic.keys():
            PercentAR_list.append(stockInfoDic[i]['PercentAR'])
            SP500_list.append(stockInfoDic[i]['SP500'])
            W5000_list.append(stockInfoDic[i]['W5000'])

        PercentAR_list_t=np.array(PercentAR_list).T
        SP500_list_t=np.array(SP500_list).T
        W5000_list_t=np.array(W5000_list).T

        PercentAR_t = []
        SP500_t = []
        W5000_t = []

        for i in range(len(PercentAR_list_t)):
            PercentAR_t.append(PercentAR_list_t[i])
            SP500_t.append(SP500_list_t[i])
            W5000_t.append(W5000_list_t[i])
        
        print("PercentAR_list_t:",PercentAR_t)
        uploaddic['PercentARlistt'] = PercentAR_t

        print("SP500_list_t:",SP500_t)
        uploaddic['SP500listt'] = SP500_t

        print("W5000_list_t:",W5000_t)
        uploaddic['W5000listt'] = W5000_t

        # uploaddic['PercentAR_list_t'] = PercentAR_list_t

        # uploaddic['SP500_list_t'] = SP500_list_t

        # uploaddic['W5000_list_t'] = W5000_list_t
                ##############  4th bar graph End ########################

        ############# 1st scatter Graph  ###################        
        # perc_returns=[]
        returns_list=[]
        std_list=[]

        for i in stockInfoDic.keys():

            returns_list.append(stockInfoDic[i]['PercentAR'])
            std_list.append(stockInfoDic[i]['StandardDev'])

            full=pd.concat((pd.DataFrame(returns_list).T,pd.DataFrame(std_list).T),axis=0)

        full.columns=stockInfoDic.keys()

        print("Full Loc 1:",full.iloc[1])
        print("Full Loc 0:",full.iloc[0])

        print("Full Loc 1:",list(full.iloc[1]))
        uploaddic['FullLoc1'] = list(full.iloc[1])
        
        print("Full Loc 0:",list(full.iloc[0])) ### For Scatter
        uploaddic['FullLoc0'] = list(full.iloc[0])

        ######################### 1st scatter End ###################################

        ################  Second Scatter Graph  #############################################
        for SN, I, PD, QP in zip(stockNames,indices, prchsdDts, quantitiesPurchased):

            Min_date=min(prchsdDts)
            Max_date=dt.today()
                    # qnttsPrchsd = list(map(lambda x: int(x), quantitiesPurchased))
            qnttsPrchsd = [int(x) for x in quantitiesPurchased]

            stocksDF = yf.download(tickers = stockNames,start=Min_date,end=Max_date)['Close']
            indexDF=yf.download(tickers = indices,start=Min_date,end=Max_date)['Close']

            daily_returns_index = indexDF[I].pct_change(1)
            standard_deviation_index=np.std(daily_returns_index)*100

            portf=stocksDF.sum(axis=1)
            daily_returns_portf=portf.pct_change(1)
            standard_deviation_portf=np.std(daily_returns_portf)*100

            if stocksDF.empty:
                return "Error! no market data available for today"

            stock = yf.Ticker(SN)
            index = yf.Ticker(I)
            PD_=dt.strptime(PD,"%Y-%m-%d").strftime("%Y-%m-%d")
            # retrieving stock information for purchaseDate
            df_stock = stock.history(start=PD_,
                end=dt.strptime(PD_,"%Y-%m-%d") + timedelta(days=1))
                    #print(df, PD, type(PD))    
            df_index = index.history(start=PD_,
                end=dt.strptime(PD_,"%Y-%m-%d") + timedelta(days=1))

            stockValuePD = df_stock.loc[PD_,"Close"]
            indexValuePD = df_index.loc[PD_,"Close"]

            FSV0 = stockValuePD * QP
            FSV0_index = indexValuePD 

            try:               
                present_date = dt.today()-BDay(1)
            #print('Present date: ', present_date)
                stockValueToday = stocksDF[SN].loc[present_date.strftime("%Y-%m-%d")]
            #print('stockvalueToday',stockValueToday)
                indexValueToday = indexDF[I].loc[present_date.strftime("%Y-%m-%d")]

            #except KeyError:
            #    return "errMessage Error! no market data available for today"
            except Exception as ex:
                template = "An exception of type {0} occurred. Arguments:\n{1!r}"
                message = template.format(type(ex).__name__, ex.args)
                return message
                print("Usman")

                    # calculating FSV1
            FSV1 = stockValueToday * QP
            FSV1_index = indexValueToday

                    # claculating stock return
            R = FSV1-FSV0
            R_index = FSV1_index-FSV0_index

                    # calculation of percentage return
            percentAR = (R/FSV0)*100
            percentAR_index = (R_index/FSV0_index)*100


            stockInfoDic[SN] = {"FSV0": FSV0, "FSV1": FSV1, "StockName": SN,"PurchaseDate":PD,
                    "PercentAR": percentAR, "R": R}

            indexDic[I]={"PercentAR":percentAR_index,"StandardDev":standard_deviation_index}


            for x in stockInfoDic.values():

                indicesDic={}    
                for i in indices:
                    indexDF = yf.download(tickers = indices,start=Min_date,end=Max_date)['Close']
                    index = yf.Ticker(i)

                    df_index = index.history(start=x['PurchaseDate'],end=dt.strptime(x['PurchaseDate'],"%Y-%m-%d") + timedelta(days=1))
                    FSV0_index = df_index.loc[x['PurchaseDate'],"Close"]

                    FSV1_index = indexDF[i].loc[present_date.strftime("%Y-%m-%d")]

                    R_index = FSV1_index-FSV0_index

                    percentAR_index = (R_index/FSV0_index)*100

                    indicesDic[i]=percentAR_index

                x['SP500']=indicesDic['^GSPC']
                x['W5000']=indicesDic['^W5000']

##################################################################
        # returns_list=[]
        # std_list=[]

        # for i in stockInfoDic.keys():

        #     returns_list.append(stockInfoDic[i]['PercentAR'])
        #     std_list.append(stockInfoDic[i]['StandardDev'])

        #     full=pd.concat((pd.DataFrame(returns_list).T,pd.DataFrame(std_list).T),axis=0)

        # full.columns=stockInfoDic.keys()
        # print("Full Loc 1:",full.iloc[1])
        # print("Full Loc 0:",full.iloc[0]) ### For Scatter
###################################################################################

        for x in stockInfoDic.values():
            PercentAR_portf=100*(x['FSV1'].sum()-x['FSV0'].sum())/x['FSV0'].sum()

        returns_list=[]
        std_list=[]

        indexDic["SP500"] = indexDic.pop("^GSPC")
        indexDic["W5000"] = indexDic.pop("^W5000")

        for i in indexDic.keys():

            returns_list.append(indexDic[i]['PercentAR'])
            std_list.append(indexDic[i]['StandardDev'])

            full=pd.concat((pd.DataFrame(returns_list).T,pd.DataFrame(std_list).T),axis=0,ignore_index=True)

        full.columns=indexDic.keys()
        portf=pd.DataFrame([PercentAR_portf,standard_deviation_portf]).rename(columns={0:'Portfolio'})
        full1=pd.concat((full,portf),axis=1)
        print("full1.iloc1",full1.iloc[1])
        print("full1.iloc0",full1.iloc[0])


        uploaddic['Full1Loc1'] = list(full1.iloc[1])
        uploaddic['Full1Loc0'] = list(full1.iloc[0])
        # # # # for i in stockInfoDic.keys():

        # # # #     perc_returns.append(stockInfoDic[i]['PercentAR'])
        # # # print("PercentageAR:",returns_list)
        # # # print("stock Names:", stockNames)

        ############################# 2nd Scatter Graph END #########################################
        # print("Full Loc 1:",full.iloc[1])
        # print("Full Loc 0:",full.iloc[0]) ### For Scatter
        # stockInfoDic = {}
        # stockInfoDic['stocknames'] = stockNames   ## For Hbar and Scatter
        # stockInfoDic['Percentage'] = returns_list  ## for Hbar and Scatter

        # ser = FirstStockSerializer(perc_Invs,many=True)       

        user=CustomUser.objects.get(user_id=request.data['user']) 
        request.data['user'] = user.id
        serializer=FirstStockSerializer(data=request.data)
        print("Serializer:",serializer)
        print("UploadDict:",uploaddic)
        if serializer.is_valid():
            serializer.save(response_data=uploaddic)
            # serializer.save(response_data={"PreviousInv": perc_Invs, "PercentageAR": perc_returns, "StockNames": stockNames, "PercentARlistT": PercentAR_t, "SP500listt": SP500_t, "W5000listt": W5000_t, "corrlist": corrlist, "dailyreturnportf": list(daily_returns_portf), "fullloc1": list(full.iloc[1]), "fullloc0": list(full.iloc[0]), "full1loc1": list(full1.iloc[1]), "full1loc0": list(full1.iloc[0])})
            print("Nice to Add Second!")
            # return Response(stockInfoDic)
            return Response(uploaddic)
        
        else:
            print('errors:  ',serializer.errors)
           
        # return Response(stockInfoDic)
        return Response(uploaddic)
    
        
class dataList2(APIView):
    def get(self,request,id):
        user=CustomUser.objects.get(user_id=id)
        stock_data=SecondStock.objects.filter(user=user).order_by('-id')[:1]
        serializer = SecondStockSerializer2(stock_data,many=True)
        
        return Response(serializer.data)

    def post(self, request):
        print('into datalist2 ===============================>')
        # serializer = DataSerializer(data=request.data,many=False)
        # print(request.data)
        # user=request.data["user"]
        # print("user",user)
        #form_data
        stockNames=request.data['form_data']['stockNames']
        quantitiesPurchased=[request.data['form_data']["quantitiesPurchased"]]
        interval=request.data['form_data']["interval"]
        
        if interval.capitalize() == "D":
            interval = "1d"
        elif interval.capitalize() == "M":
            interval = "1mo"
            return Response("M")
        elif interval.capitalize() == "W":
            interval = "1wk"
        else:
            errMessage = "Invalid interval type specified in the request"
            return Response("Invalid")
        myDf = yf.download(tickers=" ".join(stockNames),  start=datetime.date(datetime.now() - relativedelta(months=14)),
                       end=datetime.date(datetime.now(
                       )), group_by="ticker", interval=interval)

        if myDf.empty:
            return Response("Error! no market data available for today")
        
        
        srs = []
        
        for x in stockNames:
            s = myDf[x]["Close"].rename("Close "+x)
            # return Response("success")
            srs.append(s)
            
        ogDf = pd.concat(srs, axis=1)
        
       # return Response('here')
        if interval == "1wk":
            ogDf = ogDf[ogDf.index.dayofweek == 0]
        elif interval == "1mo":
            ogDf = ogDf[ogDf.index.day == 1]

        df = ogDf.rolling(2).apply(myFunc)
        
    
        means = df.mean()
        variances = df.var()
        stds = df.std()*100

        resultDic = {}
        for x in stockNames:
            mean = means["Close {}".format(
            x)]
            variance = variances["Close {}".format(x)]
            std = stds["Close {}".format(x)]
            posRan = mean+(mean*std)
            negRan = mean-(mean*std)

            result = {"Mean": mean, "variances": variance,
                  "stds": std, "posEnd": posRan, "negEnd": negRan}
            
            if math.isnan(result['Mean']):
                result['Mean'] = ''
            if math.isnan(result['variances']):
                result['variances'] = ''
            if math.isnan(result['stds']):
                result['stds'] = ''
            if math.isnan(result['posEnd']):
                result['posEnd'] = ''
            if math.isnan(result['negEnd']):
                result['negEnd'] = ''
            resultDic[x] = result
        
           

        df.dropna(axis=1, how="all", inplace=True)
        ogDf.dropna(axis=1, how="all", inplace=True)
        dropNaDf = ogDf.dropna(axis=1, how="any")
        newDf = pd.DataFrame(index=dropNaDf.index.copy())
        newDf['totalSumLog'] = np.log(dropNaDf.loc[:, :].sum(axis=1))
        newDf = newDf.rolling(2).apply(myFunc2)
        newDf.dropna(inplace=True)
        rng = np.random.default_rng()
        rsame = rng.choice(newDf, size=100000, replace=True)
        VaR = float(np.quantile(rsame, 0.05))
        VarOut = VaR*100
        
        
    # RStar = np.percentile(retVec,100.*p)
        Es = float(np.mean(newDf[newDf <= VaR]))
        esHist = 100*Es

        resultDic['var'] = VaR
        resultDic['var_out'] = VarOut
        resultDic['es'] = Es
        resultDic['es_hist'] = esHist


        stocksV = []
        for SN, QP in zip(stockNames, quantitiesPurchased):
            try:
                stocksV.append(dropNaDf.iloc[-1:]["Close "+SN][0]*QP)
            except KeyError:
                pass
        VaR = np.quantile(rsame, 0.05)
        VarOut = VaR*100
        #RStar = np.percentile(retVec,100.*p)
        Es = np.mean(newDf[newDf <= VaR])
        esHist = 100*Es
        stocksV = []
        for SN, QP in zip(stockNames, quantitiesPurchased):
            try:
                stocksV.append(dropNaDf.iloc[-1:]["Close "+SN][0]*QP)
            except KeyError:
                pass

        portfolio_value = sum(stocksV)
        VaR_value = portfolio_value*(math.e**VaR-1)
        ES_value = portfolio_value*(math.e**esHist["totalSumLog"]-1)
        # RDSB[]
        user=CustomUser.objects.get(user_id=request.data['user']) 
        request.data['user'] = user.id
        serializer=SecondStockSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(response_data=resultDic)
            print("Nice to Add Second!")
        
        else:
            print('errors:  ',serializer.errors)
        
        print(resultDic, 'resultDic')
           
        return Response(resultDic)
     

# @api_view(['GET'])
# def marketComparison(request):
#     print("Market Comparison")
#     myDf = yf.download(tickers="^W5000  ^GSPC",  start=datetime.date(datetime.now() - relativedelta(days=5)),
#                        end=datetime.date(datetime.now(
#                        )), group_by="ticker")
#     print("myDf====>",myDf)
#     myDf = myDf.to_dict('records')
#     newData = []
#     for data in myDf:
#         print(data, 'data')
#         newDict = {}
#         for subData, values in data.items():
#             print(subData, values, 'keys')
#             val = ''
#             for key in subData:
#                 val = val + key + ' '
#             newDict[val] = data[subData]
#             print(subData, val)
#         newData.append(newDict)
#     return Response(newData)

      
def myFunc(x):
    return (x[-1]/x[0])-1
    return Response("success")


def myFunc2(x):
    return x[-1]-x[0]
    return Response("success")
