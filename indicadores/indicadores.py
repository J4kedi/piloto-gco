"""Indicadores do piloto GCO. Só biblioteca padrão do Python 3.14. Rode na raiz do kit:

  python indicadores/indicadores.py coletar    fotografa git e GitHub em registros/historico.json
  python indicadores/indicadores.py            calcula sem rede e grava registros/indicadores.md
  python indicadores/indicadores.py autoteste  confere o cálculo em indicadores/exemplo-ficticio/

Formato de registros/historico.json (horários do GitHub em UTC, como a API devolve):
  repositorio, coletado_em, main (sha de origin/main), marco ("v0.1.0")
  commits    todos os commits de primeiro pai em v0.1.0..origin/main; o filtro de caminho
             controlado é feito no cálculo: [{sha, pais, autor, data, assunto, arquivos, versoes}],
             versoes = etiquetas v* que contêm o commit
  prs        PRs integrados cujo merge commit está em commits: [{numero, autor, titulo, corpo,
             rotulos, criado_em, integrado_em, merge_commit, commits: [{sha, data (committer)}],
             reviews: [{autor, estado, em, corpo}], comentarios: [{autor, em, corpo}]}]
  issues     {"<n>": [{autor, em, corpo}]}: comentários das issues ligadas (Demanda: #n ou Closes #n)
  etiquetas  [{nome, commit}]
  releases   [{etiqueta, corpo, publicada_em}], sem rascunhos
"""

import csv
import io
import json
import re
import subprocess
import sys
import unicodedata
from collections import Counter, defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path

PASTA = Path(__file__).resolve().parent
RAIZ = PASTA.parent
EXEMPLO = PASTA / 'exemplo-ficticio'
FUSO = timezone(timedelta(hours=-3))
MARCO = 'v0.1.0'
MARCA = 'FICTICIO'
PREENCHER = '[PREENCHER - autores]'
CONTROLADOS = ('app/', 'infra/', 'scripts/', '.github/')
SEMVER = re.compile(r'v\d+\.\d+\.\d+')

TAREFAS = [
    'Registrar demanda', 'Classificar mudança', 'Aprovar emergência', 'Implementar mudança',
    'Submeter pull request', 'Revisar mudança', 'Corrigir mudança', 'Integrar pull request',
    'Implantar em homologação', 'Criar baseline', 'Liberar em produção', 'Ativar nova versão',
    'Verificar nova versão', 'Registrar liberação', 'Restaurar versão anterior', 'Investigar causa',
    'Registrar incidente', 'Corrigir configuração', 'Solicitar correção urgente', 'Executar script avulso',
    'Verificar baselines', 'Conferir itens de configuração', 'Conferir registros', 'Testar restauração',
    'Registrar auditoria',
]
PAPEIS = ['Solicitante', 'Desenvolvedor(a)', 'Revisor(a)', 'Responsável por configuração', 'Aprovador emergencial']
RESULTADOS = {
    'Classificar mudança': ['normal', 'risco', 'emergencial'],
    'Revisar mudança': ['aprovada', 'reprovada'],
    'Aprovar emergência': ['aprovada', 'negada'],
    'Verificar nova versão': ['sem falha', 'com falha'],
    'Investigar causa': ['confirmada', 'não confirmada'],
    'Testar restauração': ['aprovada', 'reprovada'],
}
CONTAGEM = {'Verificar baselines', 'Conferir itens de configuração', 'Conferir registros', 'Registrar auditoria'}
FORA_DO_CONTROLE = {'Implementar mudança', 'Corrigir mudança'}
NIVEIS = ['PR obrigatório', 'registro obrigatório', 'livre']
COLUNAS = 'ciclo;cenario;tarefa;papel;quem;data;inicio;fim;demanda;pr;versao;resultado;artefato;desvio;dificuldade'
COLUNAS_LOG = 'inicio,fim,comando,versao,commit,imagem,slot,copia,impressao,resultado,detalhe,executor'
NUMEROS_AUDITORIA = ['itens identificados', 'itens completos', 'divergencias', 'baselines conferidas',
                     'desvios encontrados', 'desvios tratados']
REVISAO = {'sim': 'sim', 'posterior': 'só depois do merge', '': 'não'}
SEM_HISTORICO = ['2a', '2b', '3', '4a', '4b', '5', '6']
LINHAS = [
    ('1', 'GCO 1 — Itens de configuração controlados',
     'Itens completos / Itens identificados, último registro em `registros/auditorias/`'),
    ('1b', 'GCO 1 — Itens completos na lista atual', '`processo/1-itens-de-configuracao.md`'),
    ('2a', 'GCO 2 — Revisão por outra pessoa', 'P com review de outro login / P (`historico.json`)'),
    ('2b', 'GCO 2 — Revisão por outra pessoa, rótulo `risco`', 'o mesmo, só P com rótulo `risco`'),
    ('3', 'GCO 2 — Mudanças diretas', 'D / E (`historico.json`)'),
    ('4a', 'GCO 2 — Mudanças emergenciais', 'P com rótulo `emergencial` / P'),
    ('4b', 'GCO 2 — Emergenciais aprovadas antes do primeiro commit',
     '`Aprovação emergencial:` de outro login antes do primeiro commit / emergenciais'),
    ('5', 'GCO 3 — Baselines de produção',
     'Lib com etiqueta semântica e notas na Release / Lib (`execucoes.csv`, `historico.json`)'),
    ('6', 'GCO 4 — Registro de liberações',
     'Lib com Versão, Demanda, Liberado por e Resultado da verificação no bloco da Release / Lib'),
    ('7', 'GCO 4 — Incidentes com causa e nota',
     'notas em `registros/incidentes/` com Causa confirmada: sim / `reverter` ok no log'),
    ('8a', 'GCO 5 — Auditorias feitas', 'registros em `registros/auditorias/` / previstas (1)'),
    ('8b', 'GCO 5 — Desvios tratados', 'Desvios tratados / Desvios encontrados, soma das auditorias'),
    ('8c', 'GCO 5 — Restaurações aprovadas', 'auditorias com Restauração: aprovada / previstas (1)'),
    ('9', 'GCO 5 — Backup', 'Lib com `copia` e `impressao` preenchidas / Lib (`execucoes.csv`)'),
]


