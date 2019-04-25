function myFunction() {
  // Obtém o conteúdo
  // var txt = $(this).val();

  var lista = $('#txt_area').val();

  $.ajax({
      type: 'POST',
      url: '/analisa_cardapio',
      data: {'txt': lista.replace('[','').replace(']','').replace(',',' ')},
      success: retorno_ajax
  });
}

function botaoClicado(){
    var lista = []
    var vazio = false;
    var cardapio = $('#pratobase1').val() + ' ' + $('#pratobase2').val() + ' ' +
    $('#pratoprincipal').val() + ' ' + $('#guarnicao').val() + ' ' +
    $('#salada1').val() + ' ' + $('#salada2').val() + ' ' + $('#salada3').val() + ' ' +
    $('#sobremesa').val() + ' ' + $('#picker').val();

    lista.push($('#pratobase1').val().trim());
    lista.push($('#pratobase2').val().trim());
    lista.push($('#pratoprincipal').val().trim());
    lista.push($('#guarnicao').val().trim());
    lista.push($('#salada1').val().trim());
    lista.push($('#salada2').val().trim());
    lista.push($('#salada3').val().trim());
    lista.push($('#sobremesa').val().trim());
    lista.push($('#picker').val().trim());

    for(item in lista){
      if(lista[item] === ""){
        vazio = true;
      }
    }
    if(vazio == true){
      alert('Atenção. Há campos sem preenchimento!');
    } else {
      alert('Atenção. Há campos com preenchimento!');
      myFunction();
    }
  }
$(document).ready(function() {
    $('select').material_select();
    $('.datepicker').pickadate({
      selectMonths: true,
      selectYears: 15,
      labelMonthNext: 'Próximo mês',
      labelMonthPrev: 'Mês anterior',
      labelMonthSelect: 'Selecione o mês',
      labelYearSelect: 'Selecione o ano',
      monthsFull: [ 'Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro' ],
      monthsShort: [ 'Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez' ],
      weekdaysFull: [ 'Domingo', 'Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado' ],
      weekdaysShort: [ 'Dom', 'Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sab' ],
      weekdaysLetter: [ 'D', 'S', 'T', 'Q', 'Q', 'S', 'S' ],
      today: 'Hoje',
      clear: 'Limpar',
      close: 'Fechar',
      format: 'dd-mm-yyyy'
    });
});

// Aguarda a página carregar
function retorno_ajax(resp){
    resp = JSON.parse(resp);
    document.getElementById("barra").style.width = resp['proba'] * 100 + "%";
    new Chart($('#chart'), {
        type: 'bar',
        data: {
          labels: ['Cardápio aceito', 'Cardápio não aceito'],
          datasets: [
            {
              backgroundColor: ['#3cba9f', '#d50000'],
              data: [resp['proba'], 1 - resp['proba']]
            }
          ]
        },
        options: {
          legend: { display: false },
          title: {
            display: true,
            text: ''
          }
        }
    });
}
