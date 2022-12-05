function myrefresh() {
  main();
  //window.location.reload();
}
main();
var t2 = window.setInterval("main()", 60000);

//  # get machine data from sql <- excel data for Machine2
// check OK!!!
function Machine_data(machine) {
  let sql_db;
  $.ajax({
    url: "./php/get_mechine_data.php",
    type: "POST",
    dateType: "json",
    async: false,
    data: {
      machine: machine,
    },
    success: function (data) {
      if (data == "false") {
        sql_db = data;
      } else {
        sql_db = JSON.parse(data);
      }
      return sql_db;
    },
  });
  return sql_db;
}

// get sales data -> 客戶 & 大小
// check OK!!!
function get_customer_info(lot) {
  $.ajax({
    url: "./php/get_customer_info_1.php",
    type: "POST",
    dateType: "json",
    async: false,
    data: {
      lot: lot,
    },
    success: function (data) {
      if (data == "false") {
        sql_db = data;
      } else {
        sql_db = JSON.parse(data);
      }
      return sql_db;
    },
  });
  return sql_db;
}
// Machine1 get data
// Table : [md_now_state]
function Machine1_get_sql_now_state(machine) {
  let sql_db;
  $.ajax({
    url: "./php/get_sql_md_now_state.php",
    type: "POST",
    dateType: "json",
    async: false,
    data: {
      machine: machine,
    },
    success: function (data) {
      if (data == "false") {
        sql_db = data;
      } else {
        sql_db = JSON.parse(data);
      }
      return sql_db;
    },
  });
  return sql_db;
}
//  Table : [md_main]
function Machine1_get_sql_main_data(md_main_no) {
  let sql_db;
  $.ajax({
    url: "./php/get_sql_md_main.php",
    type: "POST",
    dateType: "json",
    async: false,
    data: {
      md_main_no: md_main_no,
    },
    success: function (data) {
      if (data != "null") {
        sql_db = JSON.parse(data);
      } else {
        sql_db = null;
      }
    },
  });
  return sql_db;
}
// Table : [md_check] check & unload
function Machine1_get_sql_check_data(md_main_no) {
  let sql_db;
  $.ajax({
    url: "./php/get_sql_md_check.php",
    type: "POST",
    dateType: "json",
    async: false,
    data: {
      md_main_no: md_main_no,
    },
    success: function (data) {
      if (data != "null") {
        sql_db = JSON.parse(data);
      } else {
        sql_db = "null";
      }
    },
  });
  return sql_db;
}
// Table : [md_error] error
function Machine1_get_sql_error_data(md_main_no) {
  let sql_db;
  $.ajax({
    url: "./php/get_sql_md_error.php",
    type: "POST",
    dateType: "json",
    async: false,
    data: {
      md_main_no: md_main_no,
    },
    success: function (data) {
      if (data != "null") {
        sql_db = JSON.parse(data);
      } else {
        sql_db = "null";
      }
    },
  });
  return sql_db;
}
// check OK!!!
function filter_customer(cust) {
  switch (cust) {
    case "Case 1":
      return "Case 1";
      break;
    case "Case 2":
      return "Case 2";
      break;
    case "Case 3":
      return "Case 3";
      break;
    default:
      return cust;
  }
}