# ---------- leitura ----------

def normalizar(texto):
    """Minúsculas, sem acento e com espaços simples, para comparar valores digitados à mão."""
    decomposto = unicodedata.normalize('NFD', texto or '')
    return ' '.join(''.join(c for c in decomposto if not unicodedata.combining(c)).lower().split())


def canonico(valor, lista):
    return next((item for item in lista if normalizar(item) == normalizar(valor)), None)


def ler_texto(caminho):
    """UTF-8 com ou sem BOM; se não decodificar, cp1252 (Excel pt-BR)."""
    bruto = caminho.read_bytes()
    try:
        return bruto.decode('utf-8-sig')
    except UnicodeDecodeError:
        return bruto.decode('cp1252', errors='replace')


def limpo(texto):
    """Texto sem comentários HTML e sem o marcador dos autores."""
    return re.sub(r'<!--.*?-->', '', texto or '', flags=re.S).replace(PREENCHER, '').strip()


def campos(texto):
    """Linhas `- Campo: valor` em {campo normalizado: valor}; vale a primeira ocorrência."""
    achados = {}
    for linha in (texto or '').splitlines():
        achado = re.match(r'\s*[-*]\s*([^:]+?)\s*:(.*)$', linha)
        if achado:
            achados.setdefault(normalizar(achado[1]), achado[2].strip())
    return achados


def titulo(linhas, nome):
    """Índice do título Markdown cujo texto normalizado é `nome`, ou None."""
    return next((i for i, linha in enumerate(linhas)
                 if linha.lstrip().startswith('#') and normalizar(linha.strip('# \t')) == nome), None)


def tabela(texto, colunas):
    """Linhas da primeira tabela Markdown com exatamente estas colunas, ou None."""
    alvo = [normalizar(c) for c in colunas]
    linhas = []
    for linha in (texto or '').splitlines() + ['']:
        if linha.strip().startswith('|'):
            linhas.append([c.strip() for c in linha.strip().strip('|').split('|')])
            continue
        if linhas and [normalizar(c) for c in linhas[0]] == alvo:
            return [l for l in linhas[1:] if not all(re.fullmatch(r':?-+:?', c) for c in l)]
        linhas = []
    return None


def quando(texto):
    return datetime.fromisoformat(texto) if texto else None


def local(texto):
    """Horário ISO (UTC do GitHub ou com fuso) exibido em −03:00."""
    return quando(texto).astimezone(FUSO).strftime('%Y-%m-%d %H:%M') if texto else '—'


def numero(valor):
    valor = (valor or '').strip()
    return int(valor) if valor.isdigit() else None


def converter(texto, formatos):
    for formato in formatos:
        try:
            return datetime.strptime(texto, formato)
        except ValueError:
            pass
    return None


def ler_planilha(nome, texto, divergencias):
    """Planilha manual: `;` ou `,`, colunas pela ordem do cabeçalho, linhas vazias ignoradas."""
    primeira = texto.partition('\n')[0]
    separador = ';' if primeira.count(';') >= primeira.count(',') else ','
    leitor = csv.reader(io.StringIO(texto, newline=''), delimiter=separador)
    cabecalho = [normalizar(c) for c in next(leitor, [])]
    faltam = [c for c in COLUNAS.split(';') if c not in cabecalho]
    if faltam:
        divergencias.append(('Linha ilegível', f'{nome}: cabeçalho sem {", ".join(faltam)}'))
        return []
    linhas = []
    for celulas in leitor:
        if not any(c.strip() for c in celulas):
            continue
        origem = f'{nome}:{leitor.line_num}'
        if any(c.strip() for c in celulas[len(cabecalho):]):
            divergencias.append(('Linha ilegível', f'{origem}: mais colunas que o cabeçalho'))
            continue
        linha = dict(zip(cabecalho, [c.strip() for c in celulas] + [''] * len(cabecalho)))
        linha['origem'] = origem
        linhas.append(conferir(linha, divergencias))
    return linhas


def conferir(linha, divergencias):
    """Põe os valores na grafia das listas fechadas e acusa o que estiver fora ou ilegível."""
    origem = linha['origem']

    def acusar(tipo, campo, valor):
        divergencias.append((tipo, f'{origem}: {campo} "{valor}"'))

    for campo, lista in (('tarefa', TAREFAS), ('papel', PAPEIS)):
        valor = canonico(linha[campo], lista)
        if valor is None:
            acusar('Valor fora da lista fechada', campo, linha[campo])
        linha[campo] = valor or ''
    for campo, padrao in (('ciclo', r'G[1-5]'), ('cenario', r'C[1-7]')):
        linha[campo] = linha[campo].upper()
        vazio_aceito = campo == 'ciclo' or linha['tarefa'] == 'Executar script avulso'
        if not re.fullmatch(padrao, linha[campo]) and not (vazio_aceito and not linha[campo]):
            acusar('Valor fora da lista fechada', campo, linha[campo])
    tarefa, resultado = linha['tarefa'], linha['resultado']
    if tarefa in RESULTADOS:
        valor = canonico(resultado, RESULTADOS[tarefa])
        aceito, linha['resultado'] = valor is not None, valor or resultado
    else:
        aceito = resultado.isdigit() if tarefa in CONTAGEM else not (tarefa and resultado)
    if not aceito:
        acusar('Valor fora da lista fechada', 'resultado', resultado)

    data = converter((linha['data'].split() or [''])[0], ('%Y-%m-%d', '%d/%m/%Y'))  # Excel: "12/11/2026 00:00"
    inicio, fim = (converter(linha[c], ('%H:%M', '%H:%M:%S')) for c in ('inicio', 'fim'))
    for campo, valor in (('data', data), ('inicio', inicio), ('fim', fim)):
        if valor is None:
            acusar('Linha ilegível', campo, linha[campo])
    linha['quando'] = datetime.combine(data.date(), inicio.time()).isoformat() if data and inicio else ''
    linha['minutos'] = None
    if data and inicio and fim:
        if fim < inicio:
            divergencias.append(('Linha ilegível', f'{origem}: fim antes do início'))
        else:
            linha['minutos'] = (fim - inicio).total_seconds() / 60
    for campo in ('demanda', 'pr', 'versao', 'quem'):
        linha[campo] = linha[campo].lstrip('#@').strip().lower()
    # `pr`: número puro é PR; `commit <hash curto>` ou hash puro é commit direto
    commit = re.fullmatch(r'(?:commit\s+)?([0-9a-f]{7,40})', linha['pr'])
    linha['commit'] = commit[1] if commit and not linha['pr'].isdigit() else ''
    if linha['commit']:
        linha['pr'] = ''
    elif linha['pr'] and not linha['pr'].isdigit():
        acusar('Linha ilegível', 'pr', linha['pr'])
    return linha


