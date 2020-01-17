from accessor import Accessor
from colab_file import train_file, evacuate_file
from driver import init_driver

if __name__ == '__main__':
    accessor = Accessor(train_file, evacuate_file)
    accessor.access_self()
