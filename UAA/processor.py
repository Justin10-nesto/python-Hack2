from TaskManagement.models import *
from django.contrib.auth.models import User

def userData(request):
    user_id = request.user.id
    user_copy_data = {}
    user_data = {}
    user = User.objects.filter(id = user_id).first() 
    userData = UserDetails.objects.filter(user=user)
    if userData.exists():
        user_data = userData.first()
    return {'user_data':user_data}
