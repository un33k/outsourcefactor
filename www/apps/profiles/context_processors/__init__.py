from django.conf import settings

# what are the available social auth providers (get from settings)
def employement_settings(request):
    cxt = {}
    if request.user.is_authenticated():
        p = request.user.get_profile()
        if p:
            cxt = {
                'is_employee': p.is_employee,
                'is_employer': p.is_employer,
            }
    return cxt
