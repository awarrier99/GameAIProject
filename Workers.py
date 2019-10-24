from multiprocessing import Pool


class Workers:
    _pool = Pool()

    @staticmethod
    def delegate(task, args, callback, error_callback):
        Workers._pool.apply_async(task, args=args, callback=callback, error_callback=error_callback)
