/*!
* Start Bootstrap - Shop Item v5.0.6 (https://startbootstrap.com/template/shop-item)
* Copyright 2013-2023 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-shop-item/blob/master/LICENSE)
*/
// This file is intentionally blank
// Use this file to add JavaScript to your project

// 當頁面滾動時，顯示或隱藏返回頂部按鈕
$('#date1').datetimepicker({
    date:null,
      format: 'YYYY-MM-DD',
      locale: moment.locale('zh-tw'),
      daysOfWeekDisabled: [0, 6],
      minDate: moment().add(1,'days'),
      maxDate: moment().add(30,'days'),
      disabledDates: [
        moment().add(1,'days'),
        moment().add(2,'days'),
        '2021-10-10',
        '2021-12-25'
      ]
  });

  

