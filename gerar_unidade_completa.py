# comando para rodar no terminal: python gerar_unidade_completa.py

import whisper
import google.generativeai as genai
import os
import glob
import time
import re
from collections import defaultdict

# ================= CONFIGURAÇÕES DE DIRETÓRIOS E API =================
PASTA_MAE_LOCAL = r"INCLUA O LINK PARA A PASTA DO SEU PC ONDE AS GRAVAÇÕES SÃO ARMAZENADAS"
PASTA_MAE_ONEDRIVE = r"C:\Users\alura\OneDrive - Fiap-Faculdade de Informática e Administração Paulista\Drives Compartilhados - [CONTEUDOS] EFAF EM"

CHAVE_API_GEMINI = "INCLUA SUA CHAVE AQUI"
# =====================================================================

TEXTO_COMPARTILHE_AULA_4 = """
## Compartilhe seu projeto 

E agora que tal **compartilhar o que você construiu**? Esse passo é importante para que seu professor ou professora veja como está seu desenvolvimento e te ajude a melhorar cada vez mais.  

**Envie**, na caixa abaixo, o **link do projeto** que você construiu durante esta unidade.
"""

TEXTO_COMPARTILHE_AULA_8 = """
## Compartilhe seu projeto 

Você concluiu mais uma unidade e aposto que conseguiu desenvolver um projeto incrível! 

E agora que tal **compartilhar o que você construiu**? Esse passo é importante para que seu professor ou professora veja como está seu desenvolvimento e te ajude a melhorar cada vez mais.  

**Envie**, na caixa abaixo, o **link do projeto** que você construiu durante esta unidade.
"""

def extrair_termos_glossario(md_text):
    """Extrai termos em negrito do glossário usando Regex (livre de erros de lista)."""
    termos = set()
    match = re.search(r'##\s*Glossário(.*?)(?=\n## |\Z)', md_text, re.DOTALL | re.IGNORECASE)
    if match:
        trecho = match.group(1)
        matches = re.findall(r'[-*]\s+\*\*([^*]+)\*\*', trecho)
        for m in matches:
            termos.add(m.strip().lower())
    return termos

def gerar_conteudo_aula(texto_transcrito, termos_vistos_global):
    termos_proibidos_str = ", ".join(sorted(list(termos_vistos_global))) if termos_vistos_global else "Nenhum termo usado ainda."
    
    prompt = f"""
    Você é um assistente especialista em educação e tecnologia, focado em ensinar programação para adolescentes de 13 a 14 anos.
    Abaixo está a transcrição combinada de todos os vídeos referentes a UMA ÚNICA AULA.
    Sua tarefa é analisar o texto completo e gerar TRÊS seções em Markdown consolidando os temas abordados.

    REGRAS PARA A SEÇÃO 1: "## O que aprendemos"
    - Siga ESTE TEMPLATE EXATAMENTE, sem negrito no primeiro parágrafo:
    Olá estudantes! O tema da nossa aula foi [tema] e o nosso objetivo era [objetivo principal]. Vamos relembrar o que fizemos até aqui?
    
    * Primeiro, **frase-chave**, explicação do que foi feito com verbos conjugados na 3ª pessoa do plural, sem parênteses extras. Uma única frase curta.
    * Depois, **frase-chave**, continuação fluida da explicação.Uma única frase curta.
    * Em seguida, **frase-chave**, continuação fluida da explicação.Uma única frase curta.
    * Por último, **frase-chave**, fechar com a última etapa.Uma única frase curta.
    
    E com isso, conseguimos [citar o objetivo da aula]! Nos vemos numa próxima, até mais!
    - IMPORTANTE PARA A LISTA: NUNCA coloque parênteses envolvendo o negrito ou a explicação. Use vírgula após a **frase-chave** em negrito e siga com texto corrido natural (ex: `* Primeiro, **salvei as respostas nas notas**, registrando a conversa...`).
    - Ajuste a concordância do primeiro parágrafo se necessário.
    - O resumo deve englobar o aprendizado de toda a transcrição. Extraia exatamente 4 passos principais.

    REGRAS PARA A SEÇÃO 2: "## Glossário"
    - Identifique apenas conceitos técnicos.
    - Crie explicações simples com analogias (tom pedagógico, direto).
    - Evite listar nomes de variáveis, funções específicas ou jargões complexos nas explicações.
    - ANTI-REPETIÇÃO: NÃO repita nenhum destes termos já definidos em aulas anteriores desta unidade: [{termos_proibidos_str}].

    REGRAS PARA A SEÇÃO 3: "## Para saber mais"
    - Escreva de 1 a 2 parágrafos com uma breve explicação conceitual/contextual aprofundando um tema relacionado ao assunto da aula.
    - Abaixo do texto, inclua de 1 a 2 links externos confiáveis em Markdown (formato [descrição](url)).
    - PROIBIDO incluir documentação de ferramentas, softwares, ambientes de desenvolvimento ou linguagens de programação (ex: sem links para docs do Python, MDN, VS Code, Git, StartLab, etc.). Foque em portais educacionais, artigos teóricos, .org/.gov ou universidades.
    - REGRA CRÍTICA DE SEGURANÇA: É TERMINANTEMENTE PROIBIDO sugerir, indicar ou linkar o Scratch (scratch.mit.edu).

    Transcrição combinada da aula:
    {texto_transcrito}

    SAÍDA: Forneça apenas o texto em Markdown, começando diretamente com "## O que aprendemos". Não inclua o título "# Aula X".
    """

    modelos_para_tentar = ["gemini-3.5-flash", "gemini-3.8-flash", "gemini-flash-latest", "gemini-3.5-flash-lite"]
    
    for nome_modelo in modelos_para_tentar:
        try:
            modelo_ia = genai.GenerativeModel(nome_modelo)
            resposta = modelo_ia.generate_content(prompt)
            return resposta.text.strip()
        except Exception:
            time.sleep(2)
            continue
            
    return "❌ Erro ao gerar conteúdo para esta aula. Verifique a API ou tente novamente."

