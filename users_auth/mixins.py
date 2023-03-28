
from django.contrib.auth.mixins import AccessMixin
from django.contrib import messages
from django.shortcuts import redirect




class InstructorAccessRequired(AccessMixin):
    """Verify that the current user is authenticated and has Instructor Profile."""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated and not request.user.is_tutor:
            messages.warning(request, "You must be Authenticated and have Instructor Access")
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)
    




class UserAccessDenied(AccessMixin):
    """Redirect Authenticated users to Home page if they visit Login/Sign up Pages"""
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.info(request, "Looks Like you visited Invalid URL!❗")
            return redirect("home")
        return super().dispatch(request, *args, **kwargs)
    



class AccessOnlyToStudents(AccessMixin):
    """Enrollements only for Students"""
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_student:
            messages.warning(request, "Enrollements only for Students")
            return redirect("home")
        return super().dispatch(request, *args, **kwargs)
    


