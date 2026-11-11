// Evidência de teste dos PRs: node --test app/teste.mjs
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { criarServidor } from './servidor.mjs';

async function subir(t, opcoes = {}) {
  const servidor = criarServidor({ banco: ':memory:', commit: 'abc123', ...opcoes });
  await new Promise((pronto) => servidor.listen(0, '127.0.0.1', pronto));
  t.after(() => servidor.close());
  const base = `http://127.0.0.1:${servidor.address().port}`;
  return async (caminho, corpo) => {
    const r = await fetch(base + caminho, corpo === undefined ? {} : { method: 'POST', body: JSON.stringify(corpo) });
    return { status: r.status, json: await r.json() };
  };
}

test('saúde e versão', async (t) => {
  const pedir = await subir(t);
  assert.deepEqual(await pedir('/saude'), { status: 200, json: { ok: true } });
  assert.deepEqual(await pedir('/versao'), { status: 200, json: { commit: 'abc123' } });
});

test('recados: grava, lista em ordem e recusa texto vazio', async (t) => {
  const pedir = await subir(t);
  assert.equal((await pedir('/recados', { texto: 'primeiro' })).status, 201);
  assert.equal((await pedir('/recados', { texto: 'segundo' })).status, 201);
  assert.equal((await pedir('/recados', { texto: '  ' })).status, 400);
  const { json } = await pedir('/recados');
  assert.deepEqual(json.map((r) => [r.id, r.texto]), [[1, 'primeiro'], [2, 'segundo']]);
  assert.match(json[0].criado_em, /^\d{4}-\d{2}-\d{2}T/);
});

test('saúde 503 quando falta variável exigida', async (t) => {
  const pedir = await subir(t, { exigidas: ['CHAVE_NOVA'], env: {} });
  assert.deepEqual(await pedir('/saude'), { status: 503, json: { ok: false, faltando: ['CHAVE_NOVA'] } });
});

test('rota inexistente', async (t) => {
  const pedir = await subir(t);
  assert.equal((await pedir('/nada')).status, 404);
});