def ler_log(texto, divergencias):
    if not texto:
        return []
    leitor = csv.DictReader(io.StringIO(texto, newline=''))
    if sorted(leitor.fieldnames or []) != sorted(COLUNAS_LOG.split(',')):
        divergencias.append(('Linha ilegível', 'execucoes.csv: cabeçalho diferente do contrato'))
        return []
    linhas = []
    for linha in leitor:
        if None in linha or None in linha.values():
            divergencias.append(('Linha ilegível', f'execucoes.csv:{leitor.line_num}: número de colunas'))
        elif linha['versao'] != MARCO:
            linhas.append(linha)
    return linhas


def ler_incidente(nome, texto, divergencias):
    lido = campos(texto).get('causa confirmada', '')
    if normalizar(lido) not in ('sim', 'nao'):
        divergencias.append(('Valor fora da lista fechada', f'incidentes/{nome}: Causa confirmada "{lido}"'))
    return normalizar(lido)


def ler_auditoria(nome, texto, divergencias):
    lidos = campos(texto)
    auditoria = {'nome': nome, 'restauracao': normalizar(lidos.get('restauracao'))}
    if auditoria['restauracao'] not in ('aprovada', 'reprovada'):
        divergencias.append(('Valor fora da lista fechada',
                             f'auditorias/{nome}: Restauração "{lidos.get("restauracao", "")}"'))
    for campo in NUMEROS_AUDITORIA:
        auditoria[campo] = numero(lidos.get(campo))
        if auditoria[campo] is None:
            divergencias.append(('Linha ilegível', f'auditorias/{nome}: {campo} "{lidos.get(campo, "")}"'))
            auditoria[campo] = 0
    return auditoria


def ler_cenarios(texto, divergencias):
    """{'C1': [tarefas do caminho previsto]} da tabela `| Cenário | Caminho previsto |`."""
    previstos = {}
    for linha in tabela(texto, ['Cenário', 'Caminho previsto']) or []:
        achado = re.match(r'\W*(C[1-7])', linha[0])
        if not achado or len(linha) < 2:
            continue
        previstos[achado[1]] = []
        for nome in re.split(r'→|->', linha[1]):
            tarefa = canonico(nome, TAREFAS)
            if tarefa:
                previstos[achado[1]].append(tarefa)
            elif nome.strip():
                divergencias.append(('Valor fora da lista fechada', f'cenarios.md, {achado[1]}: tarefa "{nome.strip()}"'))
    return previstos


def ler_itens(texto, divergencias):
    """(itens completos, itens) da lista; completo = tipo, responsável e nível válidos."""
    linhas = tabela(texto, ['Item', 'Tipo', 'Local oficial', 'Responsável', 'Nível de controle'])
    if linhas is None:
        return None
    completos = total = 0
    for item, tipo, _, responsavel, nivel in ((l + [''] * 5)[:5] for l in linhas):
        if not limpo(item):
            continue
        total += 1
        nivel_valido = canonico(nivel, NIVEIS)
        if limpo(nivel) and nivel_valido is None:
            divergencias.append(('Valor fora da lista fechada',
                                 f'processo/1-itens-de-configuracao.md: nível "{nivel}" em {item}'))
        completos += bool(limpo(tipo) and limpo(responsavel) and nivel_valido)
    return completos, total


def carregar(raiz):
    """Lê tudo o que o cálculo usa; nada de rede."""
    registros = raiz / 'registros'
    d = {'raiz': raiz, 'divergencias': [], 'faltou': [], 'textos': []}

    def ler(caminho):
        relativo = caminho.relative_to(raiz).as_posix()
        if not caminho.is_file():
            d['faltou'].append(relativo)
            return ''
        texto = ler_texto(caminho)
        d['textos'].append((relativo, texto))
        return texto

    try:
        d['historico'] = json.loads(ler(registros / 'historico.json') or 'null')
    except json.JSONDecodeError:
        d['historico'] = None
        d['faltou'].append('registros/historico.json legível')
    d['log'] = ler_log(ler(registros / 'execucoes.csv'), d['divergencias'])
    planilhas = sorted(registros.glob('tarefas-autor-*.csv'))
    if not planilhas:
        d['faltou'].append('registros/tarefas-autor-*.csv')
    d['tarefas'] = [l for c in planilhas for l in ler_planilha(c.name, ler(c), d['divergencias'])]
    d['incidentes'] = [ler_incidente(c.name, ler(c), d['divergencias'])
                       for c in sorted((registros / 'incidentes').glob('*.md'))]
    d['auditorias'] = [ler_auditoria(c.name, ler(c), d['divergencias'])
                       for c in sorted((registros / 'auditorias').glob('*.md'))]
    d['cenarios'] = ler_cenarios(ler(raiz / 'cenarios.md'), d['divergencias'])
    d['itens'] = ler_itens(ler(raiz / 'processo' / '1-itens-de-configuracao.md'), d['divergencias'])
    return d


