// global
var value1 = "2209-05"
var value2 = "latest";
var start_point = 1;
var stop_point = 1000;
var max_num = 0;

function draw_common(){
    var plotdata = document.getElementById('plotimg');
    var send_data = JSON.stringify({func: value1, mode: value2, start_point: start_point, stop_point:stop_point});
    
    $.ajax({
        method: "POST",
        url: "/plot",
        data: send_data,
        contentType: "application/json"
    })
    .done(function(data) {
        plotdata.src = "data:image/png:base64," + data;
    })
    print_sample(value1);
}

function drawGraph(obj) {
    var idx = obj.selectedIndex;
    value1 = obj.options[idx].value;
    draw_common();
};

function drawGraph2(obj) {
    var idx = obj.selectedIndex;
    value2 = obj.options[idx].value;
    draw_common();

};

function print_sample(value){
    var send_data = JSON.stringify({func: value1, mode: value2, start_point: start_point, stop_point:stop_point});
    $.ajax({
        method: "POST",
        url: "/sample",
        data: send_data,
        contentType: "application/json"
    })
    .done(function(data) {
        
        $("#sample").text(data.sample);
        $("#start_time").text(data.start_time);
        $("#stop_time").text(data.stop_time);
        max_num = data.max_num;

        let element = document.getElementById("text2");
        if (parseInt(element.value) > parseInt(max_num)){
            element.value = max_num;
        }
    });
}

function botton(){
    $(function() {
        $('#button1').click(function(e) {
            e.preventDefault();  // ボタン押下時の動作を抑制
            start_point = $('#text1').val();
            stop_point = $('#text2').val();
            draw_common();
        }); 
    });
}