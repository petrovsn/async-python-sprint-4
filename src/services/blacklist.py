from fastapi import Request, HTTPException, status

BLACK_LIST = [
    #"127.0.0.1",
]

async def check_allowed_ip(request: Request):
    def is_ip_banned(host):
        return host in BLACK_LIST

    if is_ip_banned(request.client.host):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)