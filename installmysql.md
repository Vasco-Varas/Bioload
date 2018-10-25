# Installing MySQL and the Python connector

**index:**

- [WINDOWS](#Windows:)
- [Mac](#Mac:)
- [UBUNTU 18.04 LTS](#Ubuntu:)

## Windows:

**1- Download MySQL installer from the [MySQL website](https://dev.mysql.com/downloads/installer)**.

**2- If you don't have python install it from the [Python website](https://www.python.org/downloads/windows/)**.

**2- Run the installer and install the server**.

**3- Go to** `C:\Users\<Your Name>\AppData\Local\Programs\Python\Python36-32\Scripts`

**4- In that directory run** `python3 -m pip install  mysql-connector` **from the terminal**.

**5- Install MySQL Connector with** `pip3 install mysql-connector`

**6- Open MySQL Command Line and enter your root password**.

**7- Create a user with: **`CREATE USER 'your_username'@'localhost' IDENTIFIED WITH mysql_native_password BY 'your_password';` **(Replace your_username and your_password with the values you want)**.

**8- Give root like privileges with:** `GRANT ALL PRIVILEGES ON *.* TO 'your_username'@'localhost';`

**9- Flush privileges with:** `FLUSH PRIVILEGES;`

**10- Finally, you can exit writing:** `Quit`

**11- You're done!**

## Mac:

**1- Run the command** `brew install mysql` **on the terminal**.

**2- Run** `brew services start mysql` **on the terminal**.

**3- Configure mySQL root password with** `mysqladmin -u root password <You Password>`

**4- If you don't have pip or python installed run:** `brew install python`

**5- Install MySQL Connector with** `pip3 install mysql-connector`

**6- Open MySQL With:**`mysql -u root -p` **And then enter your password when requested**.

**7- Create a user with: **`CREATE USER 'your_username'@'localhost' IDENTIFIED WITH mysql_native_password BY 'your_password';` **(Replace your_username and your_password with the values you want)**.

**8- Give root like privileges with:** `GRANT ALL PRIVILEGES ON *.* TO 'your_username'@'localhost';`

**9- Flush privileges with:** `FLUSH PRIVILEGES;`

**10- Finally, you can exit writing:** `Quit`

**11- You're done!**

## Ubuntu:

**1- Run **`sudo apt-get install mysql-server` **from the terminal**.

**2- Run **`sudo mysql_secure_installation` **from the terminal.**

Something like this should happen (Removed some lines):

```bash
secure enough. Would you like to setup VALIDATE PASSWORD plugin?

Press y|Y for Yes, any other key for No: y

Please enter 0 = LOW, 1 = MEDIUM and 2 = STRONG: 1
Please set the password for root here.

New password: 

Re-enter new password:

Remove anonymous users? (Press y|Y for Yes, any other key for No) : y

Disallow root login remotely? (Press y|Y for Yes, any other key for No) : y

Remove test database and access to it? (Press y|Y for Yes, any other key for No) : y

Reload privilege tables now? (Press y|Y for Yes, any other key for No) : y
```

**3- To check if the installation was successful run: **`systemctl status mysql.service` **and you should see something like this:**

```bash
● mysql.service - MySQL Community Server

   Loaded: loaded (/lib/systemd/system/mysql.service; enabled; vendor preset: enabled)
Active: active (running) since Wed 2018-08-08 10:36:46 -04; 15min ago  Process: 18894 ExecStart=/usr/sbin/mysqld --daemonize --pid-file=/run/mysqld/mysqld.pid (code=exited, status=0/SUCC

Process: 18883 ExecStartPre=/usr/share/mysql/mysql-systemd-start pre (code=exited, status=0/SUCCESS)
 Main PID: 18896 (mysqld)    Tasks: 31 (limit: 4915)
   CGroup: /system.slice/mysql.service
           └─18896 /usr/sbin/mysqld --daemonize --pid-file=/run/mysqld/mysqld.pid
```

**4- If you don't have pip3 installed run:** `sudo apt install python3-pip`

**5- Run:** `pip3 install mysql-connector`

**6- Open MySQL With:**`mysql -u root -p` **And then enter your password when requested**.

**7- Create a user with: **`CREATE USER 'your_username'@'localhost' IDENTIFIED WITH mysql_native_password BY 'your_password';` **(Replace your_username and your_password with the values you want).**

**8- Give root like privileges with:** `GRANT ALL PRIVILEGES ON *.* TO 'your_username'@'localhost';` **(Replace your_username with the one on the step above).**

**9- Flush privileges with:** `FLUSH PRIVILEGES;`

**10- Finally, you can exit writing:** `Quit`

**11- You're done!**
