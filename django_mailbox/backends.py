from __future__ import annotations

import logging
from O365.utils import DjangoTokenBackend
from social_django.models import UserSocialAuth

log = logging.getLogger(__name__)


class DjangoSocialAuthTokenBackend(DjangoTokenBackend):
  def __init__(self, user):
    super().__init__()
    self.user = user

  def __repr__(self):
    return "DjangoSocialAuthTokenBackend"

  def get_access_token(self, *, username: Optional[str] = None) -> Optional[dict]:
    if not self.check_token():
      return None

    token = UserSocialAuth.objects.filter(user=self.user).latest("created").extra_data
    token['secret'] = token['access_token']

    return token

  def token_is_expired(self, *, username: Optional[str] = None) -> bool:
    # TODO: check if token is expired
    return False

  def load_token(self) -> bool:
    return self.check_token()

  def save_token(self, force=False) -> bool:
    # handled by social_django
    return True

  def delete_token(self) -> bool:
    UserSocialAuth.objects.filter(user=self.user).delete()
    return True

  def check_token(self) -> bool:
    """
    Checks if any user token exists in the Django database
    :return bool: True if it exists, False otherwise
    """
    return UserSocialAuth.objects.filter(user=self.user).exists()
