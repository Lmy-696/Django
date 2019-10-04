from alipay import AliPay

alipay_public_key_string='''-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAthIIFxUu1p4k9/Eydm3CSTGRKlSmXtselygI1izhbSRYtjs1IS2rYxr9UWT9N2fWDM3GN75SEMYwRHBj+d0/7rhzTi3eGIv/5h49oiJWbltd4rCiDfrxfythtS88oRXOgV3Tc9bIMjhy9u8mbt+MUP8KRu/zY6W1TQa2dYOE6GxG1MGvYHBcPK8YNyBS/REY5FKwARDh/l/xonpbyJ+lvmPdRZIfJ8uCkHGJz2rLet1psve65YGaaEllcZrUhGSjS/HXTJiu/y+FWuX4LxhO8UQssjL8txZWIUk9ASkCyfk91O34Njs9C4t69niFDEGGZ0uiAXHKj/mhoyqVCRC0JwIDAQAB
-----END PUBLIC KEY-----'''

alipay_private_key_string='''-----BEGIN RSA PRIVATE KEY-----
MIIEpQIBAAKCAQEAthIIFxUu1p4k9/Eydm3CSTGRKlSmXtselygI1izhbSRYtjs1IS2rYxr9UWT9N2fWDM3GN75SEMYwRHBj+d0/7rhzTi3eGIv/5h49oiJWbltd4rCiDfrxfythtS88oRXOgV3Tc9bIMjhy9u8mbt+MUP8KRu/zY6W1TQa2dYOE6GxG1MGvYHBcPK8YNyBS/REY5FKwARDh/l/xonpbyJ+lvmPdRZIfJ8uCkHGJz2rLet1psve65YGaaEllcZrUhGSjS/HXTJiu/y+FWuX4LxhO8UQssjL8txZWIUk9ASkCyfk91O34Njs9C4t69niFDEGGZ0uiAXHKj/mhoyqVCRC0JwIDAQABAoIBAQCvwAwrK/mAljudUyihBSZMPRqhwACxA9ctlimhhMU9853mmpSYqFsOWZk5nsCHYSZQSboTSRYytv0Us2DuatIx/77eMox3KX0lhv97qKXB9VRVZKep0xiW5yt0GFrwK/qhCg75fNTXFYJ0NznkQMpTzT0AaNOK1wSBi/9IxGHhcDGL1oqpJGu1VuKAWHkaSZIJovOCHKErCUt0tVYRojw1Hn+i5TjKbte4ptmxU1iugacA9avv0Q6ZWGTPk9R52AAeAtQa3E1sHdk0Bl83yKJBymuzTHnsJ3L2T2WALMvzD/rVo1YrOR4c+0ZrcDMKryMCTXxVvq8lr241aKx64/xxAoGBAOk0MXqNLD2G+QBcTZHoTGFkdvzeZ9CV7E9fsPp8vGPLQRAjefqLYWJuKo7KGDZL3qVWSKAOp/npSi8wgZv+0E3nDiF+DEOS4lvMlkulzYcLeqWjKGVdyT0cOKGbqbWWCHExcRlW5KOAPpiI+BaeWXKf2TvF56tcDeTe898y0DgLAoGBAMfeQBKCxgnnIHK+9ktUB/7L+NCddbwla7+6ilaHRGkZi0RTd90yZsxtOizufsW0Ixupiyij9IstN8qvnk6meAHQdD2Ga0zzMiIklv7UH6SsecMF+ePFhQKP0L5L7/XNuvRzhJeoL2X9P624mvFy178FG6DSwlvaSwMu30EXqxnVAoGBAN6ujCCt9XS7EcIaYafV3jmRqV1FMnSm9IPGqERIH8xbJcG3Xp6zwUYwVEsNB5mxUOUoQykzVYr6DXCKLPk8lMQOwhuRNTzBYYyvC0UpCdzORUstRUGmEKdd72XCMofGwED2KT09EA5gQ2V8RQm0I02k/dZp4BJtUIcfrlePOeyJAoGBAMJkElMup+inyDJyMuAu+ZvCzNwx2XnFt5eBmdzwsQO7mW059WHJDJyVO7jJubkWK/NSogtD86uNri7PQhxi4mN5WCUi4Ke1/TOh/M4aiDBEpCSfYl07FdPZBoCfIOMkVko9NF/Ab2E1v8J5wxFEzjt2f1mawvhNRxnwc6k+mOaFAoGAYOAkC8ra1pEPu3xAN+kWOKI1vXx+6AQolln77TprFdvvkdquyxneT8nPtfUnxTaahIrAmC/0laaNis3OpZ4SiQFyxwiuMRR7nz2N39XEb2pH+wOvUY/bdYJW7ZHT+e6BdMklI96VY+SNQ7UKWA77WKNypCg9S6AN9Y9KIj/uXcs=
-----END RSA PRIVATE KEY-----'''

#实例支付
alipay=AliPay(
    appid='2016101200667742',
    app_notify_url=None,
    app_private_key_string=alipay_private_key_string,
    alipay_public_key_string=alipay_public_key_string,
    sign_type='RSA2'
)

#实例订单
order_string=alipay.api_alipay_trade_page_pay(
    out_trade_no='123456789345',#订单号
    total_amount=str(56),#支付金额-字符串
    subject='日用百货',#支付主题
    return_url=None,
    notify_url=None
)

result='https://openapi.alipaydev.com/gateway.do?'+order_string

print(result)