function data_sort_to_time_schdule(
  main_data,
  check_data,
  error_data,
  now_state
) {
  //  主要排序
  let result;
  let schdul_arr = [];
  if (main_data[0]["load_start"] != "") {
    schdul_arr.push(
      new data_obj("load start", new Date(main_data[0]["load_start"]))
    );
  }
  if (main_data[0]["load_end"] != "") {
    schdul_arr.push(
      new data_obj("load end", new Date(main_data[0]["load_end"]))
    );
  }
  let chk_schdul_arr = [];
  // check 不為空 排序
  console.log("check_data=", check_data);
  if (check_data != "null") {
    for (i = 0; i < check_data.length; i++) {
      if (check_data[i]["state"] == "Check") {
        if (
          check_data[i]["time_start"] != "" &&
          check_data[i]["time_end"] != ""
        ) {
          chk_schdul_arr.push(
            new data_obj(
              "check_start",
              new Date(check_data[i]["time_start"]),
              check_data[i].stripes,
              check_data[i].defect
            )
          );
          chk_schdul_arr.push(
            new data_obj(
              "check_end",
              new Date(check_data[i]["time_end"]),
              check_data[i].stripes,
              check_data[i].defect
            )
          );
        }

        if (
          check_data[i]["time_start"] != "" &&
          check_data[i]["time_end"] == ""
        ) {
          if (now_state["check_start"] == check_data[i]["time_start"]) {
            chk_schdul_arr.push(
              new data_obj(
                "check_start",
                new Date(check_data[i]["time_start"]),
                now_state.stripes,
                now_state.defect
              )
            );
          }
        }
      }

      if (check_data[i]["state"] == "Unload") {
        if (check_data[i]["time_start"] != "") {
          chk_schdul_arr.push(
            new data_obj("unload_start", new Date(check_data[i]["time_start"]))
          );
        }
      }

      if (
        check_data[i]["state"] == "Unload End" ||
        check_data[i]["state"] == "Unload Failed"
      ) {
        if (
          check_data[i]["time_start"] != "" &&
          check_data[i]["time_end"] != ""
        ) {
          chk_schdul_arr.push(
            new data_obj("Unload", new Date(check_data[i]["time_start"]))
          );
          // 分辨 End 與 failded
          chk_schdul_arr.push(
            new data_obj(
              check_data[i]["state"],
              new Date(check_data[i]["time_end"])
            )
          );
        }
        if (
          check_data[i]["time_end"] != "" &&
          check_data[i]["time_end"] == ""
        ) {
          chk_schdul_arr.push(
            new data_obj("unload_start", new Date(check_data[i]["time_start"]))
          );
        }
      }
    }
  }
  let err_temp_arr = [];
  if (error_data != "null") {
    let i = 0;
    console.log("bbbb", error_data);
    while (i < error_data.length) {
      err_temp_arr.push(
        new data_obj("Warning", new Date(error_data[i]["time"]))
      );
      i++;
    }
  }
  console.log(err_temp_arr);
  result = schdul_arr.concat(chk_schdul_arr, err_temp_arr);
  result.sort(function (a, b) {
    return a.time > b.time ? 1 : -1;
  });
  console.log(result);
  return result;
}

function data_obj(state, time, stripes, defect) {
  this.state = state;
  this.time = time;
  this.stripes = stripes;
  this.defect = defect;
}

function schdule_tr_id_and_color(css_class, color) {
  this.css_class = css_class;
  this.color = color;
}

function tr_time_make(start_time) {
  var count = 0;
  var st = parseInt(start_time.substr(11, 13));
  var time_temp;
  var tr_time = "";
  while (count < 25) {
    if (count % 2 == 0) {
      if (st + count < 24) {
        time_temp = st + count;
      } else {
        time_temp = st + count - 24;
      }
    } else {
      time_temp = "";
    }
    tr_time =
      tr_time + "<td class='td_time' colspan='1'>" + time_temp + "</td>";
    count += 1;
  }
  return tr_time;
}

