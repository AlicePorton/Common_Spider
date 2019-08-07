class FileUtil:
    @staticmethod
    def get_domains_from_file(file=None):
        if file is None:
            return []
        f = open(file, mode='r')
        results = [line.strip('\n') for line in f.readlines()]
        # todo: So ugly code
        return [(k.split(' ')[0], k.split(' ')[1]) for k in results[:-1]]

        # with open(file) as f:
        #     results = f.readlines()
        # return [k.split(' ')[0] for k in results][:-1]
