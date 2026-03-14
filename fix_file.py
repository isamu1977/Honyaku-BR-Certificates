import re

with open('ai_providers.py', 'r') as f:
    content = f.read()

# Verificar se há o padrão problemático
if '<think>' in content:
    print('Encontrou o padrão problemático!')
    content = content.replace('<think>\n', '')
    
    with open('ai_providers.py', 'w') as f:
        f.write(content)
    print('Arquivo corrigido!')
else:
    print('Padrão não encontrado')
