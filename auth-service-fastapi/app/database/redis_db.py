from typing import Set

blacklist: Set[str] = set()

def add_token_to_blacklist(jti: str, exp: int):
	blacklist.add(jti)

def is_token_blacklisted(jti: str) -> bool:
	return jti in blacklist