# ---------- regras ----------

def conjuntos(hist):
    """E (commits de primeiro pai em caminho controlado), P (PRs cujo merge está em E), D (E sem merges de PR)."""
    if not hist:
        return [], [], []
    e = [c for c in hist['commits'] if any(a.startswith(CONTROLADOS) for a in c['arquivos'])]
    em_e = {c['sha'] for c in e}
    merges = {pr['merge_commit'] for pr in hist['prs']}
    return e, [pr for pr in hist['prs'] if pr['merge_commit'] in em_e], [c for c in e if c['sha'] not in merges]


def classificacao(pr):
    rotulos = {normalizar(r) for r in pr['rotulos']}
    return next((r for r in RESULTADOS['Classificar mudança'] if r in rotulos), '')


def issue_ligada(corpo):
    achado = re.search(r'(?:Demanda:\s*#|Closes\s+#)(\d+)', corpo or '', re.I)
    return achado[1] if achado else ''


def outra_pessoa(login, autor):
    """Login diferente do autor e que não é bot (`...[bot]`: revisores e analisadores automáticos)."""
    return login.lower() != autor.lower() and not login.lower().endswith('[bot]')


def revisao(pr):
    """'sim', 'posterior' (emergencial revisado só depois do merge) ou ''."""
    integrado = quando(pr['integrado_em'])
    emergencial = classificacao(pr) == 'emergencial'
    tipos = set()
    for rv in pr['reviews']:
        if not outra_pessoa(rv['autor'], pr['autor']):
            continue
        depois = bool(rv['em']) and quando(rv['em']) > integrado
        if rv['estado'] in ('APPROVED', 'CHANGES_REQUESTED'):
            tipos.add('posterior' if emergencial and depois else 'sim')
        elif rv['estado'] == 'COMMENTED' and emergencial and depois:
            tipos.add('posterior')
    return 'sim' if 'sim' in tipos else 'posterior' if tipos else ''


def aprovada_antes(pr, issues):
    """`Aprovação emergencial:` de outro login, no PR ou na issue ligada, antes do primeiro commit do PR."""
    if not pr['commits']:
        return False
    primeiro = min(quando(c['data']) for c in pr['commits'])
    falas = pr['comentarios'] + pr['reviews'] + issues.get(issue_ligada(pr['corpo']), [])
    return any(outra_pessoa(f['autor'], pr['autor']) and f['em'] and quando(f['em']) < primeiro
               and any(normalizar(l).startswith('aprovacao emergencial:') for l in (f['corpo'] or '').splitlines())
               for f in falas)


def ler_release(corpo):
    """(há notas acima do bloco, campos do bloco `## Registro de liberação`)."""
    linhas = (corpo or '').splitlines()
    corte = titulo(linhas, 'registro de liberacao')
    corte = len(linhas) if corte is None else corte
    notas = [l for l in limpo('\n'.join(linhas[:corte])).splitlines() if l.strip() and not l.lstrip().startswith('#')]
    return bool(notas), campos('\n'.join(linhas[corte:]))


def bloco_completo(release):
    return bool(release) and all(limpo(release[1].get(c))
                                 for c in ('versao', 'demanda', 'liberado por', 'resultado da verificacao'))


def tem_evidencia(corpo):
    """Seção `## Evidência de teste` (ou linha `- Evidência de teste:`) não vazia no corpo do PR."""
    linhas = (corpo or '').splitlines()
    inicio = titulo(linhas, 'evidencia de teste')
    if inicio is None:
        return bool(limpo(campos(corpo).get('evidencia de teste')))
    fim = next((i for i in range(inicio + 1, len(linhas)) if linhas[i].lstrip().startswith('#')), len(linhas))
    return bool(limpo('\n'.join(linhas[inicio + 1:fim])))


def primeira_versao(commit):
    versoes = [v for v in commit['versoes'] if SEMVER.fullmatch(v)]
    return min(versoes, key=lambda v: tuple(map(int, v[1:].split('.'))), default='')


# ---------- cálculo ----------

def valores(d, e, p, diretos, lib):
    """{indicador: (numerador, denominador)}; None quando falta a fonte."""
    auditorias = d['auditorias']
    ultima = auditorias[-1] if auditorias else {}
    v = {
        '1': (ultima.get('itens completos', 0), ultima.get('itens identificados', 0)),
        '1b': d['itens'],
        '7': (d['incidentes'].count('sim'), sum(l['comando'] == 'reverter' and l['resultado'] == 'ok' for l in d['log'])),
        '8a': (len(auditorias), 1),
        '8b': (sum(a['desvios tratados'] for a in auditorias), sum(a['desvios encontrados'] for a in auditorias)),
        '8c': (sum(a['restauracao'] == 'aprovada' for a in auditorias), 1),
        '9': (sum(bool(l['copia'] and l['impressao']) for l in lib), len(lib)),
    }
    hist = d['historico']
    if not hist:
        return v | dict.fromkeys(SEM_HISTORICO)
    releases = {r['etiqueta']: ler_release(r['corpo']) for r in hist['releases']}
    etiquetas = {t['nome'] for t in hist['etiquetas']}
    risco = [pr for pr in p if classificacao(pr) == 'risco']
    emergenciais = [pr for pr in p if classificacao(pr) == 'emergencial']
    baseline = [l for l in lib if SEMVER.fullmatch(l['versao']) and l['versao'] in etiquetas
                and releases.get(l['versao'], (False,))[0]]
    return v | {
        '2a': (sum(bool(revisao(pr)) for pr in p), len(p)),
        '2b': (sum(bool(revisao(pr)) for pr in risco), len(risco)),
        '3': (len(diretos), len(e)),
        '4a': (len(emergenciais), len(p)),
        '4b': (sum(aprovada_antes(pr, hist['issues']) for pr in emergenciais), len(emergenciais)),
        '5': (len(baseline), len(lib)),
        '6': (sum(bloco_completo(releases.get(l['versao'])) for l in lib), len(lib)),
    }


