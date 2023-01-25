from rest_framework import serializers
from .models import SecondStock,FirstStock,Scenario,ScenarioSolution
class FirstStockSerializer(serializers.ModelSerializer):
    # user = serializers.CharField(source='user',read_only=True)
   
    class Meta:
        model = FirstStock
        fields = ['user','form_data']

class FirstStockSerializer2(serializers.ModelSerializer):
    # user = serializers.CharField(source='user',read_only=True)
    class Meta:
        model = FirstStock
        fields = ['user','form_data','response_data']
        
class UserSerializer(serializers.ModelSerializer):
    # user = serializers.CharField(source='user',read_only=True)
    class Meta:
        model = Scenario
        fields = ['user','response_data']
        

class SolutionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ScenarioSolution
        fields = ['user', 'trainingdata']
                
class SecondStockSerializer(serializers.ModelSerializer):
    # user = serializers.CharField(source='user',read_only=True)
   
    class Meta:
        model = SecondStock
        fields = ['user','form_data']
class SecondStockSerializer2(serializers.ModelSerializer):
    # user = serializers.CharField(source='user',read_only=True)
    class Meta:
        model = SecondStock
        fields = ['user','form_data','response_data']
