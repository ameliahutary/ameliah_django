from django.utils.deprecation import MiddlewareMixin
from .models import UserProfile

class ProfileMiddleware(MiddlewareMixin):
    def process_template_response(self, request, response):
        if request.user.is_authenticated:
            try:
                user_profile = UserProfile.objects.get(user=request.user)
            except UserProfile.DoesNotExist:
                user_profile = None
        else:
            user_profile = None
        
        response.context_data['user_profile'] = user_profile
        return response
