from slowapi import Limiter
from slowapi.util import get_remote_address

# Rate Limiter Instance using inbuilt method of limiting on remote address
limiter = Limiter(key_func=get_remote_address)
