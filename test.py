from configparser import ConfigParser as cp

configs = cp()
print(configs.read('portfoliobro.conf'))

print(configs.sections())
print(str(configs.get('mysql', 'password')))