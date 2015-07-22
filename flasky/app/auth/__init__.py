#-*-coding:utf-8-*-
#-------------------------------------
# Name: 认证蓝本
# Purpose: 
# Author:
# Date:
#-------------------------------------

from flask import Blueprint

auth = Blueprint('auth',__name__)

from . import views