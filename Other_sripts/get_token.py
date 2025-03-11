import json
import requests

# Конфигурационные данные (проверьте их в настройках интеграции AmoCRM)
CLIENT_ID = "7acbc805-d521-48fa-883a-da939b17ff7c"
CLIENT_SECRET = "lUPBTSXWSNybsXz9s1zIrWihBJDO7qhBlWt9ODv42xtQp8zSylB4lCfFWhH9Qvgi"
SUBDOMAIN = "cvetoot"
REDIRECT_URL = "https://cvetoot.posiflora.com/admin/orders"
auth_code = 'def50200f4cbc1c2d108b4430c51482e2948bc7298cbb78da6629e335110cc3d918b23aee2107fbc62fb4ca6afe02bd3689970037dd026d8f937ab6e3b369f5fc8433d5cb7a9ff57b865bc493cc0d13bbd64cd92a66f431a816d58ea2cbf17074fb9464d124ba14ee99d2e351ff4458f9f3b131b56264c756f9e1314915237d0a484fe8623aa15d00c0f41ef8b6917e81e5d6d0cc2a401f41d5c4bac5a737bbc881ac1c767557a78a13ca3b1193395f98494367270b51309e8e71629254538329d7454b840702fc7108a5319065a8f1bfc7fc41b05e200587eb83adc297d97e072be05fc4a41c28cb389ff488650b12d615180890c0489444dc13e9f0319277019861af06aa5269ecfe2326240382f6f760cb51a06b733f8bd3d9bf37959d10a124a0971b5f9a7b4f4ed4e98448648dc13c5ef74d7c5f7f914e32b30ea5cfbc0cf477052cdb4c7af06471484f490c8d44f9cb67368ca1418e4d418d257487b76e6aba2b9dafdd233c828d6c21f83e43f6910ca29d74db0170cf0a26ca73214e3fbfee1bebedf12b111babb210bdfb0312784f05a5678ad304f00448f509b6cb2d0149f37b6e2130d8a313e00edd2ef7741689316df1d4012a3bd9ecaf567bff2ec0e93a80e4813a492fdedfc2d093f197d5e9baac8b225c28702b11bce393fa7ddc8404d4fe393eb8964b4cccbd28d2a2d139437816addafe1f11c2a'

def get_tokens(auth_code):
    response = requests.post(
        f"https://{SUBDOMAIN}.amocrm.ru/oauth2/access_token",
        data={
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "grant_type": "authorization_code",
            "code": auth_code,
            "redirect_uri": REDIRECT_URL
        }
    )
    data = response.json()

    with open('access_token.json', 'w') as f:
        json.dump(data, f)
get_tokens(auth_code)