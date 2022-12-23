// global
var value1 = "2209-05"
var value2 = "latest";
var start_point = 1;
var stop_point = 1000;

function drawGraph(obj) {
    var idx = obj.selectedIndex;
    var value = obj.options[idx].value;
    value1 = value
    console.log("graph1="+value1)
    console.log("graph1="+value2)

    var plotdata = document.getElementById('plotimg');
    $.get("/plot/" + value1 + "_" + value2 + "_" + start_point + "_" + stop_point, function(data) {
        plotdata.src = "data:image/png:base64," + data;
    });
    draw_sample(value);
    draw_start_time(value);
    draw_stop_time(value);
};

function drawGraph2(obj) {
    var idx = obj.selectedIndex;
    value2 = obj.options[idx].value;

    console.log("graph2="+value1)
    console.log("graph2="+value2)

    var plotdata = document.getElementById('plotimg');
    $.get("/plot/" + value1 + "_" + value2 + "_" + start_point + "_" + stop_point, function(data) {
        plotdata.src = "data:image/png:base64," + data;
    });
    draw_sample(value1);
    draw_start_time(value1);
    draw_stop_time(value1);
};


function draw_sample(value){
    $.get("/sample/" + value1 + "_" + value2 + "_" + start_point + "_" + stop_point, function(data) {
        $("#sample").text(data);});
}

function draw_start_time(value){
    $.get("/start_time/" + value1 + "_" + value2 + "_" + start_point + "_" + stop_point, function(data) {
        $("#start_time").text(data);});
}

function draw_stop_time(value){
    $.get("/stop_time/" + value1 + "_" + value2 + "_" + start_point + "_" + stop_point, function(data) {
        $("#stop_time").text(data);});
}

function botton(){
    $(function() {
        $('#button1').click(function(e) {
            e.preventDefault();  // ボタン押下時の動作を抑制
            start_point = $('#text1').val();
            stop_point = $('#text2').val();
            
            var plotdata = document.getElementById('plotimg');
            $.get("/plot/" + value1 + "_" + value2 + "_" + start_point + "_" + stop_point, function(data) {
                  plotdata.src = "data:image/png:base64," + data;
            });
            draw_sample(value1);
            draw_start_time(value1);
            draw_stop_time(value1);
        }); 
    });
}