from pyramid.httpexceptions import HTTPFound, HTTPNotFound
from pyramid.view import view_config

from .models import (
    DBSession,
    Entry,
    )

from .forms import EntryCreateForm  #WTForm from forms.py
from .forms import EntryEditForm   #WTForm  from forms.py



@view_config(route_name='home', renderer='templates/list.jinja2')
def index_page(request):
    entries = Entry.all()
    return {'entries': entries}


@view_config(route_name='detail', renderer='templates/detail.jinja2')
def view(request):
    this_id = request.matchdict.get('id', -1)
    entries = Entry.by_id(this_id)
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
             renderer='templates/edit.jinja2')
def update(request):
    # this_id = request.matchdict.get('id', -1)
    this_id = request.matchdict.get('2', -1)
    print ('my id value ==== ', this_id)
    # entries = Entry.by_id(this_id)
    entries = Entry.by_id(3)
    form = EntryEditForm(request.POST, entries)
    if request.method == 'POST' and form.validate():
        form.populate_obj(entries)
        entries.save()
        redirect('update')
    return {'form': form, 'action': request.matchdict.get('action')}
