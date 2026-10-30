import { useEffect, useRef, useState } from 'react';
import { listarAlunos } from './api.js';
import FormularioAluno from './components/FormularioAluno.jsx';
import ListaAlunos from './components/ListaAlunos.jsx';

export default function App() {
  const [alunos, setAlunos] = useState([]);
  const [carregando, setCarregando] = useState(true);
  const [erro, setErro] = useState('');
  const [filtro, setFiltro] = useState('');
  const consulta = useRef(null);

  async function atualizar() {
    consulta.current?.abort();
    const controle = new AbortController();
    consulta.current = controle;
    setCarregando(true);
    setErro('');
    try {
      const lista = await listarAlunos(controle.signal);
      if (!controle.signal.aborted) setAlunos(lista);
    } catch (falha) {
      if (!controle.signal.aborted) setErro(falha.message || 'Confira o backend.');
    } finally {
      if (!controle.signal.aborted) setCarregando(false);
    }
  }

  useEffect(() => {
    atualizar();
    return () => consulta.current?.abort();
  }, []);

  function adicionar(aluno) {
    // Uma consulta antiga não deve apagar o cadastro que acabou de chegar.
    consulta.current?.abort();
    setCarregando(false);
    setErro('');
    setAlunos(anteriores => [aluno, ...anteriores.filter(item => item.id !== aluno.id)]);
    setFiltro('');
  }

  return (
    <main>
      <header>
        <p className="etiqueta">AULA PRÁTICA 5 / REACT + API + SQLITE</p>
        <h1>Da tela ao banco.<br /><span>Agora com React.</span></h1>
        <p>Cadastre alunos, acompanhe a lista e veja seus dados persistirem.</p>
      </header>
      <div className="painel">
        <FormularioAluno aoCadastrar={adicionar} />
        <ListaAlunos alunos={alunos} carregando={carregando} erro={erro}
          atualizar={atualizar} filtro={filtro} aoFiltrar={setFiltro} />
      </div>
      <footer>React cuida da interface. Flask valida. SQLite guarda.</footer>
    </main>
  );
}
