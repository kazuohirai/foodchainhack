# Multichain Install steps

```
su (enter root password)

cd /tmp
wget http://www.multichain.com/download/multichain-1.0-alpha-15.tar.gz
tar -xvzf multichain-1.0-alpha-15.tar.gz
cd multichain-1.0-alpha-15
mv multichaind multichain-cli multichain-util /usr/local/bin (to make easily accessible on the command line)

exit (to return to your regular user)
```
Connect to the foodchain blockchain by running 'multichaind food@192.168.0.234:7363' to get a public key. Ask the admin/regulator to grant access to you, and then you are free to mine.


# Front End
```
npm install
```
```
bower install
```

Start the server by running `gulp serve`

# Back End
Install libraries in `requirements.txt` using `pip`.

Start the server by running `python manage.py runserver`