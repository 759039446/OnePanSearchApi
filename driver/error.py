class AListError(Exception):
    '''
    基础错误类
    '''
    pass


class AuthenticationError(AListError):
    '''
    验证错误
    '''
    pass


class ServerError(AListError):
    '''
    服务器错误
    '''
    pass


class SecurityWarning(Warning):
    pass


class DeprecationError(Exception):
    pass