function time_schdule_tr_make(data_sort, now_state) {
  let end_time;
  // 時間軸 區間  以30為單位
  let start_time = new Date(now_state["load_start"]);
  let start_time_plus_30 = new Date(now_state["load_start"]);
  start_time = new Date(
    start_time.getFullYear(),
    start_time.getMonth(),
    start_time.getDate(),
    start_time.getHours(),
    00
  );
  start_time_plus_30 = new Date(
    start_time_plus_30.getFullYear(),
    start_time_plus_30.getMonth(),
    start_time_plus_30.getDate(),
    start_time_plus_30.getHours(),
    30
  );

  //設置結束時間
  if (data_sort[data_sort.length - 1].state == "Unload End") {
    end_time = new Date(data_sort[data_sort.length - 1].time);
  } else {
    end_time = new Date();
  }
  // 共檢查 ? 天
  let cl_day_count = end_time.getTime() - start_time.getTime();
  cl_day_count = Math.floor(cl_day_count / (24 * 3600 * 1000)) + 1;
  let cl_tr_arr = [];
  let cl_tr_str = "";
  let color_temp = "";
  let cl_style = [];
  let cl_color = "white";
  let x = 0;
  let isdata_ctrl = false;
  let is_error = false;
  for (i = 1; i <= cl_day_count; i++) {
    for (j = 1; j < 49; j++) {
      if (j == 1) {
        cl_style = "first";
      } else if (j % 2 == 0) {
        cl_style = "even";
      } else {
        cl_style = "odd";
      }
      x = 0;

      while (x < data_sort.length) {
        if (
          start_time <= data_sort[x].time &&
          data_sort[x].time < start_time_plus_30
        ) {
          isdata_ctrl = true;
          console.log(
            "start_time : ",
            start_time,
            " | end_time : ",
            start_time_plus_30,
            " | state : ",
            data_sort[x].state
          );
          if (
            data_sort[x].state == "Error" ||
            data_sort[x].state == "Warning"
          ) {
            //console.log("1")
            is_error = true;
            cl_color = "error";
            color_temp = "error";
          } else if (
            data_sort[x].state == "check_end" &&
            data_sort[x].stripes != "" &&
            data_sort[x].stripes.split("/")[0] ==
              data_sort[x].stripes.split("/")[1]
          ) {
            //console.log("2")
            cl_color = "review";
            color_temp = "review";
          } else if (
            data_sort[x].state == "load start" ||
            data_sort[x].state == "load_end" ||
            data_sort[x].state == "Unload" ||
            data_sort[x].state == "Unload end"
          ) {
            //console.log("3")
            cl_color = "load";
            color_temp = "load";
          } else if (
            (data_sort[x].state == "check_start" ||
              data_sort[x].state == "check_end") &&
            data_sort[x].stripes != "" &&
            data_sort[x].stripes.split("/")[0] < 40
          ) {
            //console.log("4",data_sort[x].stripes)
            cl_color = "setting";
            color_temp = "setting";
          } else if (
            (data_sort[x].state == "check_start" ||
              data_sort[x].state == "check_end") &&
            data_sort[x].stripes != "" &&
            data_sort[x].stripes.split("/")[0] > 40
          ) {
            //console.log("5")
            cl_color = "check";
            color_temp = "check";
          }
        }
        if (data_sort[x].time > start_time_plus_30) {
          break;
        }
        x = x + 1;
      }
      //console.log(x)
      if (!isdata_ctrl) {
        if (is_error) {
          cl_color = "error";
        } else {
          cl_color = color_temp;
          if (
            (x =
              data_sort.length - 1 &&
              data_sort[data_sort.length - 1].state == "Unload Failed")
          ) {
            cl_color = "review";
            color_temp = cl_color;
          }
        }

        if (end_time < start_time) {
          cl_color = "white";
        }
        //console.log(j," | ", cl_color,"|",!isdata_ctrl,color_temp)
      } else {
        if (is_error) {
          cl_color = "error";
        } else {
          cl_color = color_temp;
        }
      }
      //console.log(j," | ", cl_color,"|",!isdata_ctrl,color_temp)
      cl_tr_str =
        cl_tr_str + '<td class="' + cl_style + '" id ="' + cl_color + '"></td>';
      //cl_schdule_style.push(cl_style,color)
      start_time.setMinutes(start_time.getMinutes() + 30);
      start_time_plus_30.setMinutes(start_time_plus_30.getMinutes() + 30);
      isdata_ctrl = false;
      is_error = false;
    }
    cl_tr_arr.push(cl_tr_str);
  }

  return cl_tr_arr;
}

function baseclone(base) {
  return new Date(base.valueOf());
}

