# -*- coding:utf-8 -*-
# @Author : 'LZ'
# @Time : 2019/12/4 21:05

from stark.service.stark_module import site
from web import models
from web.views.check_payment import CheckPaymentHandler
from web.views.class_list import ClassListHandler
from web.views.course import CourseHandler
from web.views.course_record import CourseRecordHandler
from web.views.cousult_record import RecordHandler
from web.views.customer_private import CustomerPrivateHandler
from web.views.customer_public import CustomerPubHandler
from web.views.department import DepartmentHandler
from web.views.payment_record import PaymentRecordHandler
from web.views.school import SchoolHandler
from web.views.score_manage import ScoreHandler
from web.views.student import StudentHandler
from web.views.userinfo import UserInfoHandler

"""
具体的逻辑处理放在views中存放
"""

site.register(models.School, SchoolHandler)  # 校区
site.register(models.Department, DepartmentHandler)  # 部门
site.register(models.UserInfo, UserInfoHandler)  # 员工
site.register(models.Course, CourseHandler)  # 课程
site.register(models.ClassList, ClassListHandler)  # 班级
site.register(models.Customer, CustomerPubHandler, prev="pub")
site.register(models.Customer, CustomerPrivateHandler, prev="private")
site.register(models.ConsultRecord, RecordHandler)
site.register(models.PaymentRecord, PaymentRecordHandler)
site.register(models.PaymentRecord, CheckPaymentHandler, prev="check")
site.register(models.Student, StudentHandler)
site.register(models.ScoreRecord, ScoreHandler)
site.register(models.CourseRecord, CourseRecordHandler)
