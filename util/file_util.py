class FileUtil:
    @staticmethod
    def get_domains_from_file(file=None):
        if file is None:
            return []
        with open(file) as f:
            results = f.readlines()
        return results
