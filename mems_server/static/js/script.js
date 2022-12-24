// global
var value1 = "2209-05"
var value2 = "latest";
var start_point = 1;
var stop_point = 1000;

function draw_common(){
    var plotdata = document.getElementById('plotimg');
    var send_data = JSON.stringify({func; value1, mode: value2, start_point: start_point, stop_point:stop_point});
    
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
    console.log("graph1="+value1);
    console.log("graph1="+value2);
    draw_common();
};

function drawGraph2(obj) {
    var idx = obj.selectedIndex;
    value2 = obj.options[idx].value;
    console.log("graph2="+value1);
    console.log("graph2="+value2);
    draw_common();

};

function print_sample(value){
    var send_data = JSON.stringify({func; value1, mode: value2, start_point: start_point, stop_point:stop_point});
    $.ajax({
        method: "POST",
        url: "/sample",
        data: send_data,
        contentType: "application/json"
    })
    .done(function(data) {
        $("#sample").text(data);
        $("#start_time").text(data);
        $("#stop_time").text(data);
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