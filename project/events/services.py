from .models import EventResults


def user_can_access_event(event_obj):
    return not event_obj.is_private


def user_is_unregistered_on_event(event_obj, user):
    return not EventResults.objects.filter(event=event_obj, user=user).exists()


def user_end_event(event_obj, user):
    return (
        EventResults.objects.filter(event=event_obj, user=user).first() is not None
        and EventResults.objects.filter(event=event_obj, user=user).first().is_ended
    )