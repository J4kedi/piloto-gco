// Ferramenta do processo de gerência de configuração do piloto.
// Uso: node scripts/gco.mjs <comando> [versão] [--notas <arquivo>] [--demanda <n>]
import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import { createHash } from 'node:crypto';
import { appendFileSync, existsSync, mkdirSync, readFileSync, rmSync, writeFileSync } from 'node:fs';
import { join, resolve } from 'node:path';
import { setTimeout as pausa } from 'node:timers/promises';
import { fileURLToPath } from 'node:url';
import { parseArgs } from 'node:util';

const RAIZ = fileURLToPath(new URL('..', import.meta.url));
const LOG = 'registros/execucoes.csv';
const CAMPOS = ['inicio', 'fim', 'comando', 'versao', 'commit', 'imagem', 'slot', 'copia', 'impressao', 'resultado', 'detalhe', 'executor'];
const SLOTS = 'infra/.slots.env';
const CONTROLADOS = ['app', 'infra', 'scripts', '.github'];
const PORTA_PROD = process.env.PORTA_PROD || '8080';
const PORTA_HOMOLOG = process.env.PORTA_HOMOLOG || '8081';
const HOMOLOG = ['compose', '-p', 'gco-homolog', '-f', 'infra/homologacao.yml'];
const prod = () => ['compose', '-p', 'gco-prod', '-f', 'infra/producao.yml', ...(existsSync(abs(SLOTS)) ? ['--env-file', SLOTS] : [])];

// ---------- funções puras (cobertas pelo autoteste) ----------

function versaoValida(texto) {
  if (!/^v\d+\.\d+\.\d+$/.test(texto ?? '')) throw new Error('informe a versão no formato vX.Y.Z (ex.: v0.2.0)');
  return texto;
}

function agora(d = new Date()) {
  const minutos = -d.getTimezoneOffset();
  const local = new Date(d.getTime() + minutos * 60_000).toISOString().slice(0, 19);
  const m = Math.abs(minutos);
  return `${local}${minutos < 0 ? '-' : '+'}${String(Math.floor(m / 60)).padStart(2, '0')}:${String(m % 60).padStart(2, '0')}`;
}

