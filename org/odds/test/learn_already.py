import asyncio

async def do_it(prompt: str):
    pass


def main():
    asyncio.run(do_it("what kind of document is this? index | name | email | info\n1 | 'test' | 'test@me.org' | '{measurement: 3.201022}'\n2 | 'test 2' | 'test@me.org' | '{measurement: 3.201022, time: 2023-01-01 20:08:58}'\n3 | 'test 3' | 'test@me.org' | '{measurement: -1.23, time: 2025-06-09 12:33:01, msg: 'successful'}'\n4 | 'test five' | 'chrisw@olemiss.edu' | '{measurement: 5.92292}'"))

if __name__ == "__main__":
    main()