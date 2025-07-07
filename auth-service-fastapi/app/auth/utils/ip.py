from fastapi import Request

def get_client_ip(request: Request) -> str:
  """
  Extract the real client IP address from request headers.
  Works behind proxies or load balancers if 'X-Forwarded-For' is set.
  """
  x_forwarded_for = request.headers.get("x-forwarded-for")
  if x_forwarded_for:
    ip = x_forwarded_for.split(",")[0].strip()
  else:
    ip = request.client.host
  return ip
