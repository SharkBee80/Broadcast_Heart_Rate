import subprocess
import threading


def read_stream(stream, callback):
    """读取流并逐行调用回调函数"""
    for line in iter(stream.readline, ''):
        callback(line)
    stream.close()


def main():
    # 运行程序并实时打印输出
    try:
        process = subprocess.Popen(
            ["dist/HeartRate.exe"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
        )

        # 定义输出回调函数
        def print_stdout(line):
            print(f"[STDOUT] {line}", end="")  # 可选添加标签区分来源

        def print_stderr(line):
            print(f"[STDERR] {line}", end="")

        # 启动两个线程分别读取 stdout 和 stderr
        stdout_thread = threading.Thread(target=read_stream, args=(process.stdout, print_stdout))
        stderr_thread = threading.Thread(target=read_stream, args=(process.stderr, print_stderr))

        stdout_thread.start()
        stderr_thread.start()

        # 等待子进程结束
        process.wait()

        # 等待线程完成
        stdout_thread.join()
        stderr_thread.join()

    except FileNotFoundError:
        print("错误：指定的可执行文件不存在。")
    except PermissionError:
        print("错误：没有执行该文件的权限。")
    except Exception as e:
        print(f"发生未知错误：{e}")
    finally:
        try:
            process.stdout.close()
            process.stderr.close()
        except:
            pass


if __name__ == '__main__':
    main()

