from django.shortcuts import render, HttpResponse
from django import forms
from django.forms import widgets, formset_factory  # 创建多表验证
from app01 import models
# Create your views here.

class MultiPermissionForm(forms.Form):
	title = forms.CharField(max_length=32, label="权限名称",
							widget=widgets.TextInput(attrs={"class": "form-control"}))
	url = forms.CharField(max_length=32, label="含正则的URL",
							widget=widgets.TextInput(attrs={"class": "form-control"}))
	name = forms.CharField(max_length=32, label="url别名",
							widget=widgets.TextInput(attrs={"class": "form-control"}))
	menu_id = forms.ChoiceField(
		choices=[(None, "-----")],
		label="所属菜单",
		widget=forms.Select(attrs={"class": "form-control"}),
		required=False
	)
	pid_id = forms.ChoiceField(
		choices=[(None, "-----")],
		label="关联的权限",
		widget=forms.Select(attrs={"class": "form-control"}),
		required=False
	)

	def __init__(self, *args, **kwargs):
		"""
		数据继承并为menu_id和pid_id增加内容
		:param args:
		:param kwargs:
		"""
		super(MultiPermissionForm, self).__init__(*args, **kwargs)
		# self.fields["menu_id"].choices-->[(None, "-----"), (xx, xx)……]
		self.fields["menu_id"].choices += models.Menu.objects.values_list("id", "title")
		self.fields["pid_id"].choices += models.Permission.objects.filter(menu_id__isnull=False, pid_id__isnull=True).values_list("id", "title")


class MultiUpdatePermissionForm(forms.Form):
	id = forms.IntegerField(
		widget=forms.HiddenInput()  # 隐藏字段
	)
	title = forms.CharField(max_length=32, label="权限名称",
							widget=widgets.TextInput(attrs={"class": "form-control"}))
	url = forms.CharField(max_length=32, label="含正则的URL",
							widget=widgets.TextInput(attrs={"class": "form-control"}))
	name = forms.CharField(max_length=32, label="url别名",
							widget=widgets.TextInput(attrs={"class": "form-control"}))
	menu_id = forms.ChoiceField(
		choices=[(None, "-----")],
		label="所属菜单",
		widget=forms.Select(attrs={"class": "form-control"}),
		required=False
	)
	pid_id = forms.ChoiceField(
		choices=[(None, "-----")],
		label="关联的权限",
		widget=forms.Select(attrs={"class": "form-control"}),
		required=False
	)

	def __init__(self, *args, **kwargs):
		"""
		数据继承并为menu_id和pid_id增加内容
		:param args:
		:param kwargs:
		"""
		super(MultiUpdatePermissionForm, self).__init__(*args, **kwargs)
		# self.fields["menu_id"].choices-->[(None, "-----"), (xx, xx)……]
		self.fields["menu_id"].choices += models.Menu.objects.values_list("id", "title")
		self.fields["pid_id"].choices += models.Permission.objects.filter(menu_id__isnull=False, pid_id__isnull=True).values_list("id", "title")

def multi_add(request):
	"""
	批量增加数据
	数据添加过程中name字段需要唯一，但在数据校验时无法检测到，需要在内部校验
	添加数据以index索引循环的原因是要具体明确当前的的循环位置，以便添加错误信息
	:param request:
	:return:
	"""
	formset_class = formset_factory(MultiPermissionForm, extra=2)  # 创建类
	if request.method == "GET":
		# form = MultiPermissionForm()  # 创建一个表单
		# 创建多个表单
		formset = formset_class()  # 实例化
		return render(request, "multi_add.html", locals())
	# 对于提交的数据来说，需要创建formset对象
	# errors = [{}, {} ……]
	formset = formset_class(data=request.POST)
	if formset.is_valid():
		flag = True
		# 循环获取每个form，将其添加至数据库中
		formset_clean_list = formset.cleaned_data  # 验证无误后，获取当前提交的数据[{}……]
		for index in range(formset.total_form_count()):
			# models.Permission.objects.create(**form)  # 将获取到的数据添加进数据库中
			if not formset_clean_list[index]:  # 拒绝空值添加进数据库
				continue
			try:
				form_data = formset_clean_list[index]
				form_obj = models.Permission(**form_data)
				# 在数据保存前进行unique校验
				form_obj.validate_unique()  # 检查当前对象在数据库中是否存在唯一的异常
				form_obj.save()
			except Exception as e:
				formset.errors[index].update(e)  # 添加错误信息
				flag = False
		if flag:
			return HttpResponse("数据提交成功")
		return render(request, 'multi_add.html', locals()) # 错误信息返回页面
	return render(request, 'multi_add.html', locals())


def multi_edit(request):
	formset_class = formset_factory(MultiUpdatePermissionForm, extra=0)
	if request.method == "GET":
		# 初始化需要获取具体数据，显示在页面上[{}……]
		formset = formset_class(initial=models.Permission.objects.values())
		return render(request, 'multi_edit.html', locals())
	formset = formset_class(data=request.POST)
	if formset.is_valid():
		flag = True
		formset_clean_list = formset.cleaned_data  # 获取所有的校验后的数据
		for index in range(formset.total_form_count()):
			form = formset_clean_list[index]  # 一条数据
			if not form:
				continue
			# 获取当前数据的id，用于查询出对应的数据
			form_id = form['id']
			# 对unique数据校验
			try:
				'''
				# 方式1：
				form.pop('id')
				form_obj = models.Permission(**form)  数据将要存储的状态，用此数据与数据库中的所有数据校验
				form_obj.validate_unique()
				models.Permission.objects.filter(id=form_id).update(**form)
				# 方式2--》数据取出的状态，当前的数据与数据库中其他数据进行校验
				form_obj = models.Permission.objects.filter(id=form_id).first()
				form_obj.title = form["title"]
				form_obj.name = form["name"]
				form_obj.url = form["url"]
				form_obj.pid_id = form["pid_id"]
				form_obj.menu_id = form["menu_id"]
				form_obj.validate_unique()
				form_obj.save()
				'''
				# 方式3
				form_obj = models.Permission.objects.filter(id=form_id).first()
				for key, value in form.items():
					setattr(form_obj, key, value)
				form_obj.validate_unique()
				form_obj.save()
			# errors -->{'id': ['具有 ID 的 Permission 已存在。']}
			except Exception as e:
				formset.errors[index].update(e)
				flag = False
		if flag:
			return HttpResponse("数据提交成功")
	return render(request, 'multi_edit.html', locals())

