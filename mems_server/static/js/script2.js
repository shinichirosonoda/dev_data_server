// using class
const start_min = 1;
const stop_max = 100000;

class DisplayGraph{
    constructor() { 
        this.selector = { value1: "2209-05", value2: "latest", value3 : "1" };
        this.points ={ start: 1, stop: 100000};
        this.num = { min: 1, max: 100000};
        this.sample_name = "";
    }

    draw_common(){
        const plotdata = document.getElementById('plotimg');
        const send_data = JSON.stringify({func: this.selector.value1, mode: this.selector.value2, start_point: this.points.start,
                                          stop_point: this.points.stop, sample_name: this.sample_name});

        $.ajax({
            method: "POST",
            url: "/plot",
            data: send_data,
            contentType: "application/json"
        })
        .done(function(data) {
            plotdata.src = "data:image/png:base64," + data;
        })
        this.print_sample();
    }

    set_start_stop(){
        $("#text1").val(start_min);
        $("#text2").val(stop_max);
        this.points.start = start_min;
        this.points.stop = stop_max;
    }

    drawGraph(obj) {
        const idx = obj.selectedIndex;
        this.selector.value1 = obj.options[idx].value;
        this.sample_name = "";
        this.set_sample();
        this.set_start_stop();
        this.draw_common();
    }

    drawGraph2(obj) {
        const idx = obj.selectedIndex;
        this.selector.value2 = obj.options[idx].value;
        this.set_start_stop();
        this.draw_common();
    }
    
    check_box(box_name){
        let num = parseInt($(box_name).val());
        if(num > this.num.max){ $(box_name).val(this.num.max) };
        if(num < this.num.min){ $(box_name).val(this.num.min) };
        num = parseInt($(box_name).val());
        return num
    }

    print_sample(){
        const send_data = JSON.stringify({func: this.selector.value1, mode: this.selector.value2, start_point: this.points.start,
                                          stop_point: this.points.stop, sample_name: this.sample_name});
        $.ajax({
            method: "POST",
            url: "/sample",
            data: send_data,
            contentType: "application/json"
        })
        .done((data) => {
            $("#sample").text(data.sample);
            $("#start_time").text(data.start_time);
            $("#stop_time").text(data.stop_time);
            this.num.max = data.max_num;

            this.points.start = this.check_box("#text1");
            this.points.stop = this.check_box("#text2");
        });
    }

    get_start_stop() {
        this.points.start = this.check_box("#text1");
        this.points.stop = this.check_box("#text2");

        $("#text1").val(this.points.start);
        $("#text2").val(this.points.stop);

        if (this.points.start > this.points.stop){
            this.points.stop = this.points.start;
            $("#text2").val(this.points.stop);
        }

        this.print_sample()
        this.draw_common();
    }

    button(){
            $('#button1').on('click', (e)=> {
                e.preventDefault();  // ボタン押下時の動作を抑制
                this.get_start_stop();
            });
    }

    selectSample(obj){
        const idx = obj.selectedIndex;
        this.selector.value3 = obj.options[idx].value;
        this.sample_name = this.selector.value3;

        this.set_start_stop();
        this.draw_common();
    }

    set_sample(){
        const send_data = JSON.stringify({func: this.selector.value1, mode: this.selector.value2, start_point: this.points.start,
                                          stop_point: this.points.stop, sample_name: this.sample_name});

        $.ajax({
            method: "POST",
            url: "/list",
            data: send_data,
            contentType: "application/json"
        })
        .done(function(data) {
                $('#selector3').empty();

                for (let i = 0; i < data.sample_list.length; i++){
                    $('#selector3').append('<option value='+data.sample_list[i]+'>'+data.sample_list[i]+'</option>');
                 }
            }    
        )
    }
}

// Call function from HTML
const dg = new DisplayGraph;

function drawGraph(obj) {
    dg.drawGraph(obj);
}

function drawGraph2(obj) {
    dg.drawGraph2(obj);
}

function selectSample(obj) {
    dg.selectSample(obj);
}

function button(){
    dg.button();
}