def planilha(tarefas):
    """Contagem da planilha manual mostrada ao lado de cada indicador."""
    def linhas(tarefa, resultado=None):
        return [l for l in tarefas if l['tarefa'] == tarefa and resultado in (None, l['resultado'])]

    def distintos(tarefa, campo, resultado=None):
        return len({l[campo] for l in linhas(tarefa, resultado) if l[campo]})

    return {
        '1': f'linhas Conferir itens de configuração: {len(linhas("Conferir itens de configuração"))}',
        '1b': '—',
        '2a': f'PRs com Revisar mudança: {distintos("Revisar mudança", "pr")}',
        '2b': f'demandas classificadas risco: {distintos("Classificar mudança", "demanda", "risco")}',
        '3': f'commits diretos citados: {len({l["commit"] for l in tarefas if l["commit"]})}',
        '4a': f'demandas classificadas emergencial: {distintos("Classificar mudança", "demanda", "emergencial")}',
        '4b': f'linhas Aprovar emergência aprovada: {len(linhas("Aprovar emergência", "aprovada"))}',
        '5': f'versões com Criar baseline: {distintos("Criar baseline", "versao")}',
        '6': f'versões com Registrar liberação: {distintos("Registrar liberação", "versao")}',
        '7': f'linhas Registrar incidente: {len(linhas("Registrar incidente"))}',
        '8a': f'linhas Registrar auditoria: {len(linhas("Registrar auditoria"))}',
        '8b': '—',
        '8c': f'linhas Testar restauração aprovada: {len(linhas("Testar restauração", "aprovada"))}',
        '9': f'versões com Liberar em produção: {distintos("Liberar em produção", "versao")}',
    }


def divergencias(d, p, diretos):
    """Divergências entre planilha, log e histórico. Só lista; nada é corrigido."""
    lista = list(d['divergencias'])
    tarefas = d['tarefas']

    def de(tarefa):
        return [l for l in tarefas if l['tarefa'] == tarefa]

    if d['historico']:
        prs = {str(pr['numero']): pr for pr in p}
        for l in de('Revisar mudança'):
            pr = prs.get(l['pr'])
            if pr and l['quem'] not in {r['autor'].lower() for r in pr['reviews']}:
                lista.append(('Revisor declarado sem review no GitHub', f'{l["origem"]}: {l["quem"]} no PR #{l["pr"]}'))
        for l in de('Classificar mudança'):
            ligados = [prs[l['pr']]] if l['pr'] in prs else [
                pr for pr in p if l['demanda'] and issue_ligada(pr['corpo']) == l['demanda']]
            for pr in ligados:
                if l['resultado'] != classificacao(pr):
                    lista.append(('Classificação diferente do rótulo', f'{l["origem"]}: planilha "{l["resultado"]}", '
                                  f'PR #{pr["numero"]} "{classificacao(pr) or "sem rótulo"}"'))
        citados = {l['pr'] for l in tarefas}
        lista += [('PR integrado sem linha na planilha', f'#{pr["numero"]}')
                  for pr in p if str(pr['numero']) not in citados]
        commits_citados = {l['commit'] for l in tarefas if l['commit']}
        lista += [('Commit direto sem linha na planilha', c['sha'][:7]) for c in diretos
                  if not any(c['sha'].startswith(x) for x in commits_citados)]
    no_log = {l['versao'] for l in d['log'] if l['comando'] == 'liberar' and l['resultado'] == 'ok' and l['versao']}
    na_planilha = {l['versao'] for l in de('Liberar em produção') if l['versao'] and l['versao'] != MARCO}
    lista += [('`liberar` no log sem linha na planilha', v) for v in sorted(no_log - na_planilha)]
    lista += [('Linha "Liberar em produção" sem `liberar` no log', v) for v in sorted(na_planilha - no_log)]
    por_pr = defaultdict(lambda: defaultdict(set))
    for l in tarefas:
        if l['pr']:
            por_pr[l['pr']][l['tarefa']].add(l['quem'])
    for pr, feitas in sorted(por_pr.items()):
        for quem in sorted(feitas['Implementar mudança'] & feitas['Revisar mudança']):
            lista.append(('Mesma pessoa em Implementar mudança e Revisar mudança', f'PR #{pr}: {quem}'))
    return sorted(lista, key=lambda x: x[0])


def caminhos(d):
    """{cenário: (previsto ou None, percorrido, faltou, a mais)}, percorrido na ordem de data e início."""
    ordem = sorted(d['tarefas'], key=lambda l: l['quando'] or '9999')
    resultado = {}
    for cenario in sorted(set(d['cenarios']) | {l['cenario'] for l in d['tarefas'] if l['cenario']}):
        feito = [l['tarefa'] for l in ordem if l['cenario'] == cenario and l['tarefa']]
        previsto = d['cenarios'].get(cenario)
        resultado[cenario] = (previsto, feito, list((Counter(previsto or []) - Counter(feito)).elements()),
                              list((Counter(feito) - Counter(previsto or [])).elements()))
    return resultado


def elementos(d, p, diretos):
    """Os cinco elementos por mudança: issue, classificação e revisão, PR, evidência de teste, versão."""
    if not d['historico']:
        return []
    commits = {c['sha']: c for c in d['historico']['commits']}
    linhas = [{'mudanca': f'PR #{pr["numero"]}', 'issue': issue_ligada(pr['corpo']), 'classificacao': classificacao(pr),
               'revisao': revisao(pr), 'evidencia': tem_evidencia(pr['corpo']),
               'versao': primeira_versao(commits[pr['merge_commit']]), 'integrado': local(pr['integrado_em'])}
              for pr in p]
    return linhas + [{'mudanca': f'commit direto {c["sha"][:7]}', 'issue': '', 'classificacao': '', 'revisao': '',
                      'evidencia': False, 'versao': primeira_versao(c), 'integrado': local(c['data'])}
                     for c in diretos]


