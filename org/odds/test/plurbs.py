import cmd
import time
from threading import Thread, Event


class Job(Thread):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.__flag = Event()  # used to SUSPEND thread
        self.__flag.set()  # set suspended True

        self.is_running = Event()  # used to STOP the thread
        self.is_running.set()  # set stopped True

    def run(self):
        while self.is_running.is_set():
            self.__flag.wait()  # returns immediately when True, blocks when False until the internal flag is True and returns
            print(time.time())
            time.sleep(1)

    def pause(self):
        self.__flag.clear()  # set to False to block this thread

    def resume(self):
        self.__flag.set()  # set to True to prevent this thread from blocking

    def stop(self):
        self.__flag.set()  # resume this thread from suspension
        self.is_running.clear()


class MyCmd(cmd.Cmd):
    def __init__(self):
        super().__init__()
        self.prompt = '>> '

        self.long_thread = Job()
        self.long_thread.start()

    def do_greet(self, args):
        print(f"hello {args}")

    def do_quit(self, args):
        return True

    def postloop(self):
        print('postloop')

    def preloop(self):
        print('preloop')
        self.long_thread.pause()

    def precmd(self, line):
        self.long_thread.pause()

    def postcmd(self, stop, line):
        self.long_thread.resume()


def main():
    MyCmd().cmdloop()


if __name__ == "__main__":
    main()
