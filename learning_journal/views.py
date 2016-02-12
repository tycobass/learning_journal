from pyramid.httpexceptions import HTTPFound, HTTPNotFound
from pyramid.view import view_config

from .models import (
    DBSession,
    Entry,
    )

from .forms import EntryCreateForm



@view_config(route_name='home', renderer='templates/list.jinja2')
def index_page(request):
    entries = Entry.all()
    return {'entries': entries}


@view_config(route_name='detail', renderer='templates/detail.jinja2')
def view(request):
    this_id = request.matchdict.get('id', -1)
    entries = Entry.by_id(this_id)
    print('\nentries value', entries, '\n\n')
    if not entries:
        return HTTPNotFound()
    return {'entry': entries}


@view_config(route_name='action', match_param='action=create',
             renderer='templates/edit.jinja2')
def create(request):
    entry = Entry()
    form = EntryCreateForm(request.POST)
    if request.method == 'POST' and form.validate():
        form.populate_obj(entry)
        DBSession.add(entry)
        return HTTPFound(location=request.route_url('home'))
    return {'form': form, 'action': request.matchdict.get('action')}


@view_config(route_name='action', match_param='action=edit',
             renderer='string')
def update(request):
    return 'edit page'
