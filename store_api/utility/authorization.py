from decouple import config
import requests

class UserAuthentication:
    def user_authentication(self, request):
        print("Allah is one")
        url = config('TOKEN_VERIFY')
        params = {"token":request.META["HTTP_AUTHORIZATION"]}
        data = requests.post(url, data=params)
        if data.status_code == 200:
            return True
        return False 





           # url = config('TOKEN_REFRESH')
            # params = {"refresh":request.META["HTTP_REFRESH"]}
            # data = requests.post(url, data=params)
            # token = json.loads(data.content)
            # user = User.objects.get(token=request.META["HTTP_AUTHORIZATION"])
            # print(token['access'])
            # user.token = token['access']
            # user.save()