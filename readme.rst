========
Camellia
========

获取源码
---------
::

   git clone https://github.com/zytoto/camellia.git

安装
----

python项目，只支持python3.6以上版本运行

**1.使用virtualenv安装(推荐):** ::

  cd camellia
  mkdir venv-camellia
  virtualenv -p /usr/bin/python3 venv-camellia
  source venv-camellia/bin/activate

  pip install -r requirements.txt

  python setup.py install
  

**2.使用系统python环境安装:** ::

  cd camellia
  sudo pip3 install -r requirements.txt
  sudo python3 setup.py install


初始化数据库
-------------

**使用mysql作为后端数据库(可选，推荐)** ,camellia默认使用sqlite作为数据库后端，sqlite不支持多线程访问。

创建专用的数据库 ::

  mysql
  create database camellia;
  grant all privileges on camellia.* to 'camellia'@'127.0.0.1' identified by 'camellia_dbpass';
  

如果使用了virtualenv,修改 venv-camellia/etc/camellia/camellia.conf , 如果使用系统python环境，修改 /usr/local/etc/camellia/camellia.conf ,增加以下内容 ::

  database=mysql+pymysql://camellia:camellia_dbpass@127.0.0.1:3306/camellia


**初始化数据库:** ::

  camellia-db-manage

运行
----

::

   gunicorn -c etc/camellia-gunicorn.conf camellia.server:app