def minutos(tarefas):
    """{(cenário, quem): minutos} nas tarefas de controle com data e horários legíveis."""
    soma = defaultdict(float)
    for l in tarefas:
        if l['tarefa'] and l['tarefa'] not in FORA_DO_CONTROLE and l['minutos'] is not None:
            soma[l['cenario'] or '—', l['quem']] += l['minutos']
    return dict(soma)


def calcular(d):
    e, p, diretos = conjuntos(d['historico'])
    lib = [l for l in d['log'] if l['comando'] == 'liberar' and l['resultado'] == 'ok']
    return {'valores': valores(d, e, p, diretos, lib), 'posteriores': sum(revisao(pr) == 'posterior' for pr in p),
            'planilha': planilha(d['tarefas']), 'divergencias': divergencias(d, p, diretos),
            'caminhos': caminhos(d), 'elementos': elementos(d, p, diretos), 'minutos': minutos(d['tarefas'])}


# ---------- saída ----------

def porcentagem(par):
    if par is None:
        return 'sem dados'
    numerador, denominador = par
    return 'sem ocorrência' if denominador == 0 else f'{100 * numerador / denominador:.1f}%'.replace('.', ',')


def minuto(valor):
    return f'{round(valor, 1):g}'.replace('.', ',')


def head(raiz):
    feito = subprocess.run(['git', '-C', str(raiz), 'rev-parse', 'HEAD'], capture_output=True,
                           encoding='utf-8', errors='replace', check=False)
    return feito.stdout.strip() if feito.returncode == 0 else 'sem commit'


def markdown(d, c):
    hist = d['historico']
    s = ['# Indicadores do piloto', '',
         f'- Gerado em: {datetime.now(FUSO):%Y-%m-%d %H:%M} (−03:00)',
         f'- Commit de `HEAD`: `{head(d["raiz"])}`']
    if hist:
        s.append(f'- Histórico: `{hist["repositorio"]}`, coletado em {local(hist["coletado_em"])} (−03:00), '
                 f'`main` em `{hist["main"][:7]}`')
    if d['faltou']:
        s.append('- Faltou: ' + ', '.join(f'`{f}`' for f in d['faltou']))
    if not hist:
        s.append('- Sem histórico: indicadores 2 a 6 sem dados e divergências com o GitHub não conferidas '
                 '(rode `python indicadores/indicadores.py coletar`)')

    s += ['', '## Divergências', '']
    s += [f'- {tipo}: {detalhe}' for tipo, detalhe in c['divergencias']] or ['Nenhuma.']

    s += ['', '## Indicadores', '',
          'E = commits de primeiro pai em `v0.1.0..main` que tocam `app/`, `infra/`, `scripts/` ou `.github/`; '
          'P = PRs integrados cujo merge commit está em E; D = E menos os merge commits de PR; '
          'Lib = linhas `liberar` com `resultado` ok no log, fora `v0.1.0`.', '',
          '| # | Indicador | Valor | Numerador | Denominador | Planilha manual | Fonte |',
          '|---|---|---|---|---|---|---|']
    for chave, nome, fonte in LINHAS:
        par = c['valores'][chave]
        numerador, denominador = par if par else ('—', '—')
        if chave == '2a' and par:
            numerador = f'{numerador} ({c["posteriores"]} só depois do merge)'
        s.append(f'| {chave} | {nome} | {porcentagem(par)} | {numerador} | {denominador} | '
                 f'{c["planilha"][chave]} | {fonte} |')
    s += ['', 'Divergências por auditoria (GCO 1): '
          + ('; '.join(f'{a["nome"]}: {a["divergencias"]}' for a in d['auditorias']) or 'nenhum registro') + '.']

    s += ['', '## Caminho percorrido × previsto', '']
    for cenario, (previsto, feito, faltou, a_mais) in c['caminhos'].items():
        s += [f'### {cenario}', '',
              '- Previsto: ' + (' → '.join(previsto) if previsto is not None else 'não consta em `cenarios.md`'),
              '- Percorrido: ' + (' → '.join(feito) or 'nenhuma tarefa na planilha')]
        if previsto is not None:
            s += ['- Faltou: ' + (', '.join(faltou) or 'nada'), '- A mais: ' + (', '.join(a_mais) or 'nada')]
        s.append('')
    if not c['caminhos']:
        s += ['Nenhum cenário em `cenarios.md` nem na planilha.', '']

    s += ['## Cinco elementos por mudança', '']
    if c['elementos']:
        s += ['| Mudança | Issue | Classificação | Revisão por outra pessoa | Evidência de teste | Versão | '
              'Integrado em (−03:00) |', '|---|---|---|---|---|---|---|']
        s += [f'| {x["mudanca"]} | {"#" + x["issue"] if x["issue"] else "—"} | {x["classificacao"] or "—"} | '
              f'{REVISAO[x["revisao"]]} | {"sim" if x["evidencia"] else "não"} | {x["versao"] or "—"} | '
              f'{x["integrado"]} |' for x in c['elementos']]
    else:
        s.append('Nenhuma mudança em caminho controlado.' if hist else 'Sem histórico.')

    s += ['', '## Minutos nas tarefas de controle', '',
          'Todas as tarefas menos Implementar mudança e Corrigir mudança; linhas sem data ou horário legível ficam fora.', '']
    pessoas = sorted({q for _, q in c['minutos']})
    if pessoas:
        s += ['| Cenário | ' + ' | '.join(pessoas) + ' | Total |', '|---' * (len(pessoas) + 2) + '|']
        for cenario in sorted({x for x, _ in c['minutos']}) + ['Total']:
            linha = [sum(m for (x, q), m in c['minutos'].items() if q == p and cenario in (x, 'Total')) for p in pessoas]
            s.append(f'| {cenario} | ' + ' | '.join(map(minuto, linha)) + f' | {minuto(sum(linha))} |')
    else:
        s.append('Nenhuma tarefa de controle com horário.')
    return '\n'.join(s) + '\n'


