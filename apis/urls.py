
from django.urls import path
from .import views
from django.conf import settings
from django.conf.urls.static import static

# urlpatterns = [
#     path('',views.dataList1.as_view()),
#     path('datalist1/<str:id>',views.dataList1.as_view()),
#     path('marketcomparison',views.marketComparison),
#     path('datalist2/<str:id>',views.dataList2.as_view()),
#     path('datalist2',views.dataList2.as_view()),
#     path('create-checkout-session',views.create_checkout_session,name="create_checkout_session"),
#     path('freetrial/',views.FreeTrial,name="FreeTrial"),
#     path('registerUser',views.registerUser,name="registerUser"),
#     #path('dataDetail/<int:pk>/', views.dataDetail.as_view()),
   
# ]

urlpatterns = [
    path('',views.dataList1.as_view()),
    path('datalist1/<str:id>',views.dataList1.as_view()),
    #path('marketcomparison',views.marketComparison),
    path('datalist2/<str:id>',views.dataList2.as_view()),
    path('datalist2',views.dataList2.as_view()),
    path('create-checkout-session',views.create_checkout_session,name="create_checkout_session"),
    #path('freetrial/',views.FreeTrial,name="FreeTrial"),
    #path('registerUser',views.registerUser,name="registerUser"),
    path('api/registerUser',views.registerUser.as_view(),name="registerUser"),
    path('api/user',views.user.as_view()),
    path('api/user/<str:id>',views.user.as_view()),
    
    path('api/solution',views.solution.as_view()),
    path('api/solution/<str:id>',views.solution.as_view()),
    
    path('api/analyze',views.analyze.as_view()),
    
    path('api/compare',views.compare.as_view()),
    #path('api/user/<str:id>',views.user.as_view()),
    #path('dataDetail/<int:pk>/', views.dataDetail.as_view()),
   
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

'''{
    "stockNames":["GME","AAPL","AMC"],
    "purchaseDates":["19/02/2002","17/12/1980","23/12/2013"],
    "quantitiesPurchased":[15,2,10]
}
{
    "stockNames":["GME","AAPL","AMC"],
    "purchaseDates":["19/02/2020","17/12/2021","12/01/2022"],
    "quantitiesPurchased":[15,2,10]
}
GME
13/02/2002
2002-02-13->14-15-19-2020
2021-12-07->8-9-10-13
AAPl
12/12/1980
1980-12-12->15-16-17-18
2021-12-07->8-9-10-13
AMC
18/12/2013
2013-12-18->19-20-23-24
2021-12-07->8-9-10-13
{
    "stockNames":["ABC","INMD","RDSB","BA"],
    "interval":"d",
    "quantitiesPurchased":15
}'''
