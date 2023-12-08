import multiprocessing

reload = False  # 代码更新时不重启项目
daemon = False  # 不守护Gunicorn进程
backlog = 2048  # 服务器中排队等待的最大连接数，建议值64-2048，超过2048时client连接会得到一个error。
workers = multiprocessing.cpu_count() * 2 + 1  # 用于处理工作的进程数，这里使用了文档建议的值
# workers = 4  # 用于处理工作的进程数，这里使用了文档建议的值
# keyfile = '.../server.key'  # ssl证书密钥文件路径
# certfile = '.../server.crt'  # ssl证书文件路径
worker_class = "uvicorn.workers.UvicornWorker"
timeout = 60  # 访问超时时间
keepalive = 30  # server端保持连接时间。

# max_requests = 1000  # 有内存泄露时使用此选项重启work
# max_requests_jitter = 50  # 重启work的抖动幅度，一般设置为max_requests的5%

accesslog = "-"  # 日志文件路径，'-'表示输出到终端
errorlog = "-"  # 日志文件路径，'-'表示输出到终端
bind = "0:9000"  # 指定监听的地址和端口，这里使用nginx转发了，所以监听特殊端口
loglevel = "info"
