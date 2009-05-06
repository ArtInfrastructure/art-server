from django.contrib.sites.models import Site

def site(request):
    """Adds a site context variable"""
    return {'site': Site.objects.get_current() }
