# automacao-pos-gravacao
Automação que gera as atividades pós-gravação (glossário, para saber mais e oq aprendemos)

## Configurações necessárias:

1. Chave de API do Gemini (pega no googloe ai studio)
2. Link da pasta mãe onde são armazenados os vídeos (aquela pra onde o OBS manda os vídeos)
3. Adicionar atalho da pasta de conteúdo no seu onedrive:
  - Abra a pasta: https://fiapcom.sharepoint.com/:f:/s/Alura/IgCw9e2FsEL5TLvX-rmAaHSFAc2UevWC9ddH2f_iCHJJbEA?e=PVR1K1
  - Clique em "Adicionar atalho ao OneDrive" e depois em "Meus arquivos"
<img width="1397" height="106" alt="image" src="https://github.com/user-attachments/assets/8af777c2-e4e1-4147-afde-2b54ff1e4df9" />

4. Abra o seu OneDrive, encontre o atalho da pasta e copie como caminho:
<img width="807" height="136" alt="image" src="https://github.com/user-attachments/assets/a457f1dc-33ff-418b-8680-76e1770cbe6f" />

Cole essas informações nessas linhas de código:
<img width="1607" height="216" alt="image" src="https://github.com/user-attachments/assets/964cac6d-290d-402f-91fd-8ef33baa7e5a" />

__________________________________________________________________________________________________________________________________

## Organização da pasta

Dentro da pasta onde são salvos os vídeos gravados pelo OBS, crie uma pasta para a unidade e nomeie ela apenas com o ID:

<img width="1071" height="327" alt="image" src="https://github.com/user-attachments/assets/e93da2c1-a6b9-496b-8d73-19eced5c6125" />

__________________________________________________________________________________________________________________________________

## Para rodar o código, digite no terminal python gerar_unidade_completa.py

No terminal vai chegar uma msg pra vc digitar qual é o ID da unidade. Depois, ele vai processar cada um dos vídeos, enviar para a IA e quando terminar o MD com as atividades será salvo na pasta da unidade dentro do OneDrive :)

OBS: a pasta da unidade precisa existir no OneDrive, senão dá erro no código e ele avisa q a pasta não existe.