def gravar(raiz=RAIZ):
    d = carregar(raiz)
    marcados = [nome for nome, texto in d['textos'] if MARCA in texto]
    if marcados:
        sys.exit(f'Recusado: dado de teste ({MARCA}) em {", ".join(marcados)}. Nada foi gravado.')
    destino = raiz / 'registros' / 'indicadores.md'
    destino.parent.mkdir(exist_ok=True)
    destino.write_text(markdown(d, calcular(d)), encoding='utf-8', newline='\n')
    print(f'Gravado {destino}')


# ---------- coleta (rede) ----------

def rodar(*comando, raiz=RAIZ):
    feito = subprocess.run(comando, cwd=raiz, capture_output=True, encoding='utf-8', errors='replace', check=False)
    if feito.returncode:
        sys.exit(f'Falhou: {" ".join(comando)}\n{feito.stderr.strip()}')
    return feito.stdout


def gh_lista(repo, caminho, filtro):
    """Uma chamada `gh api --paginate`; cada item volta numa linha JSON."""
    saida = rodar('gh', 'api', '--paginate', f'repos/{repo}/{caminho}', '--jq', f'.[] | {filtro} | tojson')
    return [json.loads(l) for l in saida.splitlines() if l.strip()]


def coletar(raiz=RAIZ):
    origem = rodar('git', 'remote', 'get-url', 'origin', raiz=raiz).strip()
    achado = re.search(r'github\.com[:/](.+?/.+?)(?:\.git)?/?$', origem)
    if not achado:
        sys.exit(f'origin não é um repositório do GitHub: {origem}')
    repo = achado[1]
    rodar('git', 'fetch', '--quiet', '--tags', 'origin', raiz=raiz)
    saida = rodar('git', '-c', 'core.quotepath=false', 'log', '--first-parent', '--diff-merges=first-parent',
                  '--name-only', '--format=%x1e%H%x1f%P%x1f%an%x1f%cI%x1f%s', f'{MARCO}..origin/main', raiz=raiz)
    commits = []
    for bloco in saida.split('\x1e')[1:]:
        cabeca, _, arquivos = bloco.partition('\n')
        sha, pais, autor, data, assunto = cabeca.split('\x1f')
        commits.append({'sha': sha, 'pais': pais.split(), 'autor': autor, 'data': data, 'assunto': assunto,
                        'arquivos': [a for a in arquivos.splitlines() if a],
                        'versoes': rodar('git', 'tag', '--contains', sha, '--list', 'v*', raiz=raiz).split()})
    shas = {c['sha'] for c in commits}
    falas = '{autor: (.user.login // ""), em: .created_at, corpo: (.body // "")}'
    prs = [pr for pr in gh_lista(repo, 'pulls?state=closed&per_page=100',
                                 'select(.merged_at) | {numero: .number, autor: (.user.login // ""), titulo: .title, '
                                 'corpo: (.body // ""), rotulos: [.labels[].name], criado_em: .created_at, '
                                 'integrado_em: .merged_at, merge_commit: .merge_commit_sha}')
           if pr['merge_commit'] in shas]
    issues = {}
    for pr in prs:
        n = pr['numero']
        pr['commits'] = gh_lista(repo, f'pulls/{n}/commits?per_page=100', '{sha, data: .commit.committer.date}')
        pr['reviews'] = gh_lista(repo, f'pulls/{n}/reviews?per_page=100',
                                 'select(.state != "PENDING") | {autor: (.user.login // ""), estado: .state, '
                                 'em: .submitted_at, corpo: (.body // "")}')
        pr['comentarios'] = gh_lista(repo, f'issues/{n}/comments?per_page=100', falas)
        issue = issue_ligada(pr['corpo'])
        if issue and issue not in issues:
            issues[issue] = gh_lista(repo, f'issues/{issue}/comments?per_page=100', falas)
    releases = gh_lista(repo, 'releases?per_page=100', 'select(.draft | not) | {etiqueta: .tag_name, '
                        'corpo: (.body // ""), publicada_em: .published_at}')
    etiquetas = []
    for linha in rodar('git', 'for-each-ref', 'refs/tags', '--format=%(refname:short)%09%(*objectname)%09%(objectname)',
                       raiz=raiz).splitlines():
        nome, apontado, objeto = linha.split('\t')
        etiquetas.append({'nome': nome, 'commit': apontado or objeto})
    historico = {'repositorio': repo, 'coletado_em': datetime.now(FUSO).isoformat(timespec='seconds'),
                 'main': rodar('git', 'rev-parse', 'origin/main', raiz=raiz).strip(), 'marco': MARCO,
                 'commits': commits, 'prs': prs, 'issues': issues, 'etiquetas': etiquetas, 'releases': releases}
    destino = raiz / 'registros' / 'historico.json'
    destino.parent.mkdir(exist_ok=True)
    destino.write_text(json.dumps(historico, ensure_ascii=False, indent=1) + '\n', encoding='utf-8', newline='\n')
    print(f'Gravado {destino}: {len(commits)} commits de primeiro pai, {len(prs)} PRs integrados, '
          f'{len(releases)} Releases, {len(etiquetas)} etiquetas.')


# ---------- autoteste ----------

