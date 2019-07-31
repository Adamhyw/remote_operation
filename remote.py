# 用法示例
# 1. 远程执行命令调用
# Exec = remote_operation("192.168.45.1","22","root","password","mkdir -p /opt/redhat7","","")
# Exec.remote_execute()
# 2. 上传文件到远端主机
# Upload = remote_operation("192.168.45.1","22","root","password","","/opt/redhat7/redhat7.iso","/opt/redhat7/redhat7.iso")
# Upload.remote_put()
# 3. 下载本件到本地
# Download = remote_operation("192.168.45.1","22","root","password","","/opt/log/latest.log","/opt/test/log/latest.log")
# Download.remote_get()

class remote_operation:
    
    # 定义所需的所有参数
    
    def __init__(self,ip,port,user,code,cmd,localpath,remotepath):
        
        # 远程主机的IP地址
        self.re_ip = ip
        
        # 远程主机的访问端口号
        self.re_port = port
        
        # 远程主机的登录用户名
        self.re_user = user
        
        # 远程主机的登录密码
        self.re_passwd = code
        
        # 执行的命令
        self.exe_cmd = cmd
        
        # 本地文件地址
        self.lo_path = localpath
        
        # 远端文件地址
        self.re_path = remotepath
        
    # 定义远程执行命令的函数，作用是在一台远程主机上执行一条命令并返回标准输出和错误输出。执行命令须是字符串，远程IP须是字符串

    def remote_execute(self):

        # 远程连接主机
        ssh = paramiko.SSHClient()

        # 自动添加主机名和主机密钥保存到本地的HostKeys
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # 输入关键SSH参数：主机名(可以是IP)，端口号，用户名，密码
        ssh.connect(hostname=self.re_ip,port=self.re_port,username=self.re_user,password=self.re_passwd)

        # 顺序执行命令，无报错则认为成功
        stdin,stdout,stderr = ssh.exec_command(self.exe_cmd)
        result_out = stdout.readlines()
        result_err = stderr.readlines()

        # 关闭ssh连接
        ssh.close()

        return result_out,result_err

    # 定义远程传送文件的函数，作用是往一台远程主机传输一个文件。本地路径和远端路径必须是字符串，远程IP必须是字符串

    def remote_put(self):

        # 指定远程登录主机和登录端口
        trans = paramiko.Transport((self.re_ip,int(self.re_port)))

        # 连接远端主机
        trans.connect(username=self.re_user,password=self.re_passwd)

        # 指定对象sftp
        sftp = paramiko.SFTPClient.from_transport(trans)

        # 上传文件到远端主机
        sftp.put(self.lo_path,self.re_path)

        # 结束连接
        trans.close()

    # 定义远程下载文件的函数，作用是从一台远程主机下载一个文件。本地路径和远端路径必须是列表类型，远程IP必须是字符串

    def remote_get(self):
            
        # 指定远程登录主机和登录端口
        trans = paramiko.Transport((self.re_ip,int(self.re_port)))

        # 连接远端主机
        trans.connect(username=self.re_user,password=self.re_passwd)

        # 指定对象sftp
        sftp = paramiko.SFTPClient.from_transport(trans)
                
        # 上传文件到远端主机
        sftp.get(self.re_path,self.lo_path)

        # 结束连接
        trans.close()
