from flask import render_template, flash, redirect, url_for, request
from project.apps.main.decorators import admin_required
from project.apps.auth.models import User, Role
from project.extensions import db
from . import mod

@mod.route('/panel')
@admin_required
def index():
	return render_template('admin/index.html')


@mod.route('/edit_user/<user_id>', methods=[ 'GET', 'POST'])
@admin_required
def edit_user(user_id):
	user = User.query.filter_by(id=user_id).first()
	roles = Role.query.all()
	if request.method == 'POST':
		check_user = User.query.filter_by(username=request.form['username']).first()
		if not check_user or check_user.id == user.id:
			user.username = request.form['username']
		else:
			flash('This UserName Already exists !')
			return render_template('admin/edit_user.html', user=user, roles=roles)

		check_user = User.query.filter_by(username=request.form['email']).first()
		if not check_user or check_user.id == user.id:
			user.email = request.form['email']
		else:
			flash('This Email Adress Already exists !')
			return render_template('admin/edit_user.html', user=user, roles=roles)

		user.role_id = request.form['role_id']
		user.confirmed = True if request.form.getlist('confirmed') else False
		db.session.commit()
		return redirect(url_for('admin.user_list'))
	return render_template('admin/edit_user.html', user=user, roles=roles)


@mod.route('/user_list')
@admin_required
def user_list():
	users = User.query.order_by(User.id)
	return render_template('admin/user_list.html', users=users)



# @mod.route('/user_list/<user_name>/asign_grp', methods=[ 'GET', 'POST'])
# @admin_required
# def asign_grp(user_name):
# 	form = AssignGrpToUser()
# 	if form.validate_on_submit():
# 		grp = Group.query.filter_by(id=form.name.data.id).first()
# 		usr = User.query.filter_by(username=user_name).first()
# 		grp.user.append(usr)
# 		db.session.add(grp)
# 		db.session.commit()
# 		return redirect(url_for('admin.user_list'))
# 	return render_template('admin/asign_grp.html', form=form)


# @mod.route('/group_list')
# @admin_required
# def group_list():
# 	grps = Group.query.order_by(Group.id)
# 	return render_template('admin/group_list.html', grps=grps)


# @mod.route('/group_list/add_new', methods=['GET', 'POST'])
# @admin_required
# def group_add_new():
# 	form = AddNewGroup()
# 	if form.validate_on_submit():
# 		grp = Group(groupname=form.name.data)
# 		db.session.add(grp)
# 		db.session.commit()
# 		flash('Group Added.')
# 		return redirect(url_for('admin.group_list'))
# 	return render_template('admin/add_grp.html', form=form)

