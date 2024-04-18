import subprocess
from app.config import EX_PATH, EX_DIR
from time import sleep


async def add_user(user_id: str) -> str:
    p = subprocess.Popen([EX_PATH, 'add', user_id], stdin=subprocess.PIPE, encoding='utf-8', cwd=EX_DIR)
    p.communicate(input='y')
    p.wait()

    link = subprocess.check_output([EX_PATH, 'link', '/home/jootiee/_repos/easy-xray-main/conf/config_client_{}.json'.format(user_id)]).decode('utf-8').split()[-1]
    return link


async def suspend_user(user_id: str) -> None:
    p = subprocess.Popen([EX_PATH, 'suspend', user_id], stdin=subprocess.PIPE, encoding='utf-8', cwd=EX_DIR)
    p.communicate(input='y')
    p.wait()


async def resume_user(user_id: str) -> None:
    p = subprocess.Popen([EX_PATH, 'resume', user_id], stdin=subprocess.PIPE, encoding='utf-8', cwd=EX_DIR)
    p.communicate(input='y')
    p.wait()
    

async def delete_user(user_id: str) -> None:
    p = subprocess.Popen([EX_PATH, 'del', user_id], stdin=subprocess.PIPE, encoding='utf-8', cwd=EX_DIR)
    p.communicate(input='y')
    p.wait()


async def get_stats() -> str:
    res = subprocess.check_output([EX_PATH, 'stats'], cwd=EX_DIR).decode()
    return res


def main():
    print(get_stats())


if __name__ == '__main__':
    main()