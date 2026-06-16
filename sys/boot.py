try:
    from kernel.kernel import Kernel

    kernel = Kernel()
    kernel.boot()
except Exception as e:
    print(f"{"\033[91m"}[FATAL] Failed to start WeatiOS: {e}{"\033[0m"}")