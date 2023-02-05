from django.contrib import admin
from .models import SecondStock,CustomUser,FirstStock,Scenario,ScenarioSolution,ScenarioUser
# Register your models here.
admin.site.register(SecondStock)
admin.site.register(FirstStock)
admin.site.register(CustomUser)
admin.site.register(Scenario)
admin.site.register(ScenarioSolution)
admin.site.register(ScenarioUser)
