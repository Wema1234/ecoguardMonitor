from os import times
import requests
from django.shortcuts import render, redirect
from django.db.models.expressions import result
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import Transactions
import base64
from datetime import datetime 
import json
from django.core.mail import send_mail
from django.core.paginator import Paginator
from dotenv import load_dotenv

load_dotenv()


class MpesaPassword:
    pass


def generate_access_token():
    pass


def index(request):
    pass

@csrf_exempt
def stk_push(request):
    pass

@csrf_exempt
def callback(request):
    pass

def waiting_page(request,transaction_id):
    pass


def check_status(request, transaction_id):
    pass


def payment_success(request):
    pass

def payment_failed(request):
    pass


def payment_cancelled(request):
    pass


# Create your views here.
