#-*-coding:utf-8-*-
#-------------------------------------
# Name: API蓝本
# Purpose: 
# Author:
# Date:
#-------------------------------------

from flask import Blueprint

api = Blueprint('api', __name__)

from . import authentication, posts, users, comments, errors
