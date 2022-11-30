import os
from markupsafe import escape

class UserDto:
  _username = ""
  _password = ""

  def __init__(self, data):
    self.username = data.get('username')
    self.password = data.get('password')

  @property
  def username(self) -> str:
    return self._username
  
  @username.setter
  def username(self, value):
    if value == None:
      raise ValueError('Username is required')

    username = escape(str(value)).strip().lower()

    if len(username) == 0:
      raise ValueError('Username must not be empty')

    self._username = username
  
  @property
  def password(self) -> str:
    return self._password

  @password.setter
  def password(self, value):
    if value == None:
      raise ValueError('Password is required')

    password = str(value)

    if len(password) < int(os.environ['MIN_PASSWORD_LENGTH']):
      raise ValueError(f"Password length must not be less than {os.environ['MIN_PASSWORD_LENGTH']}")
    
    self._password = password

  def __repr__(self) -> str:
    return f"UserDto(username={self.username}, password={self.password})"