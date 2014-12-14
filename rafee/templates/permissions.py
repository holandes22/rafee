from rest_framework import permissions

from rafee.slideshows.models import Slideshow


class IsAllowedToSeeTemplate(permissions.BasePermission):
    '''
    Verify that the template belongs at least to one of the
    user's slideshows.
    '''

    def has_permission(self, request, view):
        if request.user.is_staff:
            return True
        else:
            template_name = request.data.get('template_name', None)
            if not template_name:
                return True  # Bad request, let the validation handle this
            # TODO: use Q here
            teams = request.user.teams.all()
            slideshows = Slideshow.objects.filter(team__in=teams)
            for slideshow in slideshows:
                if template_name in slideshow.templates:
                    return True
        return False
