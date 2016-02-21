from pyramid.httpexceptions import HTTPFound, HTTPNotFound
from pyramid.view import view_config
# add an import: from class notes
from pyramid.security import authenticated_userid

from .models import (
    DBSession,
    Entry,
    )

from .forms import ( #WTForm from forms.py
    EntryCreateForm,
    EntryEditForm,
)
# new imports: from class notes
from pyramid.security import forget, remember
from .forms import LoginForm
from .models import User

# add two imports:
from jinja2 import Markup
import markdown


@view_config(route_name='home', renderer='templates/list.jinja2')
def index_page(request):
    entries = Entry.all()
#    return {'entries': entries}
    form = None
    if not authenticated_userid(request):
        form = LoginForm()
    return {'entries': entries, 'login_form': form}



@view_config(route_name='detail', renderer='templates/detail.jinja2')
def view(request):
    this_id = request.matchdict.get('id', -1)
    entry = Entry.by_id(this_id)
    if not entry:
        return HTTPNotFound()
    return {'entry': entry}


@view_config(route_name='action', match_param='action=create',
             renderer='templates/edit.jinja2',
             permission='create') # <-- ADD THIS
def create(request):
    entry = Entry()
    form = EntryCreateForm(request.POST)
    if request.method == 'POST' and form.validate():
        form.populate_obj(entry)
        DBSession.add(entry)
        return HTTPFound(location=request.route_url('home'))
    return {'form': form, 'action': request.matchdict.get('action')}


@view_config(route_name='action', match_param='action=edit',
             renderer='templates/edit.jinja2',
             permission='edit') # <-- ADD THIS
def update(request):
    id = int(request.params.get('id', -1))
    entry = Entry.by_id(id)
    if not entry:
        return HTTPNotFound()
    form = EntryEditForm(request.POST, entry)
    if request.method == 'POST' and form.validate():
        form.populate_obj(entry)
        return HTTPFound(location=request.route_url('detail', id=entry.id))
    return {'form': form, 'action': request.matchdict.get('action')}

# and a new view from class notes for user challenge screen
@view_config(route_name='auth', match_param='action=in', renderer='string',
     request_method='POST')
def sign_in(request):
    login_form = None
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
    if login_form and login_form.validate():
        user = User.by_name(login_form.username.data)
        if user and user.verify_password(login_form.password.data):
            headers = remember(request, user.name)
        else:
            headers = forget(request)
    else:
        headers = forget(request)
    return HTTPFound(location=request.route_url('home'), headers=headers)


# and a function from class notes
def render_markdown(content):
    output = Markup(markdown.markdown(content))
    return output