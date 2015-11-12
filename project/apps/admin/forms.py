from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import Required, Length
from wtforms.ext.sqlalchemy.fields import QuerySelectField
# from project.apps.auth.models import get_groups



class AddNewGroup(Form):
    name = StringField('Name', validators=[Required(), Length(1, 64)])
    submit = SubmitField('Create')


class AddNewGenre(Form):
    name = StringField('Name', validators=[Required(), Length(1, 64)])
    submit = SubmitField('Create')


# class AssignGrpToUser(Form):
# 	name = QuerySelectField(query_factory=get_groups,
#                             get_pk=lambda a: a.id,
#                             get_label=lambda a: a.groupname)
# 	submit = SubmitField('Assign Group')