const campoCsv = (v) => (/[",\r\n]/.test(v) ? `"${v.replaceAll('"', '""')}"` : v);

function lerCsv(linha) {
  const campos = [];
  let atual = '';
  let aspas = false;
  for (let i = 0; i < linha.length; i++) {
    const c = linha[i];
    if (aspas && c === '"' && linha[i + 1] === '"') { atual += '"'; i++; }
    else if (c === '"') aspas = !aspas;
    else if (c === ',' && !aspas) { campos.push(atual); atual = ''; }
    else atual += c;
  }
  return [...campos, atual];
}

// <n linhas>:<sha256 das linhas de recados ordenadas por id>
function impressao(linhas) {
  const hash = createHash('sha256');
  for (const r of linhas) hash.update(JSON.stringify([r.id, r.texto, r.criado_em]) + '\n');
  return `${linhas.length}:${hash.digest('hex')}`;
}

function lerEnv(texto) {
  return Object.fromEntries(texto.split(/\r?\n/).filter((l) => /^\w+=/.test(l)).map((l) => [l.slice(0, l.indexOf('=')), l.slice(l.indexOf('=') + 1)]));
}

const escreverEnv = (e) => ['SLOT_ATIVO', 'IMAGEM_AZUL', 'IMAGEM_VERDE'].map((k) => `${k}=${e[k] ?? ''}`).join('\n') + '\n';
const chave = (slot) => `IMAGEM_${slot.toUpperCase()}`;
const outro = (slot) => (slot === 'azul' ? 'verde' : 'azul');

function divergencias(servicos, lista) {
  const bases = new Set(servicos.filter((s) => s && s !== 'proxy').map((s) => s.replace(/-(azul|verde)$/, '')));
  return { foraDaLista: [...bases].filter((b) => !lista.includes(b)), foraDaComposicao: lista.filter((b) => !bases.has(b)) };
}

function blocoDeLiberacao({ versao, demanda, commit, imagem, executor, fim, slot, copia, impressao, verificacao }) {
  return [
    '## Registro de liberação',
    `- Versão: ${versao}`,
    `- Demanda: #${demanda}`,
    `- Commit: ${commit}`,
    `- Imagem: ${imagem}`,
    `- Liberado por: ${executor}`,
    `- Liberado em: ${fim}`,
    `- Slot: ${slot}`,
    `- Cópia do banco: ${copia ? `${copia} (${impressao})` : 'nenhuma'}`,
    `- Resultado da verificação: ${verificacao}`,
  ].join('\n');
}

// As notas dos autores ficam acima; o bloco é sempre a última seção (substitui o anterior, se houver).
function comBloco(corpo, bloco) {
  const i = corpo.search(/^## Registro de liberação\s*$/m);
  const notas = (i < 0 ? corpo : corpo.slice(0, i)).trimEnd();
  return [notas, bloco].filter(Boolean).join('\n\n') + '\n';
}

const commitDe = (texto) => { try { return JSON.parse(texto).commit ?? ''; } catch { return ''; } };

// ---------- acesso a arquivos, processos e rede ----------

function abs(caminho) { return join(RAIZ, caminho); }

function chamar(programa, args, opcoes = {}) {
  const r = spawnSync(programa, args, { cwd: RAIZ, encoding: 'utf8', ...opcoes, env: { ...process.env, ...opcoes.env } });
  if (r.error) throw new Error(`não consegui executar ${programa} (${r.error.code}); confira se está instalado e no PATH`);
  return r;
}

function rodar(programa, args, opcoes) {
  const r = chamar(programa, args, opcoes);
  if (r.status !== 0) throw new Error(`${programa} ${args.slice(0, 2).join(' ')} falhou:\n${(r.stderr || r.stdout).trim()}`);
  return r.stdout.trimEnd();
}

function lerLog() {
  if (!existsSync(abs(LOG))) return [];
  return readFileSync(abs(LOG), 'utf8').split(/\r?\n/).slice(1).filter(Boolean)
    .map((linha) => { const v = lerCsv(linha); return Object.fromEntries(CAMPOS.map((c, i) => [c, v[i] ?? ''])); });
}

function ultima(comando, versao, resultado) {
  return lerLog().filter((l) => l.comando === comando && (!versao || l.versao === versao) && (!resultado || l.resultado === resultado)).at(-1);
}

function anotar(linha) {
  if (!existsSync(abs(LOG))) { mkdirSync(abs('registros'), { recursive: true }); writeFileSync(abs(LOG), CAMPOS.join(',') + '\n'); }
  appendFileSync(abs(LOG), CAMPOS.map((c) => campoCsv(String(linha[c] ?? ''))).join(',') + '\n');
}

const lerEstado = () => (existsSync(abs(SLOTS)) ? lerEnv(readFileSync(abs(SLOTS), 'utf8')) : {});

// Grava o novo estado dos slots antes de chamar o compose (que o lê) e devolve o anterior se o compose falhar.
function comEstado(novo, fn) {
  const antes = existsSync(abs(SLOTS)) ? readFileSync(abs(SLOTS), 'utf8') : null;
  writeFileSync(abs(SLOTS), escreverEnv(novo));
  try { return fn(); } catch (erro) {
    if (antes === null) rmSync(abs(SLOTS)); else writeFileSync(abs(SLOTS), antes);
    throw erro;
  }
}

function repo() {
  const url = rodar('git', ['remote', 'get-url', 'origin']);
  const m = url.match(/github\.com[:/](.+?)(?:\.git)?\/?$/);
  if (!m) throw new Error(`o origin (${url}) não é um repositório do GitHub`);
  return m[1];
}

function conteinerDe(projeto, servico, dica) {
  const id = rodar('docker', ['ps', '-a', '-q', '--filter', `label=com.docker.compose.project=${projeto}`, '--filter', `label=com.docker.compose.service=${servico}`]);
  if (!id) throw new Error(`não existe contêiner ${servico} em ${projeto}; ${dica}`);
  return id.split('\n')[0];
}

function idDaImagem(ref, dica) {
  const r = chamar('docker', ['image', 'inspect', '--format', '{{.Id}}', ref]);
  if (r.status !== 0) throw new Error(`a imagem ${ref} não existe nesta máquina; ${dica}`);
  return r.stdout.trim();
}

const listaDaLiberacao = () => readFileSync(abs('infra/servicos-da-liberacao.txt'), 'utf8').split(/\r?\n/).map((s) => s.trim()).filter(Boolean);

async function ler(url) {
  try {
    const r = await fetch(url, { signal: AbortSignal.timeout(3000) });
    return { status: r.status, texto: await r.text() };
  } catch {
    return { status: 0, texto: '' };
  }
}

// Espera até ~10 s por /saude 200 e (se informado) /versao igual ao commit.
async function conferir(base, commit) {
  let resumo = '';
  for (let tentativa = 0; tentativa < 20; tentativa++) {
    const versao = await ler(`${base}/versao`);
    const saude = await ler(`${base}/saude`);
    const obtido = commitDe(versao.texto);
    resumo = `/versao ${obtido ? obtido.slice(0, 7) : 'sem resposta'}; /saude ${saude.status || 'sem resposta'}`;
    if ((!commit || obtido === commit) && saude.status === 200) return resumo;
    await pausa(500);
  }
  throw new Error(`${base} não confere${commit ? ` com o commit ${commit.slice(0, 7)}` : ''} (${resumo})`);
}

// Slot sem porta publicada: pergunta /versao de dentro do contêiner.
async function conferirSlot(conteiner, commit) {
  let obtido = '';
  for (let tentativa = 0; tentativa < 20; tentativa++) {
    const r = chamar('docker', ['exec', conteiner, 'node', '-e', "fetch('http://127.0.0.1:3000/versao').then((r) => r.text()).then(console.log)"]);
    obtido = commitDe(r.stdout);
    if (obtido === commit) return;
    await pausa(500);
  }
  throw new Error(`o slot não respondeu /versao com o commit ${commit.slice(0, 7)} (obtido: ${obtido.slice(0, 7) || 'sem resposta'})`);
}

// O compose não recria o proxy quando só o conteúdo do config muda; por isso --force-recreate.
function apontarProxy(estado, slot) {
  comEstado({ ...estado, SLOT_ATIVO: slot }, () => rodar('docker', [...prod(), 'up', '-d', '--force-recreate', 'proxy']));
}

// VACUUM INTO dentro do contêiner e docker cp para o host.
function copiarBanco(conteiner, destino) {
  const codigo = "require('node:fs').rmSync('/tmp/copia.db', { force: true }); new (require('node:sqlite').DatabaseSync)(process.env.BANCO).exec(\"VACUUM INTO '/tmp/copia.db'\")";
  rodar('docker', ['exec', conteiner, 'node', '--disable-warning=ExperimentalWarning', '-e', codigo]);
  mkdirSync(abs('copias'), { recursive: true });
  rodar('docker', ['cp', `${conteiner}:/tmp/copia.db`, destino]);
}

async function impressaoDoBanco(arquivo) {
  const { DatabaseSync } = await import('node:sqlite');
  const db = new DatabaseSync(abs(arquivo), { readOnly: true });
  try { return impressao(db.prepare('SELECT id, texto, criado_em FROM recados ORDER BY id').all()); } finally { db.close(); }
}

// ---------- comandos que alteram estado (cada um grava uma linha no log) ----------

async function homologar(l) {
  const sujos = rodar('git', ['status', '--porcelain', '--', ...CONTROLADOS]);
  if (sujos) throw new Error(`há alteração não commitada em caminho controlado; faça commit ou descarte antes:\n${sujos}`);
  l.commit = rodar('git', ['rev-parse', 'HEAD']);
  const imagem = `exemplo-gco:${l.commit.slice(0, 7)}`;
  console.log(`Construindo ${imagem}...`);
  rodar('docker', ['build', '-t', imagem, '--build-arg', `COMMIT=${l.commit}`, 'app']);
  l.imagem = idDaImagem(imagem, 'o build falhou');
  rodar('docker', [...HOMOLOG, 'up', '-d'], { env: { IMAGEM_HOMOLOG: imagem } });
  l.detalhe = `${imagem} em homologação: ${await conferir(`http://localhost:${PORTA_HOMOLOG}`, l.commit)}`;
}

async function baseline(l, versao, { notas }) {
  l.versao = versaoValida(versao);
  if (!notas || !existsSync(notas) || !readFileSync(notas, 'utf8').trim()) throw new Error('informe --notas <arquivo> com as notas da versão escritas pelos autores');
  // A baseline é do commit homologado; commits só em caminhos livres depois dele não impedem.
  const h = ultima('homologar', '', 'ok');
  if (!h) throw new Error('não há homologação ok no log; rode homologar antes');
  l.commit = h.commit;
  const diff = chamar('git', ['diff', '--quiet', l.commit, 'HEAD', '--', ...CONTROLADOS]);
  if (diff.status === 1) throw new Error(`há mudança em caminho controlado entre o commit homologado (${l.commit.slice(0, 7)}) e o HEAD; rode homologar de novo`);
  if (diff.status !== 0) throw new Error(`git diff falhou:\n${diff.stderr.trim()}`);
  l.imagem = rodar('docker', ['inspect', '--format', '{{.Image}}', conteinerDe('gco-homolog', 'app', 'rode homologar')]);
  if (l.imagem !== h.imagem) throw new Error('a imagem em homologação não é a que homologar conferiu; rode homologar de novo');
  if (rodar('git', ['tag', '-l', l.versao])) throw new Error(`a etiqueta ${l.versao} já existe; escolha outra versão`);
  rodar('docker', ['tag', l.imagem, `exemplo-gco:${l.versao}`]);
  rodar('git', ['tag', '-a', l.versao, '-m', `Baseline ${l.versao}`, l.commit]);
  rodar('git', ['push', 'origin', l.versao]);
  rodar('gh', ['release', 'create', l.versao, '-R', repo(), '--verify-tag', '--title', l.versao, '--notes-file', resolve(notas)]);
  l.detalhe = `etiqueta, Release e exemplo-gco:${l.versao} criadas`;
}

async function liberar(l, versao) {
  l.versao = versaoValida(versao);
  const b = ultima('baseline', l.versao, 'ok');
  if (!b) throw new Error(`não há baseline ok de ${l.versao} no log; rode baseline ${l.versao} --notas <arquivo>`);
  l.commit = b.commit;
  const imagem = `exemplo-gco:${l.versao}`;
  l.imagem = idDaImagem(imagem, `ela é criada por baseline ${l.versao}`);
  if (l.imagem !== b.imagem) {
    throw new Error(`${imagem} não é a imagem gravada na baseline (${b.imagem.slice(7, 19)} ≠ ${l.imagem.slice(7, 19)}); a imagem foi reconstruída: homologue e crie uma nova versão`);
  }
  if (!existsSync(abs('infra/producao.env'))) throw new Error('falta infra/producao.env; copie infra/producao.env.exemplo e preencha');
  const estado = lerEstado();
  const ativo = estado.SLOT_ATIVO;
  l.slot = ativo ? outro(ativo) : 'azul';
  if (ativo) {
    l.copia = `copias/antes-${l.versao}.db`;
    copiarBanco(conteinerDe('gco-prod', `app-${ativo}`, 'o slot ativo sumiu; rode situacao'), l.copia);
    l.impressao = await impressaoDoBanco(l.copia);
  }
  const servicos = listaDaLiberacao().map((nome) => `${nome}-${l.slot}`);
  comEstado({ ...estado, [chave(l.slot)]: imagem }, () => rodar('docker', [...prod(), 'up', '-d', '--pull', 'never', ...servicos]));
  await conferirSlot(conteinerDe('gco-prod', `app-${l.slot}`, 'o compose não criou o slot'), l.commit);
  l.detalhe = `${servicos.join(' ')} no ar com ${imagem}; slot ativo continua ${ativo || 'nenhum'}`;
}

async function ativar(l, versao) {
  l.versao = versaoValida(versao);
  const lib = ultima('liberar', l.versao);
  if (lib?.resultado !== 'ok') throw new Error(`a última liberação de ${l.versao} não está ok; rode liberar ${l.versao}`);
  const estado = lerEstado();
  l.slot = lib.slot;
  if (estado[chave(l.slot)] !== `exemplo-gco:${l.versao}`) throw new Error(`o slot ${l.slot} não tem mais ${l.versao}; rode liberar ${l.versao}`);
  Object.assign(l, { commit: lib.commit, imagem: lib.imagem });
  apontarProxy(estado, l.slot);
  l.detalhe = `proxy aponta para app-${l.slot}`;
}

async function verificar(l, versao) {
  l.versao = versaoValida(versao);
  l.commit = rodar('git', ['rev-parse', `${l.versao}^{commit}`]);
  l.imagem = ultima('liberar', l.versao, 'ok')?.imagem ?? '';
  l.slot = lerEstado().SLOT_ATIVO ?? '';
  l.detalhe = await conferir(`http://localhost:${PORTA_PROD}`, l.commit);
}

async function registrar(l, versao, { demanda }) {
  l.versao = versaoValida(versao);
  if (!/^\d+$/.test(demanda ?? '')) throw new Error('informe --demanda <número da issue>');
  const lib = ultima('liberar', l.versao, 'ok');
  if (!lib) throw new Error(`não há liberação ok de ${l.versao} no log`);
  const ver = ultima('verificar', l.versao);
  if (!ver) throw new Error(`não há verificação de ${l.versao} no log; rode verificar ${l.versao}`);
  Object.assign(l, { commit: lib.commit, imagem: lib.imagem, slot: lib.slot, copia: lib.copia, impressao: lib.impressao });
  const verificacao = ver.resultado === 'ok' ? 'sem falha' : 'com falha';
  const bloco = blocoDeLiberacao({ ...lib, demanda, verificacao });
  const r = repo();
  const corpo = rodar('gh', ['api', `repos/${r}/releases/tags/${l.versao}`, '--jq', '.body']);
  rodar('gh', ['release', 'edit', l.versao, '-R', r, '--notes-file', '-'], { input: comBloco(corpo, bloco) });
  l.detalhe = `demanda #${demanda}; verificação ${verificacao}`;
}

async function reverter(l) {
  const estado = lerEstado();
  const de = estado.SLOT_ATIVO;
  if (!de) throw new Error('não há slot ativo; nada a reverter');
  const para = outro(de);
  const rodando = chamar('docker', ['ps', '-q', '--filter', 'label=com.docker.compose.project=gco-prod', '--filter', `label=com.docker.compose.service=app-${para}`]).stdout.trim();
  if (!estado[chave(para)] || !rodando) throw new Error(`o slot ${para} não está no ar; não há versão anterior para onde voltar`);
  // A linha registra a versão retirada; o slot é o que volta a receber tráfego.
  l.versao = estado[chave(de)].split(':')[1];
  const lib = ultima('liberar', l.versao, 'ok');
  Object.assign(l, { commit: lib?.commit ?? '', imagem: lib?.imagem ?? '', slot: para });
  apontarProxy(estado, para);
  l.detalhe = `proxy voltou de ${de} (${l.versao}) para ${para} (${estado[chave(para)].split(':')[1]})`;
}

async function restaurar(l, versao) {
  l.versao = versaoValida(versao);
  const lib = ultima('liberar', l.versao, 'ok');
  if (!lib?.copia) throw new Error(`a liberação de ${l.versao} não gravou cópia do banco (a primeira liberação não tem)`);
  if (!existsSync(abs(lib.copia))) throw new Error(`não encontrei ${lib.copia} nesta máquina`);
  l.copia = lib.copia;
  const conteiner = conteinerDe('gco-homolog', 'app', 'rode homologar antes');
  l.imagem = rodar('docker', ['inspect', '--format', '{{.Image}}', conteiner]);
  rodar('docker', ['stop', conteiner]);
  rodar('docker', ['cp', l.copia, `${conteiner}:/dados/recados.db`]);
  rodar('docker', ['start', conteiner]);
  await conferir(`http://localhost:${PORTA_HOMOLOG}`);
  const devolvida = `copias/restaurada-${l.versao}.db`;
  copiarBanco(conteiner, devolvida);
  l.impressao = await impressaoDoBanco(devolvida);
  if (l.impressao !== lib.impressao) throw new Error(`impressão digital diferente: gravada ${lib.impressao}, obtida ${l.impressao}`);
  l.detalhe = `${l.copia} restaurada em homologação; impressão igual à gravada`;
}

// ---------- comandos de consulta ----------

function situacao() {
  const estado = lerEstado();
  const descrever = (projeto, servico) => chamar('docker', ['ps', '-a', '--filter', `label=com.docker.compose.project=${projeto}`, '--filter', `label=com.docker.compose.service=${servico}`, '--format', '{{.Image}} ({{.State}})']).stdout.trim() || 'sem contêiner';
  console.log(`Slot ativo: ${estado.SLOT_ATIVO || 'nenhum'}`);
  for (const slot of ['azul', 'verde']) console.log(`  ${slot}: ${descrever('gco-prod', `app-${slot}`)}`);
  console.log(`Homologação: ${descrever('gco-homolog', 'app')}`);
  const login = chamar('gh', ['api', 'user', '--jq', '.login']);
  console.log(`Login do gh: ${login.status === 0 ? login.stdout.trim() : 'sem login (rode gh auth login)'}`);
  const servicos = rodar('docker', [...prod(), 'config', '--services']).split(/\r?\n/).sort();
  const { foraDaLista, foraDaComposicao } = divergencias(servicos, listaDaLiberacao());
  console.log(`Serviços em infra/producao.yml: ${servicos.join(', ')}`);
  console.log(`Lista da liberação (infra/servicos-da-liberacao.txt): ${listaDaLiberacao().join(', ')}`);
  if (!foraDaLista.length && !foraDaComposicao.length) console.log('Divergências: nenhuma');
  for (const s of foraDaLista) console.log(`Divergência: ${s} está na composição de produção e fora da lista da liberação`);
  for (const s of foraDaComposicao) console.log(`Divergência: ${s} está na lista da liberação e fora da composição de produção`);
}

function autoteste() {
  assert.equal(versaoValida('v0.10.2'), 'v0.10.2');
  for (const ruim of ['0.1.0', 'v1.2', 'v1.2.3-rc', undefined]) assert.throws(() => versaoValida(ruim));

  assert.match(agora(), /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}[+-]\d{2}:\d{2}$/);
  const d = new Date('2026-11-12T22:03:11Z');
  assert.equal(Date.parse(agora(d)), d.getTime());

  const campos = ['a', 'tem, vírgula', 'tem "aspas"', ''];
  assert.deepEqual(lerCsv(campos.map(campoCsv).join(',')), campos);

  const recados = [{ id: 1, texto: 'a', criado_em: 't1' }, { id: 2, texto: 'b', criado_em: 't2' }];
  assert.equal(impressao([]), '0:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855');
  assert.match(impressao(recados), /^2:[0-9a-f]{64}$/);
  assert.equal(impressao(recados), impressao(recados.map((r) => ({ ...r }))));
  assert.notEqual(impressao(recados), impressao([recados[0], { ...recados[1], texto: 'B' }]));

  const env = { SLOT_ATIVO: 'verde', IMAGEM_AZUL: 'exemplo-gco:v0.1.0', IMAGEM_VERDE: 'exemplo-gco:v0.2.0' };
  assert.deepEqual(lerEnv(escreverEnv(env)), env);
  assert.deepEqual(lerEnv('# comentário\r\nSLOT_ATIVO=\r\n'), { SLOT_ATIVO: '' });
  assert.equal(outro('azul'), 'verde');
  assert.equal(outro('verde'), 'azul');

  assert.deepEqual(divergencias(['app-azul', 'app-verde', 'proxy'], ['app']), { foraDaLista: [], foraDaComposicao: [] });
  assert.deepEqual(divergencias(['app-azul', 'app-verde', 'fila-azul', 'fila-verde', 'proxy'], ['app']), { foraDaLista: ['fila'], foraDaComposicao: [] });
  assert.deepEqual(divergencias(['app-azul', 'app-verde', 'proxy'], ['app', 'fila']), { foraDaLista: [], foraDaComposicao: ['fila'] });

  const bloco = blocoDeLiberacao({ versao: 'v0.2.0', demanda: '12', commit: 'c', imagem: 'sha256:i', executor: 'login', fim: 'f', slot: 'verde', copia: 'copias/antes-v0.2.0.db', impressao: '5:ab', verificacao: 'sem falha' });
  assert.ok(bloco.startsWith('## Registro de liberação\n- Versão: v0.2.0\n- Demanda: #12\n'));
  assert.ok(bloco.includes('\n- Cópia do banco: copias/antes-v0.2.0.db (5:ab)\n'));
  assert.ok(bloco.endsWith('\n- Resultado da verificação: sem falha'));
  assert.equal(comBloco('Notas.\n', bloco), `Notas.\n\n${bloco}\n`);
  assert.equal(comBloco(`Notas.\r\n\r\n${bloco.replace('sem falha', 'com falha')}\r\n`, bloco), `Notas.\n\n${bloco}\n`);
  assert.equal(comBloco('', bloco), `${bloco}\n`);

  assert.equal(commitDe('{"commit":"abc"}'), 'abc');
  assert.equal(commitDe('<html>502</html>'), '');
  console.log('autoteste ok');
}

// ---------- entrada ----------

const ALTERAM = { homologar, baseline, liberar, ativar, verificar, registrar, reverter, restaurar };
const USO = 'Uso: node scripts/gco.mjs <homologar | baseline <versão> --notas <arquivo> | liberar <versão> | ativar <versão> | verificar <versão> | registrar <versão> --demanda <n> | reverter | restaurar <versão> | situacao | autoteste>';

async function executar(comando, fn, args) {
  const linha = { inicio: agora(), comando };
  try {
    linha.executor = rodar('gh', ['api', 'user', '--jq', '.login']);
    await fn(linha, ...args);
    linha.resultado = 'ok';
    console.log(`${comando} ok: ${linha.detalhe ?? ''}`);
  } catch (erro) {
    linha.resultado = 'falha';
    linha.detalhe = erro.message.replace(/\s+/g, ' ').slice(0, 300);
    console.error(`${comando} falhou: ${erro.message}`);
    process.exitCode = 1;
  }
  linha.fim = agora();
  anotar(linha);
}

const { positionals, values } = parseArgs({ allowPositionals: true, options: { notas: { type: 'string' }, demanda: { type: 'string' } } });
const [comando, versao] = positionals;
if (ALTERAM[comando]) await executar(comando, ALTERAM[comando], [versao, values]);
else if (comando === 'situacao') situacao();
else if (comando === 'autoteste') autoteste();
else { console.error(USO); process.exitCode = 1; }
