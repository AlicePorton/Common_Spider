class DataUtil:
    @staticmethod
    def format_by_ip(obj):
        if obj is None:
            return None
        if 'ips' not in obj:
            return obj
        _obj = obj.copy()
        del _obj['ips']
        results = []
        for ip in obj['ips'].split(','):
            _obj['ip'] = ip
            results.append(_obj.copy())
        return results

    @staticmethod
    def append(results, a):
        if isinstance(a, dict):
            return results.append(a)
        if isinstance(a, list):
            return results + a