function Machine1_ui_upgrade(
  Machine1_data_to_update,
  get_tr_to_update,
  Machine1_data_sort,
  error_sql_data
) {
  //取ID
  // lot information
  let cl_lot_id = document.getElementById("Machine1Lot");
  let cl_customer = document.getElementById("Machine1Custromer");
  let cl_size = document.getElementById("Machine1MaskSize");
  // machine information
  let cl_black_ground = document.querySelector("machine1");
  let cl_status = document.getElementById("Machine1Status");
  let cl_load_time = document.getElementById("Machine1StartTime");
  let cl_chk_end_time = document.getElementById("Machine1EndTime");
  let cl_defect = document.getElementById("Machine1Defect");
  let cl_check_time = document.getElementById("Machine1CheckTime");
  // 時間軸
  var cl_schedule_time = document.getElementById("tr_time1");
  let cl_tr_time = "";
  let cl_tr_1 = document.getElementById("Machine1Tr1");
  let cl_tr_2 = document.getElementById("Machine1Tr2");
  let cl_tr_3 = document.getElementById("Machine1Tr3");

  // 狀態更新
  cl_status.innerHTML = Machine1_data_to_update["state"];
  // 客戶資訊更新
  cl_lot_id.innerHTML = Machine1_data_to_update["lot"];
  cl_customer.innerHTML = Machine1_data_to_update["customer"];
  cl_size.innerHTML = Machine1_data_to_update["size"];
  //
  cl_load_time.innerHTML = Machine1_data_to_update["load_start"].substr(5, 11);
  cl_chk_end_time.innerHTML = Machine1_data_to_update[
    "expect_finish_time"
  ].substr(5, 11);
  cl_defect.innerHTML = "defect : " + String(Machine1_data_to_update["defect"]);
  // 空機時間 / 檢查總計時間
  let work_t = new Date().getTime();
  let load_st = new Date(Machine1_data_to_update["load_start"]).getTime();
  let h = parseInt((work_t - load_st) / (1000 * 60 * 60));
  let m = parseInt((work_t - load_st - 1000 * 60 * 60 * h) / (1000 * 60));
  cl_check_time.innerHTML = "總時: " + h + " 時 " + m + " 分 ";
  // 時間軸
  if (get_tr_to_update != []) {
    cl_schedule_time.innerHTML = tr_time_make(
      Machine1_data_to_update["load_start"]
    );
    for (let i = 0; i < get_tr_to_update.length; i++) {
      if (i == 0) {
        cl_tr_1.innerHTML = get_tr_to_update[i];
      } else if (i == 1) {
        cl_tr_2.innerHTML = get_tr_to_update[i];
      } else {
        cl_tr_3.innerHTML = get_tr_to_update[i];
      }
    }
  }
  // error text
  if (error_sql_data != "null") {
    error_sql_data.sort(function (a, b) {
      return a.time < b.time ? 1 : -1;
    });

    for (i = 0; i < 3; i++) {
      switch (i) {
        case 0: {
          msg = document.getElementById("msg1");
          break;
        }
        case 1: {
          msg = document.getElementById("msg2");
          break;
        }
        case 2: {
          msg = document.getElementById("msg3");

          break;
        }
        default: {
          break;
        }
      }
      text_temp =
        error_sql_data[i].time.substr(5, 5).replace("-", "/") +
        " " +
        error_sql_data[i].time.substr(11, 5) +
        " ";
      text_temp = text_temp + error_sql_data[i].text;
      if (text_temp.length > 80) {
        text_temp = text_temp.substr(0, 80);
      }
      msg.innerHTML = text_temp;
      msg.style.color = "red";
    }
  }

  if (
    Machine1_data_to_update["state"] == "Error" ||
    Machine1_data_to_update["state"] == "Warning"
  ) {
    cl_black_ground.style.backgroundColor = "#FF2F27";
  } else {
    cl_black_ground.style.backgroundColor = "#f8f8c4";
  }

  if (
    Machine1_data_to_update["state"] == "Unload End" ||
    Machine1_data_to_update["state"] == "Unload Failed"
  ) {
    let last_time = baseclone(
      Machine1_data_sort[Machine1_data_sort.length - 1].time
    );
    last_time.setMinutes(last_time.getMinutes() + 30);
    if (last_time < new Date()) {
      cl_status.innerHTML = "IDLE";
      cl_status = document.querySelector("Machine1Status");
      cl_status.style.backgroundColor = "#ffffff";
      // 客戶資料
      cl_lot_id.innerHTML = "";
      cl_customer.innerHTML = "";
      cl_size.innerHTML = "";

      //
      cl_load_time.innerHTML = "";
      cl_chk_end_time.innerHTML = "";
      cl_defect.innerHTML = "defect : ";
      // 空機時間 / 檢查總計時間
      cl_check_time.innerHTML = "";

      cl_tr_1.innerHTML = "";
      cl_tr_2.innerHTML = "";
      cl_tr_3.innerHTML = "";

      for (i = 0; i < 3; i++) {
        switch (i) {
          case 0: {
            msg = document.getElementById("msg_1");
            break;
          }
          case 1: {
            msg = document.getElementById("msg_2");
            break;
          }
          case 2: {
            msg = document.getElementById("msg_3");

            break;
          }
          default: {
            break;
          }
        }
        if (text_temp.length > 80) {
          text_temp = text_temp.substr(0, 80);
        }
        msg.innerHTML = " ";
      }
    } else {
      cl_status.innerHTML = "Review";
      cl_status.style.backgroundColor = "#528434";
      cl_load_time.innerHTML = Machine1_data_to_update["load_start"].substr(
        5,
        11
      );
      cl_chk_end_time.innerHTML = "";
      cl_check_time.innerHTML = h + " 時 " + m + " 分 ";
    }
  }
}
//
function get_machine_data_and_create_schdule() {
  let Machine1_now_state = Machine1_get_sql_now_state("Machine1");
  console.log(Machine1_now_state);
  if (Machine1_now_state != false) {
    let loadstart = Machine1_now_state["load_start"].split("-");
    let main_key =
      loadstart[0] + loadstart[1] + loadstart[2].substr(0, 5).replace(" ", "");
    let get_tr_to_update;
    console.log(main_key);
    // 資料庫資料

    let main_sql_data = Machine1_get_sql_main_data(main_key);
    let chk_sql_data = Machine1_get_sql_check_data(main_key);
    let error_sql_data = Machine1_get_sql_error_data(main_key);

    console.log(main_sql_data);
    console.log(chk_sql_data);
    console.log(error_sql_data);
    // 狀態 排序 依時間
    let Machine1_data_sort = data_sort_to_time_schdule(
      main_sql_data,
      chk_sql_data,
      error_sql_data,
      Machine1_now_state
    );
    if (Machine1_data_sort != false) {
      console.log("Make tr");
      get_tr_to_update = time_schdule_tr_make(
        Machine1_data_sort,
        Machine1_now_state
      );
      //console.log(get_tr_to_update)
    }
    let customer = get_customer_info(Machine1_now_state["lot"]);
    let Machine1_data_to_update = {
      state: Machine1_now_state["state"],
      lot: Machine1_now_state["lot"],
      customer: "",
      size: "",
      load_start: Machine1_now_state["load_start"],
      expect_finish_time: Machine1_now_state["expect_finish_time"],
      defect: Machine1_now_state["defect"],
      sensitivity: "",
    };
    //console.log(customer);
    if (customer != "false") {
      Machine1_data_to_update["customer"] = filter_customer(customer["Name"]);
      let size = customer["TD006"].split("-")[0].split("mm*");
      Machine1_data_to_update["size"] = size[0] + "x" + size[1];
    } else {
      Machine1_data_to_update["customer"] = "";
      Machine1_data_to_update["size"] = "";
    }

    //console.log(Machine1_data_to_update,Machine1_data_sort,error_sql_data)
    Machine1_ui_upgrade(
      Machine1_data_to_update,
      get_tr_to_update,
      Machine1_data_sort,
      error_sql_data
    );
  }
}

