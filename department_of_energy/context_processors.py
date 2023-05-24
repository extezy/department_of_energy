from accounts.forms import AuthenticationAjaxForm
from lighting_objects.forms import DetailForm


def get_context_data(request):
    context = {
        'login_ajax': AuthenticationAjaxForm(),
        'details_modal': DetailForm
    }
    return context
