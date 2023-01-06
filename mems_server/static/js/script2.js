// using class
const start_min = 1;
const stop_max = 100000;

class DisplayGraph{
    constructor() { 
        this.value1 = "2209-05"
        this.value2 = "latest";
        this.value3 = "1"
        this.start_point = 1;
        this.stop_point = 100000;
        this.min_num = 1;
        this.max_num = 100000;
        this.sample_name = "";
    }

    draw_common(){
        const plotdata = document.getElementById('plotimg');
        const send_data = JSON.stringify({func: this.value1, mode: this.value2, start_point: this.start_point,
                                          stop_point: this.stop_point, sample_name: this.sample_name});
    
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
        this.start_point = start_min;
        this.stop_point = stop_max;
    }

    drawGraph(obj) {
        const idx = obj.selectedIndex;
        this.value1 = obj.options[idx].value;
        this.sample_name = "";
        this.set_sample();
        this.set_start_stop();
        this.draw_common();
    }

    drawGraph2(obj) {
        const idx = obj.selectedIndex;
        this.value2 = obj.options[idx].value;
        this.set_start_stop();
        this.draw_common();
    }
    
    check_box(box_name){
        let num = parseInt($(box_name).val());
        if(num > this.max_num){ $(box_name).val(this.max_num)};
        if(num < this.min_num){ $(box_name).val(this.min_num)};
        num = parseInt($(box_name).val());
        return num
    }

    print_sample(){
        const send_data = JSON.stringify({func: this.value1, mode: this.value2, start_point: this.start_point,
                                          stop_point: this.stop_point, sample_name: this.sample_name});
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
            this.max_num = data.max_num;

            this.start_point = this.check_box("#text1");
            this.stop_point = this.check_box("#text2");
        });
    }

    get_start_stop() {
        this.start_point = this.check_box("#text1");
        this.stop_point = this.check_box("#text2");

        $("#text1").val(this.start_point);
        $("#text2").val(this.stop_point);

        if (this.start_point > this.stop_point){
            this.stop_point = this.start_point;
            $("#text2").val(this.stop_point);
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
        this.value3 = obj.options[idx].value;
        this.sample_name = this.value3;

        this.set_start_stop();
        this.draw_common();
    }

    set_sample(){
        const send_data = JSON.stringify({func: this.value1, mode: this.value2, start_point: this.start_point,
                                          stop_point: this.stop_point, sample_name: this.sample_name});

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


// html call function

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