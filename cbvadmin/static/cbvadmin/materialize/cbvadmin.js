$(document).ready(function(){
    $.extend($.fn.pickadate.defaults, {
        monthsFull: ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agusto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'],
        monthsShort: ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dec'],
        weekdaysFull: ['Domingo', 'Segunda-feira', 'Terça-feira', 'Quarta-feira', 'Quinta-feira', 'Sexta-feira', 'Sábado'],
        weekdaysShort: ['Dom', 'Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sab'],
        format: 'dd/mm/yyyy',
        onClose: function(e) {
            $(this.$node).removeClass('invalid').addClass('valid')
        }
    })
    $('.datepicker').pickadate()
    $('.button-collapse').sideNav()
    $('.right-sidenav').sideNav({edge: 'right', menuWidth: 300})
    $('select').not('.django-select2').material_select()
    $('select').not('.django-select2').on("change", function(){
        $(this).parents(".select-wrapper").addClass("valid")
    })
    $('.modal').modal()
    $('.form-submit').click(function(e){
        target = $(this).attr("href")
        $(target).submit()
        return false
    })
    $(".context-modal-trigger").each(function(i, it) {
        var mc = new Hammer(it)
        mc.on('press', function(ev) {
            $(ev.target).parents("a").siblings(".context-modal").openModal()
        })
    })

    // filter form
    $("#filter-form").submit(function(){
        $(this).find(":input").filter(function(){ return !this.value; }).attr("disabled", "disabled");
        return true;
    })

    // global search trigger
    $("#global-search input[type='search']").on("blur", function(e){
      $("#global-search").hide()
    })
    $(".trigger-global-search").click(function(e){
      $("#global-search").show()
      $("#global-search input[type='search']").focus()
      return false
    })
})