def processar_unidade():
    print(r"""
      ___  ____  ___    ___  __  __ 
     / _ \| __ )/ __|  |_ _||  \/  |
    | | | |  _ \\__ \   | | | |\/| |
    | |_| | |_) |___/   | | | |  | |
     \___/|____/|___/  |___||_|  |_| Processador Consolidado
    """)
    
    id_unidade = input("👉 Digite o ID da Unidade (ex: 6872): ").strip()
    
    pasta_local = os.path.join(PASTA_MAE_LOCAL, id_unidade)
    if not os.path.exists(pasta_local):
        print(f"❌ Erro: Pasta local não encontrada ({pasta_local})")
        return
        
    pasta_onedrive = None
    if os.path.exists(PASTA_MAE_ONEDRIVE):
        for nome_pasta in os.listdir(PASTA_MAE_ONEDRIVE):
            if nome_pasta.startswith(str(id_unidade)):
                caminho_completo = os.path.join(PASTA_MAE_ONEDRIVE, nome_pasta)
                if os.path.isdir(caminho_completo):
                    pasta_onedrive = caminho_completo
                    break

    if not pasta_onedrive:
        print(f"❌ Erro: Nenhuma pasta começando com o ID '{id_unidade}' foi encontrada em {PASTA_MAE_ONEDRIVE}")
        return

    arquivos = glob.glob(os.path.join(pasta_local, "*.mp4")) + glob.glob(os.path.join(pasta_local, "*.mkv"))
    
    if not arquivos:
        print("❌ Nenhum vídeo encontrado na pasta local.")
        return

    aulas_agrupadas = defaultdict(list)
    
    for arquivo in arquivos:
        nome_arquivo = os.path.basename(arquivo)
        match = re.search(r'v[íi]deo\s*(\d+)', nome_arquivo, re.IGNORECASE)
        
        if match:
            numero_aula = int(match.group(1))
            aulas_agrupadas[numero_aula].append(arquivo)
        else:
            print(f"⚠️ Aviso: Não foi possível identificar o número da aula no arquivo '{nome_arquivo}'. Ele será ignorado.")

    arquivo_md = os.path.join(pasta_onedrive, f"{id_unidade} Atividades.md")
    
    print(f"\n📂 Identificadas {len(aulas_agrupadas)} aulas diferentes.")
    print(f"Salvando o documento final na pasta: {os.path.basename(pasta_onedrive)}\n")
    
    genai.configure(api_key=CHAVE_API_GEMINI)
    modelo_whisper = whisper.load_model("base")
    
    termos_vistos_global = set()
    
    with open(arquivo_md, "w", encoding="utf-8") as md:
        md.write(f"<!-- Documento gerado automaticamente para a Unidade {id_unidade} -->\n\n")
        
        for numero_aula in sorted(aulas_agrupadas.keys()):
            videos_da_aula = sorted(aulas_agrupadas[numero_aula])
            
            print(f"\n▶️ Processando Aula {numero_aula} (contém {len(videos_da_aula)} vídeo(s))...")
            
            texto_completo_aula = ""
            
            for index, video in enumerate(videos_da_aula, start=1):
                print(f"   🎙️ Extraindo áudio do vídeo {index}/{len(videos_da_aula)}: {os.path.basename(video)}...")
                resultado = modelo_whisper.transcribe(video, language="pt")
                texto_transcrito = resultado["text"].strip()
                
                if texto_transcrito:
                    texto_completo_aula += texto_transcrito + "\n\n"
            
            if not texto_completo_aula.strip():
                print(f"   ⚠️ Aviso: Nenhum áudio detectado nos vídeos da Aula {numero_aula}.")
                conteudo_ia = "*(Áudio não detectado. Verifique os arquivos originais.)*"
            else:
                print(f"   🧠 Gerando consolidação com IA para a Aula {numero_aula}...")
                conteudo_ia = gerar_conteudo_aula(texto_completo_aula, termos_vistos_global)
                novos_termos = extrair_termos_glossario(conteudo_ia)
                termos_vistos_global.update(novos_termos)
            
            md.write(f"# Aula {numero_aula}\n\n")
            md.write(conteudo_ia + "\n\n")
            
            if numero_aula == 4:
                md.write(TEXTO_COMPARTILHE_AULA_4 + "\n\n")
            elif numero_aula == 8:
                md.write(TEXTO_COMPARTILHE_AULA_8 + "\n\n")
                
            print(f"✅ Aula {numero_aula} consolidada com sucesso no OneDrive!")
            
    print(f"\n🎉 SUCESSO! Todas as atividades consolidadas em: {arquivo_md}")

if __name__ == "__main__":
    processar_unidade()