//時間軸 履歷   For Machine2
function history_t(start_time, end_time) {
  //console.log(start_time)
  var tr_1 = document.getElementById("Machine2Tr1");
  var tr_2 = document.getElementById("Machine2Tr2");
  var tr_3 = document.getElementById("Machine2Tr3");
  var day_count = 1;
  var st_temp = new Date(start_time);
  var end_temp = new Date(end_time);
  while (day_count < 3) {
    st_temp.setDate(st_temp.getDate() + 1);
    if (st_temp < new Date(end_time)) {
      day_count += 1;
    } else {
      break;
    }
  }
  var tr_make = "";
  st_temp = new Date(start_time);
  var now = new Date();
  var st_temp_t;
  if (new Date().getMinutes() > 30) {
    st_temp_t = new Date(
      now.getFullYear(),
      now.getMonth(),
      now.getDate(),
      now.getHours() + 1,
      00
    );
  } else {
    st_temp_t = new Date(
      now.getFullYear(),
      now.getMonth(),
      now.getDate(),
      now.getHours(),
      30
    );
  }
  var style;
  var color;
  for (i = 1; i <= day_count; i++) {
    for (j = 1; j <= 48; j++) {
      if (j == 1) {
        style = "first";
      } else if (j % 2 == 0) {
        style = "even";
      } else {
        style = "odd";
      }
      if (st_temp < end_temp && st_temp < st_temp_t) {
        color = "check";
      } else {
        color = "white";
      }
      tr_make = tr_make + '<td class="' + style + '" id ="' + color + '"></td>';
      st_temp.setMinutes(st_temp.getMinutes() + 30);
    }
    if (i == 1) {
      tr_1.innerHTML = tr_make;
    } else if (i == 2) {
      tr_2.innerHTML = tr_make;
    } else {
      tr_3.innerHTML = tr_make;
    }
    tr_make = "";
  }
}

