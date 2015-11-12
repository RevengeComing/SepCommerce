from ..admin import mod as adminPanel
from project.apps.main.decorators import admin_required
from .models import ProductCategory
from . import mod

@adminPanel.route('/categories')
@admin_required
def categories():
	categories = ProductCategory.query.order_by(ProductCategory.id)
	return render_template('admin/categories.html', categories=categories)