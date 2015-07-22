#-*-coding:utf-8-*-
#-------------------------------------
# Name: 创建蓝本
# Purpose: 
# Author:
# Date:
#-------------------------------------

from flask import Blueprint

main = Blueprint('main', __name__)

from . import views, errors
from ..models import Permission


#把Permission类加入模板上下文
@main.app_context_processor
def inject_permissions():
	return dict(Permission=Permission)