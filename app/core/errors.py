
class BaseError(Exception):

    message = "An error has occured"
    code = 400

    def __init__(self, message=None, code=None, payload=None):
        '''
        __init__ for our custom errors

        args
            message       Message of the error

        kwargs
            code          HTTP status code appropriate for this error
            payload       Additional dict that can be used to send data along
                          with the error
        '''

        super(BaseError, self).__init__(self)
        self.message = message or self.message
        self.code = code or self.code
        self.payload = payload

        print self


    def __str__(self):
        return "%s: %s" % (self.code, self.message)


class BaseBadRequest(BaseError):
    pass


class NotFoundMixin(BaseError):

    code = 404

    def __init__(self, id=None, *args, **kwargs):
        self.id = id
        kwargs.update({"payload": {"template": "404.html"}})
        super(NotFoundMixin, self).__init__(*args, **kwargs)


    def __str__(self):
        m = super(NotFoundMixin, self).__str__()
        if self.id:
            return "%s: %s" % (m, self.id)
        else:
            return m


class UnauthorisedMixin(BaseError):
    code = 403
