jQuery.ajaxSettings.traditional = true;

$(document).ready(function () {
    $("#load_button").addClass("loading");
    populate();
    $("#load_button").click(function(){
        $("#load_button").addClass("loading");
        $('#stocks_view_body').empty()
        populate();
    });});

hosts_global = []

function populate(){
    $.getJSON("/stock",{},function(hosts){
        $.each(hosts, function(index, val){
            let id = Math.random().toString(36).substring(7);
            $('#stocks_view_table').append('<tr><td>'+val['name']+'</td><td>'+val['symbol']+'</td><td>'+val['value']+'</td></tr>');
        });
        $("#load_button").removeClass("loading");
    });
}
