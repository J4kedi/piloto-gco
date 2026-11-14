// Aplicação de exemplo do piloto: mural de recados (node:http + node:sqlite).
// A porta vem de PORTA (padrão 3000); o proxy de produção escolhe o slot ativo.
import { createServer } from 'node:http';
import { DatabaseSync } from 'node:sqlite';

// Variáveis de ambiente sem as quais a aplicação não está saudável: /saude responde 503.
export const EXIGIDAS = [];

export function criarServidor({ banco, commit = '', exigidas = EXIGIDAS, env = process.env }) {
  const db = new DatabaseSync(banco);
  db.exec('CREATE TABLE IF NOT EXISTS recados(id INTEGER PRIMARY KEY, texto TEXT NOT NULL, criado_em TEXT NOT NULL)');
  const inserir = db.prepare('INSERT INTO recados(texto, criado_em) VALUES (?, ?)');
  const listar = db.prepare('SELECT id, texto, criado_em FROM recados ORDER BY id');

  return createServer(async (req, res) => {
    const responder = (status, corpo) => {
      res.writeHead(status, { 'content-type': 'application/json; charset=utf-8' });
      res.end(JSON.stringify(corpo));
    };
    const rota = `${req.method} ${new URL(req.url, 'http://localhost').pathname}`;

    if (rota === 'GET /saude') {
      const faltando = exigidas.filter((nome) => !env[nome]);
      return faltando.length ? responder(503, { ok: false, faltando }) : responder(200, { ok: true });
    }
    if (rota === 'GET /versao') return responder(200, { commit });
    if (rota === 'GET /recados') return responder(200, listar.all());
    if (rota === 'POST /recados') {
      const texto = await lerTexto(req);
      if (!texto) return responder(400, { erro: 'envie {"texto":"..."} com até 10 kB' });
      const { lastInsertRowid } = inserir.run(texto, new Date().toISOString());
      return responder(201, { id: Number(lastInsertRowid) });
    }
    responder(404, { erro: 'rota inexistente' });
  });
}

async function lerTexto(req) {
  let corpo = '';
  req.setEncoding('utf8');
  for await (const pedaco of req) {
    corpo += pedaco;
    if (corpo.length > 10_000) return null;
  }
  try {
    const { texto } = JSON.parse(corpo);
    return typeof texto === 'string' && texto.trim() ? texto : null;
  } catch {
    return null;
  }
}

if (import.meta.main) {
  const servidor = criarServidor({ banco: process.env.BANCO ?? '/dados/recados.db', commit: process.env.COMMIT ?? '' });
  servidor.listen(Number(process.env.PORTA ?? 3000));
  process.on('SIGTERM', () => process.exit(0)); // node como PID 1 ignora SIGTERM sem este tratador
}
