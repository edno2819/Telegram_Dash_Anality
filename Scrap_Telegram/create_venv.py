import os

path = os.path.dirname(__file__)
locate = f'cd {path} & '
create = 'python -m venv venv & '
activate = f'cmd /c "cd venv\Scripts & activate & cd .. & cd .. & '
requirements = 'pip install -r requirements.txt"'
command = f'{locate}{create}{activate}{requirements}'
os.system(command)
