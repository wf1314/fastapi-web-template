from common.exceptions.handler import CustomException


class JWTTokenError:
    class InvalidAccessTokenError(CustomException):
        status_code = 401
        default_detail = "无效的access token!"
        default_code = "10001"

    class InvalidRefreshTokenError(CustomException):
        status_code = 400
        default_detail = "无效的refresh token!"
        default_code = "10002"

    class InvalidUserError(CustomException):
        status_code = 400
        default_detail = "用户已被禁用!"
        default_code = "10003"

    class InvalidPasswordError(CustomException):
        status_code = 400
        default_detail = "密码输入有误!"
        default_code = "10004"


class ExampleError:
    class OnPurposeError(CustomException):
        status_code = 400
        default_detail = "演示报错示例!"
        default_code = "20001"