def autoteste():
    d = carregar(EXEMPLO)
    c = calcular(d)
    assert d['faltou'] == [], d['faltou']
    assert c['valores'] == {
        '1': (8, 10), '1b': (2, 4), '2a': (4, 5), '2b': (0, 1), '3': (2, 7), '4a': (2, 5), '4b': (1, 2),
        '5': (4, 5), '6': (3, 5), '7': (1, 1), '8a': (1, 1), '8b': (0, 0), '8c': (0, 1), '9': (2, 5),
    }, c['valores']
    assert c['posteriores'] == 1
    tipos = Counter(tipo for tipo, _ in c['divergencias'])
    assert tipos == {
        'Revisor declarado sem review no GitHub': 1, 'Classificação diferente do rótulo': 1,
        'PR integrado sem linha na planilha': 1, 'Commit direto sem linha na planilha': 1,
        '`liberar` no log sem linha na planilha': 1, 'Linha "Liberar em produção" sem `liberar` no log': 1,
        'Mesma pessoa em Implementar mudança e Revisar mudança': 1, 'Valor fora da lista fechada': 3,
        'Linha ilegível': 2,
    }, tipos
    detalhes = dict(c['divergencias'])
    assert detalhes['PR integrado sem linha na planilha'] == '#8'
    assert detalhes['Commit direto sem linha na planilha'] == 'e3e3e3e'  # d1d1d1d citado como `commit d1d1d1d`
    assert any(x.endswith('pr "1,20e+08"') for t, x in c['divergencias'] if t == 'Linha ilegível')
    assert detalhes['`liberar` no log sem linha na planilha'] == 'v0.5.0'  # v0.6.0 só tem `liberar` recusado
    assert any('cenario ""' in x for t, x in c['divergencias'] if t == 'Valor fora da lista fechada')
    assert next(l for l in d['tarefas'] if l['tarefa'] == 'Executar script avulso')['cenario'] == ''

    # leitor tolerante: cp1252 com `;` e datas AAAA-MM-DD; UTF-8 com BOM, `,`, DD/MM/AAAA e segundos
    assert b'\xe7' in (EXEMPLO / 'registros' / 'tarefas-autor-a.csv').read_bytes()
    assert (EXEMPLO / 'registros' / 'tarefas-autor-b.csv').read_bytes().startswith(b'\xef\xbb\xbf')
    assert Counter(l['origem'].split(':')[0] for l in d['tarefas']) == {'tarefas-autor-a.csv': 17,
                                                                        'tarefas-autor-b.csv': 14}
    diretos = [(l['commit'], l['pr'], l['quando']) for l in d['tarefas'] if l['commit']]  # data com hora (Excel)
    assert diretos == [('d1d1d1d', '', '2026-11-12T18:30:00'), ('d1d1d1d', '', '2026-11-12T19:10:00')], diretos
    a = next(l for l in d['tarefas'] if l['pr'] == '4' and l['tarefa'] == 'Classificar mudança')
    assert (a['papel'], a['resultado']) == ('Desenvolvedor(a)', 'normal'), a
    b = next(l for l in d['tarefas'] if l['quem'] == 'ficticio-b' and l['tarefa'] == 'Revisar mudança')
    assert (b['pr'], b['resultado'], b['quando'], b['minutos']) == ('2', 'aprovada', '2026-11-12T09:50:00', 10.0), b

    assert sum(c['minutos'].values()) == 177 and c['minutos']['C1', 'ficticio-a'] == 25, c['minutos']
    assert c['planilha']['3'] == 'commits diretos citados: 1'
    assert c['minutos']['C5', 'ficticio-a'] == 65 and c['minutos']['—', 'ficticio-b'] == 7, c['minutos']
    assert c['caminhos']['C1'][2] == ['Implantar em homologação', 'Criar baseline']
    assert c['caminhos']['C4'][2:] == (['Registrar demanda'], ['Liberar em produção'])
    assert c['caminhos']['C5'][0] is None
    assert c['caminhos']['C3'][2:] == ([], ['Submeter pull request', 'Verificar baselines'])
    e = {x['mudanca']: x for x in c['elementos']}
    assert [e[f'PR #{n}']['evidencia'] for n in (2, 4, 6, 8, 10)] == [True, False, True, True, False]
    assert [e[f'PR #{n}']['revisao'] for n in (2, 4, 6, 8, 10)] == ['sim', '', 'posterior', 'sim', 'sim']
    assert (e['PR #2']['versao'], e['PR #10']['versao'], e['PR #10']['issue']) == ('v0.2.0', '', '')
    assert e['commit direto d1d1d1d']['versao'] == 'v0.3.0' and e['commit direto e3e3e3e']['versao'] == ''

    assert local('2026-11-12T12:00:00Z') == '2026-11-12 09:00'
    assert porcentagem((0, 0)) == 'sem ocorrência' and porcentagem((1, 6)) == '16,7%'
    texto = markdown(d, c)
    assert '| 8b | GCO 5 — Desvios tratados | sem ocorrência |' in texto and '| 3 | GCO 2 — Mudanças diretas | 28,6% |' in texto

    sem_historico = dict(d, historico=None)
    cs = calcular(sem_historico)
    assert cs['valores']['2a'] is None and cs['valores']['9'] == (2, 5)
    assert 'sem dados' in markdown(sem_historico, cs)
    vazio = carregar(EXEMPLO / 'nao-existe')
    cv = calcular(vazio)
    assert 'registros/historico.json' in vazio['faltou'] and cv['valores']['9'] == (0, 0)
    assert '| 9 | GCO 5 — Backup | sem ocorrência |' in markdown(vazio, cv)

    try:
        gravar(EXEMPLO)
    except SystemExit as erro:
        assert MARCA in str(erro)
    else:
        raise AssertionError('gravou indicadores com dado FICTICIO')
    assert not (EXEMPLO / 'registros' / 'indicadores.md').exists()
    print(f'autoteste ok: 14 valores dos 9 indicadores, {len(c["divergencias"])} divergencias de '
          f'{len(tipos)} tipos, recusa de dado {MARCA}; nada gravado em registros/.')


if __name__ == '__main__':
    modo = sys.argv[1:]
    if not modo:
        gravar()
    elif modo == ['coletar']:
        coletar()
    elif modo == ['autoteste']:
        autoteste()
    else:
        sys.exit('Uso: python indicadores/indicadores.py [coletar | autoteste]')
