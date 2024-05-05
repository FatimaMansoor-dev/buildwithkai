import google.generativeai as genai
import pyttsx3 
import speech_recognition
import requests
import sys
import datetime
import json
import dataset

api_key = 'AIzaSyBUFwHsf_r3u1tLVuBk2z6vxiCG4XkMJcM'
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-pro')


def calculate_estimated_budget(src):
    '''
        the function gets estimated budget for the trip, so the traveller gets
         idea of minimum amount to spend.
    '''

    # Define the prompt 
    prompt = f'''
        provide a single estimated amount in $ to travel from {src} to pakistan in 2024, make it precise
        respond in format : the estimated budget for your trip is : $
        '''

    # Generate estimated budget using the GenerativeModel
    response = genai.generate_text(prompt=prompt)
    
    # Extract and return the generated budget
    budget_details = response.result.strip().split("\n")
    budget = budget_details[0].split(".")[0]
    return budget


def generate_travel_plan(budget, days, src, interest, time):
    '''
        the function return entire travel plan including the places of their interests
    '''
    # Define the prompt for generating travel plans
    prompt = f'''
        You are a travel agent. Generate travel plan for a trip to Pakistan from {src} for {days} days within total trip budget of {budget}.
      Recommend places in pakistan with best {interest} locations only.
      Start from {time} and tell hourly plan till 10 pm to visit the specific places of {interest} within pakistan. 
      '''

    # Generate travel plans using the GenerativeModel
    response = genai.generate_text(prompt=prompt)
    
    # Extract and return the generated travel plans
    travel_plans = response.result.strip().split("\n")
    print(travel_plans)
    return travel_plans

def hotel_details(city):
    my_df = dataset.hotel_data()

    prompt = f'''
        Give 3 hotel names and urls both in a single string whose city is equal to {city}
        {my_df[['hotelname','hotelcity','hotelimg','hotelUrl','hotelrating']]}
        '''

    # Generate estimated budget using the GenerativeModel
    response = genai.generate_text(prompt=prompt)
    
    # Extract and return the generated budget
    hotel_info = response.result.strip().split("\n")
    print(hotel_info)
    return hotel_info