function Machine2_UI_update(li_data) {
  console.log(li_data);
  var li_lot = document.getElementById("Machine2Lot");
  var li_customer = document.getElementById("Machine2Custromer");
  var li_size = document.getElementById("Machine2MaskSize");
  var li_status = document.getElementById("Machine2Status");
  var li_start_time = document.getElementById("Machine2StartTime");
  var li_end_time = document.getElementById("Machine2EndTime");
  var Machine2_time_status = document.getElementById("Machine2_time_status");
  var li_tb_tr_time = document.getElementById("Machine2TrTime");
  var li_history = document.getElementById("Machine2Table");

  if (
    new Date(li_data["start_time"]) <= new Date() ||
    new Date(li_data["end_time"]) >= new Date()
  ) {
    li_status.innerHTML = "檢查";
    li_tb_tr_time.innerHTML = tr_time_make(li_data["start_time"]);

    history_t(li_data["start_time"], li_data["end_time"]);

    //li_status.style.transform="rotateX(360deg)"
  } else {
    var tr_1 = document.getElementById("Machine2Tr1");
    var tr_2 = document.getElementById("Machine2Tr2");
    var tr_3 = document.getElementById("Machine2Tr3");
    li_status.innerHTML = "IDLE";
    Machine2_time_status.innerHTML = "";
    li_tb_tr_time.innerHTML = null;
    tr_1.innerHTML = "";
    tr_2.innerHTML = "";
    tr_3.innerHTML = "";
  }
  li_lot.innerHTML = li_data["lot"];
  li_customer.innerHTML = li_data["customer"];
  li_size.innerHTML = li_data["size"];
  li_start_time.innerHTML = li_data["start_time"].substr(5);
  li_end_time.innerHTML = li_data["end_time"].substr(5);
}

function get_Machine2_data_and_create_schdule() {
  let Machine2_data = Machine_data("Machine2");

  if (Machine2_data != "false") {
    Machine2_data["lot"] = Machine2_data["lot"].substr(0, 9);
    var customer = get_customer_info(Machine2_data["lot"]);
    //console.log(customer)
    if (customer != "false") {
      Machine2_data["customer"] = filter_customer(customer["Name"]);
      var size = customer["TD006"].split("-")[0].split("mm*");
      Machine2_data["size"] = size[0] + "x" + size[1];
    } else {
      Machine2_data["customer"] = "";
      Machine2_data["size"] = "";
    }
    if (Machine2_data["start_time"] != null) {
      var head = parseInt(Machine2_data["start_time"].substr(11, 13));
      var first_day = new Date(Machine2_data["start_time"]);
      //if
      first_day.setDate(new Date(Machine2_data["start_time"]).getDate() + 1);
    }
  } else {
    Machine2_data = {
      status: "IDLE",
      lot: "",
      customer: "",
      size: "",
      start_time: "",
      end_time: "",
    };
  }

  Machine2_UI_update(Machine2_data);
}

function main() {
  get_machine_data_and_create_schdule();
  get_Machine2_data_and_create_schdule();
}
