from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User

from database.models import Student

@login_required
@user_passes_test(is_admin)
def set_up_appointments(request):


