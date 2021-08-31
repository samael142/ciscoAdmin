from django.views.generic import TemplateView


class index(TemplateView):
    template_name = 'ciscoadmin/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Index'
        return context
