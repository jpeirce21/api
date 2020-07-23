"""
This contains custom decorators that can be used to check that specific 
conditions have been satisfied
"""
from django.core.exceptions import PermissionDenied
from _main_.utils.context import Context

def login_required(function):
  """
  This decorator enforces that a user is logged in before a view can run
  """
  def wrap(request, *args, **kwargs):
    context = request.context
    if context.user_is_logged_in:
      return function(request, *args, **kwargs)
    else:
      raise PermissionDenied
  wrap.__doc__ = function.__doc__
  wrap.__name__ = function.__name__
  return wrap


def admins_only(function):
  """
  This decorator enforces that the user is an admin before the view can run
  """
  def wrap(request, *args, **kwargs):
    context: Context = request.context
    if context.user_is_logged_in and context.user_is_admin():
      return function(request, *args, **kwargs)
    else:
      raise PermissionDenied
  wrap.__doc__ = function.__doc__
  wrap.__name__ = function.__name__
  return wrap


def super_admins_only(function):
  """
  This decorator enforces that a user is a super admin before the view can run
  """
  def wrap(request, *args, **kwargs):
    context: Context = request.context
    if context.user_is_logged_in and context.user_is_super_admin:
      return function(request, *args, **kwargs)
    else:
      raise PermissionDenied
  wrap.__doc__ = function.__doc__
  wrap.__name__ = function.__name__
  return wrap

