from kernel.kernel import Kernel

kernel = Kernel()
kernel.boot()

kernel.filesystem.create("secret", "you found my secret!!!!!")