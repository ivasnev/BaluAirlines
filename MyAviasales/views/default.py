# coding: utf-8
from pyramid.interfaces import IRoutesMapper
from pyramid.view import view_config


@view_config(route_name='home', renderer="study_proj:templates/routes.pt")
def home_view(request):
    # выдираю список роутов из регистра
    route_list = [item.path for item in request.registry.queryUtility(IRoutesMapper).routelist]

    # роуты с {} или * это шаблоны, просто покажу их. остальные сделаю кликабельными линками
    links = []
    templates = []
    for route in route_list:
        if '{' in route or '*' in route:
            templates.append(route)
        else:
            links.append(route)
    return {
        "links": sorted(links),
        "templates": sorted(templates)
    }
