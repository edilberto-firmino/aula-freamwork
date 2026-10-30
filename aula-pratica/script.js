'use strict';

document.addEventListener('DOMContentLoaded', function () {
  var menuBtn = document.getElementById('menuBtn');
  var menu = document.getElementById('menu');
  var buscaBtn = document.getElementById('buscaBtn');
  var modalBusca = document.getElementById('modalBusca');
  var fecharBusca = document.getElementById('fecharBusca');
  var campoBusca = document.getElementById('campoBusca');
  var resultadoBusca = document.getElementById('resultadoBusca');

  if (menuBtn && menu) {
    menuBtn.addEventListener('click', function () {
      menu.classList.toggle('aberto');
    });
  }

  function abrirModal() {
    if (!modalBusca) return;

    modalBusca.classList.add('aberto');
    modalBusca.setAttribute('aria-hidden', 'false');

    if (campoBusca) {
      campoBusca.focus();
    }
  }

  function fecharModal() {
    if (!modalBusca) return;

    modalBusca.classList.remove('aberto');
    modalBusca.setAttribute('aria-hidden', 'true');
  }

  if (buscaBtn) {
    buscaBtn.addEventListener('click', abrirModal);
  }

  if (fecharBusca) {
    fecharBusca.addEventListener('click', fecharModal);
  }

  if (modalBusca) {
    modalBusca.addEventListener('click', function (evento) {
      if (evento.target === modalBusca) {
        fecharModal();
      }
    });
  }

  if (campoBusca && resultadoBusca) {
    campoBusca.addEventListener('input', function () {
      var termo = campoBusca.value.trim();

      if (termo !== '') {
        resultadoBusca.textContent = 'Busca simulada por: "' + termo + '"';
      } else {
        resultadoBusca.textContent = 'Digite um termo para simular uma busca.';
      }
    });
  }

  document.addEventListener('keydown', function (evento) {
    if (evento.key === 'Escape') {
      fecharModal();
    }
  });
});
