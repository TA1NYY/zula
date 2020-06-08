
def header(host: str, port: int, token: str) -> bool:
    header = f"""
                _____   __  ____    ___   V:0.1 Alpha
               /__  /  / / / / /   /   |
                 / /  / / / / /   / /| |
                / /__/ /_/ / /___/ ___ |
               /____/\____/_____/_/  |_|

Another confidential and sensitive data management tool. For me.

    ######################################################

    Adress : http://{host}:{port}                      
    Token : {token}
    
    ######################################################
"""
    print(header)
    return True