import requests

resp = requests.post('http://localhost:8000/upload/',
              files={
                  'file1': ('code.png', open('code.png', 'rb'), 'image/png')
              })

print(resp.json())