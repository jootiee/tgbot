import subprocess
from time import sleep

class EXBridge:
    def __init__(self, PATH_EX: str, DIR_EX: str):
        self.executable = PATH_EX
        self.dir = DIR_EX
    
    async def add_user(self, user_id: str) -> str:
        p = subprocess.Popen([self.executable, 'add', user_id], stdin=subprocess.PIPE, encoding='utf-8', cwd=self.dir)
        p.communicate(input='y')
        p.wait()

        link = subprocess.check_output([self.executable, 'link', '/home/jootiee/_repos/easy-xray-main/conf/config_client_{}.json'.format(user_id)]).decode('utf-8').split()[-1]
        return link


    async def suspend_user(self, user_id: str) -> None:
        p = subprocess.Popen([self.executable, 'suspend', user_id], stdin=subprocess.PIPE, encoding='utf-8', cwd=self.dir)
        p.communicate(input='y')
        p.wait()


    async def resume_user(self, user_id: str) -> None:
        p = subprocess.Popen([self.executable, 'resume', user_id], stdin=subprocess.PIPE, encoding='utf-8', cwd=self.dir)
        p.communicate(input='y')
        p.wait()
        

    async def delete_user(self, user_id: str) -> None:
        p = subprocess.Popen([self.executable, 'del', user_id], stdin=subprocess.PIPE, encoding='utf-8', cwd=self.dir)
        p.communicate(input='y')
        p.wait()


    async def get_stats(self) -> str:
        res = subprocess.check_output([self.executable, 'stats'], cwd=self.dir).decode()
        return res


async def main():
    ex = EXBridge()
    data = await ex.get_stats()
    print(data)


if __name__ == '__main__':
    import asyncio
    asyncio.run(main())